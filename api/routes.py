"""
API Routes

FastAPI endpoint handlers for reliability analysis.
"""

from fastapi import APIRouter, HTTPException
from typing import List

from api.schemas import AnalyzeRequest, AnalyzeResponse, EvidenceChunk
from llm.generator import generate_answer
from retrieval.service import retrieve_documents


router = APIRouter(prefix="/api/v1", tags=["analysis"])


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Analyze LLM response reliability"
)
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analyze the reliability of an LLM response.
    
    1. Generates an LLM response for the query
    2. Retrieves relevant evidence documents
    3. Returns response with evidence for verification
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    llm_answer = generate_answer(request.query)
    evidence_data = retrieve_documents(request.query)
    
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
