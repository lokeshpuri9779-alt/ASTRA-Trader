from __future__ import annotations

def daily_health_report(metrics: dict) -> dict:
    keys=(
        "uptime_pct","data_gaps","reconciliation_mismatches",
        "order_rejections","slippage_bps","drawdown_pct",
        "risk_events","auto_disable_events","unresolved_incidents",
    )
    return {k:metrics.get(k,0) for k in keys}
