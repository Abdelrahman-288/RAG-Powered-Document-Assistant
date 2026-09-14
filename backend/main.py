from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.schemas import (
    HealthResponse,
    QueryRequest,
    QueryResponse,
    StatsResponse,
)
from backend.services import RAGService


rag_service: RAGService | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_service

    print("Starting TechRAG API...")

    rag_service = RAGService()

    yield

    print("Shutting down TechRAG API...")


app = FastAPI(
    title="TechRAG Architect API",
    description=(
        "Local RAG API for technical document "
        "retrieval and grounded generation."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict:
    return {
        "name": "TechRAG Architect API",
        "status": "running",
        "docs": "/docs",
    }


@app.get(
    "/health",
    response_model=HealthResponse,
)
def health() -> HealthResponse:
    if rag_service is None:
        raise HTTPException(
            status_code=503,
            detail="RAG service is not ready.",
        )

    return HealthResponse(
        status="healthy",
        model=rag_service.generation_service.model_name,
        vector_store_ready=True,
    )


@app.get(
    "/stats",
    response_model=StatsResponse,
)
def stats() -> StatsResponse:
    if rag_service is None:
        raise HTTPException(
            status_code=503,
            detail="RAG service is not ready.",
        )

    stats_data = rag_service.get_stats()

    return StatsResponse(
        indexed_chunks=stats_data[
            "indexed_chunks"
        ],
        categories=stats_data[
            "categories"
        ],
        embedding_model=stats_data[
            "embedding_model"
        ],
        generation_model=stats_data[
            "generation_model"
        ],
        reranker_enabled=stats_data[
            "reranker_enabled"
        ],
    )


@app.post(
    "/query",
    response_model=QueryResponse,
)
def query(
    request: QueryRequest,
) -> QueryResponse:
    if rag_service is None:
        raise HTTPException(
            status_code=503,
            detail="RAG service is not ready.",
        )

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:
        result = rag_service.query(
            question=question,
            category=request.category,
        )

        return QueryResponse(
            **result
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc