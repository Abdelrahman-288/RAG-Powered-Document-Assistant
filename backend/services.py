from pathlib import Path

import numpy as np

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


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

VECTOR_STORE_DIR = (
    PROJECT_ROOT
    / "data"
    / "vector_store"
)


# ==========================================================
# Semantic descriptions used only for Auto routing
# ==========================================================

CATEGORY_DESCRIPTIONS = {
    "ai_ml": (
        "artificial intelligence machine learning "
        "supervised learning unsupervised learning "
        "classification regression clustering "
        "overfitting underfitting regularization "
        "feature engineering model evaluation "
        "training validation prediction"
    ),

    "algorithms_data_structures": (
        "algorithms data structures computational complexity "
        "dynamic programming recursion greedy algorithms "
        "binary search trees trees graphs stacks queues "
        "linked lists sorting searching hash tables"
    ),

    "cloud_security": (
        "cloud security cloud computing AWS Azure GCP "
        "cloud infrastructure cloud identity IAM "
        "cloud threats access control encryption "
        "cloud network security secure cloud architecture"
    ),

    "computer_vision": (
        "computer vision image processing object detection "
        "image classification segmentation OpenCV "
        "feature detection image recognition YOLO "
        "convolutional vision systems"
    ),

    "cybersecurity": (
        "cybersecurity information security web security "
        "network security SQL injection cross site scripting "
        "penetration testing privilege escalation "
        "vulnerabilities exploits authentication attacks "
        "ethical hacking security testing"
    ),

    "data_science": (
        "data science pandas NumPy exploratory data analysis "
        "EDA data preprocessing data cleaning "
        "data transformation statistics visualization "
        "dataframes datasets analytics feature analysis"
    ),

    "deep_learning": (
        "deep learning neural networks artificial neural networks "
        "CNN convolutional neural networks recurrent neural networks "
        "RNN transformers backpropagation transfer learning "
        "representation learning neural network training"
    ),

    "embedded_systems": (
        "embedded systems microcontrollers firmware "
        "hardware software integration sensors actuators "
        "real time systems RTOS embedded processors "
        "embedded programming electronics"
    ),

    "llm": (
        "large language models LLM generative artificial intelligence "
        "transformer language models prompting prompt engineering "
        "inference fine tuning retrieval augmented generation "
        "foundation models language generation"
    ),

    "malware_analysis": (
        "malware analysis malicious software static malware analysis "
        "dynamic malware analysis reverse engineering malware behavior "
        "virus trojan ransomware disassembly debugging "
        "malware detection"
    ),

    "nlp": (
        "natural language processing NLP text processing "
        "tokenization stemming lemmatization language processing "
        "named entity recognition sentiment analysis "
        "text classification language understanding "
        "word embeddings linguistic text analysis"
    ),

    "python": (
        "Python programming Python language functions classes "
        "decorators generators context managers comprehensions "
        "modules packages exceptions iterators "
        "object oriented programming Python code"
    ),
}


