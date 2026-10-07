from datetime import datetime
import pytest

from astra_trader.integrations.indmoney import IndMoneyMarketContext
from astra_trader.integrations.indmoney_market import normalize_market_context
from astra_trader.runtime.environment import RuntimeConfig, RuntimeEnvironment
from astra_trader.runtime.live_guard import assert_live_allowed
from astra_trader.runtime.promotion import PromotionEvidence, evaluate_live_promotion

def test_market_context_normalization():
    rows=[IndMoneyMarketContext("NIFTY",last_price=25000,implied_volatility=14,open_interest=1000,delta=.5)]
    out=normalize_market_context(rows,timestamp=datetime(2026,10,8))
    assert out[0].source=="INDMONEY_READ_ONLY"
    assert out[0].last_price==25000

def test_live_gate_requires_everything():
    e=PromotionEvidence(
        ci_passed=True,
        secret_scan_passed=True,
        dependency_audit_passed=True,
        paper_validation_passed=True,
        shadow_validation_passed=False,
        reconciliation_passed=True,
        risk_checks_passed=True,
        compliance_verified=False,
        external_broker_ready=False,
    )
    d=evaluate_live_promotion(e)
    assert not d.allowed
    cfg=RuntimeConfig(RuntimeEnvironment.LIVE,True)
    with pytest.raises(RuntimeError):
        assert_live_allowed(cfg,d)
