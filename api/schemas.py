"""
Pydantic Schemas for API

Request and response models with validation.
"""

from pydantic import BaseModel, Field
from typing import List


class AnalyzeRequest(BaseModel):
    """Request schema for /analyze endpoint."""
    query: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The query to analyze"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [{"query": "What are the health impacts of air pollution?"}]
        }
    }


class EvidenceChunk(BaseModel):
    """Single piece of retrieved evidence."""
    content: str = Field(..., description="Evidence text content")
    source: str = Field(..., description="Source document identifier")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Relevance score")


class AnalyzeResponse(BaseModel):
    """Response schema for /analyze endpoint."""
    query: str = Field(..., description="Original query")
    llm_answer: str = Field(..., description="LLM-generated answer")
    retrieved_evidence: List[EvidenceChunk] = Field(
        default_factory=list,
        description="Retrieved evidence chunks"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "query": "What are the health impacts of air pollution?",
                "llm_answer": "Air pollution has significant health impacts...",
                "retrieved_evidence": [{
                    "content": "Studies show air pollution affects health...",
                    "source": "WHO Report 2023",
                    "relevance_score": 0.92
                }]
            }]
        }
    }
