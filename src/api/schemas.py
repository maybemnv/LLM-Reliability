"""
Pydantic Schemas for API Request/Response Validation

This module defines the data contracts for the LLM Reliability Engine API.
All schemas use strict validation to ensure data integrity.
"""

from pydantic import BaseModel, Field
from typing import List


class AnalyzeRequest(BaseModel):
    """
    Request schema for the /analyze endpoint.
    
    Attributes:
        query: The user's query to analyze for reliability.
    """
    query: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The query to analyze for reliability assessment"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"query": "What are the health impacts of air pollution?"}
            ]
        }
    }


class EvidenceChunk(BaseModel):
    """
    Represents a single piece of retrieved evidence.
    
    Attributes:
        content: The text content of the evidence chunk.
        source: The source document or reference for this evidence.
        relevance_score: Similarity score between 0 and 1.
    """
    content: str = Field(
        ...,
        description="The text content of the evidence chunk"
    )
    source: str = Field(
        ...,
        description="Source document or reference identifier"
    )
    relevance_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Relevance score between 0.0 and 1.0"
    )


class AnalyzeResponse(BaseModel):
    """
    Response schema for the /analyze endpoint.
    
    Contains the original query, the LLM-generated answer,
    and a list of retrieved evidence chunks for verification.
    
    Attributes:
        query: The original query that was analyzed.
        llm_answer: The generated response from the LLM.
        retrieved_evidence: List of evidence chunks retrieved for verification.
    """
    query: str = Field(
        ...,
        description="The original query that was analyzed"
    )
    llm_answer: str = Field(
        ...,
        description="The LLM-generated answer to the query"
    )
    retrieved_evidence: List[EvidenceChunk] = Field(
        default_factory=list,
        description="List of evidence chunks retrieved for verification"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query": "What are the health impacts of air pollution?",
                    "llm_answer": "Air pollution has significant health impacts...",
                    "retrieved_evidence": [
                        {
                            "content": "Studies show air pollution affects respiratory health...",
                            "source": "WHO Health Report 2023",
                            "relevance_score": 0.92
                        }
                    ]
                }
            ]
        }
    }
