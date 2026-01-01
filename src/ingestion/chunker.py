"""
Text Chunking

This module provides functionality for splitting documents into smaller chunks
suitable for embedding and retrieval.

Implements token-based chunking with configurable overlap.
"""

from dataclasses import dataclass
from typing import List, Optional
import re

from src.ingestion.document_loader import DocumentChunk


@dataclass
class ChunkerConfig:
    """
    Configuration for the TokenChunker.
    
    Attributes:
        chunk_size: Target number of tokens per chunk (default: 600).
        overlap: Number of overlapping tokens between chunks (default: 60).
        min_chunk_size: Minimum chunk size to keep (default: 50).
    """
    chunk_size: int = 600
    overlap: int = 60
    min_chunk_size: int = 50
    
    def __post_init__(self):
        """Validate configuration."""
        if self.chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if self.overlap < 0:
            raise ValueError("overlap cannot be negative")
        if self.overlap >= self.chunk_size:
            raise ValueError("overlap must be less than chunk_size")
        if self.min_chunk_size < 0:
            raise ValueError("min_chunk_size cannot be negative")


class TokenChunker:
    """
    Splits documents into overlapping chunks based on token count.
    
    Uses simple word-based tokenization (split on whitespace).
    For production use, consider integrating tiktoken for accurate
    token counts matching the embedding model.
    
    Example:
        >>> chunker = TokenChunker(chunk_size=500, overlap=50)
        >>> chunks = chunker.chunk_document(document)
    """
    
    def __init__(
        self,
        chunk_size: int = 600,
        overlap: int = 60,
        min_chunk_size: int = 50
    ):
        """
        Initialize the chunker with configuration.
        
        Args:
            chunk_size: Target tokens per chunk (500-700 recommended).
            overlap: Overlapping tokens between chunks (10-15% of chunk_size).
            min_chunk_size: Minimum tokens to keep a chunk.
        """
        self.config = ChunkerConfig(
            chunk_size=chunk_size,
            overlap=overlap,
            min_chunk_size=min_chunk_size
        )
    
    def _tokenize(self, text: str) -> List[str]:
        """
        Simple word-based tokenization.
        
        Args:
            text: Input text to tokenize.
            
        Returns:
            List of tokens (words).
        """
        # Split on whitespace while preserving some structure
        tokens = re.split(r'\s+', text.strip())
        return [t for t in tokens if t]
    
    def _detokenize(self, tokens: List[str]) -> str:
        """
        Join tokens back into text.
        
        Args:
            tokens: List of tokens to join.
            
        Returns:
            Joined text string.
        """
        return " ".join(tokens)
    
    def chunk_text(
        self,
        text: str,
        source: str = "unknown"
    ) -> List[DocumentChunk]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: The text to chunk.
            source: Source identifier for the chunks.
            
        Returns:
            List of DocumentChunks.
        """
        if not text or not text.strip():
            return []
        
        tokens = self._tokenize(text)
        
        # If text is smaller than chunk size, return as single chunk
        if len(tokens) <= self.config.chunk_size:
            return [
                DocumentChunk(
                    content=self._detokenize(tokens),
                    source=source,
                    metadata={
                        "token_count": len(tokens),
                        "is_single_chunk": True
                    },
                    chunk_index=0
                )
            ]
        
        chunks: List[DocumentChunk] = []
        step = self.config.chunk_size - self.config.overlap
        chunk_index = 0
        
        for start in range(0, len(tokens), step):
            end = min(start + self.config.chunk_size, len(tokens))
            chunk_tokens = tokens[start:end]
            
            # Skip chunks that are too small
            if len(chunk_tokens) < self.config.min_chunk_size:
                continue
            
            chunk_text = self._detokenize(chunk_tokens)
            
            chunks.append(
                DocumentChunk(
                    content=chunk_text,
                    source=source,
                    metadata={
                        "token_count": len(chunk_tokens),
                        "start_token": start,
                        "end_token": end,
                        "is_single_chunk": False
                    },
                    chunk_index=chunk_index
                )
            )
            chunk_index += 1
            
            # Stop if we've reached the end
            if end >= len(tokens):
                break
        
        return chunks
    
    def chunk_document(self, document: DocumentChunk) -> List[DocumentChunk]:
        """
        Split a document chunk into smaller chunks.
        
        Preserves source metadata from the original document.
        
        Args:
            document: The document to chunk.
            
        Returns:
            List of smaller DocumentChunks.
        """
        chunks = self.chunk_text(document.content, document.source)
        
        # Merge original metadata into each chunk
        for chunk in chunks:
            chunk.metadata.update({
                "original_filename": document.metadata.get("filename", "unknown"),
                "original_size": document.metadata.get("size_bytes", 0)
            })
        
        return chunks
    
    def chunk_documents(
        self,
        documents: List[DocumentChunk]
    ) -> List[DocumentChunk]:
        """
        Process multiple documents into chunks.
        
        Args:
            documents: List of documents to chunk.
            
        Returns:
            Flat list of all chunks from all documents.
        """
        all_chunks: List[DocumentChunk] = []
        
        for doc in documents:
            chunks = self.chunk_document(doc)
            all_chunks.extend(chunks)
        
        return all_chunks
    
    def get_token_count(self, text: str) -> int:
        """
        Count tokens in text.
        
        Args:
            text: Text to count tokens in.
            
        Returns:
            Number of tokens.
        """
        return len(self._tokenize(text))
