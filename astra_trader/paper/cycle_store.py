"""Fail-closed cycle claiming for unattended PAPER-only jobs."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib
import json
import os

@dataclass(frozen=True)
class CycleClaim:
    cycle_id: str
    accepted: bool
    reason: str

def claim_cycle(root: str | Path, cycle_id: str) -> CycleClaim:
    if not cycle_id or len(cycle_id)>200:
        return CycleClaim(cycle_id, False, "INVALID_CYCLE_ID")
    root=Path(root)
    root.mkdir(parents=True,exist_ok=True)
    digest=hashlib.sha256(cycle_id.encode("utf-8")).hexdigest()
    path=root/(digest+".json")
    try:
        fd=os.open(str(path),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    except FileExistsError:
        return CycleClaim(cycle_id,False,"DUPLICATE_OR_PREVIOUSLY_STARTED_CYCLE")
    with os.fdopen(fd,"w",encoding="utf-8") as f:
        json.dump({"cycle_id":cycle_id,"status":"CLAIMED"},f)
        f.flush()
        os.fsync(f.fileno())
    return CycleClaim(cycle_id,True,"CLAIMED")

def record_cycle_result(root: str | Path, cycle_id: str, *, status: str,
                        simulated_fills: int, rejected: int) -> None:
    if status not in {"COMPLETED","FAILED"}:
        raise ValueError("Invalid cycle status")
    path=Path(root)/(hashlib.sha256(cycle_id.encode("utf-8")).hexdigest()+".json")
    if not path.exists():
        raise FileNotFoundError("Cycle must be claimed first")
    tmp=path.with_suffix(".tmp")
    with tmp.open("w",encoding="utf-8") as f:
        json.dump({"cycle_id":cycle_id,"status":status,"simulated_fills":simulated_fills,
                   "rejected":rejected},f,sort_keys=True)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp,path)
