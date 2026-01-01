"""
Shared Test Fixtures and Configuration

This module provides shared pytest fixtures and test utilities
used across all test modules.
"""

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client() -> TestClient:
    """
    Create a FastAPI test client.
    
    Returns:
        TestClient instance for making test requests.
    """
    return TestClient(app)


@pytest.fixture
def sample_query() -> str:
    """
    Provide a sample query for testing.
    
    Returns:
        A sample query string.
    """
    return "What are the health impacts of air pollution?"


@pytest.fixture
def sample_health_query() -> str:
    """
    Provide a health-related query for testing.
    
    Returns:
        A health-related query string.
    """
    return "What are the effects of pollution on respiratory health?"


@pytest.fixture
def sample_climate_query() -> str:
    """
    Provide a climate-related query for testing.
    
    Returns:
        A climate-related query string.
    """
    return "How does climate change affect global temperatures?"
