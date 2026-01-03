"""
Document and Chunk Models

Dataclasses for representing documents and their chunks.
Single responsibility: data structures only, no logic.
"""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class Document:
    """
    Represents a loaded document with its content and metadata.
    
    Attributes:
        content: The full text content of the document.
        source: The file path or identifier of the document source.
        metadata: Additional metadata (file type, size, etc.).
    """
    content: str
    source: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate document after initialization."""
        if not self.content:
            raise ValueError("Document content cannot be empty")
        if not self.source:
            raise ValueError("Document source cannot be empty")


@dataclass
class DocumentChunk:
    """
    Represents a chunk of a document with metadata.
    
    Attributes:
        content: The text content of the chunk.
        source: The source document path or identifier.
        chunk_index: The index of this chunk within the document.
        token_count: Number of tokens in this chunk.
        metadata: Additional metadata from parent document.
    """
    content: str
    source: str
    chunk_index: int
    token_count: int
    metadata: Dict[str, Any] = field(default_factory=dict)
