from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from backend.services import RAGService


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

EVALUATION_DIR = (
    PROJECT_ROOT
    / "evaluation"
)

CSV_PATH = (
    EVALUATION_DIR
    / "rag_evaluation_results.csv"
)

MARKDOWN_PATH = (
    EVALUATION_DIR
    / "rag_evaluation_summary.md"
)


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
            "What is privilege escalation?",
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
            "What is a Python context manager?",
        "expected_category":
            "python",
    },
    {
        "question":
            "What is transfer learning in deep learning?",
        "expected_category":
            "deep_learning",
    },
    {
        "question":
            "What is an object detector in computer vision?",
        "expected_category":
            "computer_vision",
    },
    {
        "question":
            "What is cloud security?",
        "expected_category":
            "cloud_security",
    },
    {
        "question":
            "What is an embedded system?",
        "expected_category":
            "embedded_systems",
    },
    {
        "question":
            "What is a large language model?",
        "expected_category":
            "llm",
    },
    {
        "question":
            "What is tokenization in natural language processing?",
        "expected_category":
            "nlp",
    },
]


def format_bool(
    value: bool,
) -> str:
    return (
        "PASS"
        if value
        else "FAIL"
    )


def safe_text(
    value: Any,
) -> str:
    if value is None:
        return ""

    return str(
        value
    ).replace(
        "\n",
        " ",
    ).strip()


def evaluate_case(
    rag_service: RAGService,
    test_case: dict[str, str],
) -> dict[str, Any]:

    question = (
        test_case[
            "question"
        ]
    )

    expected_category = (
        test_case[
            "expected_category"
        ]
    )

    try:
        result = (
            rag_service.query(
                question=question,
                category=None,
            )
        )

    except Exception as exc:
        return {
            "question":
                question,

            "expected_category":
                expected_category,

            "resolved_category":
                "",

            "category_correct":
                False,

            "needs_category_selection":
                False,

            "grounding_success":
                False,

            "citation_valid":
                False,

            "citation_count":
                0,

            "top_document":
                "",

            "top_page":
                "",

            "top_similarity":
                "",

            "top_reranker_score":
                "",

            "answer":
                "",

            "overall_pass":
                False,

            "error":
                str(
                    exc
                ),
        }

    resolved_category = (
        result.get(
            "resolved_category"
        )
    )

    category_correct = (
        resolved_category
        == expected_category
    )

    grounding_success = bool(
        result.get(
            "grounding_success",
            False,
        )
    )

    citation_valid = bool(
        result.get(
            "citation_valid",
            False,
        )
    )

    citation_count = int(
        result.get(
            "citation_count",
            0,
        )
    )

    needs_category_selection = bool(
        result.get(
            "needs_category_selection",
            False,
        )
    )

    sources = (
        result.get(
            "sources",
            [],
        )
        or []
    )

    top_document = ""
    top_page = ""
    top_similarity: float | str = ""
    top_reranker_score: float | str = ""

    if sources:
        top_source = (
            sources[
                0
            ]
        )

        top_document = (
            safe_text(
                top_source.get(
                    "document",
                    "",
                )
            )
        )

        top_page = (
            safe_text(
                top_source.get(
                    "page",
                    "",
                )
            )
        )

        top_similarity = (
            top_source.get(
                "similarity",
                "",
            )
        )

        top_reranker_score = (
            top_source.get(
                "reranker_score",
                "",
            )
        )

    answer = (
        safe_text(
            result.get(
                "answer",
                "",
            )
        )
    )

    overall_pass = (
        category_correct
        and not needs_category_selection
        and grounding_success
        and citation_valid
        and citation_count > 0
        and len(
            sources
        ) > 0
    )

    return {
        "question":
            question,

        "expected_category":
            expected_category,

        "resolved_category":
            resolved_category
            or "",

        "category_correct":
            category_correct,

        "needs_category_selection":
            needs_category_selection,

        "grounding_success":
            grounding_success,

        "citation_valid":
            citation_valid,

        "citation_count":
            citation_count,

        "top_document":
            top_document,

        "top_page":
            top_page,

        "top_similarity":
            top_similarity,

        "top_reranker_score":
            (
                top_reranker_score
                if top_reranker_score
                is not None
                else ""
            ),

        "answer":
            answer,

        "overall_pass":
            overall_pass,

        "error":
            "",
    }


