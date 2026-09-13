from pathlib import Path

from src.ingestion.chunker import chunk_pages
from src.ingestion.cleaner import clean_pages
from src.ingestion.pdf_loader import load_all_pdfs


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def main() -> None:
    pages, issues = load_all_pdfs(RAW_DATA_DIR)

    cleaned_pages = clean_pages(pages)

    chunks = chunk_pages(
        pages=cleaned_pages,
        chunk_size=1200,
        chunk_overlap=200,
    )

    print("\n=== SUMMARY ===")
    print(f"Raw extracted pages: {len(pages)}")
    print(f"Cleaned pages: {len(cleaned_pages)}")
    print(f"Generated chunks: {len(chunks)}")
    print(f"Issues detected: {len(issues)}")

    if chunks:
        first_chunk = chunks[0]

        print("\n=== FIRST CHUNK ===")

        print("ID:")
        print(first_chunk["id"])

        print("\nMetadata:")
        print(first_chunk["metadata"])

        print("\nText:")
        print(first_chunk["text"])

    if issues:
        print("\n=== FIRST 10 ISSUES ===")

        for issue in issues[:10]:
            print(issue)


if __name__ == "__main__":
    main()