"""
API Module - FastAPI routes and request/response schemas

This module provides:
- routes: API endpoint handlers
- schemas: Pydantic models for request/response validation
"""

from src.api.routes import router
from src.api.schemas import AnalyzeRequest, AnalyzeResponse, EvidenceChunk

__all__ = ["router", "AnalyzeRequest", "AnalyzeResponse", "EvidenceChunk"]
