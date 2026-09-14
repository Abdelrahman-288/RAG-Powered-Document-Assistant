from fastapi.testclient import TestClient

from backend.main import app


def test_health_endpoint() -> None:
    """
    Happy-path health check.

    The application lifespan starts the RAG service,
    loads the embedding model, reranker, vector store,
    and generation service.
    """

    with TestClient(app) as client:
        response = client.get(
            "/health"
        )

        assert (
            response.status_code
            == 200
        )

        data = response.json()

        assert (
            data[
                "status"
            ]
            == "healthy"
        )

        assert (
            data[
                "vector_store_ready"
            ]
            is True
        )

        assert (
            isinstance(
                data[
                    "model"
                ],
                str,
            )
        )

        assert (
            len(
                data[
                    "model"
                ]
            )
            > 0
        )


def test_query_success() -> None:
    """
    Happy-path RAG query.

    Uses a real technical question and verifies
    that the backend returns the expected response
    structure.
    """

    with TestClient(app) as client:
        response = client.post(
            "/query",
            json={
                "question":
                    "What is SQL injection?",

                "category":
                    "cybersecurity",
            },
        )

        assert (
            response.status_code
            == 200
        )

        data = response.json()

        assert (
            data[
                "question"
            ]
            == "What is SQL injection?"
        )

        assert (
            isinstance(
                data[
                    "answer"
                ],
                str,
            )
        )

        assert (
            len(
                data[
                    "answer"
                ]
            )
            > 0
        )

        assert (
            isinstance(
                data[
                    "sources"
                ],
                list,
            )
        )

        assert (
            isinstance(
                data[
                    "citation_valid"
                ],
                bool,
            )
        )

        assert (
            isinstance(
                data[
                    "citation_count"
                ],
                int,
            )
        )

        assert (
            isinstance(
                data[
                    "grounding_success"
                ],
                bool,
            )
        )

        assert (
            data[
                "resolved_category"
            ]
            == "cybersecurity"
        )


def test_query_missing_question_returns_422() -> None:
    """
    Invalid request.

    QueryRequest requires the 'question' field.
    Omitting it should be rejected automatically
    by FastAPI/Pydantic with HTTP 422.
    """

    with TestClient(app) as client:
        response = client.post(
            "/query",
            json={
                "category":
                    "cybersecurity",
            },
        )

        assert (
            response.status_code
            == 422
        )


def test_query_null_question_returns_422() -> None:
    """
    Invalid request.

    A null question does not satisfy the
    QueryRequest schema.
    """

    with TestClient(app) as client:
        response = client.post(
            "/query",
            json={
                "question":
                    None,

                "category":
                    "cybersecurity",
            },
        )

        assert (
            response.status_code
            == 422
        )


def test_query_empty_question_returns_422() -> None:
    """
    Empty string violates the Pydantic
    min_length=1 constraint.
    """

    with TestClient(app) as client:
        response = client.post(
            "/query",
            json={
                "question":
                    "",

                "category":
                    "cybersecurity",
            },
        )

        assert (
            response.status_code
            == 422
        )


def test_stats_endpoint() -> None:
    """
    Verify knowledge-base/model statistics.
    """

    with TestClient(app) as client:
        response = client.get(
            "/stats"
        )

        assert (
            response.status_code
            == 200
        )

        data = response.json()

        assert (
            data[
                "indexed_chunks"
            ]
            > 0
        )

        assert (
            isinstance(
                data[
                    "categories"
                ],
                list,
            )
        )

        assert (
            len(
                data[
                    "categories"
                ]
            )
            > 0
        )

        assert (
            isinstance(
                data[
                    "embedding_model"
                ],
                str,
            )
        )

        assert (
            isinstance(
                data[
                    "generation_model"
                ],
                str,
            )
        )

        assert (
            data[
                "reranker_enabled"
            ]
            is True
        )


def test_knowledge_base_endpoint() -> None:
    """
    Verify the structured knowledge-base
    overview endpoint.
    """

    with TestClient(app) as client:
        response = client.get(
            "/knowledge-base"
        )

        assert (
            response.status_code
            == 200
        )

        data = response.json()

        assert (
            data[
                "total_chunks"
            ]
            > 0
        )

        assert (
            data[
                "total_documents"
            ]
            > 0
        )

        assert (
            data[
                "total_categories"
            ]
            > 0
        )

        assert (
            isinstance(
                data[
                    "categories"
                ],
                list,
            )
        )