import re
from typing import Any


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace while preserving paragraph boundaries.
    """

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = re.sub(r"[ \t]+", " ", text)

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def fix_broken_words(text: str) -> str:
    """
    Fix simple hyphenated word breaks caused by PDF line wrapping.

    Example:
        machin-\nlearning
        -> machinlearning

    This is intentionally conservative.
    """

    text = re.sub(
        r"(\w)-\n(\w)",
        r"\1\2",
        text,
    )

    return text


def clean_text(text: str) -> str:
    """
    Apply the complete text-cleaning pipeline.
    """

    text = fix_broken_words(text)
    text = normalize_whitespace(text)

    return text


def clean_pages(
    pages: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Clean all extracted PDF pages while preserving metadata.
    """

    cleaned_pages: list[dict[str, Any]] = []

    for page in pages:
        cleaned_text = clean_text(page["text"])

        if not cleaned_text:
            continue

        cleaned_pages.append(
            {
                "text": cleaned_text,
                "metadata": page["metadata"],
            }
        )

    return cleaned_pages