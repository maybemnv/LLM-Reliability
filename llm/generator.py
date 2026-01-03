"""
LLM Response Generator

Stub implementation for LLM response generation.
Returns deterministic responses based on query keywords.
"""

from typing import Dict

STUB_RESPONSES = {
    "default": (
        "Based on available information, this topic involves multiple factors "
        "that require careful consideration. The evidence suggests several key points: "
        "First, there are environmental considerations that affect outcomes. "
        "Second, health implications vary based on exposure levels and duration. "
        "Third, mitigation strategies exist but require proper implementation."
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
    
    Stub implementation: returns keyword-based responses.
    
    Args:
        query: The user's query.
        
    Returns:
        Generated response string.
    """
    if not query or not query.strip():
        return "Unable to generate response for empty query."
    
    query_lower = query.lower()
    
    if any(kw in query_lower for kw in ["health", "pollution", "air", "disease"]):
        return STUB_RESPONSES["health"]
    elif any(kw in query_lower for kw in ["climate", "warming", "carbon", "temperature"]):
        return STUB_RESPONSES["climate"]
    
    return STUB_RESPONSES["default"]


def generate_answer_with_metadata(query: str) -> Dict[str, str]:
    """Generate response with model metadata."""
    return {
        "answer": generate_answer(query),
        "model": "stub-v1",
        "provider": "local-stub"
    }
