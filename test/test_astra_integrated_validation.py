from astra_trader.validation.integrated import run_integrated_validation

def test_integrated_paper_shadow_validation_passes_but_live_remains_blocked():
    result = run_integrated_validation()
    assert result.paper_ok
    assert result.shadow_ok
    assert result.reconciliation_ok
    assert result.risk_ok
    assert not result.promotion.allowed
    assert result.promotion.missing == ("BROKER_READY",)

def test_integrated_validation_rejects_excessive_divergence():
    result = run_integrated_validation(shadow_price=101.0, max_divergence_bps=20.0)
    assert not result.risk_ok
    assert "RISK_CHECKS" in result.promotion.missing
