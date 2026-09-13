import json
from pathlib import Path
from typing import Any


def load_manifest(
    manifest_path: str | Path,
) -> dict[str, Any]:
    manifest_path = Path(manifest_path)

    if not manifest_path.exists():
        return {}

    with manifest_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def save_manifest(
    manifest: dict[str, Any],
    manifest_path: str | Path,
) -> None:
    manifest_path = Path(manifest_path)

    manifest_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with manifest_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            manifest,
            file,
            indent=2,
        )


def get_file_signature(
    file_path: str | Path,
) -> dict[str, Any]:
    file_path = Path(file_path)

    stat = file_path.stat()

    return {
        "size": stat.st_size,
        "modified_time": stat.st_mtime,
    }


def needs_ingestion(
    file_path: str | Path,
    manifest: dict[str, Any],
) -> bool:
    file_path = Path(file_path)

    key = str(file_path.resolve())

    current_signature = get_file_signature(
        file_path
    )

    previous_signature = manifest.get(key)

    return previous_signature != current_signature