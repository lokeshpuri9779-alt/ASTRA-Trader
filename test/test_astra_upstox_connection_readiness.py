import os

from astra_trader.execution.upstox_connection import evaluate_upstox_connection_readiness

def test_connection_readiness_blocks_missing_credentials(monkeypatch):
    for key in ("UPSTOX_CLIENT_ID","UPSTOX_CLIENT_SECRET","UPSTOX_REDIRECT_URI"):
        monkeypatch.delenv(key,raising=False)
    r=evaluate_upstox_connection_readiness(primary_static_ip="8.8.8.8")
    assert not r.ready_for_auth
    assert not r.credentials_ready

def test_connection_readiness_accepts_external_setup(monkeypatch):
    monkeypatch.setenv("UPSTOX_CLIENT_ID","x")
    monkeypatch.setenv("UPSTOX_CLIENT_SECRET","y")
    monkeypatch.setenv("UPSTOX_REDIRECT_URI","https://example.com/callback")
    r=evaluate_upstox_connection_readiness(
        primary_static_ip="8.8.8.8",
        secondary_static_ip="1.1.1.1",
    )
    assert r.ready_for_auth
