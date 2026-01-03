"""
Semantic Document Chunker

Implements semantic-aware chunking strategy:
1. Split by paragraph boundaries first
2. Merge small paragraphs to reach minimum token threshold
3. Split oversized paragraphs at sentence boundaries
4. Apply configurable overlap between chunks
"""

import re
from typing import List, Dict, Any, Optional

import tiktoken

from ingestion.models import Document, DocumentChunk


class SemanticChunker:
    """
    Semantic-aware document chunker with token-based sizing.
    
    Attributes:
        min_chunk_tokens: Minimum tokens per chunk (default: 500).
        max_chunk_tokens: Maximum tokens per chunk (default: 700).
        overlap_ratio: Overlap ratio between chunks (default: 0.12).
    """
    
    PARAGRAPH_PATTERN = re.compile(r"\n\s*\n")
    SENTENCE_PATTERN = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")
    
    def __init__(
        self,
        min_chunk_tokens: int = 500,
        max_chunk_tokens: int = 700,
        overlap_ratio: float = 0.12,
        encoding_name: str = "cl100k_base"
    ):
        self._validate_params(min_chunk_tokens, max_chunk_tokens, overlap_ratio)
        
        self.min_chunk_tokens = min_chunk_tokens
        self.max_chunk_tokens = max_chunk_tokens
        self.overlap_ratio = overlap_ratio
        self.encoding = tiktoken.get_encoding(encoding_name)
    
    def _validate_params(self, min_t: int, max_t: int, overlap: float) -> None:
        if min_t <= 0:
            raise ValueError("min_chunk_tokens must be positive")
        if max_t <= 0:
            raise ValueError("max_chunk_tokens must be positive")
        if min_t > max_t:
            raise ValueError("min_chunk_tokens cannot exceed max_chunk_tokens")
        if not 0 <= overlap < 1:
            raise ValueError("overlap_ratio must be between 0 and 1")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in a text string."""
        return len(self.encoding.encode(text)) if text else 0
    
    def _split_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs."""
        paragraphs = self.PARAGRAPH_PATTERN.split(text)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        sentences = self.SENTENCE_PATTERN.split(text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _merge_segments(self, segments: List[str]) -> List[str]:
        """Merge small segments until reaching token threshold."""
        if not segments:
            return []
        
        merged: List[str] = []
        current = ""
        current_tokens = 0
        
        for segment in segments:
            seg_tokens = self.count_tokens(segment)
            
            if current_tokens + seg_tokens > self.max_chunk_tokens:
                if current:
                    merged.append(current)
                
                if seg_tokens > self.max_chunk_tokens:
                    merged.extend(self._split_oversized(segment))
                    current = ""
                    current_tokens = 0
                else:
                    current = segment
                    current_tokens = seg_tokens
            else:
                current = f"{current}\n\n{segment}".strip() if current else segment
                current_tokens = self.count_tokens(current)
        
        if current:
            merged.append(current)
        
        return merged
    
    def _split_oversized(self, text: str) -> List[str]:
        """Split oversized segment at sentence boundaries."""
        sentences = self._split_sentences(text)
        
        if len(sentences) <= 1:
            return [text]
        
        result: List[str] = []
        current = ""
        
        for sentence in sentences:
            potential = f"{current} {sentence}".strip()
            
            if self.count_tokens(potential) > self.max_chunk_tokens:
                if current:
                    result.append(current)
                current = sentence
            else:
                current = potential
        
        if current:
            result.append(current)
        
        return result
    
    def _apply_overlap(self, chunks: List[str]) -> List[str]:
        """Apply overlap between consecutive chunks."""
        if len(chunks) <= 1:
            return chunks
        
        overlapped: List[str] = [chunks[0]]
        
        for i in range(1, len(chunks)):
            prev = chunks[i - 1]
            overlap_tokens = int(self.count_tokens(prev) * self.overlap_ratio)
            
            if overlap_tokens > 0:
                sentences = self._split_sentences(prev)
                overlap_text = ""
                
                for s in reversed(sentences):
                    potential = f"{s} {overlap_text}".strip()
                    if self.count_tokens(potential) <= overlap_tokens:
                        overlap_text = potential
                    else:
                        break
                
                if overlap_text:
                    overlapped.append(f"{overlap_text} {chunks[i]}")
                else:
                    overlapped.append(chunks[i])
            else:
                overlapped.append(chunks[i])
        
        return overlapped
    
    def chunk_text(
        self,
        text: str,
        source: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[DocumentChunk]:
        """Chunk text into semantically coherent pieces."""
        if not text or not text.strip():
            return []
        
        metadata = metadata or {}
        
        paragraphs = self._split_paragraphs(text)
        if not paragraphs:
            return []
        
        merged = self._merge_segments(paragraphs)
        overlapped = self._apply_overlap(merged)
        
        return [
            DocumentChunk(
                content=chunk_text,
                source=source,
                chunk_index=i,
                token_count=self.count_tokens(chunk_text),
                metadata=metadata.copy()
            )
            for i, chunk_text in enumerate(overlapped)
        ]
    
    def chunk_document(self, document: Document) -> List[DocumentChunk]:
        """Chunk a Document object."""
        return self.chunk_text(
            text=document.content,
            source=document.source,
            metadata=document.metadata
        )
