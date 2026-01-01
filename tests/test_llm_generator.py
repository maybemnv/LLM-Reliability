"""
LLM Generator Tests

Tests for the stub LLM response generator including:
- Basic response generation
- Keyword-based response selection
- Edge case handling
"""

import pytest

from src.llm.generator import generate_answer, generate_answer_with_metadata


class TestGenerateAnswer:
    """Tests for the generate_answer function."""
    
    def test_returns_string(self):
        """generate_answer should return a string."""
        result = generate_answer("Test query")
        assert isinstance(result, str)
    
    def test_returns_non_empty_string(self):
        """generate_answer should return non-empty content."""
        result = generate_answer("Test query")
        assert len(result) > 0
    
    def test_deterministic_output(self):
        """Same query should produce same output."""
        query = "What are the health impacts of air pollution?"
        result1 = generate_answer(query)
        result2 = generate_answer(query)
        assert result1 == result2
    
    def test_health_query_returns_health_response(self):
        """Health-related query should return health response."""
        query = "What are the health effects of pollution?"
        result = generate_answer(query)
        assert any(word in result.lower() for word in ["health", "respiratory", "cardiovascular"])
    
    def test_climate_query_returns_climate_response(self):
        """Climate-related query should return climate response."""
        query = "How does climate change affect temperature?"
        result = generate_answer(query)
        assert any(word in result.lower() for word in ["climate", "warming", "temperature", "paris"])
    
    def test_generic_query_returns_default_response(self):
        """Generic query should return default response."""
        query = "Tell me something interesting"
        result = generate_answer(query)
        assert "factors" in result.lower() or "consideration" in result.lower()
    
    def test_empty_query_handled(self):
        """Empty query should return appropriate response."""
        result = generate_answer("")
        assert "empty" in result.lower()
    
    def test_whitespace_only_query_handled(self):
        """Whitespace-only query should return appropriate response."""
        result = generate_answer("   ")
        assert "empty" in result.lower()
    
    def test_none_query_handled(self):
        """None query should return appropriate response."""
        result = generate_answer(None)
        assert "empty" in result.lower()
    
    def test_disease_keyword_triggers_health_response(self):
        """Disease keyword should trigger health response."""
        query = "What diseases are common?"
        result = generate_answer(query)
        assert any(word in result.lower() for word in ["health", "disease", "respiratory"])
    
    def test_carbon_keyword_triggers_climate_response(self):
        """Carbon keyword should trigger climate response."""
        query = "What is the carbon cycle?"
        result = generate_answer(query)
        assert any(word in result.lower() for word in ["climate", "carbon", "emissions"])


class TestGenerateAnswerWithMetadata:
    """Tests for the generate_answer_with_metadata function."""
    
    def test_returns_dictionary(self):
        """Should return a dictionary."""
        result = generate_answer_with_metadata("Test query")
        assert isinstance(result, dict)
    
    def test_contains_answer_key(self):
        """Result should contain 'answer' key."""
        result = generate_answer_with_metadata("Test query")
        assert "answer" in result
    
    def test_contains_model_key(self):
        """Result should contain 'model' key."""
        result = generate_answer_with_metadata("Test query")
        assert "model" in result
        assert result["model"] == "stub-v1"
    
    def test_contains_provider_key(self):
        """Result should contain 'provider' key."""
        result = generate_answer_with_metadata("Test query")
        assert "provider" in result
        assert result["provider"] == "local-stub"
    
    def test_answer_matches_direct_call(self):
        """Answer should match direct function call."""
        query = "Test query"
        direct_answer = generate_answer(query)
        metadata_result = generate_answer_with_metadata(query)
        assert metadata_result["answer"] == direct_answer
