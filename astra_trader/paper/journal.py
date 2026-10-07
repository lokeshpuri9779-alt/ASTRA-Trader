from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import json
from pathlib import Path

@dataclass(frozen=True)
class JournalEntry:
    timestamp: str
    category: str
    message: str
    metadata: dict

class PaperJournal:
    def __init__(self,path: str | Path):
        self.path=Path(path)
        self.path.parent.mkdir(parents=True,exist_ok=True)

    def append(self, category: str, message: str, metadata: dict | None=None) -> None:
        entry=JournalEntry(
            timestamp=datetime.utcnow().isoformat(timespec="seconds")+"Z",
            category=category,
            message=message,
            metadata=metadata or {},
        )
        with self.path.open("a",encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(entry),sort_keys=True)+"\n")
