from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import json
from pathlib import Path

@dataclass(frozen=True)
class Incident:
    incident_id: str
    severity: str
    component: str
    message: str
    started_at: str
    resolved_at: str | None = None

class IncidentLedger:
    def __init__(self,path: str | Path):
        self.path=Path(path)
        self.path.parent.mkdir(parents=True,exist_ok=True)

    def append(self,incident: Incident) -> None:
        with self.path.open("a",encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(incident),sort_keys=True)+"\n")
