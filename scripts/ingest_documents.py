from pathlib import Path

from src.ingestion.chunker import chunk_pages
from src.ingestion.cleaner import clean_pages
from src.ingestion.indexer import ChromaIndexer
from src.ingestion.manifest import (
    get_file_signature,
    load_manifest,
    needs_ingestion,
    save_manifest,
)
from src.ingestion.pdf_loader import (
    discover_pdf_files,
    load_pdf,
)
from src.rag.embeddings import EmbeddingService


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
VECTOR_STORE_DIR = PROJECT_ROOT / "data" / "vector_store"

MANIFEST_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ingestion_manifest.json"
)


def main() -> None:
    print("=" * 70)
    print("TechRAG Incremental Ingestion")
    print("=" * 70)

    pdf_files = discover_pdf_files(
        RAW_DATA_DIR
    )

    print(
        f"\nFound {len(pdf_files)} PDF file(s)."
    )

    manifest = load_manifest(
        MANIFEST_PATH
    )

    files_to_process = [
        pdf_path
        for pdf_path in pdf_files
        if needs_ingestion(
            pdf_path,
            manifest,
        )
    ]

    if not files_to_process:
        print(
            "\nNo new or modified PDFs found."
        )
        print(
            "Vector store is already up to date."
        )
        return

    print(
        f"\nFiles requiring ingestion: "
        f"{len(files_to_process)}"
    )

    all_pages = []
    all_issues = []

    for pdf_path in files_to_process:
        print(
            f"\nLoading: {pdf_path}"
        )

        pages, issues = load_pdf(
            pdf_path=pdf_path,
            raw_data_dir=RAW_DATA_DIR,
        )

        all_pages.extend(pages)
        all_issues.extend(issues)

    cleaned_pages = clean_pages(
        all_pages
    )

    chunks = chunk_pages(
        pages=cleaned_pages,
        chunk_size=1200,
        chunk_overlap=200,
    )

    print("\n=== INGESTION SUMMARY ===")
    print(
        f"Files processed: "
        f"{len(files_to_process)}"
    )
    print(
        f"Extracted pages: "
        f"{len(all_pages)}"
    )
    print(
        f"Cleaned pages: "
        f"{len(cleaned_pages)}"
    )
    print(
        f"Generated chunks: "
        f"{len(chunks)}"
    )
    print(
        f"Issues detected: "
        f"{len(all_issues)}"
    )

    if not chunks:
        print("\nNo chunks generated.")
        return

    embedding_service = EmbeddingService()

    indexer = ChromaIndexer(
        persist_directory=VECTOR_STORE_DIR,
    )

    indexer.index_chunks(
        chunks=chunks,
        embedding_service=embedding_service,
        batch_size=32,
        indexing_batch_size=256,
    )

    for pdf_path in files_to_process:
        manifest[
            str(pdf_path.resolve())
        ] = get_file_signature(
            pdf_path
        )

    save_manifest(
        manifest,
        MANIFEST_PATH,
    )

    print("\n=== VECTOR STORE ===")
    print(
        f"Stored chunks: "
        f"{indexer.count()}"
    )

    print(
        f"Location: "
        f"{VECTOR_STORE_DIR}"
    )

    print(
        "\nManifest updated successfully."
    )


if __name__ == "__main__":
    main()