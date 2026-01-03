"""
LLM Generator Tests
"""

import pytest

from llm.generator import generate_answer, generate_answer_with_metadata


class TestGenerateAnswer:
    def test_returns_string(self):
        result = generate_answer("Test query")
        assert isinstance(result, str)
    
    def test_non_empty_result(self):
        result = generate_answer("Test query")
        assert len(result) > 0
    
    def test_health_query_returns_health_response(self):
        result = generate_answer("health impacts of pollution")
        assert "health" in result.lower() or "respiratory" in result.lower()
    
    def test_climate_query_returns_climate_response(self):
        result = generate_answer("climate change effects")
        assert "climate" in result.lower() or "warming" in result.lower()
    
    def test_empty_query(self):
        result = generate_answer("")
        assert "empty" in result.lower()
    
    def test_deterministic_output(self):
        query = "test query"
        r1 = generate_answer(query)
        r2 = generate_answer(query)
        assert r1 == r2


class TestGenerateAnswerWithMetadata:
    def test_returns_dict(self):
        result = generate_answer_with_metadata("Test query")
        assert isinstance(result, dict)
    
    def test_contains_answer(self):
        result = generate_answer_with_metadata("Test query")
        assert "answer" in result
        assert len(result["answer"]) > 0
    
    def test_contains_model_info(self):
        result = generate_answer_with_metadata("Test query")
        assert "model" in result
        assert "provider" in result
