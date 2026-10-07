from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from astra_trader.replay.accounting import AccountLedger

def save_paper_portfolio(ledger: AccountLedger, path: str | Path) -> Path:
    out=Path(path)
    out.parent.mkdir(parents=True,exist_ok=True)
    payload={
        "cash":ledger.cash,
        "realized_pnl":ledger.realized_pnl,
        "fees":ledger.fees,
        "positions":ledger.positions,
        "average_prices":ledger.average_prices,
    }
    out.write_text(json.dumps(payload,sort_keys=True),encoding="utf-8")
    return out

def load_paper_portfolio(path: str | Path) -> AccountLedger:
    raw=json.loads(Path(path).read_text(encoding="utf-8"))
    return AccountLedger(
        cash=float(raw["cash"]),
        realized_pnl=float(raw.get("realized_pnl",0.0)),
        fees=float(raw.get("fees",0.0)),
        positions={k:int(v) for k,v in raw.get("positions",{}).items()},
        average_prices={k:float(v) for k,v in raw.get("average_prices",{}).items()},
    )
