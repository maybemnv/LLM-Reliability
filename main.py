"""
LLM Reliability Engine - FastAPI Application

Auditing and Scoring Trustworthiness of LLM Outputs.

Usage:
    uvicorn main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router

APP_TITLE = "LLM Reliability Engine"
APP_VERSION = "0.1.0"

app = FastAPI(
    title=APP_TITLE,
    description="Auditing and Scoring Trustworthiness of LLM Outputs",
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["root"])
async def root() -> dict:
    """Root endpoint - API information."""
    return {
        "name": APP_TITLE,
        "version": APP_VERSION,
        "documentation": "/docs"
    }


@app.get("/health", tags=["health"])
async def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": APP_VERSION,
        "service": "llm-reliability-engine"
    }
