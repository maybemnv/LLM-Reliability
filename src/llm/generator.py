"""
LLM Response Generator

This module provides LLM response generation functionality.
Phase 1: Stub implementation with deterministic responses.
Future phases will integrate with actual LLM APIs (OpenAI/Gemini).
"""

from typing import Dict

# Stub responses for deterministic testing
_STUB_RESPONSES: Dict[str, str] = {
    "default": (
        "Based on available information, this topic involves multiple factors "
        "that require careful consideration. The evidence suggests several key points: "
        "First, there are environmental considerations that affect outcomes. "
        "Second, health implications vary based on exposure levels and duration. "
        "Third, mitigation strategies exist but require proper implementation. "
        "Further analysis of specific context would provide more detailed insights."
    ),
    "health": (
        "Air pollution has significant health impacts including respiratory diseases, "
        "cardiovascular problems, and reduced life expectancy. Studies indicate that "
        "fine particulate matter (PM2.5) can penetrate deep into the lungs and bloodstream. "
        "Long-term exposure is associated with increased mortality rates. "
        "Vulnerable populations include children, elderly, and those with pre-existing conditions."
    ),
    "climate": (
        "Climate change is driven by greenhouse gas emissions from human activities. "
        "Key impacts include rising global temperatures, sea level rise, and extreme weather events. "
        "The Paris Agreement aims to limit warming to 1.5°C above pre-industrial levels. "
        "Mitigation strategies include renewable energy adoption and carbon capture technologies."
    )
}


def generate_answer(query: str) -> str:
    """
    Generate an LLM response for the given query.
    
    Phase 1 Implementation: Returns deterministic stub responses
    based on query keywords for consistent testing.
    
    Args:
        query: The user's query to generate a response for.
        
    Returns:
        A string containing the generated response.
        
    Examples:
        >>> answer = generate_answer("What are the health impacts of pollution?")
        >>> assert "health" in answer.lower() or len(answer) > 0
    """
    if not query or not query.strip():
        return "Unable to generate response for empty query."
    
    query_lower = query.lower()
    
    # Select appropriate stub response based on query keywords
    if any(keyword in query_lower for keyword in ["health", "pollution", "air", "disease"]):
        return _STUB_RESPONSES["health"]
    elif any(keyword in query_lower for keyword in ["climate", "warming", "carbon", "temperature"]):
        return _STUB_RESPONSES["climate"]
    
    return _STUB_RESPONSES["default"]


def generate_answer_with_metadata(query: str) -> Dict[str, str]:
    """
    Generate an LLM response with additional metadata.
    
    This function wraps generate_answer and provides additional
    context for debugging and analysis.
    
    Args:
        query: The user's query to generate a response for.
        
    Returns:
        Dictionary containing 'answer' and 'model' metadata.
    """
    return {
        "answer": generate_answer(query),
        "model": "stub-v1",
        "provider": "local-stub"
    }
