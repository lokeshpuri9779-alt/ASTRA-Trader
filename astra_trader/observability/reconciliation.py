from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class ReconciliationStatus:
    matched: bool
    mismatches: tuple[str,...]

def reconcile_positions(local: dict[str,int], external: dict[str,int]) -> ReconciliationStatus:
    keys=set(local)|set(external)
    mismatches=[]
    for k in sorted(keys):
        if local.get(k,0)!=external.get(k,0):
            mismatches.append(k)
    return ReconciliationStatus(not mismatches,tuple(mismatches))
