from pathlib import Path
from typing import Any

import chromadb

from src.rag.embeddings import EmbeddingService


DEFAULT_COLLECTION_NAME = "techrag_documents"


class RetrievalService:
    def __init__(
        self,
        persist_directory: str | Path,
        embedding_service: EmbeddingService,
        collection_name: str = DEFAULT_COLLECTION_NAME,
    ) -> None:
        self.persist_directory = Path(persist_directory)
        self.embedding_service = embedding_service

        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory)
        )

        self.collection = self.client.get_collection(
            name=collection_name
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        category: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Retrieve the most relevant chunks for a query.

        Optionally restrict retrieval to a single category.
        """

        query_embedding = self.embedding_service.encode([query])[0]

        where_filter = None

        if category is not None:
            where_filter = {"category": category}

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            where=where_filter,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        retrieved_chunks: list[dict[str, Any]] = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for rank, (document, metadata, distance) in enumerate(
            zip(documents, metadatas, distances),
            start=1,
        ):
            retrieved_chunks.append(
                {
                    "rank": rank,
                    "text": document,
                    "metadata": metadata,
                    "distance": distance,
                    "similarity": 1 - distance,
                }
            )

        return retrieved_chunks