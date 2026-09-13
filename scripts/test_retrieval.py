from pathlib import Path

from src.rag.embeddings import EmbeddingService
from src.rag.retrieval import RetrievalService


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VECTOR_STORE_DIR = PROJECT_ROOT / "data" / "vector_store"


def main() -> None:
    query = "What is overfitting in machine learning?"

    print(f"\nQuery: {query}")

    embedding_service = EmbeddingService()

    retrieval_service = RetrievalService(
        persist_directory=VECTOR_STORE_DIR,
        embedding_service=embedding_service,
    )

    results = retrieval_service.retrieve(
        query=query,
        top_k=5,
        category="ai_ml",
    )

    print("\n=== RETRIEVAL RESULTS ===")

    for result in results:
        metadata = result["metadata"]

        print("\n" + "=" * 80)
        print(f"Rank: {result['rank']}")
        print(f"Similarity: {result['similarity']:.4f}")
        print(f"Document: {metadata['document']}")
        print(f"Category: {metadata['category']}")
        print(f"Page: {metadata['page']}")
        print(f"Chunk ID: {metadata['chunk_id']}")

        print("\nText:")
        print(result["text"][:800])


if __name__ == "__main__":
    main()