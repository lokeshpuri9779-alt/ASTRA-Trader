"""Explicit-signal paper trading engine: offline, deterministic, no broker IO."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path

from astra_trader.models import RiskState, TradeSignal
from astra_trader.risk import RiskEngine
from astra_trader.replay.fills import FillModel, MarketSnapshot, Side
from astra_trader.paper.journal import PaperJournal

@dataclass(frozen=True)
class PaperOutcome:
    symbol: str
    status: str
    reason: str
    quantity: int = 0
    price: float | None = None

class PaperSession:
    """One cycle; only explicit signals, verified quotes and deterministic risk.

    No fabricated signals or market data; never connects to a live broker.
    """
    def __init__(self, journal_path: str | Path, *, fill_model: FillModel | None = None):
        self.journal=PaperJournal(journal_path)
        self.risk=RiskEngine()
        self.fill_model=fill_model or FillModel(slippage_bps=5)

    def run(self, signals: list[TradeSignal], quotes: dict[str, MarketSnapshot],
            state: RiskState, *, observed_at: datetime,
            max_quote_age_seconds: float = 120,
            quote_times: dict[str, datetime] | None = None) -> list[PaperOutcome]:
        if observed_at.tzinfo is None:
            raise ValueError("observed_at must be timezone-aware")
        results=[]
        for signal in signals:
            snap=quotes.get(signal.symbol)
            ts=(quote_times or {}).get(signal.symbol)
            failure=None
            if snap is None or ts is None:
                failure="MISSING_QUOTE_OR_TIMESTAMP"
            elif ts.tzinfo is None:
                failure="QUOTE_TIMESTAMP_NOT_TIMEZONE_AWARE"
            else:
                age=(observed_at-ts).total_seconds()
                if age < -5 or age > max_quote_age_seconds:
                    failure="STALE_OR_FUTURE_QUOTE"
            if failure:
                outcome=PaperOutcome(signal.symbol,"REJECTED",failure)
            elif signal.side.upper() not in {"BUY","SELL"}:
                outcome=PaperOutcome(signal.symbol,"REJECTED","INVALID_SIDE")
            else:
                reference = snap.ask if signal.side.upper() == "BUY" else snap.bid
                if reference is None or reference <= 0:
                    failure = "NO_EXECUTABLE_BID_ASK"
                elif signal.entry <= 0 or abs(reference-signal.entry)/signal.entry > .02:
                    failure = "SIGNAL_PRICE_QUOTE_MISMATCH"
                if failure:
                    outcome=PaperOutcome(signal.symbol,"REJECTED",failure)
                    self.journal.append("PAPER_DECISION",f"{outcome.symbol}: {outcome.status}",{
                        "reason":outcome.reason,"quantity":0,"price":None,
                        "execution":"SIMULATION_ONLY","observed_at":observed_at.isoformat()})
                    results.append(outcome)
                    continue
                decision=self.risk.evaluate(signal,state)
                if not decision.allowed:
                    outcome=PaperOutcome(signal.symbol,"REJECTED",decision.reason)
                else:
                    side=Side(signal.side.upper())
                    fill=self.fill_model.market_fill(side=side,quantity=decision.quantity,snapshot=snap)
                    if not fill:
                        outcome=PaperOutcome(signal.symbol,"NO_FILL","INSUFFICIENT_QUOTE_OR_VOLUME")
                    else:
                        outcome=PaperOutcome(signal.symbol,"SIMULATED_FILL",
                            "PARTIAL" if fill.partial else "FILLED",fill.quantity,fill.price)
                        state.open_risk += fill.quantity * abs(fill.price - signal.stop)
                        state.current_equity -= fill.quantity * fill.price
            self.journal.append("PAPER_DECISION",f"{outcome.symbol}: {outcome.status}",{
                "reason":outcome.reason,"quantity":outcome.quantity,"price":outcome.price,
                "execution":"SIMULATION_ONLY","observed_at":observed_at.isoformat()})
            results.append(outcome)
        return results

def run_manifest(manifest_path: str | Path, journal_path: str | Path) -> list[PaperOutcome]:
    """Run one offline batch; file must supply signals, quote timestamp and risk capital.

    An absent signal is an empty session, never a synthetic trade.
    """
    payload=json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    observed=datetime.fromisoformat(payload["observed_at"])
    state=RiskState(**payload["risk_state"])
    signals=[TradeSignal(**x) for x in payload.get("signals",[])]
    quotes={k:MarketSnapshot(**v["market"]) for k,v in payload.get("quotes",{}).items()}
    times={k:datetime.fromisoformat(v["timestamp"]) for k,v in payload.get("quotes",{}).items()}
    return PaperSession(journal_path).run(signals,quotes,state,observed_at=observed,quote_times=times)
