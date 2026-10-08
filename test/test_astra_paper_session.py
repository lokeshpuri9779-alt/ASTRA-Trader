from datetime import datetime, timedelta, timezone
import json

from astra_trader.models import RiskState, TradeSignal
from astra_trader.paper.session import PaperSession, run_manifest
from astra_trader.replay.fills import MarketSnapshot

NOW=datetime(2026,10,8,10,0,tzinfo=timezone.utc)

def _signal(score=90):
    return TradeSignal("TEST","BUY",100,98,106,score=score,spread_pct=.4)

def _state():
    return RiskState(starting_capital=100000,current_equity=100000)

def test_simulated_fill_and_journal(tmp_path):
    journal=tmp_path/"trades.jsonl"
    results=PaperSession(journal).run([_signal()],{"TEST":MarketSnapshot(99,100,100,5000)},
                                  _state(),observed_at=NOW,quote_times={"TEST":NOW})
    assert results[0].status=="SIMULATED_FILL"
    assert results[0].quantity>0
    assert results[0].price>=100
    assert "SIMULATION_ONLY" in journal.read_text()

def test_stale_quote_rejected(tmp_path):
    results=PaperSession(tmp_path/"journal").run([_signal()],{"TEST":MarketSnapshot(99,100,100,5000)},
                        _state(),observed_at=NOW,quote_times={"TEST":NOW-timedelta(minutes=10)})
    assert results[0].reason=="STALE_OR_FUTURE_QUOTE"

def test_low_score_rejected(tmp_path):
    results=PaperSession(tmp_path/"journal").run([_signal(score=50)],
                        {"TEST":MarketSnapshot(99,100,100,5000)},
                        _state(),observed_at=NOW,quote_times={"TEST":NOW})
    assert results[0].status=="REJECTED"
    assert "threshold" in results[0].reason

def test_missing_quote_rejected(tmp_path):
    results=PaperSession(tmp_path/"journal").run([_signal()],{},_state(),
                                                    observed_at=NOW,quote_times={})
    assert results[0].reason=="MISSING_QUOTE_OR_TIMESTAMP"

def test_empty_manifest_never_invents_trades(tmp_path):
    manifest=tmp_path/"input.json"
    manifest.write_text(json.dumps({"observed_at":NOW.isoformat(),
        "risk_state":{"starting_capital":100000,"current_equity":100000},
        "signals":[],"quotes":{}}))
    assert run_manifest(manifest,tmp_path/"journal.jsonl")==[]
