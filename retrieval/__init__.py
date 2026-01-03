"""
Retrieval Module - Vector Store and Evidence Retrieval

This module provides:
- FAISSVectorStore class for vector similarity search
- retrieve_documents function for API integration
"""

from retrieval.store import FAISSVectorStore
from retrieval.service import retrieve_documents, get_vector_store

__all__ = [
    "FAISSVectorStore",
    "retrieve_documents",
    "get_vector_store"
]
