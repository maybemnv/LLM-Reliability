from fastapi import FastAPI
from pydantic import BaseModel

from src.llm.generator import generate_answer
from src.retrieval.vector_store import retrieve_documents

app = FastAPI(title="LLM Reliability Engine")

class AnalyzeRequest(BaseModel):
    query: str

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    answer = generate_answer(request.query)
    evidence = retrieve_documents(request.query)

    return {
        "query": request.query,
        "llm_answer": answer,
        "retrieved_evidence": evidence
    }
