# TechRAG Architect

TechRAG Architect is a local Retrieval-Augmented Generation (RAG) assistant for technical documents.

It allows users to ask questions across multiple technical study fields and receive answers grounded in a local document knowledge base with source citations.

The system combines PDF ingestion, text cleaning, overlapping chunking, sentence-transformer embeddings, persistent ChromaDB vector storage, semantic retrieval, CrossEncoder reranking, automatic category routing, Ollama-based local generation, citation validation, a FastAPI backend, and a Next.js frontend.

---

## Features

- Grounded answers generated from retrieved technical documents
- Source citations with document name and page number
- Automatic study-field routing
- Manual category selection
- Persistent ChromaDB vector database
- CrossEncoder reranking
- Local LLM inference using Ollama
- Knowledge-base browser
- Source inspection
- FastAPI REST API
- Next.js web interface
- End-to-end evaluation
- Automated API tests
- Reproducible RAG pipeline notebook

---

## Architecture

```text
User Question
    |
    v
Next.js Frontend
    |
    v
FastAPI Backend
    |
    v
Auto Category Router
    |
    v
Embedding Model
    |
    v
ChromaDB Vector Search
    |
    v
CrossEncoder Reranker
    |
    v
Top Retrieved Chunks
    |
    v
Grounded Prompt Builder
    |
    v
Gemma 3 4B via Ollama
    |
    v
Citation Validator
    |
    v
Grounded Answer + Sources
```

### Document Ingestion

```text
Technical PDFs
    |
    v
PDF Loader
    |
    v
Text Cleaner
    |
    v
Page-Based Chunking
    |
    v
MiniLM Embeddings
    |
    v
Persistent ChromaDB
```

---

## Knowledge Base

The current local knowledge base contains:

- 38 technical PDF documents
- 42,124 indexed chunks
- 12 technical categories

Categories:

- AI / Machine Learning
- Algorithms & Data Structures
- Cloud Security
- Computer Vision
- Cybersecurity
- Data Science
- Deep Learning
- Embedded Systems
- Large Language Models
- Malware Analysis
- Natural Language Processing
- Python

Raw knowledge-base documents are intentionally excluded from GitHub.

---

## Tech Stack

### Backend
- Python 3.11
- FastAPI
- Pydantic
- Uvicorn

### RAG
- Sentence Transformers
- `sentence-transformers/all-MiniLM-L6-v2`
- ChromaDB
- `cross-encoder/ms-marco-MiniLM-L-6-v2`
- Ollama
- `gemma3:4b`

### Frontend
- Next.js
- TypeScript
- React

### Testing and Evaluation
- Pytest
- FastAPI TestClient
- Pandas
- Jupyter Notebook

---

## Project Structure

