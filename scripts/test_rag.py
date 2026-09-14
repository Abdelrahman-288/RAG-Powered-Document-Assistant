from pathlib import Path

from src.rag.embeddings import EmbeddingService
from src.rag.generation import GenerationService
from src.rag.grounded_generation import GroundedGenerationService
from src.rag.reranker import RerankerService
from src.rag.retrieval import RetrievalService


PROJECT_ROOT = Path(__file__).resolve().parents[1]

VECTOR_STORE_DIR = (
    PROJECT_ROOT
    / "data"
    / "vector_store"
)

TOP_K = 5
CANDIDATE_K = 15
MIN_SIMILARITY = 0.30
MODEL_NAME = "gemma3:4b"


def print_retrieved_sources(
    retrieved_chunks: list[dict],
) -> None:
    print("\n=== RETRIEVED SOURCES ===")

    for result in retrieved_chunks:
        metadata = result.get(
            "metadata",
            {},
        )

        document = metadata.get(
            "document",
            "Unknown document",
        )

        page = metadata.get(
            "page",
            "?",
        )

        category = metadata.get(
            "category",
            "Unknown",
        )

        similarity = result.get(
            "similarity",
            0.0,
        )

        reranker_score = result.get(
            "reranker_score",
        )

        line = (
            f"- Rank {result['rank']} "
            f"| {document} "
            f"| Page {page} "
            f"| Category: {category} "
            f"| Similarity: {similarity:.4f}"
        )

        if reranker_score is not None:
            line += (
                f" | Reranker: "
                f"{reranker_score:.4f}"
            )

        print(line)


def print_citation_validation(
    validation: dict,
) -> None:
    print("\n=== CITATION VALIDATION ===")

    print(
        f"Citations found: "
        f"{validation['citation_count']}"
    )

    print(
        f"Valid citations: "
        f"{len(validation['valid'])}"
    )

    print(
        f"Invalid citations: "
        f"{len(validation['invalid'])}"
    )

    if validation["invalid"]:
        print(
            "\nInvalid citations:"
        )

        for document, page in validation["invalid"]:
            print(
                f"- {document} | Page {page}"
            )
    else:
        print(
            "All citations are grounded "
            "in retrieved sources."
        )


def main() -> None:
    print("=" * 70)

    print(
        "TechRAG Architect — "
        "Grounded RAG Test"
    )

    print("=" * 70)

    print("\nLoading services...")

    embedding_service = EmbeddingService()

    reranker_service = RerankerService()

    retrieval_service = RetrievalService(
        persist_directory=VECTOR_STORE_DIR,
        embedding_service=embedding_service,
        reranker_service=reranker_service,
    )

    generation_service = GenerationService(
        model_name=MODEL_NAME,
    )

    grounded_generation_service = (
        GroundedGenerationService(
            generation_service=generation_service,
            max_retries=1,
        )
    )

    print("\nSystem ready.")

    print(
        f"Indexed chunks: "
        f"{retrieval_service.count()}"
    )

    print(
        "Retrieval mode: "
        "GLOBAL + RERANKING"
    )

    print(
        f"Candidate chunks: "
        f"{CANDIDATE_K}"
    )

    print(
        f"Final chunks: "
        f"{TOP_K}"
    )

    print(
        f"Minimum similarity: "
        f"{MIN_SIMILARITY}"
    )

    print(
        "\nType 'exit' or 'quit' "
        "to stop."
    )

    while True:
        print(
            "\n"
            + "-" * 70
        )

        query = input(
            "\nYou: "
        ).strip()

        if query.lower() in {
            "exit",
            "quit",
        }:
            print("\nGoodbye.")
            break

        if not query:
            continue

        try:
            retrieved_chunks = (
                retrieval_service.retrieve(
                    query=query,
                    top_k=TOP_K,
                    candidate_k=CANDIDATE_K,
                    category=None,
                    min_similarity=MIN_SIMILARITY,
                    use_reranker=True,
                )
            )

        except Exception as exc:
            print(
                "\nRetrieval error:"
            )
            print(
                str(exc)
            )
            continue

        if not retrieved_chunks:
            print(
                "\n=== RETRIEVED SOURCES ==="
            )

            print(
                "No sufficiently relevant "
                "information was found."
            )

            print(
                "\nTechRAG: "
                "I don't have enough "
                "information in the indexed "
                "documents to answer that "
                "question reliably."
            )

            continue

        print_retrieved_sources(
            retrieved_chunks
        )

        try:
            result = (
                grounded_generation_service
                .generate_grounded_answer(
                    query=query,
                    retrieved_chunks=retrieved_chunks,
                )
            )

        except Exception as exc:
            print(
                "\nGeneration error:"
            )
            print(
                str(exc)
            )
            continue

        print(
            "\n=== ANSWER ==="
        )

        print(
            result["answer"]
        )

        print_citation_validation(
            result["validation"]
        )

        print(
            f"\nGeneration attempts: "
            f"{result['attempts']}"
        )

        print(
            f"Grounding status: "
            f"{'PASS' if result['success'] else 'FAIL'}"
        )


if __name__ == "__main__":
    main()