"""
API Module - FastAPI Routes and Schemas

Provides API endpoints and request/response models.
"""

from api.routes import router
from api.schemas import AnalyzeRequest, AnalyzeResponse, EvidenceChunk

__all__ = ["router", "AnalyzeRequest", "AnalyzeResponse", "EvidenceChunk"]
