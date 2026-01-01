"""
API Routes for LLM Reliability Engine

This module defines the FastAPI routes for the reliability analysis endpoints.
"""

from fastapi import APIRouter, HTTPException
from typing import List

from src.api.schemas import AnalyzeRequest, AnalyzeResponse, EvidenceChunk
from src.llm.generator import generate_answer
from src.retrieval.vector_store import retrieve_documents


router = APIRouter(prefix="/api/v1", tags=["analysis"])


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Analyze LLM response reliability",
    description="Analyzes a query by generating an LLM response and retrieving evidence for verification."
)
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analyze the reliability of an LLM response for a given query.
    
    This endpoint:
    1. Generates an LLM response for the query
    2. Retrieves relevant evidence documents
    3. Returns the response with evidence for verification
    
    Args:
        request: The analysis request containing the query.
        
    Returns:
        AnalyzeResponse with query, LLM answer, and retrieved evidence.
        
    Raises:
        HTTPException: If the query is empty or processing fails.
    """
    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty or whitespace only"
        )
    
    # Generate LLM response (stub implementation)
    llm_answer = generate_answer(request.query)
    
    # Retrieve relevant evidence (stub implementation)
    evidence_data = retrieve_documents(request.query)
    
    # Convert to EvidenceChunk models
    evidence_chunks: List[EvidenceChunk] = [
        EvidenceChunk(
            content=chunk["content"],
            source=chunk["source"],
            relevance_score=chunk["relevance_score"]
        )
        for chunk in evidence_data
    ]
    
    return AnalyzeResponse(
        query=request.query,
        llm_answer=llm_answer,
        retrieved_evidence=evidence_chunks
    )
