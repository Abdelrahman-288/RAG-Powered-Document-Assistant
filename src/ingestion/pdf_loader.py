from pathlib import Path
from typing import Any

from pypdf import PdfReader


def discover_pdf_files(data_dir: str | Path) -> list[Path]:
    """
    Recursively discover all PDF files inside the raw data directory.

    Example:
        data/raw/ai_ml/book.pdf
        data/raw/networking/ccna.pdf
    """
    data_dir = Path(data_dir)

    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory does not exist: {data_dir}")

    pdf_files = sorted(data_dir.rglob("*.pdf"))

    return pdf_files


def get_category_from_path(pdf_path: Path, raw_data_dir: Path) -> str:
    """
    Determine the document category from the first folder
    underneath data/raw/.

    Example:
        data/raw/cybersecurity/security.pdf
        -> cybersecurity
    """
    relative_path = pdf_path.relative_to(raw_data_dir)

    if len(relative_path.parts) < 2:
        return "uncategorized"

    return relative_path.parts[0]


def load_pdf(
    pdf_path: str | Path,
    raw_data_dir: str | Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Load a PDF page-by-page.

    Returns:
        pages:
            Successfully extracted pages.

        issues:
            Pages/files that failed or contained no extractable text.
    """
    pdf_path = Path(pdf_path)
    raw_data_dir = Path(raw_data_dir)

    pages: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []

    category = get_category_from_path(pdf_path, raw_data_dir)

    try:
        reader = PdfReader(str(pdf_path))
    except Exception as exc:
        issues.append(
            {
                "document": pdf_path.name,
                "path": str(pdf_path),
                "page": None,
                "issue": "failed_to_open",
                "error": str(exc),
            }
        )

        return pages, issues

    for page_index, page in enumerate(reader.pages):
        page_number = page_index + 1

        try:
            text = page.extract_text()

            if text is None or not text.strip():
                issues.append(
                    {
                        "document": pdf_path.name,
                        "path": str(pdf_path),
                        "page": page_number,
                        "issue": "empty_or_scanned_page",
                        "error": None,
                    }
                )
                continue

            pages.append(
                {
                    "text": text,
                    "metadata": {
                        "category": category,
                        "document": pdf_path.name,
                        "path": str(pdf_path),
                        "page": page_number,
                    },
                }
            )

        except Exception as exc:
            issues.append(
                {
                    "document": pdf_path.name,
                    "path": str(pdf_path),
                    "page": page_number,
                    "issue": "page_extraction_failed",
                    "error": str(exc),
                }
            )

    return pages, issues


def load_all_pdfs(
    raw_data_dir: str | Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Discover and load every PDF inside the raw data directory.
    """
    raw_data_dir = Path(raw_data_dir)

    pdf_files = discover_pdf_files(raw_data_dir)

    all_pages: list[dict[str, Any]] = []
    all_issues: list[dict[str, Any]] = []

    print(f"Found {len(pdf_files)} PDF file(s).")

    for pdf_path in pdf_files:
        print(f"Loading: {pdf_path}")

        pages, issues = load_pdf(
            pdf_path=pdf_path,
            raw_data_dir=raw_data_dir,
        )

        all_pages.extend(pages)
        all_issues.extend(issues)

    print()
    print("PDF loading complete.")
    print(f"Extracted pages: {len(all_pages)}")
    print(f"Pages/files with issues: {len(all_issues)}")

    return all_pages, all_issues