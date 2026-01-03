"""
Retrieval Service

Provides singleton pattern and high-level retrieval function for API use.
Single responsibility: service layer between API and vector store.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional

from retrieval.store import FAISSVectorStore


_vector_store: Optional[FAISSVectorStore] = None


def get_vector_store() -> FAISSVectorStore:
    """
    Get or create the global vector store instance.
    
    Returns:
        The FAISSVectorStore singleton.
    """
    global _vector_store
    
    if _vector_store is None:
        _vector_store = FAISSVectorStore()
        
        default_path = Path("Data/vector_store")
        if default_path.exists():
            try:
                _vector_store.load_index(str(default_path))
            except FileNotFoundError:
                pass
    
    return _vector_store


def retrieve_documents(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Retrieve relevant documents for a query.
    
    This is the main retrieval function used by the API.
    
    Args:
        query: The search query.
        top_k: Number of results to return.
        
    Returns:
        List of evidence dictionaries.
    """
    store = get_vector_store()
    
    if store.is_empty:
        return []
    
    return store.search(query, top_k=top_k)


def reset_vector_store() -> None:
    """Reset the singleton (useful for testing)."""
    global _vector_store
    _vector_store = None
