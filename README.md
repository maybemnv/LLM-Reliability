# LLM Reliability

### Auditing and Scoring Trustworthiness of Large Language Model Outputs

## Overview

Large Language Models (LLMs) are increasingly deployed in high-impact domains such as healthcare, legal analysis, governance, and enterprise decision-making. While these models generate fluent responses, they often produce hallucinations—confident but unsupported or incorrect claims.

The LLM Reliability Engine is a system designed to audit, evaluate, and score the trustworthiness of LLM-generated responses using retrieval-based evidence verification and explainable scoring mechanisms.

Unlike traditional RAG systems that support generation, this project focuses on post-hoc evaluation and reliability assessment.

## Key Capabilities

- Claim-level verification of LLM responses
- Evidence retrieval using vector search (FAISS)
- Semantic alignment scoring between claims and evidence
- Explainable confidence score and hallucination risk labeling
- Structured, machine-readable reliability reports

## System Architecture

1. **User Query**: Input from the user.
2. **LLM Response Generator**: The model generates a response.
3. **Evidence Retrieval**: Relevant documents are fetched from the vector database.
4. **Claim Decomposition**: The response is split into individual claims.
5. **Claim-Evidence Matching**: Claims are compared against evidence.
6. **Reliability Aggregation**: Scores are combined.
7. **Reliability Report**: Final JSON output.

## Tech Stack

- **Language**: Python
- **API Framework**: FastAPI
- **LLM Integration**: OpenAI / Gemini
- **Embeddings**: SentenceTransformers
- **Vector Store**: FAISS
- **ML Utilities**: scikit-learn
- **Frameworks**: LangChain (minimal usage)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/maybemnv/llm-reliability-engine.git
cd llm-reliability-engine
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Knowledge Base Documents

Place PDF or text files inside `data/knowledge_base/`.

### 5. Run the API

```bash
uvicorn src.api.main:app --reload
```

## Usage

### Analyze Endpoint

**POST** `/analyze`

**Request:**

```json
{
  "query": "What are the health impacts of air pollution?"
}
```

**Response:**

```json
{
  "confidence_score": 0.78,
  "hallucination_risk": "MEDIUM",
  "unsupported_claims": ["Air pollution causes all forms of cancer"]
}
```

## Limitations

- Semantic similarity does not guarantee factual correctness.
- Dependent on quality and coverage of the knowledge base.
- No real-time web verification.
- Sentence-level claim extraction may miss complex logic.

## Future Improvements

- Cross-claim logical consistency checks.
- Cross-encoder reranking for stronger verification.
- Domain-specific reliability calibration.
- Monitoring dashboards for enterprise usage.

## Author

**Manav Kaushal**

- GitHub: https://github.com/maybemnv
- LinkedIn: https://linkedin.com/in/maybmnv

## License

This project is released for educational and research purposes.
