from pathlib import Path

from astra_trader.integrations.indmoney import IndMoneyAdapter, IndMoneyPosition
from astra_trader.integrations.indmoney_normalize import normalize_positions
from astra_trader.regime.hmm_challenger import cluster_regime_features
from astra_trader.runtime.backup import backup_file, restore_file
from astra_trader.runtime.environment import RuntimeConfig, RuntimeEnvironment
from astra_trader.security.redaction import redact_sensitive

class FakeClient:
    def positions(self):
        return [IndMoneyPosition("NIFTY",2,100,110)]
    def market_context(self,symbols):
        return []

def test_indmoney_read_only_adapter():
    a=IndMoneyAdapter(FakeClient())
    p=a.fetch_positions()
    assert len(p)==1
    state=normalize_positions(p,cash=1000)
    assert state.gross_exposure==220

def test_redaction():
    x=redact_sensitive("api_key=abc password=secret")
    assert "abc" not in x and "secret" not in x

def test_live_flag_defaults_off(monkeypatch):
    monkeypatch.delenv("ASTRA_LIVE_ENABLED",raising=False)
    monkeypatch.setenv("ASTRA_ENV","PAPER")
    c=RuntimeConfig.from_env()
    assert c.environment is RuntimeEnvironment.PAPER
    assert not c.live_enabled

def test_backup_restore(tmp_path: Path):
    a=tmp_path/"a.txt"; a.write_text("ok")
    b=backup_file(a,tmp_path/"bak")
    out=restore_file(b,tmp_path/"restored.txt")
    assert out.read_text()=="ok"

def test_regime_challenger():
    labels=cluster_regime_features([(1,.1),(1.1,.2),(-1,2),(-1.1,2.1)],k=2)
    assert len(labels)==4
