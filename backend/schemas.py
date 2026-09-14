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

    needs_category_selection: bool = False

    suggested_categories: list[str] = Field(
        default_factory=list
    )

    # Category actually used by the backend.
    #
    # Examples:
    # - "cybersecurity"
    # - "python"
    # - "computer_vision"
    #
    # None means no category was resolved yet,
    # such as when Auto mode asks the user
    # to choose between multiple fields.
    resolved_category: str | None = None


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

    reranker_model: str | None = None


# ==========================================================
# Knowledge Base Models
# ==========================================================

class KnowledgeBaseDocument(BaseModel):
    document: str

    category: str

    chunk_count: int


class KnowledgeBaseCategory(BaseModel):
    category: str

    document_count: int

    chunk_count: int

    documents: list[
        KnowledgeBaseDocument
    ]


class KnowledgeBaseResponse(BaseModel):
    total_chunks: int

    total_documents: int

    total_categories: int

    categories: list[
        KnowledgeBaseCategory
    ]