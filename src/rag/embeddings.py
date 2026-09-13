import re
from collections.abc import Iterable

import numpy as np
import torch
from sentence_transformers import SentenceTransformer


DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def sanitize_text(text: object) -> str:
    """
    Convert arbitrary input to safe Unicode text for Hugging Face tokenizers.

    PDF extraction can occasionally produce malformed Unicode,
    null characters, or other control characters that fast tokenizers
    do not handle reliably.
    """

    if not isinstance(text, str):
        text = str(text)

    # Replace malformed Unicode sequences safely.
    text = text.encode(
        "utf-8",
        errors="replace",
    ).decode(
        "utf-8",
        errors="replace",
    )

    # Remove NULL characters.
    text = text.replace("\x00", " ")

    # Remove control characters while preserving:
    # \n = newline
    # \t = tab
    text = "".join(
        char
        for char in text
        if char in "\n\t" or ord(char) >= 32
    )

    # Normalize excessive spaces.
    text = re.sub(r"[ \t]+", " ", text)

    text = text.strip()

    if not text:
        text = "[EMPTY]"

    return text


class EmbeddingService:
    def __init__(
        self,
        model_name: str = DEFAULT_EMBEDDING_MODEL,
        device: str | None = None,
    ) -> None:

        if device is None:
            device = (
                "cuda"
                if torch.cuda.is_available()
                else "cpu"
            )

        self.device = device
        self.model_name = model_name

        print(
            f"Loading embedding model: "
            f"{self.model_name}"
        )

        print(
            f"Embedding device: "
            f"{self.device}"
        )

        self.model = SentenceTransformer(
            self.model_name,
            device=self.device,
        )

    def encode(
        self,
        texts: Iterable[object],
        batch_size: int = 32,
        show_progress_bar: bool = True,
    ) -> np.ndarray:
        """
        Generate normalized embeddings.

        Every input is sanitized before reaching the tokenizer.
        """

        sanitized_texts = [
            sanitize_text(text)
            for text in texts
        ]

        if not sanitized_texts:
            raise ValueError(
                "No texts were provided for embedding."
            )

        return self.model.encode(
            sanitized_texts,
            batch_size=batch_size,
            show_progress_bar=show_progress_bar,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

    def encode_one(
        self,
        text: object,
    ) -> np.ndarray:
        """
        Safely generate an embedding for one text.
        """

        sanitized_text = sanitize_text(text)

        embedding = self.model.encode(
            [sanitized_text],
            batch_size=1,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embedding[0]