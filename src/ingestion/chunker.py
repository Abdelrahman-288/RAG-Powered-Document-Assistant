from pathlib import Path
from typing import Any
import hashlib


DEFAULT_CHUNK_SIZE = 1200
DEFAULT_CHUNK_OVERLAP = 200


def split_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[str]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative.")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size.")

    if not isinstance(text, str):
        text = str(text)

    text = text.strip()

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - chunk_overlap

    return chunks


def create_chunk_id(
    document: str,
    page: int,
    page_chunk_index: int,
) -> str:
    raw_id = f"{document}|{page}|{page_chunk_index}"

    digest = hashlib.sha256(
        raw_id.encode("utf-8")
    ).hexdigest()[:16]

    return f"chunk_{digest}"


def chunk_pages(
    pages: list[dict[str, Any]],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[dict[str, Any]]:

    all_chunks = []

    for page in pages:
        page_text = page["text"]
        page_metadata = page["metadata"]

        text_chunks = split_text(
            text=page_text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        for chunk_index, chunk_text in enumerate(text_chunks):
            document = page_metadata["document"]
            page_number = page_metadata["page"]

            chunk_id = create_chunk_id(
                document=document,
                page=page_number,
                page_chunk_index=chunk_index,
            )

            metadata = page_metadata.copy()

            metadata.update(
                {
                    "chunk_id": chunk_id,
                    "page_chunk_index": chunk_index,
                    "chunk_size": len(chunk_text),
                }
            )

            all_chunks.append(
                {
                    "id": chunk_id,
                    "text": chunk_text,
                    "metadata": metadata,
                }
            )

    return all_chunks