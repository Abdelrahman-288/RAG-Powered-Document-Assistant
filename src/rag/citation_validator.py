import re
import unicodedata
from typing import Any


CITATION_PATTERN = re.compile(
    r"Document:\s*([^;\]\n]+?)\s*,\s*Page:\s*(\d+)",
    re.IGNORECASE,
)


def normalize_document_name(
    document: str,
) -> str:
    """
    Normalize harmless formatting differences while
    preserving the actual document identity.

    Handles:
    - case differences
    - repeated whitespace
    - Unicode normalization
    - curly quotes
    - Unicode dash variants
    """

    normalized = unicodedata.normalize(
        "NFKC",
        document,
    )

    normalized = (
        normalized
        .replace("–", "-")
        .replace("—", "-")
        .replace("−", "-")
        .replace("’", "'")
        .replace("‘", "'")
        .replace("“", '"')
        .replace("”", '"')
    )

    normalized = " ".join(
        normalized
        .strip()
        .split()
    )

    return normalized.casefold()


def build_allowed_citations(
    retrieved_chunks: list[dict[str, Any]],
) -> set[tuple[str, int]]:
    """
    Build the exact set of document/page citations
    supported by the retrieved context.
    """

    allowed: set[
        tuple[str, int]
    ] = set()

    for chunk in retrieved_chunks:
        metadata = (
            chunk.get(
                "metadata",
                {},
            )
            or {}
        )

        document = metadata.get(
            "document"
        )

        page = metadata.get(
            "page"
        )

        if (
            document is None
            or page is None
        ):
            continue

        try:
            page_number = int(
                page
            )

        except (
            TypeError,
            ValueError,
        ):
            continue

        normalized_document = (
            normalize_document_name(
                str(document)
            )
        )

        allowed.add(
            (
                normalized_document,
                page_number,
            )
        )

    return allowed


def extract_citations(
    answer: str,
) -> list[tuple[str, int]]:
    """
    Extract all citations written as:

    [Document: file.pdf, Page: 10]

    Multiple citations inside one bracket are also
    supported.
    """

    citations: list[
        tuple[str, int]
    ] = []

    matches = (
        CITATION_PATTERN.findall(
            answer
        )
    )

    for document, page in matches:
        document = (
            document.strip()
        )

        try:
            page_number = int(
                page
            )

        except ValueError:
            continue

        citations.append(
            (
                document,
                page_number,
            )
        )

    return citations


def validate_citations(
    answer: str,
    retrieved_chunks: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Validate citations against retrieved context.

    A grounded answer must:
    1. contain at least one citation;
    2. contain no unsupported citations.
    """

    allowed = (
        build_allowed_citations(
            retrieved_chunks
        )
    )

    found = (
        extract_citations(
            answer
        )
    )

    valid: list[
        tuple[str, int]
    ] = []

    invalid: list[
        tuple[str, int]
    ] = []

    for document, page in found:
        normalized = (
            normalize_document_name(
                document
            ),
            page,
        )

        if normalized in allowed:
            valid.append(
                (
                    document,
                    page,
                )
            )

        else:
            invalid.append(
                (
                    document,
                    page,
                )
            )

    has_citations = (
        len(found) > 0
    )

    all_valid = (
        has_citations
        and len(invalid) == 0
    )

    return {
        "valid":
            valid,

        "invalid":
            invalid,

        "all_valid":
            all_valid,

        "has_citations":
            has_citations,

        "citation_count":
            len(found),
    }