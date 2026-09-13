from typing import Iterable

import torch
from sentence_transformers import SentenceTransformer


DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingService:
    def __init__(
        self,
        model_name: str = DEFAULT_EMBEDDING_MODEL,
        device: str | None = None,
    ) -> None:
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        self.device = device
        self.model_name = model_name

        print(f"Loading embedding model: {self.model_name}")
        print(f"Embedding device: {self.device}")

        self.model = SentenceTransformer(
            self.model_name,
            device=self.device,
        )

    def encode(
        self,
        texts: Iterable[str],
        batch_size: int = 32,
    ):
        texts = list(texts)

        return self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )