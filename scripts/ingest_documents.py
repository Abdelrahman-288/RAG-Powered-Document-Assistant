from pathlib import Path

from src.ingestion.chunker import chunk_pages
from src.ingestion.cleaner import clean_pages
from src.ingestion.indexer import ChromaIndexer
from src.ingestion.pdf_loader import load_all_pdfs
from src.rag.embeddings import EmbeddingService


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
VECTOR_STORE_DIR = PROJECT_ROOT / "data" / "vector_store"


def main() -> None:
    # 1. Load PDFs
    pages, issues = load_all_pdfs(RAW_DATA_DIR)

    # 2. Clean extracted text
    cleaned_pages = clean_pages(pages)

    # 3. Create RAG chunks
    chunks = chunk_pages(
        pages=cleaned_pages,
        chunk_size=1200,
        chunk_overlap=200,
    )

    print("\n=== INGESTION SUMMARY ===")
    print(f"Raw extracted pages: {len(pages)}")
    print(f"Cleaned pages: {len(cleaned_pages)}")
    print(f"Generated chunks: {len(chunks)}")
    print(f"Issues detected: {len(issues)}")

    if not chunks:
        print("\nNo chunks were generated. Nothing to index.")
        return

    # 4. Load embedding model on CUDA
    embedding_service = EmbeddingService()

    # 5. Connect to persistent ChromaDB
    indexer = ChromaIndexer(
        persist_directory=VECTOR_STORE_DIR,
    )

    # 6. Generate embeddings and store everything
    indexer.index_chunks(
        chunks=chunks,
        embedding_service=embedding_service,
        batch_size=32,
    )

    print("\n=== VECTOR STORE ===")
    print(f"Stored chunks: {indexer.count()}")
    print(f"Location: {VECTOR_STORE_DIR}")

    if issues:
        print("\n=== DOCUMENT ISSUES ===")
        print(f"{len(issues)} page(s) could not provide extractable text.")


if __name__ == "__main__":
    main()