def save_csv(
    results:
        list[
            dict[
                str,
                Any,
            ]
        ],
) -> None:

    EVALUATION_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "question",
        "expected_category",
        "resolved_category",
        "category_correct",
        "needs_category_selection",
        "grounding_success",
        "citation_valid",
        "citation_count",
        "top_document",
        "top_page",
        "top_similarity",
        "top_reranker_score",
        "answer",
        "overall_pass",
        "error",
    ]

    with CSV_PATH.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        writer = (
            csv.DictWriter(
                file,
                fieldnames=fieldnames,
            )
        )

        writer.writeheader()

        writer.writerows(
            results
        )


def save_markdown(
    results:
        list[
            dict[
                str,
                Any,
            ]
        ],
) -> None:

    total = (
        len(
            results
        )
    )

    category_correct_count = sum(
        1
        for item
        in results
        if item[
            "category_correct"
        ]
    )

    grounded_count = sum(
        1
        for item
        in results
        if item[
            "grounding_success"
        ]
    )

    citation_valid_count = sum(
        1
        for item
        in results
        if item[
            "citation_valid"
        ]
    )

    overall_pass_count = sum(
        1
        for item
        in results
        if item[
            "overall_pass"
        ]
    )

    ambiguity_count = sum(
        1
        for item
        in results
        if item[
            "needs_category_selection"
        ]
    )

    def percentage(
        value: int,
    ) -> float:
        if total == 0:
            return 0.0

        return (
            value
            / total
            * 100
        )

    lines = [
        "# TechRAG End-to-End RAG Evaluation",
        "",
        "## Summary",
        "",
        f"- Total questions: **{total}**",
        (
            f"- Auto-routing accuracy: "
            f"**{category_correct_count}/{total} "
            f"({percentage(category_correct_count):.2f}%)**"
        ),
        (
            f"- Grounded responses: "
            f"**{grounded_count}/{total} "
            f"({percentage(grounded_count):.2f}%)**"
        ),
        (
            f"- Citation validity: "
            f"**{citation_valid_count}/{total} "
            f"({percentage(citation_valid_count):.2f}%)**"
        ),
        (
            f"- Overall pass rate: "
            f"**{overall_pass_count}/{total} "
            f"({percentage(overall_pass_count):.2f}%)**"
        ),
        (
            f"- Questions requiring manual "
            f"category selection: "
            f"**{ambiguity_count}**"
        ),
        "",
        "## Results",
        "",
        (
            "| # | Question | Expected | Resolved | "
            "Grounded | Citations | Overall |"
        ),
        (
            "|---:|---|---|---|---|---|---|"
        ),
    ]

    for index, item in enumerate(
        results,
        start=1,
    ):

        question = (
            safe_text(
                item[
                    "question"
                ]
            )
            .replace(
                "|",
                "\\|",
            )
        )

        expected = (
            safe_text(
                item[
                    "expected_category"
                ]
            )
        )

        resolved = (
            safe_text(
                item[
                    "resolved_category"
                ]
            )
            or "None"
        )

        grounded = (
            format_bool(
                item[
                    "grounding_success"
                ]
            )
        )

        citation_status = (
            (
                f"PASS "
                f"({item['citation_count']})"
            )
            if (
                item[
                    "citation_valid"
                ]
                and item[
                    "citation_count"
                ] > 0
            )
            else "FAIL"
        )

        overall = (
            format_bool(
                item[
                    "overall_pass"
                ]
            )
        )

        lines.append(
            (
                f"| {index} "
                f"| {question} "
                f"| {expected} "
                f"| {resolved} "
                f"| {grounded} "
                f"| {citation_status} "
                f"| {overall} |"
            )
        )

    failed_results = [
        item
        for item
        in results
        if not item[
            "overall_pass"
        ]
    ]

    lines.extend(
        [
            "",
            "## Failure Analysis",
            "",
        ]
    )

    if not failed_results:
        lines.append(
            "All evaluation questions passed."
        )

    else:
        for item in (
            failed_results
        ):

            lines.extend(
                [
                    (
                        f"### {item['question']}"
                    ),
                    "",
                    (
                        f"- Expected category: "
                        f"`{item['expected_category']}`"
                    ),
                    (
                        f"- Resolved category: "
                        f"`{item['resolved_category'] or 'None'}`"
                    ),
                    (
                        f"- Grounded: "
                        f"{item['grounding_success']}"
                    ),
                    (
                        f"- Citation valid: "
                        f"{item['citation_valid']}"
                    ),
                    (
                        f"- Citation count: "
                        f"{item['citation_count']}"
                    ),
                    (
                        f"- Required category selection: "
                        f"{item['needs_category_selection']}"
                    ),
                ]
            )

            if (
                item[
                    "error"
                ]
            ):
                lines.append(
                    (
                        f"- Error: "
                        f"`{item['error']}`"
                    )
                )

            lines.append(
                ""
            )

    lines.extend(
        [
            "## Evaluation Criteria",
            "",
            (
                "A test case is considered an overall pass "
                "when:"
            ),
            "",
            "1. Auto routing selects the expected category.",
            "2. The system does not require manual category selection.",
            "3. The generated response is marked as grounded.",
            "4. All generated citations are valid.",
            "5. At least one citation is produced.",
            "6. At least one source is retrieved.",
            "",
            "## Pipeline Evaluated",
            "",
            (
                "**Question → Auto Routing → Retrieval → "
                "Reranking → Grounded Generation → "
                "Citation Validation**"
            ),
            "",
        ]
    )

    MARKDOWN_PATH.write_text(
        "\n".join(
            lines
        ),
        encoding="utf-8",
    )


