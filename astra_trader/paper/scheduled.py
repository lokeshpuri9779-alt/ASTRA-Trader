"""One cycle of unattended PAPER trading; callable by an external scheduler.

Requires a real pre-collected manifest and a persistent writable directory.
No network access or live-broker execution.
"""
from __future__ import annotations

from dataclasses import asdict
import argparse
import json
from pathlib import Path

from astra_trader.paper.cycle_store import claim_cycle, record_cycle_result
from astra_trader.paper.session import run_manifest

def run_cycle(manifest: str | Path, state_dir: str | Path) -> dict:
    manifest=Path(manifest)
    root=Path(state_dir)
    payload=json.loads(manifest.read_text(encoding="utf-8"))
    if payload.get("mode") != "PAPER":
        raise ValueError("Manifest must explicitly specify PAPER mode")
    cycle_id=payload.get("cycle_id")
    if not isinstance(cycle_id,str):
        raise ValueError("Missing cycle_id")
    claim=claim_cycle(root/"cycles",cycle_id)
    if not claim.accepted:
        return {"cycle_id":cycle_id,"mode":"PAPER","status":"BLOCKED","reason":claim.reason,
                "simulated_fills":0}
    journal=root/"paper-journal.jsonl"
    try:
        result=run_manifest(manifest,journal)
        fills=sum(x.status=="SIMULATED_FILL" for x in result)
        rejects=sum(x.status=="REJECTED" for x in result)
        record_cycle_result(root/"cycles",cycle_id,status="COMPLETED",
                            simulated_fills=fills,rejected=rejects)
        return {"cycle_id":cycle_id,"mode":"PAPER","status":"COMPLETED",
                "simulated_fills":fills,"rejected":rejects,
                "evaluated_signals":len(result)}
    except Exception:
        record_cycle_result(root/"cycles",cycle_id,status="FAILED",simulated_fills=0,rejected=0)
        raise

def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("manifest")
    parser.add_argument("state_dir")
    args=parser.parse_args()
    print(json.dumps(run_cycle(args.manifest,args.state_dir),sort_keys=True))

if __name__=="__main__":
    main()
