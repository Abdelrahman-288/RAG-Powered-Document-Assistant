from src.rag.embeddings import EmbeddingService


def main() -> None:
    texts = [
        "Machine learning is a field of artificial intelligence.",
        "PyTorch is a deep learning framework.",
        "Cybersecurity protects systems and networks.",
    ]

    service = EmbeddingService()

    embeddings = service.encode(texts)

    print("\n=== EMBEDDING TEST ===")
    print(f"Number of embeddings: {len(embeddings)}")
    print(f"Embedding dimension: {embeddings.shape[1]}")
    print(f"Embedding array shape: {embeddings.shape}")


if __name__ == "__main__":
    main()