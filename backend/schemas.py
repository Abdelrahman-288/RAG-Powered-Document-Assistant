from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="User question for the RAG system.",
    )

    category: str | None = Field(
        default=None,
        description="Optional knowledge category filter.",
    )

class SourceItem(BaseModel):
    rank: int
    document: str
    page: int | str
    category: str
    similarity: float
    reranker_score: float | None = None


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceItem]

    citation_valid: bool
    citation_count: int
    invalid_citations: list[str]

    generation_attempts: int
    grounding_success: bool


class HealthResponse(BaseModel):
    status: str
    model: str
    vector_store_ready: bool


class StatsResponse(BaseModel):
    indexed_chunks: int
    categories: list[str]
    embedding_model: str
    generation_model: str
    reranker_enabled: bool