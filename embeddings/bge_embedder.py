"""
BGE Embedder

Text embedding using BGE (BAAI/bge-base-en-v1.5) model.
Optimized for retrieval with query prefixing support.
"""

from typing import List, Optional

import numpy as np
from sentence_transformers import SentenceTransformer


class BGEEmbedder:
    """
    Text embedder using BGE model from SentenceTransformers.
    
    Attributes:
        model_name: The HuggingFace model identifier.
        dimension: The embedding dimension size (768 for bge-base).
    """
    
    DEFAULT_MODEL = "BAAI/bge-base-en-v1.5"
    QUERY_PREFIX = "Represent this sentence for searching relevant passages: "
    
    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        device: Optional[str] = None,
        use_query_prefix: bool = True
    ):
        self.model_name = model_name
        self.use_query_prefix = use_query_prefix
        
        self._model = SentenceTransformer(
            model_name, device=device
        ) if device else SentenceTransformer(model_name)
        
        self.dimension = self._model.get_sentence_embedding_dimension()
    
    def embed(self, text: str, normalize: bool = True) -> np.ndarray:
        """Generate embedding for a single text."""
        if not text or not text.strip():
            raise ValueError("Cannot embed empty text")
        
        return self._model.encode(
            text,
            normalize_embeddings=normalize,
            convert_to_numpy=True
        )
    
    def embed_batch(
        self,
        texts: List[str],
        normalize: bool = True,
        batch_size: int = 32,
        show_progress: bool = False
    ) -> np.ndarray:
        """Generate embeddings for a batch of texts."""
        if not texts:
            return np.array([]).reshape(0, self.dimension)
        
        valid_texts = [t for t in texts if t and t.strip()]
        if not valid_texts:
            return np.array([]).reshape(0, self.dimension)
        
        return self._model.encode(
            valid_texts,
            normalize_embeddings=normalize,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )
    
    def embed_query(self, query: str, normalize: bool = True) -> np.ndarray:
        """Generate embedding for a search query (with prefix)."""
        if not query or not query.strip():
            raise ValueError("Cannot embed empty query")
        
        prefixed = f"{self.QUERY_PREFIX}{query}" if self.use_query_prefix else query
        return self.embed(prefixed, normalize=normalize)
    
    def embed_documents(
        self,
        documents: List[str],
        normalize: bool = True,
        batch_size: int = 32,
        show_progress: bool = False
    ) -> np.ndarray:
        """Generate embeddings for documents (without prefix)."""
        return self.embed_batch(
            texts=documents,
            normalize=normalize,
            batch_size=batch_size,
            show_progress=show_progress
        )
    
    def similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """Compute cosine similarity between two embeddings."""
        return float(np.dot(emb1, emb2))
