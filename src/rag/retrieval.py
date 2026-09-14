from pathlib import Path
from typing import Any

import chromadb

from src.rag.embeddings import EmbeddingService
from src.rag.reranker import RerankerService


DEFAULT_COLLECTION_NAME = "techrag_documents"


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

        self.client = chromadb.PersistentClient(
            path=str(
                self.persist_directory
            )
        )

        self.collection = (
            self.client.get_collection(
                name=self.collection_name
            )
        )

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
            if use_reranker
            and self.reranker_service
            is not None
            else top_k
        )

        results = self.collection.query(
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

        documents = (
            results.get("documents")
            or [[]]
        )[0]

        metadatas = (
            results.get("metadatas")
            or [[]]
        )[0]

        distances = (
            results.get("distances")
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
                1.0 - float(distance)
            )

            if (
                min_similarity
                is not None
                and similarity
                < min_similarity
            ):
                continue

            candidates.append(
                {
                    "rank": rank,
                    "text": document,
                    "metadata": metadata,
                    "distance": float(
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
                self.reranker_service.rerank(
                    query=query,
                    candidates=candidates,
                    top_k=top_k,
                )
            )

        return candidates[:top_k]

    def count(self) -> int:
        return self.collection.count()

    def get_categories(
        self,
    ) -> list[str]:
        results = self.collection.get(
            include=["metadatas"]
        )

        categories = set()

        for metadata in (
            results.get("metadatas")
            or []
        ):
            category = metadata.get(
                "category"
            )

            if category:
                categories.add(
                    str(category)
                )

        return sorted(categories)