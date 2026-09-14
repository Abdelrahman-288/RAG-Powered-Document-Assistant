# TechRAG Architect

TechRAG Architect is a local Retrieval-Augmented Generation (RAG) assistant for technical documents.

It allows users to ask questions across multiple technical study fields and receive answers grounded in a local document knowledge base with source citations.

The system combines:

- PDF document ingestion
- text cleaning
- overlapping chunking
- sentence-transformer embeddings
- persistent ChromaDB vector storage
- semantic retrieval
- CrossEncoder reranking
- automatic category routing
- Ollama-based local generation
- citation validation
- FastAPI backend
- Next.js frontend

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
    ↓
Next.js Frontend
    ↓
FastAPI Backend
    ↓
Auto Category Router
    ↓
Embedding Model
    ↓
ChromaDB Vector Search
    ↓
CrossEncoder Reranker
    ↓
Top Retrieved Chunks
    ↓
Grounded Prompt Builder
    ↓
Gemma 3 4B via Ollama
    ↓
Citation Validator
    ↓
Grounded Answer + Sources