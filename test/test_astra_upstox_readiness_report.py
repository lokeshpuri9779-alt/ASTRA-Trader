from astra_trader.execution.upstox_readiness import build_upstox_readiness_report

def test_internal_upstox_readiness_is_complete_without_external_static_ip():
    r=build_upstox_readiness_report()
    assert r.internal_ready
    assert not r.static_ip_config_ready
    assert r.external_setup_required

def test_readiness_accepts_valid_public_static_ips():
    r=build_upstox_readiness_report(primary_static_ip="8.8.8.8",secondary_static_ip="1.1.1.1")
    assert r.internal_ready
    assert r.static_ip_config_ready
    assert not r.external_setup_required
