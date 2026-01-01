"""
Pydantic Schema Validation Tests

Tests for request/response schema validation including:
- AnalyzeRequest validation
- EvidenceChunk validation
- AnalyzeResponse validation
"""

import pytest
from pydantic import ValidationError

from src.api.schemas import AnalyzeRequest, EvidenceChunk, AnalyzeResponse


class TestAnalyzeRequest:
    """Tests for AnalyzeRequest schema validation."""
    
    def test_valid_query(self):
        """Valid query should create request successfully."""
        request = AnalyzeRequest(query="What is machine learning?")
        assert request.query == "What is machine learning?"
    
    def test_query_with_special_characters(self):
        """Query with special characters should be accepted."""
        request = AnalyzeRequest(query="What's the effect of CO2 & pollution?")
        assert "CO2" in request.query
    
    def test_empty_query_rejected(self):
        """Empty query should be rejected."""
        with pytest.raises(ValidationError):
            AnalyzeRequest(query="")
    
    def test_missing_query_rejected(self):
        """Missing query field should be rejected."""
        with pytest.raises(ValidationError):
            AnalyzeRequest()
    
    def test_query_max_length(self):
        """Query exceeding max length should be rejected."""
        long_query = "a" * 10001
        with pytest.raises(ValidationError):
            AnalyzeRequest(query=long_query)
    
    def test_query_at_max_length(self):
        """Query at max length should be accepted."""
        max_query = "a" * 10000
        request = AnalyzeRequest(query=max_query)
        assert len(request.query) == 10000


class TestEvidenceChunk:
    """Tests for EvidenceChunk schema validation."""
    
    def test_valid_evidence_chunk(self):
        """Valid evidence chunk should create successfully."""
        chunk = EvidenceChunk(
            content="This is evidence content.",
            source="Test Source 2023",
            relevance_score=0.85
        )
        assert chunk.content == "This is evidence content."
        assert chunk.source == "Test Source 2023"
        assert chunk.relevance_score == 0.85
    
    def test_relevance_score_at_zero(self):
        """Relevance score of 0 should be valid."""
        chunk = EvidenceChunk(
            content="Content",
            source="Source",
            relevance_score=0.0
        )
        assert chunk.relevance_score == 0.0
    
    def test_relevance_score_at_one(self):
        """Relevance score of 1 should be valid."""
        chunk = EvidenceChunk(
            content="Content",
            source="Source",
            relevance_score=1.0
        )
        assert chunk.relevance_score == 1.0
    
    def test_relevance_score_below_zero_rejected(self):
        """Relevance score below 0 should be rejected."""
        with pytest.raises(ValidationError):
            EvidenceChunk(
                content="Content",
                source="Source",
                relevance_score=-0.1
            )
    
    def test_relevance_score_above_one_rejected(self):
        """Relevance score above 1 should be rejected."""
        with pytest.raises(ValidationError):
            EvidenceChunk(
                content="Content",
                source="Source",
                relevance_score=1.1
            )
    
    def test_missing_content_rejected(self):
        """Missing content field should be rejected."""
        with pytest.raises(ValidationError):
            EvidenceChunk(source="Source", relevance_score=0.5)
    
    def test_missing_source_rejected(self):
        """Missing source field should be rejected."""
        with pytest.raises(ValidationError):
            EvidenceChunk(content="Content", relevance_score=0.5)


class TestAnalyzeResponse:
    """Tests for AnalyzeResponse schema validation."""
    
    def test_valid_response(self):
        """Valid response should create successfully."""
        response = AnalyzeResponse(
            query="Test query",
            llm_answer="Test answer",
            retrieved_evidence=[]
        )
        assert response.query == "Test query"
        assert response.llm_answer == "Test answer"
        assert response.retrieved_evidence == []
    
    def test_response_with_evidence(self):
        """Response with evidence chunks should work."""
        evidence = EvidenceChunk(
            content="Evidence content",
            source="Source",
            relevance_score=0.9
        )
        response = AnalyzeResponse(
            query="Query",
            llm_answer="Answer",
            retrieved_evidence=[evidence]
        )
        assert len(response.retrieved_evidence) == 1
        assert response.retrieved_evidence[0].relevance_score == 0.9
    
    def test_response_default_empty_evidence(self):
        """Response should default to empty evidence list."""
        response = AnalyzeResponse(
            query="Query",
            llm_answer="Answer"
        )
        assert response.retrieved_evidence == []
    
    def test_response_missing_query_rejected(self):
        """Missing query should be rejected."""
        with pytest.raises(ValidationError):
            AnalyzeResponse(llm_answer="Answer")
    
    def test_response_missing_answer_rejected(self):
        """Missing llm_answer should be rejected."""
        with pytest.raises(ValidationError):
            AnalyzeResponse(query="Query")
