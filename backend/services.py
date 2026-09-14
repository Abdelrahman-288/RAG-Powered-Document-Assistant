from pathlib import Path

from src.rag.embeddings import (
    DEFAULT_EMBEDDING_MODEL,
    EmbeddingService,
)
from src.rag.generation import (
    DEFAULT_MODEL,
    GenerationService,
)
from src.rag.grounded_generation import (
    GroundedGenerationService,
)
from src.rag.reranker import (
    DEFAULT_RERANKER_MODEL,
    RerankerService,
)
from src.rag.retrieval import (
    RetrievalService,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

VECTOR_STORE_DIR = (
    PROJECT_ROOT
    / "data"
    / "vector_store"
)


class RAGService:
    def __init__(self) -> None:
        print("Initializing TechRAG backend services...")

        self.embedding_service = EmbeddingService()

        self.reranker_service = RerankerService()

        self.retrieval_service = RetrievalService(
            persist_directory=VECTOR_STORE_DIR,
            embedding_service=self.embedding_service,
            reranker_service=self.reranker_service,
        )

        self.generation_service = GenerationService(
            model_name=DEFAULT_MODEL,
        )

        self.grounded_generation_service = (
            GroundedGenerationService(
                generation_service=self.generation_service,
                max_retries=1,
            )
        )

        print("TechRAG backend services ready.")

    def query(
        self,
        question: str,
        category: str | None = None,
        top_k: int = 5,
        candidate_k: int = 15,
        min_similarity: float = 0.30,
    ) -> dict:

        # --------------------------------------------------
        # Auto mode ambiguity handling
        # --------------------------------------------------
        if category is None:
            ambiguity_response = (
                self._check_ambiguous_question(
                    question
                )
            )

            if ambiguity_response is not None:
                return ambiguity_response

        # --------------------------------------------------
        # Retrieval
        # --------------------------------------------------
        retrieved_chunks = (
            self.retrieval_service.retrieve(
                query=question,
                top_k=top_k,
                candidate_k=candidate_k,
                category=category,
                min_similarity=min_similarity,
                use_reranker=True,
            )
        )

        # --------------------------------------------------
        # No useful documents found
        # --------------------------------------------------
        if not retrieved_chunks:
            return {
                "question": question,
                "answer": (
                    "I don't have enough information "
                    "in the indexed documents to answer "
                    "that question reliably."
                ),
                "sources": [],
                "citation_valid": True,
                "citation_count": 0,
                "invalid_citations": [],
                "generation_attempts": 0,
                "grounding_success": False,
            }

        # --------------------------------------------------
        # Grounded generation
        # --------------------------------------------------
        generation_result = (
            self.grounded_generation_service
            .generate_grounded_answer(
                query=question,
                retrieved_chunks=retrieved_chunks,
            )
        )

        # --------------------------------------------------
        # Prepare sources for API response
        # --------------------------------------------------
        sources = []

        for result in retrieved_chunks:
            metadata = result.get(
                "metadata",
                {},
            )

            sources.append(
                {
                    "rank": result["rank"],

                    "document": metadata.get(
                        "document",
                        "Unknown document",
                    ),

                    "page": metadata.get(
                        "page",
                        "?",
                    ),

                    "category": metadata.get(
                        "category",
                        "Unknown",
                    ),

                    "similarity": float(
                        result.get(
                            "similarity",
                            0.0,
                        )
                    ),

                    "reranker_score": (
                        float(
                            result[
                                "reranker_score"
                            ]
                        )
                        if result.get(
                            "reranker_score"
                        )
                        is not None
                        else None
                    ),
                }
            )

        # --------------------------------------------------
        # Citation validation
        # --------------------------------------------------
        validation = (
            generation_result["validation"]
        )

        invalid_citations = [
            f"{document} | Page {page}"
            for document, page
            in validation["invalid"]
        ]

        # --------------------------------------------------
        # Final response
        # --------------------------------------------------
        return {
            "question": question,

            "answer": generation_result[
                "answer"
            ],

            "sources": sources,

            "citation_valid": validation[
                "all_valid"
            ],

            "citation_count": validation[
                "citation_count"
            ],

            "invalid_citations": (
                invalid_citations
            ),

            "generation_attempts": (
                generation_result[
                    "attempts"
                ]
            ),

            "grounding_success": (
                generation_result[
                    "success"
                ]
            ),
        }

    def _check_ambiguous_question(
        self,
        question: str,
    ) -> dict | None:
        """
        Detect simple ambiguous technical terms when
        the user is using Auto mode.

        If a term can reasonably belong to multiple
        indexed study fields, ask the user to choose
        a field instead of mixing unrelated documents.
        """

        normalized_question = (
            question
            .strip()
            .lower()
        )

        ambiguous_terms = {
            "buffer": [
                "Cybersecurity",
                "Python",
                "Malware Analysis",
            ],

            "overflow": [
                "Cybersecurity",
                "Algorithms & Data Structures",
            ],

            "model": [
                "AI / Machine Learning",
                "Data Science",
            ],
        }

        for (
            term,
            possible_fields,
        ) in ambiguous_terms.items():

            if term in normalized_question:
                fields_text = ", ".join(
                    possible_fields
                )

                return {
                    "question": question,

                    "answer": (
                        f'The term "{term}" can have '
                        f"different meanings depending "
                        f"on the technical field.\n\n"
                        f"Please select a study field "
                        f"before continuing.\n\n"
                        f"Possible fields: "
                        f"{fields_text}."
                    ),

                    "sources": [],

                    "citation_valid": True,

                    "citation_count": 0,

                    "invalid_citations": [],

                    "generation_attempts": 0,

                    "grounding_success": True,
                }

        return None

    def get_stats(self) -> dict:
        return {
            "indexed_chunks":
                self.retrieval_service.count(),

            "categories":
                self.retrieval_service
                .get_categories(),

            "embedding_model":
                DEFAULT_EMBEDDING_MODEL,

            "generation_model":
                DEFAULT_MODEL,

            "reranker_enabled":
                True,

            "reranker_model":
                DEFAULT_RERANKER_MODEL,
        }