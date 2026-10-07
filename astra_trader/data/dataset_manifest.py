from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json

@dataclass(frozen=True)
class DatasetManifest:
    dataset_id: str
    source_files: tuple[str, ...]
    source_hashes: tuple[str, ...]
    parser_versions: tuple[str, ...]
    start_time: str
    end_time: str
    instrument_master_version: str

    def digest(self) -> str:
        raw = json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()
