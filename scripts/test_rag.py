from pathlib import Path

from src.rag.embeddings import EmbeddingService
from src.rag.generation import GenerationService
from src.rag.prompting import build_rag_prompt
from src.rag.retrieval import RetrievalService


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VECTOR_STORE_DIR = PROJECT_ROOT / "data" / "vector_store"


def main() -> None:
    print("=" * 70)
    print("TechRAG Architect — Local RAG Test")
    print("=" * 70)

    print("\nLoading services...")

    embedding_service = EmbeddingService()

    retrieval_service = RetrievalService(
        persist_directory=VECTOR_STORE_DIR,
        embedding_service=embedding_service,
    )

    generation_service = GenerationService(
        model_name="gemma3:4b",
    )

    print("\nSystem ready.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        query = input("You: ").strip()

        if query.lower() in {"exit", "quit"}:
            print("\nGoodbye.")
            break

        if not query:
            continue

        retrieved_chunks = retrieval_service.retrieve(
            query=query,
            top_k=5,
            min_similarity=0.30,
        )

        print("\n=== RETRIEVED SOURCES ===")

        if not retrieved_chunks:
            print("No sufficiently relevant information was found.")
            print(
                "\nTechRAG: I don't have enough information "
                "in the available documents to answer that question.\n"
            )
            continue

        for result in retrieved_chunks:
            metadata = result["metadata"]

            print(
                f"- {metadata['document']} "
                f"| Page {metadata['page']} "
                f"| Similarity {result['similarity']:.4f}"
            )

        prompt = build_rag_prompt(
            query=query,
            retrieved_chunks=retrieved_chunks,
        )

        answer = generation_service.generate(prompt)

        print("\n=== ANSWER ===")
        print(answer)
        print()


if __name__ == "__main__":
    main()