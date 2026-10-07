import json

from astra_trader.research.ledger import ExperimentLedger, ExperimentResult
from astra_trader.research.manifest import ExperimentManifest

def test_manifest_hash_is_stable():
    kwargs = dict(
        experiment_id="exp-1",
        hypothesis_id="hyp-1",
        strategy_name="demo",
        strategy_version="1",
        code_commit="abc",
        dataset_id="d1",
        dataset_hash="hash",
        start_time="2026-01-01",
        end_time="2026-02-01",
        parameters={"x": 1},
        cost_model={"brokerage": 0},
        slippage_model={"bps": 5},
        seed=42,
    )
    a = ExperimentManifest.create(**kwargs)
    b = ExperimentManifest.create(**kwargs)
    object.__setattr__(b, "created_at", a.created_at)
    assert a.manifest_hash() == b.manifest_hash()

def test_ledger_is_append_only(tmp_path):
    manifest = ExperimentManifest.create(
        experiment_id="exp-1",
        hypothesis_id="hyp-1",
        strategy_name="demo",
        strategy_version="1",
        code_commit="abc",
        dataset_id="d1",
        dataset_hash="hash",
        start_time="2026-01-01",
        end_time="2026-02-01",
        parameters={},
        cost_model={},
        slippage_model={},
        seed=1,
    )
    ledger = ExperimentLedger(tmp_path / "ledger.jsonl")
    ledger.append(manifest, ExperimentResult("exp-1", "COMPLETED", {"net_pnl": 100.0}))
    ledger.append(manifest, ExperimentResult("exp-1-rerun", "FAILED", {}, "example"))
    lines = (tmp_path / "ledger.jsonl").read_text().strip().splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["manifest_hash"] == manifest.manifest_hash()
