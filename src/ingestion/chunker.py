from typing import Any


DEFAULT_CHUNK_SIZE = 1200
DEFAULT_CHUNK_OVERLAP = 200


def split_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[str]:
    """
    Split text into overlapping character-based chunks.

    Each chunk overlaps with the previous chunk so important
    context is less likely to be lost at chunk boundaries.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative.")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size.")

    text = text.strip()

    if not text:
        return []

    chunks: list[str] = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = end - chunk_overlap

    return chunks


def chunk_pages(
    pages: list[dict[str, Any]],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[dict[str, Any]]:
    """
    Convert cleaned PDF pages into retrieval-ready chunks.

    Page metadata is preserved for citations.
    """

    all_chunks: list[dict[str, Any]] = []

    chunk_id = 0

    for page in pages:
        page_text = page["text"]
        page_metadata = page["metadata"]

        text_chunks = split_text(
            text=page_text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        for chunk_index, chunk_text in enumerate(text_chunks):
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
                    "id": f"chunk_{chunk_id}",
                    "text": chunk_text,
                    "metadata": metadata,
                }
            )

            chunk_id += 1

    return all_chunks