class RAGService:
    def __init__(self) -> None:
        print(
            "Initializing TechRAG backend services..."
        )

        self.embedding_service = (
            EmbeddingService()
        )

        self.reranker_service = (
            RerankerService()
        )

        self.retrieval_service = (
            RetrievalService(
                persist_directory=VECTOR_STORE_DIR,
                embedding_service=self.embedding_service,
                reranker_service=self.reranker_service,
            )
        )

        self.generation_service = (
            GenerationService(
                model_name=DEFAULT_MODEL,
            )
        )

        self.grounded_generation_service = (
            GroundedGenerationService(
                generation_service=self.generation_service,

                # One extra retry for occasional
                # citation-formatting failures.
                max_retries=2,
            )
        )

        # --------------------------------------------------
        # Pre-compute semantic category description vectors
        # once when the backend starts.
        # --------------------------------------------------
        self.category_description_embeddings = {}

        available_categories = (
            self.retrieval_service
            .get_categories()
        )

        for category in available_categories:
            description = (
                CATEGORY_DESCRIPTIONS.get(
                    category,
                    category.replace(
                        "_",
                        " ",
                    ),
                )
            )

            self.category_description_embeddings[
                category
            ] = (
                self.embedding_service
                .encode_one(
                    description
                )
            )

        print(
            "TechRAG backend services ready."
        )

    # ==========================================================
    # Query
    # ==========================================================

    def query(
        self,
        question: str,
        category: str | None = None,
        top_k: int = 5,
        candidate_k: int = 15,
        min_similarity: float = 0.30,
    ) -> dict:

        resolved_category = category

        # --------------------------------------------------
        # Auto-mode category routing
        # --------------------------------------------------

        if category is None:
            route_result = (
                self._route_auto_category(
                    question
                )
            )

            # --------------------------------------------------
            # Unknown category
            # --------------------------------------------------

            if (
                route_result[
                    "status"
                ]
                == "unknown"
            ):
                return {
                    "question":
                        question,

                    "answer": (
                        "I couldn't determine which "
                        "technical field this question "
                        "belongs to confidently.\n\n"
                        "Please select a study field "
                        "before continuing."
                    ),

                    "sources":
                        [],

                    "citation_valid":
                        False,

                    "citation_count":
                        0,

                    "invalid_citations":
                        [],

                    "generation_attempts":
                        0,

                    "grounding_success":
                        False,

                    "needs_category_selection":
                        True,

                    "suggested_categories":
                        route_result[
                            "suggested_categories"
                        ],

                    "resolved_category":
                        None,
                }

            # --------------------------------------------------
            # Ambiguous category
            # --------------------------------------------------

            if (
                route_result[
                    "status"
                ]
                == "ambiguous"
            ):
                return {
                    "question":
                        question,

                    "answer": (
                        "This question appears relevant "
                        "to more than one technical field.\n\n"
                        "Please select the field you mean."
                    ),

                    "sources":
                        [],

                    "citation_valid":
                        False,

                    "citation_count":
                        0,

                    "invalid_citations":
                        [],

                    "generation_attempts":
                        0,

                    "grounding_success":
                        False,

                    "needs_category_selection":
                        True,

                    "suggested_categories":
                        route_result[
                            "suggested_categories"
                        ],

                    "resolved_category":
                        None,
                }

            resolved_category = (
                route_result[
                    "category"
                ]
            )

        # --------------------------------------------------
        # Final document retrieval
        # --------------------------------------------------

        retrieved_chunks = (
            self.retrieval_service.retrieve(
                query=question,
                top_k=top_k,
                candidate_k=candidate_k,
                category=resolved_category,
                min_similarity=min_similarity,
                use_reranker=True,
            )
        )

        # --------------------------------------------------
        # No useful document context
        # --------------------------------------------------

        if not retrieved_chunks:
            return {
                "question":
                    question,

                "answer": (
                    "I don't have enough "
                    "information in the indexed "
                    "documents to answer that "
                    "question reliably."
                ),

                "sources":
                    [],

                "citation_valid":
                    False,

                "citation_count":
                    0,

                "invalid_citations":
                    [],

                "generation_attempts":
                    0,

                "grounding_success":
                    False,

                "needs_category_selection":
                    False,

                "suggested_categories":
                    [],

                "resolved_category":
                    resolved_category,
            }

        # --------------------------------------------------
        # Grounded generation
        # --------------------------------------------------

        generation_result = (
            self
            .grounded_generation_service
            .generate_grounded_answer(
                query=question,
                retrieved_chunks=(
                    retrieved_chunks
                ),
            )
        )

        # --------------------------------------------------
        # Sources
        # --------------------------------------------------

        sources = []

        for result in retrieved_chunks:
            metadata = (
                result.get(
                    "metadata",
                    {},
                )
                or {}
            )

            sources.append(
                {
                    "rank":
                        result[
                            "rank"
                        ],

                    "document":
                        metadata.get(
                            "document",
                            "Unknown document",
                        ),

                    "page":
                        metadata.get(
                            "page",
                            "?",
                        ),

                    "category":
                        metadata.get(
                            "category",
                            "Unknown",
                        ),

                    "similarity":
                        float(
                            result.get(
                                "similarity",
                                0.0,
                            )
                        ),

                    "reranker_score":
                        (
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
            generation_result[
                "validation"
            ]
        )

        invalid_citations = [
            f"{document} | Page {page}"

            for (
                document,
                page,
            )

            in validation[
                "invalid"
            ]
        ]

        # --------------------------------------------------
        # Final API response
        # --------------------------------------------------

        return {
            "question":
                question,

            "answer":
                generation_result[
                    "answer"
                ],

            "sources":
                sources,

            "citation_valid":
                validation[
                    "all_valid"
                ],

            "citation_count":
                validation[
                    "citation_count"
                ],

            "invalid_citations":
                invalid_citations,

            "generation_attempts":
                generation_result[
                    "attempts"
                ],

            "grounding_success":
                generation_result[
                    "success"
                ],

            "needs_category_selection":
                False,

            "suggested_categories":
                [],

            "resolved_category":
                resolved_category,
        }

    # ==========================================================
    # Category-description semantic score
    # ==========================================================

    def _get_category_semantic_scores(
        self,
        question: str,
    ) -> dict[str, float]:
        """
        Compare the user question directly against
        semantic descriptions of every available category.

        The embedding model already returns normalized vectors,
        so their dot product is cosine similarity.
        """

        question_embedding = (
            self.embedding_service
            .encode_one(
                question
            )
        )

        scores = {}

        for (
            category,
            category_embedding,
        ) in (
            self
            .category_description_embeddings
            .items()
        ):

            similarity = float(
                np.dot(
                    question_embedding,
                    category_embedding,
                )
            )

            scores[
                category
            ] = similarity

        return scores

    # ==========================================================
    # Intelligent hybrid Auto router
    # ==========================================================

    def _route_auto_category(
        self,
        question: str,
    ) -> dict:
        """
        Determine the most relevant study category.

        The router combines:

        1. Evidence retrieved from the real document corpus.
        2. Semantic similarity between the question and
           category descriptions.

        Retrieval remains the primary signal.

        Category descriptions act as a secondary signal that
        helps separate overlapping subjects such as:

        - AI/ML vs Deep Learning
        - Data Science vs AI/ML
        - NLP vs Deep Learning
        - Algorithms vs AI/ML
        """

        # --------------------------------------------------
        # Global document retrieval
        #
        # Slightly more than the original 15 results gives
        # smaller categories a better opportunity to appear.
        # --------------------------------------------------

        routing_results = (
            self.retrieval_service.retrieve(
                query=question,
                top_k=25,
                candidate_k=25,
                category=None,
                min_similarity=None,
                use_reranker=False,
            )
        )

        # --------------------------------------------------
        # Semantic category descriptions
        # --------------------------------------------------

        semantic_scores = (
            self._get_category_semantic_scores(
                question
            )
        )

        if (
            not routing_results
            and not semantic_scores
        ):
            return {
                "status":
                    "unknown",

                "category":
                    None,

                "suggested_categories":
                    [],
            }

        # --------------------------------------------------
        # Group document similarities by category
        # --------------------------------------------------

        retrieval_scores: dict[
            str,
            list[float],
        ] = {}

        for result in routing_results:
            metadata = (
                result.get(
                    "metadata",
                    {},
                )
                or {}
            )

            category = (
                metadata.get(
                    "category"
                )
            )

            if not category:
                continue

            similarity = float(
                result.get(
                    "similarity",
                    0.0,
                )
            )

            category_name = str(
                category
            )

            retrieval_scores.setdefault(
                category_name,
                [],
            ).append(
                similarity
            )

        # --------------------------------------------------
        # Score every known category
        # --------------------------------------------------

        all_categories = set(
            semantic_scores.keys()
        )

        all_categories.update(
            retrieval_scores.keys()
        )

        scored_categories = []

        for category_name in (
            all_categories
        ):

            similarities = (
                retrieval_scores.get(
                    category_name,
                    [],
                )
            )

            if similarities:
                ordered_scores = sorted(
                    similarities,
                    reverse=True,
                )

                top_scores = (
                    ordered_scores[
                        :3
                    ]
                )

                best_retrieval = (
                    top_scores[
                        0
                    ]
                )

                average_retrieval = (
                    sum(
                        top_scores
                    )
                    / len(
                        top_scores
                    )
                )

                evidence_bonus = min(
                    len(
                        similarities
                    )
                    * 0.004,
                    0.020,
                )

                retrieval_score = (
                    0.65
                    * best_retrieval

                    + 0.35
                    * average_retrieval

                    + evidence_bonus
                )

            else:
                best_retrieval = 0.0
                retrieval_score = 0.0

            semantic_score = float(
                semantic_scores.get(
                    category_name,
                    0.0,
                )
            )

            # --------------------------------------------------
            # Hybrid score
            #
            # 72% real-document retrieval
            # 28% category-description semantics
            #
            # Retrieval remains dominant.
            # --------------------------------------------------

            combined_score = (
                0.72
                * retrieval_score

                + 0.28
                * semantic_score
            )

            scored_categories.append(
                {
                    "category":
                        category_name,

                    "score":
                        combined_score,

                    "retrieval_score":
                        retrieval_score,

                    "semantic_score":
                        semantic_score,

                    "best_similarity":
                        best_retrieval,

                    "evidence_count":
                        len(
                            similarities
                        ),
                }
            )

        scored_categories.sort(
            key=lambda item:
                item[
                    "score"
                ],
            reverse=True,
        )

        if not scored_categories:
            return {
                "status":
                    "unknown",

                "category":
                    None,

                "suggested_categories":
                    [],
            }

        best = (
            scored_categories[
                0
            ]
        )

        suggested_categories = [
            item[
                "category"
            ]

            for item
            in scored_categories[
                :3
            ]
        ]

        # --------------------------------------------------
        # Weak evidence rejection
        #
        # Require BOTH document evidence and semantic
        # evidence to be weak before giving up.
        # --------------------------------------------------

        if (
            best[
                "best_similarity"
            ]
            < 0.16

            and best[
                "semantic_score"
            ]
            < 0.25
        ):
            return {
                "status":
                    "unknown",

                "category":
                    None,

                "suggested_categories":
                    suggested_categories,
            }

        if (
            len(
                scored_categories
            )
            == 1
        ):
            return {
                "status":
                    "confident",

                "category":
                    best[
                        "category"
                    ],

                "suggested_categories":
                    suggested_categories,
            }

        second = (
            scored_categories[
                1
            ]
        )

        score_margin = (
            best[
                "score"
            ]
            - second[
                "score"
            ]
        )

        # --------------------------------------------------
        # Ask user only when the scores are extremely close.
        #
        # Previous 0.025 threshold caused valid questions like
        # overfitting/EDA to unnecessarily return None.
        # --------------------------------------------------

        if (
            score_margin
            < 0.010
        ):
            return {
                "status":
                    "ambiguous",

                "category":
                    None,

                "suggested_categories":
                    suggested_categories,
            }

        return {
            "status":
                "confident",

            "category":
                best[
                    "category"
                ],

            "suggested_categories":
                suggested_categories,
        }

    # ==========================================================
    # Knowledge Base
    # ==========================================================

    def get_knowledge_base(
        self,
    ) -> dict:
        """
        Return a structured overview of the indexed
        Chroma knowledge base.
        """

        category_map: dict[
            str,
            dict[str, int],
        ] = {}

        for metadata in (
            self
            .retrieval_service
            .iter_metadatas()
        ):

            category = str(
                metadata.get(
                    "category",
                    "Unknown",
                )
            )

            document = str(
                metadata.get(
                    "document",
                    "Unknown document",
                )
            )

            if (
                category
                not in category_map
            ):
                category_map[
                    category
                ] = {}

            category_map[
                category
            ][
                document
            ] = (
                category_map[
                    category
                ].get(
                    document,
                    0,
                )
                + 1
            )

        categories = []

        total_documents = 0

        for category in sorted(
            category_map.keys()
        ):

            documents_map = (
                category_map[
                    category
                ]
            )

            documents = [
                {
                    "document":
                        document,

                    "category":
                        category,

                    "chunk_count":
                        chunk_count,
                }

                for (
                    document,
                    chunk_count,
                )

                in sorted(
                    documents_map.items()
                )
            ]

            document_count = (
                len(
                    documents
                )
            )

            chunk_count = sum(
                item[
                    "chunk_count"
                ]

                for item
                in documents
            )

            total_documents += (
                document_count
            )

            categories.append(
                {
                    "category":
                        category,

                    "document_count":
                        document_count,

                    "chunk_count":
                        chunk_count,

                    "documents":
                        documents,
                }
            )

        return {
            "total_chunks":
                self
                .retrieval_service
                .count(),

            "total_documents":
                total_documents,

            "total_categories":
                len(
                    categories
                ),

            "categories":
                categories,
        }

    # ==========================================================
    # Stats
    # ==========================================================

    def get_stats(
        self,
    ) -> dict:

        return {
            "indexed_chunks":
                self
                .retrieval_service
                .count(),

            "categories":
                self
                .retrieval_service
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