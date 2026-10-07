from __future__ import annotations

def volatility_adjusted_size(*, base_risk_rupees: float, stop_distance: float, volatility_scale: float = 1.0) -> int:
    if base_risk_rupees <= 0 or stop_distance <= 0 or volatility_scale <= 0:
        return 0
    effective_risk=base_risk_rupees/volatility_scale
    return max(0,int(effective_risk//stop_distance))

def inverse_vol_weights(volatilities: dict[str,float]) -> dict[str,float]:
    inv={k:(1/v if v>0 else 0.0) for k,v in volatilities.items()}
    total=sum(inv.values())
    return {k:(v/total if total>0 else 0.0) for k,v in inv.items()}
