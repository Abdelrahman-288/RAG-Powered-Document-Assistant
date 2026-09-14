from pathlib import Path

import chromadb

from src.ingestion.chunker import (
    chunk_pages,
)
from src.ingestion.cleaner import (
    clean_pages,
)
from src.ingestion.indexer import (
    ChromaIndexer,
)
from src.ingestion.manifest import (
    MANIFEST_VERSION,
    build_manifest_entry,
    get_deleted_entries,
    get_manifest_key,
    load_manifest,
    needs_ingestion,
    save_manifest,
)
from src.ingestion.pdf_loader import (
    discover_pdf_files,
    load_pdf,
)
from src.rag.embeddings import (
    EmbeddingService,
)


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

RAW_DATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
)

VECTOR_STORE_DIR = (
    PROJECT_ROOT
    / "data"
    / "vector_store"
)

MANIFEST_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ingestion_manifest.json"
)

COLLECTION_NAME = (
    "techrag_documents"
)


# ==========================================================
# Chroma helpers
# ==========================================================
def get_collection():
    client = (
        chromadb.PersistentClient(
            path=str(
                VECTOR_STORE_DIR
            )
        )
    )

    return (
        client.get_collection(
            name=COLLECTION_NAME
        )
    )


def delete_document_chunks(
    collection,
    document: str,
    category: str,
) -> None:
    """
    Delete every indexed chunk belonging
    to one document/category pair.
    """

    print(
        f"Removing old chunks: "
        f"{category}/{document}"
    )

    collection.delete(
        where={
            "$and": [
                {
                    "document":
                        document
                },
                {
                    "category":
                        category
                },
            ]
        }
    )


# ==========================================================
# Legacy manifest migration
# ==========================================================
def migrate_legacy_manifest(
    manifest: dict,
    pdf_files: list[Path],
) -> dict:
    """
    Convert the old absolute-path manifest
    into the new portable relative-path format.

    Only currently existing PDFs are migrated.
    """

    if (
        manifest.get(
            "version"
        )
        != 1
    ):
        return manifest

    print(
        "\nMigrating old ingestion manifest..."
    )

    legacy_files = (
        manifest.get(
            "legacy_files",
            {},
        )
    )

    migrated_manifest = {
        "version":
            MANIFEST_VERSION,

        "files":
            {},
    }

    for pdf_path in pdf_files:
        resolved = str(
            pdf_path.resolve()
        )

        old_signature = (
            legacy_files.get(
                resolved
            )
        )

        # If old manifest contains this file,
        # migrate it.
        if old_signature is not None:

            entry = (
                build_manifest_entry(
                    file_path=pdf_path,
                    raw_data_dir=RAW_DATA_DIR,
                )
            )

            # Old signature used modified_time,
            # while the new one uses nanoseconds.
            #
            # We intentionally keep the newly
            # calculated signature so the format
            # becomes consistent immediately.
            key = get_manifest_key(
                file_path=pdf_path,
                raw_data_dir=RAW_DATA_DIR,
            )

            migrated_manifest[
                "files"
            ][
                key
            ] = entry

    print(
        "Manifest migration completed."
    )

    return (
        migrated_manifest
    )


# ==========================================================
# Ingest one PDF
# ==========================================================
def process_pdf(
    pdf_path: Path,
    embedding_service:
        EmbeddingService,
    indexer:
        ChromaIndexer,
    collection,
) -> tuple[
    bool,
    int,
    int,
    int,
]:
    """
    Process one PDF independently.

    Returns:
        success
        extracted pages
        generated chunks
        issue count
    """

    print(
        "\n"
        + "-" * 70
    )

    print(
        f"Processing: {pdf_path}"
    )

    try:
        pages, issues = (
            load_pdf(
                pdf_path=pdf_path,
                raw_data_dir=RAW_DATA_DIR,
            )
        )

        cleaned_pages = (
            clean_pages(
                pages
            )
        )

        chunks = (
            chunk_pages(
                pages=cleaned_pages,
                chunk_size=1200,
                chunk_overlap=200,
            )
        )

        print(
            f"Extracted pages: "
            f"{len(pages)}"
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
            f"{len(issues)}"
        )

        if not chunks:
            print(
                "Skipping file because "
                "no chunks were generated."
            )

            return (
                False,
                len(pages),
                0,
                len(issues),
            )

        # --------------------------------------------------
        # Remove previous version of this PDF
        #
        # This prevents old chunks from remaining after
        # the document has changed.
        # --------------------------------------------------
        relative_key = (
            get_manifest_key(
                file_path=pdf_path,
                raw_data_dir=RAW_DATA_DIR,
            )
        )

        relative_path = Path(
            relative_key
        )

        if (
            len(
                relative_path.parts
            )
            > 1
        ):
            category = (
                relative_path.parts[0]
            )
        else:
            category = (
                "uncategorized"
            )

        delete_document_chunks(
            collection=collection,
            document=pdf_path.name,
            category=category,
        )

        # --------------------------------------------------
        # Index fresh version
        # --------------------------------------------------
        indexer.index_chunks(
            chunks=chunks,
            embedding_service=embedding_service,
            batch_size=32,
            indexing_batch_size=256,
        )

        print(
            "Indexed successfully."
        )

        return (
            True,
            len(pages),
            len(chunks),
            len(issues),
        )

    except Exception as exc:
        print(
            f"FAILED: {pdf_path}"
        )

        print(
            f"Reason: {exc}"
        )

        return (
            False,
            0,
            0,
            0,
        )


