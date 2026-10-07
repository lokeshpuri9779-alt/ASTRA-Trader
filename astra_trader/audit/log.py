from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import json
from pathlib import Path

@dataclass(frozen=True)
class AuditRecord:
    timestamp: str
    category: str
    event_id: str
    payload: dict

class AuditLog:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, *, category: str, event_id: str, payload: dict) -> None:
        record = AuditRecord(
            timestamp=datetime.utcnow().isoformat(timespec="seconds")+"Z",
            category=category,
            event_id=event_id,
            payload=payload,
        )
        with self.path.open("a",encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(record),sort_keys=True)+"\n")
