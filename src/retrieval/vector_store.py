"""
Vector Store and Evidence Retrieval

This module provides evidence retrieval functionality using vector similarity search.
Phase 1: Stub implementation with deterministic evidence chunks.
Future phases will integrate with FAISS for actual vector search.
"""

from typing import List, Dict, Any

# Stub evidence corpus for deterministic testing
_STUB_EVIDENCE_CORPUS: List[Dict[str, Any]] = [
    {
        "content": (
            "Air pollution is a major environmental health risk. According to the World Health Organization, "
            "ambient air pollution causes an estimated 4.2 million premature deaths worldwide per year. "
            "This mortality is due to exposure to fine particulate matter (PM2.5), which causes cardiovascular "
            "and respiratory disease, and cancers."
        ),
        "source": "WHO Air Quality Guidelines 2021",
        "keywords": ["air", "pollution", "health", "disease", "respiratory"],
        "base_relevance": 0.92
    },
    {
        "content": (
            "Long-term exposure to air pollution is associated with increased mortality from heart disease, "
            "stroke, chronic obstructive pulmonary disease, lung cancer, and acute lower respiratory infections. "
            "Children, the elderly, and people with pre-existing health conditions are particularly vulnerable."
        ),
        "source": "Environmental Health Perspectives Research 2023",
        "keywords": ["exposure", "mortality", "heart", "lung", "vulnerable"],
        "base_relevance": 0.88
    },
    {
        "content": (
            "Climate change refers to long-term shifts in temperatures and weather patterns. Human activities "
            "have been the main driver of climate change, primarily due to burning fossil fuels. The Paris Agreement "
            "adopted in 2015 aims to limit global warming to 1.5 degrees Celsius above pre-industrial levels."
        ),
        "source": "IPCC Sixth Assessment Report 2022",
        "keywords": ["climate", "temperature", "warming", "paris", "fossil"],
        "base_relevance": 0.90
    },
    {
        "content": (
            "Renewable energy sources including solar, wind, and hydroelectric power are crucial for reducing "
            "greenhouse gas emissions. The transition to clean energy requires significant investment in "
            "infrastructure and technology development."
        ),
        "source": "International Energy Agency Report 2023",
        "keywords": ["renewable", "energy", "solar", "wind", "emissions"],
        "base_relevance": 0.85
    },
    {
        "content": (
            "Scientific research methodology requires rigorous experimental design, peer review, and reproducibility. "
            "Evidence-based conclusions must be supported by data from multiple independent studies. "
            "Statistical significance alone does not imply practical importance or causation."
        ),
        "source": "Nature Scientific Methods Handbook 2022",
        "keywords": ["research", "scientific", "evidence", "methodology", "study"],
        "base_relevance": 0.75
    }
]


def retrieve_documents(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Retrieve relevant evidence documents for the given query.
    
    Phase 1 Implementation: Returns deterministic stub evidence
    based on query keyword matching for consistent testing.
    
    Args:
        query: The query to search for relevant documents.
        top_k: Maximum number of documents to retrieve (default: 3).
        
    Returns:
        List of dictionaries containing 'content', 'source', and 'relevance_score'.
        
    Examples:
        >>> docs = retrieve_documents("health impacts of pollution", top_k=2)
        >>> assert len(docs) <= 2
        >>> assert all('content' in d and 'source' in d for d in docs)
    """
    if not query or not query.strip():
        return []
    
    if top_k <= 0:
        return []
    
    query_lower = query.lower()
    scored_evidence: List[tuple[float, Dict[str, Any]]] = []
    
    for evidence in _STUB_EVIDENCE_CORPUS:
        # Calculate keyword match score
        keyword_matches = sum(
            1 for keyword in evidence["keywords"]
            if keyword in query_lower
        )
        
        # Combine base relevance with keyword boost
        if keyword_matches > 0:
            relevance_boost = min(keyword_matches * 0.05, 0.15)
            final_relevance = min(evidence["base_relevance"] + relevance_boost, 1.0)
        else:
            # Still include with lower relevance for variety
            final_relevance = evidence["base_relevance"] * 0.5
        
        scored_evidence.append((
            final_relevance,
            {
                "content": evidence["content"],
                "source": evidence["source"],
                "relevance_score": round(final_relevance, 3)
            }
        ))
    
    # Sort by relevance (descending) and take top_k
    scored_evidence.sort(key=lambda x: x[0], reverse=True)
    
    return [item[1] for item in scored_evidence[:top_k]]


def get_corpus_size() -> int:
    """
    Get the total number of documents in the evidence corpus.
    
    Returns:
        Number of documents in the corpus.
    """
    return len(_STUB_EVIDENCE_CORPUS)


def get_available_sources() -> List[str]:
    """
    Get a list of all available evidence sources.
    
    Returns:
        List of source identifiers in the corpus.
    """
    return [evidence["source"] for evidence in _STUB_EVIDENCE_CORPUS]
