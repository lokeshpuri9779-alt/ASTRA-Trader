from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import hashlib
import json
from pathlib import Path

@dataclass(frozen=True)
class IngestionManifest:
    source: str
    source_file: str
    file_sha256: str
    file_size: int
    retrieved_at: str
    parser_version: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True)

def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def build_ingestion_manifest(
    path: str | Path,
    *,
    source: str,
    parser_version: str,
    retrieved_at: datetime | None = None,
) -> IngestionManifest:
    p = Path(path)
    ts = retrieved_at or datetime.utcnow()
    return IngestionManifest(
        source=source,
        source_file=p.name,
        file_sha256=sha256_file(p),
        file_size=p.stat().st_size,
        retrieved_at=ts.isoformat(timespec="seconds") + "Z",
        parser_version=parser_version,
    )
