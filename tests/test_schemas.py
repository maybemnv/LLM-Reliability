"""
Pydantic Schema Tests
"""

import pytest
from pydantic import ValidationError

from api.schemas import AnalyzeRequest, AnalyzeResponse, EvidenceChunk


class TestAnalyzeRequest:
    def test_valid_request(self):
        request = AnalyzeRequest(query="Test query")
        assert request.query == "Test query"
    
    def test_empty_query_fails(self):
        with pytest.raises(ValidationError):
            AnalyzeRequest(query="")
    
    def test_long_query_fails(self):
        with pytest.raises(ValidationError):
            AnalyzeRequest(query="x" * 10001)


class TestEvidenceChunk:
    def test_valid_chunk(self):
        chunk = EvidenceChunk(
            content="Evidence content",
            source="document.txt",
            relevance_score=0.85
        )
        assert chunk.content == "Evidence content"
        assert chunk.relevance_score == 0.85
    
    def test_score_too_high_fails(self):
        with pytest.raises(ValidationError):
            EvidenceChunk(
                content="Content",
                source="source",
                relevance_score=1.5
            )
    
    def test_score_negative_fails(self):
        with pytest.raises(ValidationError):
            EvidenceChunk(
                content="Content",
                source="source",
                relevance_score=-0.1
            )


class TestAnalyzeResponse:
    def test_valid_response(self):
        response = AnalyzeResponse(
            query="Test query",
            llm_answer="Answer text",
            retrieved_evidence=[]
        )
        assert response.query == "Test query"
        assert response.llm_answer == "Answer text"
    
    def test_response_with_evidence(self):
        evidence = EvidenceChunk(
            content="Evidence",
            source="source.txt",
            relevance_score=0.9
        )
        response = AnalyzeResponse(
            query="Query",
            llm_answer="Answer",
            retrieved_evidence=[evidence]
        )
        assert len(response.retrieved_evidence) == 1
