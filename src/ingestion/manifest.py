import json
from pathlib import Path
from typing import Any


MANIFEST_VERSION = 2


def load_manifest(
    manifest_path: str | Path,
) -> dict[str, Any]:
    """
    Load the ingestion manifest.

    Supports both:
    - the new versioned manifest format;
    - the older flat path -> signature format.
    """

    manifest_path = Path(
        manifest_path
    )

    if not manifest_path.exists():
        return {
            "version":
                MANIFEST_VERSION,

            "files":
                {},
        }

    try:
        with manifest_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(
                file
            )

    except (
        json.JSONDecodeError,
        OSError,
    ):
        return {
            "version":
                MANIFEST_VERSION,

            "files":
                {},
        }

    # --------------------------------------------------
    # New manifest format
    # --------------------------------------------------
    if (
        isinstance(data, dict)
        and "files" in data
    ):
        files = data.get(
            "files",
            {},
        )

        if not isinstance(
            files,
            dict,
        ):
            files = {}

        return {
            "version":
                data.get(
                    "version",
                    MANIFEST_VERSION,
                ),

            "files":
                files,
        }

    # --------------------------------------------------
    # Legacy manifest format
    #
    # Old structure:
    #
    # {
    #   "C:\\absolute\\path\\book.pdf": {
    #       "size": ...,
    #       "modified_time": ...
    #   }
    # }
    #
    # Keep it temporarily so the ingestion script
    # can migrate it.
    # --------------------------------------------------
    if isinstance(
        data,
        dict,
    ):
        return {
            "version":
                1,

            "legacy_files":
                data,

            "files":
                {},
        }

    return {
        "version":
            MANIFEST_VERSION,

        "files":
            {},
    }


def save_manifest(
    manifest: dict[str, Any],
    manifest_path: str | Path,
) -> None:
    manifest_path = Path(
        manifest_path
    )

    manifest_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    manifest["version"] = (
        MANIFEST_VERSION
    )

    manifest.pop(
        "legacy_files",
        None,
    )

    with manifest_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            manifest,
            file,
            indent=2,
            ensure_ascii=False,
        )


def get_manifest_key(
    file_path: str | Path,
    raw_data_dir: str | Path,
) -> str:
    """
    Return a portable path relative to data/raw.

    Example:

    cybersecurity/web_hacking.pdf
    """

    file_path = Path(
        file_path
    ).resolve()

    raw_data_dir = Path(
        raw_data_dir
    ).resolve()

    try:
        relative_path = (
            file_path.relative_to(
                raw_data_dir
            )
        )

    except ValueError:
        relative_path = Path(
            file_path.name
        )

    # Always use forward slashes so the manifest
    # remains portable across Windows/Linux.
    return relative_path.as_posix()


def get_file_signature(
    file_path: str | Path,
) -> dict[str, Any]:
    """
    Return file properties used to detect changes.
    """

    file_path = Path(
        file_path
    )

    stat = (
        file_path.stat()
    )

    return {
        "size":
            stat.st_size,

        "modified_time_ns":
            stat.st_mtime_ns,
    }


def build_manifest_entry(
    file_path: str | Path,
    raw_data_dir: str | Path,
) -> dict[str, Any]:
    """
    Build one complete manifest entry.

    Stores enough metadata to remove stale
    Chroma chunks later.
    """

    file_path = Path(
        file_path
    )

    raw_data_dir = Path(
        raw_data_dir
    )

    key = get_manifest_key(
        file_path=file_path,
        raw_data_dir=raw_data_dir,
    )

    relative_path = Path(
        key
    )

    # First directory under data/raw is the category.
    if len(
        relative_path.parts
    ) > 1:
        category = (
            relative_path.parts[0]
        )
    else:
        category = "uncategorized"

    return {
        "signature":
            get_file_signature(
                file_path
            ),

        "document":
            file_path.name,

        "category":
            category,

        "relative_path":
            key,
    }


def needs_ingestion(
    file_path: str | Path,
    manifest: dict[str, Any],
    raw_data_dir: str | Path,
) -> bool:
    """
    Return True when a PDF is new or modified.
    """

    key = get_manifest_key(
        file_path=file_path,
        raw_data_dir=raw_data_dir,
    )

    files = manifest.get(
        "files",
        {},
    )

    previous_entry = (
        files.get(
            key
        )
    )

    if previous_entry is None:
        return True

    previous_signature = (
        previous_entry.get(
            "signature"
        )
    )

    current_signature = (
        get_file_signature(
            file_path
        )
    )

    return (
        previous_signature
        != current_signature
    )


def get_deleted_entries(
    current_files:
        list[str | Path],
    manifest:
        dict[str, Any],
    raw_data_dir:
        str | Path,
) -> list[dict[str, Any]]:
    """
    Return manifest entries whose PDFs
    no longer exist in data/raw.
    """

    existing_keys = {
        get_manifest_key(
            file_path=file_path,
            raw_data_dir=raw_data_dir,
        )
        for file_path
        in current_files
    }

    files = manifest.get(
        "files",
        {},
    )

    deleted_entries = []

    for key, entry in (
        files.items()
    ):
        if (
            key
            not in existing_keys
        ):
            deleted_entries.append(
                {
                    "key":
                        key,

                    **entry,
                }
            )

    return (
        deleted_entries
    )