from pathlib import Path
from typing import Any

import chromadb

from src.rag.embeddings import EmbeddingService
from src.rag.reranker import RerankerService


DEFAULT_COLLECTION_NAME = "techrag_documents"

METADATA_BATCH_SIZE = 500


class RetrievalService:
    def __init__(
        self,
        persist_directory: str | Path,
        embedding_service: EmbeddingService,
        reranker_service: RerankerService | None = None,
        collection_name: str = DEFAULT_COLLECTION_NAME,
    ) -> None:
        self.persist_directory = Path(
            persist_directory
        )

        self.embedding_service = (
            embedding_service
        )

        self.reranker_service = (
            reranker_service
        )

        self.collection_name = (
            collection_name
        )

        self.client = (
            chromadb.PersistentClient(
                path=str(
                    self.persist_directory
                )
            )
        )

        self.collection = (
            self.client.get_collection(
                name=self.collection_name
            )
        )

    # ==========================================================
    # Retrieval
    # ==========================================================
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        candidate_k: int = 15,
        category: str | None = None,
        min_similarity: float | None = None,
        use_reranker: bool = True,
    ) -> list[dict[str, Any]]:

        query = query.strip()

        if not query:
            return []

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than 0."
            )

        if candidate_k < top_k:
            candidate_k = top_k

        query_embedding = (
            self.embedding_service.encode(
                [query],
                show_progress_bar=False,
            )[0]
        )

        where_filter = None

        if category is not None:
            where_filter = {
                "category": category
            }

        search_k = (
            candidate_k
            if (
                use_reranker
                and self.reranker_service
                is not None
            )
            else top_k
        )

        results = (
            self.collection.query(
                query_embeddings=[
                    query_embedding.tolist()
                ],
                n_results=search_k,
                where=where_filter,
                include=[
                    "documents",
                    "metadatas",
                    "distances",
                ],
            )
        )

        documents = (
            results.get(
                "documents"
            )
            or [[]]
        )[0]

        metadatas = (
            results.get(
                "metadatas"
            )
            or [[]]
        )[0]

        distances = (
            results.get(
                "distances"
            )
            or [[]]
        )[0]

        candidates: list[
            dict[str, Any]
        ] = []

        for rank, (
            document,
            metadata,
            distance,
        ) in enumerate(
            zip(
                documents,
                metadatas,
                distances,
            ),
            start=1,
        ):

            similarity = (
                1.0 -
                float(distance)
            )

            if (
                min_similarity
                is not None
                and similarity <
                min_similarity
            ):
                continue

            candidates.append(
                {
                    "rank":
                        rank,

                    "text":
                        document,

                    "metadata":
                        metadata,

                    "distance":
                        float(
                            distance
                        ),

                    "similarity":
                        similarity,
                }
            )

        if (
            use_reranker
            and self.reranker_service
            is not None
        ):

            return (
                self
                .reranker_service
                .rerank(
                    query=query,
                    candidates=candidates,
                    top_k=top_k,
                )
            )

        return (
            candidates[
                :top_k
            ]
        )

    # ==========================================================
    # Collection count
    # ==========================================================
    def count(
        self,
    ) -> int:

        return (
            self.collection.count()
        )

    # ==========================================================
    # Safe batched metadata iterator
    # ==========================================================
    def iter_metadatas(
        self,
        batch_size: int = METADATA_BATCH_SIZE,
    ):
        """
        Safely yield Chroma metadata in batches.

        Avoids loading tens of thousands of rows
        in one SQLite query.
        """

        if batch_size <= 0:
            raise ValueError(
                "batch_size must be greater than 0."
            )

        total = (
            self.collection.count()
        )

        offset = 0

        while offset < total:

            result = (
                self.collection.get(
                    limit=batch_size,
                    offset=offset,
                    include=[
                        "metadatas"
                    ],
                )
            )

            metadatas = (
                result.get(
                    "metadatas"
                )
                or []
            )

            if not metadatas:
                break

            for metadata in metadatas:
                if metadata:
                    yield metadata

            offset += len(
                metadatas
            )

    # ==========================================================
    # Categories
    # ==========================================================
    def get_categories(
        self,
    ) -> list[str]:

        categories: set[str] = (
            set()
        )

        for metadata in (
            self.iter_metadatas()
        ):

            category = (
                metadata.get(
                    "category"
                )
            )

            if category:
                categories.add(
                    str(category)
                )

        return sorted(
            categories
        )