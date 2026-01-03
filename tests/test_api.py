"""
API Endpoint Tests
"""

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestRootEndpoint:
    def test_root_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_contains_name(self, client):
        response = client.get("/")
        assert "name" in response.json()


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_status_healthy(self, client):
        response = client.get("/health")
        assert response.json()["status"] == "healthy"


class TestAnalyzeEndpoint:
    def test_analyze_returns_200(self, client):
        response = client.post(
            "/api/v1/analyze",
            json={"query": "What are the health impacts of pollution?"}
        )
        assert response.status_code == 200
    
    def test_analyze_returns_query(self, client):
        query = "Test query"
        response = client.post("/api/v1/analyze", json={"query": query})
        assert response.json()["query"] == query
    
    def test_analyze_returns_llm_answer(self, client):
        response = client.post(
            "/api/v1/analyze",
            json={"query": "health effects"}
        )
        assert "llm_answer" in response.json()
        assert len(response.json()["llm_answer"]) > 0
    
    def test_analyze_returns_evidence(self, client):
        response = client.post(
            "/api/v1/analyze",
            json={"query": "climate change"}
        )
        assert "retrieved_evidence" in response.json()
    
    def test_analyze_empty_query_fails(self, client):
        response = client.post("/api/v1/analyze", json={"query": ""})
        assert response.status_code == 422
    
    def test_analyze_missing_query_fails(self, client):
        response = client.post("/api/v1/analyze", json={})
        assert response.status_code == 422
