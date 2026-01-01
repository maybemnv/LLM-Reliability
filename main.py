"""
LLM Reliability Engine - Main Application Entry Point

This is the FastAPI application entry point for the LLM Reliability Engine.
The engine provides post-hoc evaluation and reliability assessment of LLM outputs.

Usage:
    uvicorn main:app --reload

API Documentation:
    - Swagger UI: http://localhost:8000/docs
    - ReDoc: http://localhost:8000/redoc
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import router

# Application metadata
APP_TITLE = "LLM Reliability Engine"
APP_DESCRIPTION = """
Auditing and Scoring Trustworthiness of Large Language Model Outputs.

This API provides:
- **Claim-level verification** of LLM responses
- **Evidence retrieval** using vector search
- **Semantic alignment scoring** between claims and evidence
- **Explainable confidence scores** and hallucination risk labeling
"""
APP_VERSION = "0.1.0"

# Initialize FastAPI application
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router)


@app.get("/", tags=["root"])
async def root() -> dict:
    """
    Root endpoint - returns API information.
    """
    return {
        "name": APP_TITLE,
        "version": APP_VERSION,
        "documentation": "/docs"
    }


@app.get("/health", tags=["health"])
async def health_check() -> dict:
    """
    Health check endpoint for service monitoring.
    
    Returns:
        Dictionary with status and version information.
    """
    return {
        "status": "healthy",
        "version": APP_VERSION,
        "service": "llm-reliability-engine"
    }
