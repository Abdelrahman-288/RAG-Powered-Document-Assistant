from pathlib import Path

from src.rag.embeddings import EmbeddingService
from src.rag.generation import GenerationService
from src.rag.prompting import build_rag_prompt
from src.rag.retrieval import RetrievalService


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VECTOR_STORE_DIR = PROJECT_ROOT / "data" / "vector_store"


def main() -> None:
    query = "What is overfitting in machine learning?"

    print("\n=== USER QUESTION ===")
    print(query)

    # 1. Load embedding model
    embedding_service = EmbeddingService()

    # 2. Initialize retrieval
    retrieval_service = RetrievalService(
        persist_directory=VECTOR_STORE_DIR,
        embedding_service=embedding_service,
    )

    # 3. Retrieve relevant document chunks
    retrieved_chunks = retrieval_service.retrieve(
        query=query,
        top_k=5,
        category="ai_ml",
    )

    print("\n=== RETRIEVED SOURCES ===")

    for result in retrieved_chunks:
        metadata = result["metadata"]

        print(
            f"- {metadata['document']} "
            f"| Page {metadata['page']} "
            f"| Similarity {result['similarity']:.4f}"
        )

    # 4. Build grounded prompt
    prompt = build_rag_prompt(
        query=query,
        retrieved_chunks=retrieved_chunks,
    )

    # 5. Generate answer using Ollama
    generation_service = GenerationService(
        model_name="gemma3:4b",
    )

    print("\n=== RAG ANSWER ===")

    answer = generation_service.generate(prompt)

    print(answer)


if __name__ == "__main__":
    main()