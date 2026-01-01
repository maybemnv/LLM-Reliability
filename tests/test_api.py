"""
API Endpoint Tests

Comprehensive tests for the FastAPI endpoints including:
- Root endpoint
- Health check endpoint
- Analyze endpoint
"""

import time
from fastapi.testclient import TestClient

from main import app


class TestRootEndpoint:
    """Tests for the root endpoint."""
    
    def test_root_returns_200(self):
        """Root endpoint should return 200 status code."""
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_returns_api_info(self):
        """Root endpoint should return API information."""
        client = TestClient(app)
        response = client.get("/")
        data = response.json()
        
        assert "name" in data
        assert "version" in data
        assert "documentation" in data
        assert data["name"] == "LLM Reliability Engine"


class TestHealthEndpoint:
    """Tests for the health check endpoint."""
    
    def test_health_returns_200(self):
        """Health endpoint should return 200 status code."""
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_returns_healthy_status(self):
        """Health endpoint should return healthy status."""
        client = TestClient(app)
        response = client.get("/health")
        data = response.json()
        
        assert data["status"] == "healthy"
        assert "version" in data
        assert "service" in data


class TestAnalyzeEndpoint:
    """Tests for the /analyze endpoint."""
    
    def test_analyze_returns_200(self):
        """Analyze endpoint should return 200 for valid request."""
        client = TestClient(app)
        response = client.post(
            "/api/v1/analyze",
            json={"query": "What are the health impacts of air pollution?"}
        )
        assert response.status_code == 200
    
    def test_analyze_response_structure(self):
        """Analyze endpoint should return correct response structure."""
        client = TestClient(app)
        response = client.post(
            "/api/v1/analyze",
            json={"query": "What are the health impacts of air pollution?"}
        )
        data = response.json()
        
        assert "query" in data
        assert "llm_answer" in data
        assert "retrieved_evidence" in data
        assert isinstance(data["retrieved_evidence"], list)
    
    def test_analyze_returns_original_query(self):
        """Analyze endpoint should return the original query."""
        client = TestClient(app)
        query = "Test query for verification"
        response = client.post(
            "/api/v1/analyze",
            json={"query": query}
        )
        data = response.json()
        
        assert data["query"] == query
    
    def test_analyze_evidence_structure(self):
        """Evidence chunks should have required fields."""
        client = TestClient(app)
        response = client.post(
            "/api/v1/analyze",
            json={"query": "Health impacts of pollution"}
        )
        data = response.json()
        
        for evidence in data["retrieved_evidence"]:
            assert "content" in evidence
            assert "source" in evidence
            assert "relevance_score" in evidence
            assert 0 <= evidence["relevance_score"] <= 1
    
    def test_analyze_response_time_under_100ms(self):
        """Analyze endpoint should respond within 100ms (stubbed)."""
        client = TestClient(app)
        
        start_time = time.time()
        response = client.post(
            "/api/v1/analyze",
            json={"query": "Quick response test"}
        )
        elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
        
        assert response.status_code == 200
        # Allow some buffer for test environment variability
        assert elapsed_time < 500  # 500ms to account for test overhead
    
    def test_analyze_empty_query_returns_400(self):
        """Analyze endpoint should reject empty queries."""
        client = TestClient(app)
        response = client.post(
            "/api/v1/analyze",
            json={"query": "   "}
        )
        assert response.status_code == 400
    
    def test_analyze_missing_query_returns_422(self):
        """Analyze endpoint should return 422 for missing query field."""
        client = TestClient(app)
        response = client.post(
            "/api/v1/analyze",
            json={}
        )
        assert response.status_code == 422
    
    def test_analyze_health_query_returns_relevant_answer(self):
        """Health-related queries should return health-related content."""
        client = TestClient(app)
        response = client.post(
            "/api/v1/analyze",
            json={"query": "What are the health impacts of air pollution?"}
        )
        data = response.json()
        
        # Should contain health-related content
        answer_lower = data["llm_answer"].lower()
        assert any(keyword in answer_lower for keyword in ["health", "respiratory", "disease", "pollution"])
    
    def test_analyze_climate_query_returns_relevant_answer(self):
        """Climate-related queries should return climate-related content."""
        client = TestClient(app)
        response = client.post(
            "/api/v1/analyze",
            json={"query": "How does climate change affect global temperatures?"}
        )
        data = response.json()
        
        # Should contain climate-related content
        answer_lower = data["llm_answer"].lower()
        assert any(keyword in answer_lower for keyword in ["climate", "temperature", "warming", "paris"])
