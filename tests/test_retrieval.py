"""
Evidence Retrieval Integration Tests
"""

import pytest

from retrieval.service import retrieve_documents


class TestRetrieveDocuments:
    def test_returns_list(self):
        result = retrieve_documents("Test query")
        assert isinstance(result, list)
    
    def test_empty_query_returns_empty(self):
        assert retrieve_documents("") == []
    
    def test_whitespace_query_returns_empty(self):
        assert retrieve_documents("   ") == []
    
    def test_top_k_zero_returns_empty(self):
        assert retrieve_documents("test", top_k=0) == []
    
    def test_top_k_negative_returns_empty(self):
        assert retrieve_documents("test", top_k=-1) == []


class TestRetrieveDocumentsWithIndex:
    """Tests that require an indexed knowledge base."""
    
    @pytest.fixture(autouse=True)
    def skip_if_empty(self):
        result = retrieve_documents("test")
        if not result:
            pytest.skip("Vector store is empty - run ingestion first")
    
    def test_returns_results(self):
        result = retrieve_documents("health impacts")
        assert len(result) > 0
    
    def test_respects_top_k(self):
        result = retrieve_documents("test query", top_k=2)
        assert len(result) <= 2
    
    def test_result_structure(self):
        result = retrieve_documents("test query")
        for r in result:
            assert "content" in r
            assert "source" in r
            assert "relevance_score" in r
    
    def test_relevance_score_range(self):
        result = retrieve_documents("climate change")
        for r in result:
            assert 0 <= r["relevance_score"] <= 1