```text
RAG-Powered Document/
|
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   └── services.py
|
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   │   └── api.ts
│   ├── .env.example
│   └── package.json
|
├── src/
│   ├── ingestion/
│   │   ├── pdf_loader.py
│   │   ├── cleaner.py
│   │   ├── chunker.py
│   │   └── indexer.py
│   └── rag/
│       ├── embeddings.py
│       ├── retrieval.py
│       ├── reranker.py
│       ├── prompting.py
│       ├── generation.py
│       ├── citation_validator.py
│       └── grounded_generation.py
|
├── scripts/
│   ├── ingest_documents.py
│   ├── test_embeddings.py
│   ├── test_retrieval.py
│   ├── test_rag.py
│   ├── evaluate_rag.py
│   └── evaluate_rag_full.py
|
├── notebooks/
│   └── rag_pipeline.ipynb
|
├── evaluation/
│   ├── rag_evaluation_results.csv
│   └── rag_evaluation_summary.md
|
├── tests/
│   └── test_api.py
|
├── data/
│   ├── raw/
│   ├── processed/
│   └── vector_store/
|
├── .env.example
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## RAG Pipeline

### 1. PDF Loading

The ingestion pipeline recursively discovers PDFs inside:

```text
data/raw/
```

The first folder under `data/raw/` is used as the category.

Example:

```text
data/raw/cybersecurity/book.pdf
```

becomes:

```text
category = cybersecurity
```

PDFs are processed page-by-page using `pypdf`.

### 2. Text Cleaning

The cleaning pipeline:

- fixes simple hyphenated line breaks
- normalizes whitespace
- preserves paragraph structure
- removes empty text

The cleaning process is intentionally conservative to avoid damaging technical content.

### 3. Chunking

The default chunk configuration is:

```text
Chunk size:    1200 characters
Chunk overlap: 200 characters
```

Each chunk receives a deterministic SHA-256-based ID derived from the document, page, and page-local chunk index.

### 4. Embeddings

Embedding model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The project automatically uses CUDA when available.

### 5. Vector Store

ChromaDB is used as the persistent vector database.

Location:

```text
data/vector_store/
```

The collection uses cosine similarity.

### 6. Retrieval and Reranking

The query is embedded and used to search ChromaDB. Candidate chunks are then reranked using:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

### 7. Automatic Category Routing

When the frontend is set to Auto, TechRAG chooses the most relevant technical category.

The routing system combines:

- global semantic document retrieval
- document-level category evidence
- semantic similarity against category descriptions

### 8. Grounded Generation

The generation model is:

```text
gemma3:4b
```

served locally using Ollama.

The model is instructed to answer only from retrieved context.

### 9. Citation Validation

Generated answers are checked against the actual retrieved document/page pairs.

Valid citation format:

```text
[Document: filename.pdf, Page: 10]
```

If citations are missing or invalid, the grounded-generation pipeline can retry with stricter citation instructions.

---

## Evaluation

### Retrieval Evaluation

```text
Top-1 accuracy: 19 / 20
Top-5 accuracy: 20 / 20
```

### Full End-to-End Evaluation

| Metric | Result |
|---|---:|
| Auto-routing correct | 20 / 21 |
| Grounded answers | 20 / 21 |
| Valid citations | 20 / 21 |
| Overall passed | 19 / 21 |
| Overall pass rate | 90.48% |

Evaluation files:

```text
evaluation/rag_evaluation_results.csv
evaluation/rag_evaluation_summary.md
```

Run:

```powershell
python -m scripts.evaluate_rag_full
```

---

## Known Failure Cases

### Dynamic Programming

Expected category:

```text
algorithms_data_structures
```

Resolved category:

```text
ai_ml
```

This is caused by semantic overlap between algorithmic material and machine-learning documents.

### SQL Injection

The router correctly identifies cybersecurity, but some local LLM generations can occasionally fail citation validation.

Mitigations include:

- strict grounding prompts
- exact citation whitelisting
- citation validation
- generation retries

---

## API

Default base URL:

```text
http://127.0.0.1:8000
```

Endpoints:

```text
GET  /health
GET  /stats
GET  /knowledge-base
POST /query
```

Example request:

```json
{
  "question": "What is SQL injection?",
  "category": "cybersecurity"
}
```

Use `null` for automatic category routing:

```json
{
  "question": "What is SQL injection?",
  "category": null
}
```

Example with curl:

```bash
curl -X POST "http://127.0.0.1:8000/query" \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"What is SQL injection?\",\"category\":null}"
```

---

## Installation

### Requirements

- Python 3.11
- Node.js and npm
- Ollama
- Git
- Optional NVIDIA GPU with CUDA support

### 1. Clone

```bash
git clone https://github.com/Abdelrahman-288/RAG-Powered-Document-Assistant.git
cd RAG-Powered-Document-Assistant
```

### 2. Create a Python virtual environment

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Install the Ollama model

```powershell
ollama pull gemma3:4b
ollama list
```

### 5. Environment configuration

Copy `.env.example` to `.env`.

Example:

```env
OLLAMA_MODEL=gemma3:4b
VECTOR_STORE_DIR=data/vector_store
```

Copy `frontend/.env.example` to `frontend/.env.local`.

Example:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

### 6. Add technical documents

Place PDFs under category folders inside:

```text
data/raw/
```

### 7. Build the vector store

```powershell
python -m scripts.ingest_documents
```

---

## Running the Application

### Backend

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

FastAPI docs:

```text
http://127.0.0.1:8000/docs
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

---

## Testing

Run:

```powershell
python -m pytest tests/test_api.py -v
```

Latest result:

```text
7 passed
```

Tests cover:

- health endpoint
- successful query
- missing question
- null question
- empty question
- statistics endpoint
- knowledge-base endpoint

---

## RAG Pipeline Notebook

The full pipeline is documented in:

```text
notebooks/rag_pipeline.ipynb
```

It covers:

- corpus inspection
- PDF extraction
- text cleaning
- chunking
- embeddings
- ChromaDB
- retrieval
- reranking
- prompt construction
- grounded generation
- citation validation
- evaluation
- failure analysis

---

## Docker

Build:

```bash
docker build -t techrag-backend .
```

Run:

```bash
docker run -p 8000:8000 techrag-backend
```

The backend still depends on access to a running Ollama server containing `gemma3:4b`.

---

## Privacy and Local Inference

The generation model runs locally through Ollama.

The raw technical document corpus and persistent vector database are intentionally excluded from GitHub.

---

## Limitations

- Answer quality depends on retrieved context.
- Category routing can confuse semantically overlapping technical fields.
- Local generation can occasionally produce citation-format failures.
- Scanned PDFs without extractable text require OCR before indexing.
- Ollama must be running for answer generation.
- GPU acceleration depends on local hardware and configuration.

---

## Future Improvements

- OCR support for scanned PDFs
- semantic chunking
- hybrid BM25 + vector retrieval
- query rewriting
- improved category classification
- conversational memory
- document upload through the web interface
- hosted inference
- Project Architect mode

---

## Author

**Abdelrahman Ihab**  
Computer Engineering Student

GitHub: https://github.com/Abdelrahman-288

---

## License

This project is currently intended for educational and research purposes.
