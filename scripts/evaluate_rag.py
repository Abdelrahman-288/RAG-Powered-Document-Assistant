from pathlib import Path

from src.rag.embeddings import (
    EmbeddingService,
)
from src.rag.reranker import (
    RerankerService,
)
from src.rag.retrieval import (
    RetrievalService,
)


PROJECT_ROOT = (
    Path(__file__).resolve().parents[1]
)

VECTOR_STORE_DIR = (
    PROJECT_ROOT
    / "data"
    / "vector_store"
)

TOP_K = 5
CANDIDATE_K = 15


TEST_CASES = [
    {
        "question":
            "What is overfitting in machine learning?",
        "expected_category":
            "ai_ml",
    },
    {
        "question":
            "What is regularization in machine learning?",
        "expected_category":
            "ai_ml",
    },
    {
        "question":
            "What is dynamic programming?",
        "expected_category":
            "algorithms_data_structures",
    },
    {
        "question":
            "What is a binary search tree?",
        "expected_category":
            "algorithms_data_structures",
    },
    {
        "question":
            "What is a buffer overflow?",
        "expected_category":
            "cybersecurity",
    },
    {
        "question":
            "What is SQL injection?",
        "expected_category":
            "cybersecurity",
    },
    {
        "question":
            "What is cross-site scripting?",
        "expected_category":
            "cybersecurity",
    },
    {
        "question":
            "What is penetration testing?",
        "expected_category":
            "cybersecurity",
    },
    {
        "question":
            "What is a pandas DataFrame?",
        "expected_category":
            "data_science",
    },
    {
        "question":
            "What is data preprocessing?",
        "expected_category":
            "data_science",
    },
    {
        "question":
            "What is exploratory data analysis?",
        "expected_category":
            "data_science",
    },
    {
        "question":
            "What is static malware analysis?",
        "expected_category":
            "malware_analysis",
    },
    {
        "question":
            "What is dynamic malware analysis?",
        "expected_category":
            "malware_analysis",
    },
    {
        "question":
            "What is a Python decorator?",
        "expected_category":
            "python",
    },
    {
        "question":
            "What is a Python generator?",
        "expected_category":
            "python",
    },
    {
        "question":
            "What is a Python list comprehension?",
        "expected_category":
            "python",
    },
    {
        "question":
            "What is a Python context manager?",
        "expected_category":
            "python",
    },
    {
        "question":
            "What is NumPy used for?",
        "expected_category":
            "data_science",
    },
    {
        "question":
            "What is recursion?",
        "expected_category":
            "algorithms_data_structures",
    },
    {
        "question":
            "What is privilege escalation?",
        "expected_category":
            "cybersecurity",
    },
]


def main() -> None:
    print("=" * 80)
    print(
        "TechRAG Retrieval Evaluation "
        "with Reranking"
    )
    print("=" * 80)

    embedding_service = (
        EmbeddingService()
    )

    reranker_service = (
        RerankerService()
    )

    retrieval_service = (
        RetrievalService(
            persist_directory=(
                VECTOR_STORE_DIR
            ),
            embedding_service=(
                embedding_service
            ),
            reranker_service=(
                reranker_service
            ),
        )
    )

    correct_top1 = 0
    correct_top5 = 0

    results_summary = []

    print(
        f"\nIndexed chunks: "
        f"{retrieval_service.count()}"
    )

    print(
        f"Questions: "
        f"{len(TEST_CASES)}"
    )

    print(
        f"Initial candidates: "
        f"{CANDIDATE_K}"
    )

    print(
        f"Final results: "
        f"{TOP_K}"
    )

    for index, test_case in enumerate(
        TEST_CASES,
        start=1,
    ):
        question = (
            test_case["question"]
        )

        expected_category = (
            test_case[
                "expected_category"
            ]
        )

        print(
            "\n"
            + "-" * 80
        )

        print(
            f"Question {index}/"
            f"{len(TEST_CASES)}"
        )

        print(
            f"Question: {question}"
        )

        print(
            f"Expected: "
            f"{expected_category}"
        )

        retrieved_chunks = (
            retrieval_service.retrieve(
                query=question,
                top_k=TOP_K,
                candidate_k=(
                    CANDIDATE_K
                ),
                min_similarity=None,
                use_reranker=True,
            )
        )

        if not retrieved_chunks:
            print(
                "FAIL: No results."
            )
            continue

        top_result = (
            retrieved_chunks[0]
        )

        top_category = (
            top_result[
                "metadata"
            ].get(
                "category",
                "unknown",
            )
        )

        top_similarity = (
            top_result.get(
                "similarity",
                0.0,
            )
        )

        reranker_score = (
            top_result.get(
                "reranker_score",
                0.0,
            )
        )

        top1_correct = (
            top_category
            == expected_category
        )

        top5_categories = [
            result[
                "metadata"
            ].get(
                "category",
                "unknown",
            )
            for result
            in retrieved_chunks
        ]

        top5_correct = (
            expected_category
            in top5_categories
        )

        if top1_correct:
            correct_top1 += 1

        if top5_correct:
            correct_top5 += 1

        print(
            f"Top-1 category: "
            f"{top_category}"
        )

        print(
            f"Vector similarity: "
            f"{top_similarity:.4f}"
        )

        print(
            f"Reranker score: "
            f"{reranker_score:.4f}"
        )

        print(
            f"Top-5 categories: "
            f"{top5_categories}"
        )

        print(
            f"Top-1: "
            f"{'PASS' if top1_correct else 'FAIL'}"
        )

        print(
            f"Top-5: "
            f"{'PASS' if top5_correct else 'FAIL'}"
        )

        results_summary.append(
            {
                "question": question,
                "expected":
                    expected_category,
                "retrieved":
                    top_category,
                "top1_correct":
                    top1_correct,
            }
        )

    total = len(TEST_CASES)

    top1_accuracy = (
        correct_top1
        / total
        * 100
    )

    top5_accuracy = (
        correct_top5
        / total
        * 100
    )

    print(
        "\n"
        + "=" * 80
    )

    print(
        "FINAL RERANKED RESULTS"
    )

    print(
        "=" * 80
    )

    print(
        f"Top-1 correct: "
        f"{correct_top1}/{total}"
    )

    print(
        f"Top-1 accuracy: "
        f"{top1_accuracy:.2f}%"
    )

    print(
        f"Top-5 correct: "
        f"{correct_top5}/{total}"
    )

    print(
        f"Top-5 accuracy: "
        f"{top5_accuracy:.2f}%"
    )

    print(
        "\nFailed Top-1 questions:"
    )

    failed = [
        result
        for result
        in results_summary
        if not result[
            "top1_correct"
        ]
    ]

    if not failed:
        print("None.")
    else:
        for result in failed:
            print(
                f"- {result['question']}"
            )
            print(
                f"  Expected: "
                f"{result['expected']}"
            )
            print(
                f"  Retrieved: "
                f"{result['retrieved']}"
            )

    print(
        "=" * 80
    )


if __name__ == "__main__":
    main()