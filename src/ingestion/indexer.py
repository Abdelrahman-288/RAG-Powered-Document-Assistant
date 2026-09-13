from pathlib import Path
from typing import Any

import chromadb

from src.rag.embeddings import EmbeddingService


DEFAULT_COLLECTION_NAME = "techrag_documents"


class ChromaIndexer:
    def __init__(
        self,
        persist_directory: str | Path,
        collection_name: str = DEFAULT_COLLECTION_NAME,
    ) -> None:
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory)
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def index_chunks(
        self,
        chunks: list[dict[str, Any]],
        embedding_service: EmbeddingService,
        batch_size: int = 32,
    ) -> None:
        if not chunks:
            print("No chunks to index.")
            return

        texts = [chunk["text"] for chunk in chunks]
        ids = [chunk["id"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]

        print(f"Generating embeddings for {len(texts)} chunks...")

        embeddings = embedding_service.encode(
            texts,
            batch_size=batch_size,
        )

        print("Saving embeddings to ChromaDB...")

        self.collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings.tolist(),
        )

        print("Indexing complete.")

    def count(self) -> int:
        return self.collection.count()