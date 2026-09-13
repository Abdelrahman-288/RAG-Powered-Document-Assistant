from pathlib import Path
from typing import Any

import chromadb

from src.rag.embeddings import EmbeddingService, sanitize_text


DEFAULT_COLLECTION_NAME = "techrag_documents"


def sanitize_metadata(
    metadata: dict[str, Any],
) -> dict[str, Any]:
    """
    Sanitize metadata before storing it in ChromaDB.

    ChromaDB metadata values should be simple values such as:
    str, int, float, or bool.
    """

    sanitized: dict[str, Any] = {}

    for key, value in metadata.items():

        # Sanitize string metadata.
        if isinstance(value, str):
            sanitized[key] = sanitize_text(value)

        # Keep supported primitive values unchanged.
        elif isinstance(value, (int, float, bool)):
            sanitized[key] = value

        # Convert unsupported values to safe strings.
        elif value is None:
            sanitized[key] = ""

        else:
            sanitized[key] = sanitize_text(str(value))

    return sanitized


class ChromaIndexer:
    """
    Persistent ChromaDB indexer.

    Features:
    - Batch indexing
    - Safe Unicode sanitization
    - GPU embeddings
    - Automatic batch recovery
    - Individual chunk fallback
    - Persistent storage
    - Safe upserts
    """

    def __init__(
        self,
        persist_directory: str | Path,
        collection_name: str = DEFAULT_COLLECTION_NAME,
    ) -> None:

        self.persist_directory = Path(
            persist_directory
        )

        self.collection_name = collection_name

        self.persist_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory)
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={
                    "hnsw:space": "cosine",
                },
            )
        )

    def index_chunks(
        self,
        chunks: list[dict[str, Any]],
        embedding_service: EmbeddingService,
        batch_size: int = 32,
        indexing_batch_size: int = 256,
    ) -> None:
        """
        Embed and store chunks in ChromaDB.

        The corpus is processed in smaller groups so large
        knowledge bases can be indexed safely.

        If a complete batch fails, each chunk is processed
        individually so that one malformed chunk does not
        terminate the entire ingestion process.
        """

        if not chunks:
            print("No chunks to index.")
            return

        total_chunks = len(chunks)

        total_saved = 0
        total_skipped = 0

        print(
            f"\nIndexing {total_chunks} chunks "
            f"in batches of {indexing_batch_size}..."
        )

        for start in range(
            0,
            total_chunks,
            indexing_batch_size,
        ):

            end = min(
                start + indexing_batch_size,
                total_chunks,
            )

            batch = chunks[start:end]

            valid_chunks: list[dict[str, Any]] = []

            texts: list[str] = []
            ids: list[str] = []
            metadatas: list[dict[str, Any]] = []

            #
            # Prepare and sanitize batch
            #
            for chunk in batch:

                raw_text = chunk.get(
                    "text",
                    "",
                )

                safe_text = sanitize_text(
                    raw_text
                )

                if not safe_text:
                    total_skipped += 1
                    continue

                chunk_id = chunk.get("id")

                if not chunk_id:
                    print(
                        "Warning: skipping chunk "
                        "without ID."
                    )

                    total_skipped += 1
                    continue

                raw_metadata = chunk.get(
                    "metadata",
                    {},
                )

                if not isinstance(
                    raw_metadata,
                    dict,
                ):
                    print(
                        f"Warning: skipping "
                        f"{chunk_id}: invalid metadata."
                    )

                    total_skipped += 1
                    continue

                safe_metadata = sanitize_metadata(
                    raw_metadata
                )

                safe_chunk = {
                    "id": str(chunk_id),
                    "text": safe_text,
                    "metadata": safe_metadata,
                }

                valid_chunks.append(
                    safe_chunk
                )

                texts.append(
                    safe_text
                )

                ids.append(
                    str(chunk_id)
                )

                metadatas.append(
                    safe_metadata
                )

            if not valid_chunks:
                print(
                    f"\nSkipping chunks "
                    f"{start + 1}-{end}: "
                    f"no valid text found."
                )

                continue

            print(
                f"\nProcessing chunks "
                f"{start + 1}-{end} "
                f"/ {total_chunks}"
            )

            #
            # Normal batch embedding + storage
            #
            try:

                embeddings = (
                    embedding_service.encode(
                        texts,
                        batch_size=batch_size,
                    )
                )

                self.collection.upsert(
                    ids=ids,
                    documents=texts,
                    metadatas=metadatas,
                    embeddings=embeddings.tolist(),
                )

                batch_saved = len(ids)

                total_saved += batch_saved

                print(
                    f"Saved {batch_saved} chunks."
                )

            #
            # Batch failure recovery
            #
            except Exception as batch_exc:

                print(
                    f"\nBatch failed for chunks "
                    f"{start + 1}-{end}."
                )

                print(
                    f"Reason: {batch_exc}"
                )

                print(
                    "\nTrying chunks individually..."
                )

                successful_ids: list[str] = []
                successful_texts: list[str] = []
                successful_metadatas: list[
                    dict[str, Any]
                ] = []
                successful_embeddings: list[
                    list[float]
                ] = []

                failed_chunks: list[
                    dict[str, Any]
                ] = []

                for local_index, chunk in enumerate(
                    valid_chunks
                ):

                    global_index = (
                        start
                        + local_index
                    )

                    chunk_id = chunk["id"]
                    text = chunk["text"]
                    metadata = chunk["metadata"]

                    try:

                        #
                        # Sanitize again defensively.
                        #
                        safe_text = sanitize_text(
                            text
                        )

                        safe_metadata = (
                            sanitize_metadata(
                                metadata
                            )
                        )

                        embedding = (
                            embedding_service.encode_one(
                                safe_text
                            )
                        )

                        successful_ids.append(
                            chunk_id
                        )

                        successful_texts.append(
                            safe_text
                        )

                        successful_metadatas.append(
                            safe_metadata
                        )

                        successful_embeddings.append(
                            embedding.tolist()
                        )

                    except Exception as item_exc:

                        failed_chunks.append(
                            {
                                "global_index":
                                    global_index,

                                "chunk_id":
                                    chunk_id,

                                "document":
                                    metadata.get(
                                        "document"
                                    ),

                                "page":
                                    metadata.get(
                                        "page"
                                    ),

                                "category":
                                    metadata.get(
                                        "category"
                                    ),

                                "text_length":
                                    len(text),

                                "error":
                                    str(item_exc),
                            }
                        )

                #
                # Save recovered chunks.
                #
                if successful_ids:

                    try:

                        self.collection.upsert(
                            ids=successful_ids,
                            documents=successful_texts,
                            metadatas=successful_metadatas,
                            embeddings=successful_embeddings,
                        )

                        recovered_count = len(
                            successful_ids
                        )

                        total_saved += (
                            recovered_count
                        )

                        print(
                            f"\nRecovered and saved "
                            f"{recovered_count} chunks."
                        )

                    except Exception as db_exc:

                        print(
                            "\nFailed to save the "
                            "recovered chunks."
                        )

                        print(
                            f"Reason: {db_exc}"
                        )

                        raise

                #
                # Report truly bad chunks.
                #
                if failed_chunks:

                    total_skipped += len(
                        failed_chunks
                    )

                    print(
                        "\n"
                        + "=" * 70
                    )

                    print(
                        "SKIPPED PROBLEMATIC CHUNKS"
                    )

                    print(
                        "=" * 70
                    )

                    for failed in failed_chunks:

                        print(
                            "\n"
                            f"Global index: "
                            f"{failed['global_index']}\n"

                            f"Chunk ID: "
                            f"{failed['chunk_id']}\n"

                            f"Document: "
                            f"{failed['document']}\n"

                            f"Page: "
                            f"{failed['page']}\n"

                            f"Category: "
                            f"{failed['category']}\n"

                            f"Text length: "
                            f"{failed['text_length']}\n"

                            f"Error: "
                            f"{failed['error']}"
                        )

                    print(
                        "=" * 70
                    )

                print(
                    "\nContinuing with "
                    "the next batch..."
                )

        #
        # Final summary
        #
        print(
            "\n"
            + "=" * 70
        )

        print(
            "INDEXING COMPLETE"
        )

        print(
            "=" * 70
        )

        print(
            f"Input chunks: "
            f"{total_chunks}"
        )

        print(
            f"Chunks saved this run: "
            f"{total_saved}"
        )

        print(
            f"Chunks skipped: "
            f"{total_skipped}"
        )

        print(
            f"Chunks currently in "
            f"ChromaDB: {self.count()}"
        )

        print(
            "=" * 70
        )

    def count(self) -> int:
        """
        Return the current number of records
        inside the collection.
        """

        return self.collection.count()

    def delete_collection(self) -> None:
        """
        Delete the configured collection.
        """

        try:

            self.client.delete_collection(
                name=self.collection_name
            )

            print(
                f"Deleted collection: "
                f"{self.collection_name}"
            )

        except Exception as exc:

            print(
                f"Could not delete collection "
                f"{self.collection_name}: "
                f"{exc}"
            )

    def collection_exists(self) -> bool:
        """
        Check whether the configured collection exists.
        """

        try:

            self.client.get_collection(
                name=self.collection_name
            )

            return True

        except Exception:
            return False