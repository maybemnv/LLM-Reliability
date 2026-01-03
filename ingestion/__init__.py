"""
Ingestion Module - Document Loading and Processing

This module provides functionality for:
- Document models (Document, DocumentChunk dataclasses)
- Loading documents from various formats (PDF, TXT)
- Semantic-aware chunking with token-based sizing
"""

from ingestion.models import Document, DocumentChunk
from ingestion.loaders import (
    load_txt,
    load_pdf,
    load_document,
    load_documents_from_directory
)
from ingestion.chunker import SemanticChunker

__all__ = [
    "Document",
    "DocumentChunk",
    "load_txt",
    "load_pdf",
    "load_document",
    "load_documents_from_directory",
    "SemanticChunker"
]
