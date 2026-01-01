"""
Evidence Retrieval Tests

Tests for the stub evidence retrieval including:
- Document retrieval
- Relevance scoring
- Edge case handling
"""

import pytest

from src.retrieval.vector_store import (
    retrieve_documents,
    get_corpus_size,
    get_available_sources
)


class TestRetrieveDocuments:
    """Tests for the retrieve_documents function."""
    
    def test_returns_list(self):
        """retrieve_documents should return a list."""
        result = retrieve_documents("Test query")
        assert isinstance(result, list)
    
    def test_returns_non_empty_for_valid_query(self):
        """Valid query should return non-empty list."""
        result = retrieve_documents("health impacts of pollution")
        assert len(result) > 0
    
    def test_respects_top_k_parameter(self):
        """Should return at most top_k documents."""
        result = retrieve_documents("test query", top_k=2)
        assert len(result) <= 2
    
    def test_top_k_one(self):
        """top_k=1 should return single document."""
        result = retrieve_documents("test query", top_k=1)
        assert len(result) == 1
    
    def test_default_top_k_is_three(self):
        """Default top_k should be 3."""
        result = retrieve_documents("test query")
        assert len(result) <= 3
    
    def test_document_structure(self):
        """Each document should have required fields."""
        result = retrieve_documents("test query")
        for doc in result:
            assert "content" in doc
            assert "source" in doc
            assert "relevance_score" in doc
    
    def test_relevance_score_range(self):
        """Relevance scores should be between 0 and 1."""
        result = retrieve_documents("test query")
        for doc in result:
            assert 0 <= doc["relevance_score"] <= 1
    
    def test_sorted_by_relevance(self):
        """Documents should be sorted by relevance (descending)."""
        result = retrieve_documents("test query")
        if len(result) > 1:
            scores = [doc["relevance_score"] for doc in result]
            assert scores == sorted(scores, reverse=True)
    
    def test_health_query_returns_health_evidence(self):
        """Health query should return health-related evidence."""
        result = retrieve_documents("health impacts of air pollution")
        assert len(result) > 0
        # First result should be health-related
        top_content = result[0]["content"].lower()
        assert any(word in top_content for word in ["health", "air", "pollution", "respiratory"])
    
    def test_climate_query_returns_climate_evidence(self):
        """Climate query should return climate-related evidence."""
        result = retrieve_documents("climate change global warming temperatures")
        assert len(result) > 0
        # Check if climate-related evidence is in top results
        all_content = " ".join(doc["content"].lower() for doc in result)
        assert any(word in all_content for word in ["climate", "warming", "temperature"])
    
    def test_empty_query_returns_empty_list(self):
        """Empty query should return empty list."""
        result = retrieve_documents("")
        assert result == []
    
    def test_whitespace_query_returns_empty_list(self):
        """Whitespace-only query should return empty list."""
        result = retrieve_documents("   ")
        assert result == []
    
    def test_top_k_zero_returns_empty(self):
        """top_k=0 should return empty list."""
        result = retrieve_documents("test query", top_k=0)
        assert result == []
    
    def test_top_k_negative_returns_empty(self):
        """Negative top_k should return empty list."""
        result = retrieve_documents("test query", top_k=-1)
        assert result == []
    
    def test_deterministic_output(self):
        """Same query should produce same output."""
        query = "health impacts"
        result1 = retrieve_documents(query)
        result2 = retrieve_documents(query)
        assert result1 == result2
    
    def test_sources_are_strings(self):
        """All sources should be strings."""
        result = retrieve_documents("test query")
        for doc in result:
            assert isinstance(doc["source"], str)
            assert len(doc["source"]) > 0
    
    def test_content_is_non_empty(self):
        """All content should be non-empty strings."""
        result = retrieve_documents("test query")
        for doc in result:
            assert isinstance(doc["content"], str)
            assert len(doc["content"]) > 0


class TestCorpusMetadata:
    """Tests for corpus metadata functions."""
    
    def test_get_corpus_size_returns_int(self):
        """get_corpus_size should return an integer."""
        result = get_corpus_size()
        assert isinstance(result, int)
    
    def test_corpus_size_is_positive(self):
        """Corpus size should be positive."""
        result = get_corpus_size()
        assert result > 0
    
    def test_get_available_sources_returns_list(self):
        """get_available_sources should return a list."""
        result = get_available_sources()
        assert isinstance(result, list)
    
    def test_sources_list_matches_corpus_size(self):
        """Number of sources should match corpus size."""
        sources = get_available_sources()
        size = get_corpus_size()
        assert len(sources) == size
    
    def test_all_sources_are_strings(self):
        """All sources should be strings."""
        sources = get_available_sources()
        for source in sources:
            assert isinstance(source, str)
            assert len(source) > 0
