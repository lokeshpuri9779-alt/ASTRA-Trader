"""Run: python -m astra_trader.paper INPUT.json journal.jsonl"""
from __future__ import annotations
import argparse
import json
from dataclasses import asdict
from astra_trader.paper.session import run_manifest

def main() -> None:
    parser=argparse.ArgumentParser(description="ASTRA offline paper-trading batch; no live orders")
    parser.add_argument("manifest")
    parser.add_argument("journal")
    args=parser.parse_args()
    outcomes=run_manifest(args.manifest,args.journal)
    print(json.dumps({"mode":"PAPER","live_enabled":False,
                      "simulated_fills":sum(o.status=="SIMULATED_FILL" for o in outcomes),
                      "outcomes":[asdict(o) for o in outcomes]},indent=2))
if __name__=="__main__":
    main()
