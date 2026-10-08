import json
from datetime import datetime, timezone
from astra_trader.paper.scheduled import run_cycle

def test_cycle_once_and_duplicate_blocked(tmp_path):
    manifest=tmp_path/"input.json"
    manifest.write_text(json.dumps({
        "mode":"PAPER","cycle_id":"2026-10-08-NSE-001",
        "observed_at":datetime(2026,10,8,tzinfo=timezone.utc).isoformat(),
        "risk_state":{"starting_capital":100000,"current_equity":100000},
        "signals":[],"quotes":{}
    }))
    root=tmp_path/"durable"
    first=run_cycle(manifest,root)
    second=run_cycle(manifest,root)
    assert first["status"]=="COMPLETED"
    assert first["simulated_fills"]==0
    assert second["status"]=="BLOCKED"
    assert len(list((root/"cycles").glob("*.json")))==1

def test_live_manifest_is_refused(tmp_path):
    manifest=tmp_path/"input.json"
    manifest.write_text(json.dumps({"mode":"LIVE","cycle_id":"x"}))
    import pytest
    with pytest.raises(ValueError,match="PAPER"):
        run_cycle(manifest,tmp_path/"durable")