def print_case_result(
    index: int,
    total: int,
    result:
        dict[
            str,
            Any,
        ],
) -> None:

    print(
        "\n"
        + "-" * 80
    )

    print(
        f"Question "
        f"{index}/{total}"
    )

    print(
        f"Question: "
        f"{result['question']}"
    )

    print(
        f"Expected category: "
        f"{result['expected_category']}"
    )

    print(
        f"Resolved category: "
        f"{result['resolved_category'] or 'None'}"
    )

    print(
        "Category routing: "
        + format_bool(
            result[
                "category_correct"
            ]
        )
    )

    print(
        "Grounding: "
        + format_bool(
            result[
                "grounding_success"
            ]
        )
    )

    print(
        "Citation validation: "
        + format_bool(
            result[
                "citation_valid"
            ]
        )
    )

    print(
        f"Citation count: "
        f"{result['citation_count']}"
    )

    print(
        f"Top document: "
        f"{result['top_document'] or 'None'}"
    )

    print(
        "Overall: "
        + format_bool(
            result[
                "overall_pass"
            ]
        )
    )

    if (
        result[
            "error"
        ]
    ):
        print(
            f"ERROR: "
            f"{result['error']}"
        )


def main() -> None:

    print(
        "=" * 80
    )

    print(
        "TechRAG Full End-to-End Evaluation"
    )

    print(
        "=" * 80
    )

    print(
        "\nInitializing RAG service..."
    )

    rag_service = (
        RAGService()
    )

    print(
        f"\nEvaluation questions: "
        f"{len(TEST_CASES)}"
    )

    results: list[
        dict[
            str,
            Any,
        ]
    ] = []

    for index, test_case in enumerate(
        TEST_CASES,
        start=1,
    ):

        result = (
            evaluate_case(
                rag_service=rag_service,
                test_case=test_case,
            )
        )

        results.append(
            result
        )

        print_case_result(
            index=index,
            total=len(
                TEST_CASES
            ),
            result=result,
        )

    save_csv(
        results
    )

    save_markdown(
        results
    )

    total = (
        len(
            results
        )
    )

    overall_passes = sum(
        1
        for result
        in results
        if result[
            "overall_pass"
        ]
    )

    routing_passes = sum(
        1
        for result
        in results
        if result[
            "category_correct"
        ]
    )

    grounded_passes = sum(
        1
        for result
        in results
        if result[
            "grounding_success"
        ]
    )

    citation_passes = sum(
        1
        for result
        in results
        if result[
            "citation_valid"
        ]
    )

    print(
        "\n"
        + "=" * 80
    )

    print(
        "FINAL END-TO-END RESULTS"
    )

    print(
        "=" * 80
    )

    print(
        f"Auto-routing correct: "
        f"{routing_passes}/{total}"
    )

    print(
        f"Grounded answers: "
        f"{grounded_passes}/{total}"
    )

    print(
        f"Valid citations: "
        f"{citation_passes}/{total}"
    )

    print(
        f"Overall passed: "
        f"{overall_passes}/{total}"
    )

    if total > 0:
        overall_pass_rate = (
            overall_passes
            / total
            * 100
        )

        print(
            f"Overall pass rate: "
            f"{overall_pass_rate:.2f}%"
        )

    print(
        "\nResults saved to:"
    )

    print(
        f"- {CSV_PATH}"
    )

    print(
        f"- {MARKDOWN_PATH}"
    )

    print(
        "=" * 80
    )


if __name__ == "__main__":
    main()