# ==========================================================
# Main
# ==========================================================
def main() -> None:
    print(
        "=" * 70
    )

    print(
        "TechRAG Incremental Ingestion"
    )

    print(
        "=" * 70
    )


    # --------------------------------------------------
    # Discover PDFs
    # --------------------------------------------------
    pdf_files = (
        discover_pdf_files(
            RAW_DATA_DIR
        )
    )

    pdf_files = sorted(
        Path(path)
        for path in pdf_files
    )

    print(
        f"\nFound "
        f"{len(pdf_files)} "
        f"PDF file(s)."
    )


    # --------------------------------------------------
    # Load + migrate manifest
    # --------------------------------------------------
    manifest = (
        load_manifest(
            MANIFEST_PATH
        )
    )

    manifest = (
        migrate_legacy_manifest(
            manifest=manifest,
            pdf_files=pdf_files,
        )
    )


    # --------------------------------------------------
    # Find removed PDFs
    # --------------------------------------------------
    deleted_entries = (
        get_deleted_entries(
            current_files=pdf_files,
            manifest=manifest,
            raw_data_dir=RAW_DATA_DIR,
        )
    )


    # --------------------------------------------------
    # Find new/modified PDFs
    # --------------------------------------------------
    files_to_process = [
        pdf_path

        for pdf_path
        in pdf_files

        if needs_ingestion(
            file_path=pdf_path,
            manifest=manifest,
            raw_data_dir=RAW_DATA_DIR,
        )
    ]


    print(
        f"New/modified files: "
        f"{len(files_to_process)}"
    )

    print(
        f"Deleted files: "
        f"{len(deleted_entries)}"
    )


    if (
        not files_to_process
        and not deleted_entries
    ):
        print(
            "\nNo changes detected."
        )

        print(
            "Vector store is already up to date."
        )

        # Save migrated manifest if necessary.
        save_manifest(
            manifest=manifest,
            manifest_path=MANIFEST_PATH,
        )

        return


    # --------------------------------------------------
    # Initialize Chroma
    # --------------------------------------------------
    collection = (
        get_collection()
    )


    # --------------------------------------------------
    # Remove deleted documents
    # --------------------------------------------------
    if deleted_entries:

        print(
            "\n=== REMOVING DELETED DOCUMENTS ==="
        )

        for entry in (
            deleted_entries
        ):
            document = (
                entry.get(
                    "document"
                )
            )

            category = (
                entry.get(
                    "category"
                )
            )

            key = (
                entry[
                    "key"
                ]
            )

            if (
                document
                and category
            ):
                delete_document_chunks(
                    collection=collection,
                    document=str(
                        document
                    ),
                    category=str(
                        category
                    ),
                )

            manifest[
                "files"
            ].pop(
                key,
                None,
            )


    # --------------------------------------------------
    # Initialize models only when needed
    # --------------------------------------------------
    if files_to_process:

        print(
            "\nInitializing embedding model..."
        )

        embedding_service = (
            EmbeddingService()
        )

        indexer = (
            ChromaIndexer(
                persist_directory=VECTOR_STORE_DIR,
            )
        )


        total_pages = 0
        total_chunks = 0
        total_issues = 0

        successful_files = 0
        failed_files = 0


        # --------------------------------------------------
        # Process each PDF separately
        # --------------------------------------------------
        for pdf_path in (
            files_to_process
        ):

            (
                success,
                page_count,
                chunk_count,
                issue_count,
            ) = process_pdf(
                pdf_path=pdf_path,
                embedding_service=embedding_service,
                indexer=indexer,
                collection=collection,
            )

            total_pages += (
                page_count
            )

            total_chunks += (
                chunk_count
            )

            total_issues += (
                issue_count
            )


            if success:

                successful_files += 1

                key = (
                    get_manifest_key(
                        file_path=pdf_path,
                        raw_data_dir=RAW_DATA_DIR,
                    )
                )

                manifest[
                    "files"
                ][
                    key
                ] = (
                    build_manifest_entry(
                        file_path=pdf_path,
                        raw_data_dir=RAW_DATA_DIR,
                    )
                )

                # Save after every successful PDF.
                #
                # If ingestion is interrupted, completed
                # files do not have to be reprocessed.
                save_manifest(
                    manifest=manifest,
                    manifest_path=MANIFEST_PATH,
                )

            else:

                failed_files += 1


        print(
            "\n=== INGESTION SUMMARY ==="
        )

        print(
            f"Successful files: "
            f"{successful_files}"
        )

        print(
            f"Failed files: "
            f"{failed_files}"
        )

        print(
            f"Extracted pages: "
            f"{total_pages}"
        )

        print(
            f"Generated chunks: "
            f"{total_chunks}"
        )

        print(
            f"Issues detected: "
            f"{total_issues}"
        )


    # --------------------------------------------------
    # Save final manifest
    # --------------------------------------------------
    save_manifest(
        manifest=manifest,
        manifest_path=MANIFEST_PATH,
    )


    # --------------------------------------------------
    # Final vector-store count
    # --------------------------------------------------
    final_count = (
        collection.count()
    )

    print(
        "\n=== VECTOR STORE ==="
    )

    print(
        f"Stored chunks: "
        f"{final_count}"
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