"""
FAISS Vector Store

Core vector store implementation using FAISS for similarity search.
Single responsibility: index management and search.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any

import numpy as np
import faiss

from embeddings.bge_embedder import BGEEmbedder
from ingestion.models import DocumentChunk


class FAISSVectorStore:
    """
    FAISS-based vector store for document retrieval.
    
    Uses normalized embeddings with inner product index
    for cosine similarity search.
    """
    
    INDEX_FILENAME = "faiss_index.bin"
    METADATA_FILENAME = "chunks_metadata.json"
    
    def __init__(
        self,
        embedder: Optional[BGEEmbedder] = None,
        index_path: Optional[str] = None
    ):
        self.embedder = embedder or BGEEmbedder()
        self.dimension = self.embedder.dimension
        self._index: Optional[faiss.IndexFlatIP] = None
        self._chunks: List[Dict[str, Any]] = []
        
        if index_path:
            self.load_index(index_path)
    
    @property
    def is_empty(self) -> bool:
        return self._index is None or self._index.ntotal == 0
    
    @property
    def size(self) -> int:
        return self._index.ntotal if self._index else 0
    
    def _create_index(self) -> faiss.IndexFlatIP:
        return faiss.IndexFlatIP(self.dimension)
    
    def add_chunks(
        self,
        chunks: List[DocumentChunk],
        batch_size: int = 32,
        show_progress: bool = False
    ) -> None:
        """Add document chunks to the vector store."""
        if not chunks:
            return
        
        if self._index is None:
            self._index = self._create_index()
        
        texts = [chunk.content for chunk in chunks]
        embeddings = self.embedder.embed_documents(
            documents=texts,
            normalize=True,
            batch_size=batch_size,
            show_progress=show_progress
        )
        
        self._index.add(embeddings.astype(np.float32))
        
        for chunk in chunks:
            self._chunks.append({
                "content": chunk.content,
                "source": chunk.source,
                "chunk_index": chunk.chunk_index,
                "token_count": chunk.token_count,
                "metadata": chunk.metadata
            })
    
    def build_index(
        self,
        chunks: List[DocumentChunk],
        batch_size: int = 32,
        show_progress: bool = False
    ) -> None:
        """Build a new index (replaces existing)."""
        self._index = self._create_index()
        self._chunks = []
        self.add_chunks(chunks, batch_size, show_progress)
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search for relevant documents."""
        if self.is_empty or not query or not query.strip():
            return []
        
        top_k = min(top_k, self.size)
        if top_k <= 0:
            return []
        
        query_emb = self.embedder.embed_query(query, normalize=True)
        query_emb = query_emb.reshape(1, -1).astype(np.float32)
        
        scores, indices = self._index.search(query_emb, top_k)
        
        results: List[Dict[str, Any]] = []
        for score, idx in zip(scores[0], indices[0]):
            if 0 <= idx < len(self._chunks):
                chunk = self._chunks[idx]
                relevance = max(0.0, min(1.0, (score + 1) / 2))
                
                results.append({
                    "content": chunk["content"],
                    "source": chunk["source"],
                    "relevance_score": round(relevance, 3),
                    "chunk_index": chunk["chunk_index"],
                    "metadata": chunk.get("metadata", {})
                })
        
        return results
    
    def save_index(self, directory: str) -> None:
        """Save index and metadata to disk."""
        if self.is_empty:
            raise ValueError("Cannot save empty index")
        
        dir_path = Path(directory)
        dir_path.mkdir(parents=True, exist_ok=True)
        
        faiss.write_index(self._index, str(dir_path / self.INDEX_FILENAME))
        
        with open(dir_path / self.METADATA_FILENAME, "w", encoding="utf-8") as f:
            json.dump(self._chunks, f, ensure_ascii=False, indent=2)
    
    def load_index(self, directory: str) -> None:
        """Load index and metadata from disk."""
        dir_path = Path(directory)
        index_path = dir_path / self.INDEX_FILENAME
        metadata_path = dir_path / self.METADATA_FILENAME
        
        if not index_path.exists():
            raise FileNotFoundError(f"Index not found: {index_path}")
        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata not found: {metadata_path}")
        
        self._index = faiss.read_index(str(index_path))
        
        with open(metadata_path, "r", encoding="utf-8") as f:
            self._chunks = json.load(f)
