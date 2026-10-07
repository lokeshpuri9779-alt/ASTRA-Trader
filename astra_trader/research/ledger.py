from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path

from .manifest import ExperimentManifest

@dataclass(frozen=True)
class ExperimentResult:
    experiment_id: str
    status: str
    metrics: dict
    failure_reason: str | None = None

class ExperimentLedger:
    """Append-only JSONL experiment ledger."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, manifest: ExperimentManifest, result: ExperimentResult) -> None:
        record = {
            "manifest": asdict(manifest),
            "manifest_hash": manifest.manifest_hash(),
            "result": asdict(result),
        }
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, sort_keys=True) + "\n")
