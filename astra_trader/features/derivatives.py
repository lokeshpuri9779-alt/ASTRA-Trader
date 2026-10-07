from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class DerivativesContext:
    futures_basis_pct: float | None
    put_call_oi_ratio: float | None
    iv_minus_realized: float | None
    skew_25d: float | None

def futures_basis_pct(*, futures_price: float, spot_price: float) -> float | None:
    if spot_price <= 0:
        return None
    return (futures_price/spot_price-1.0)*100

def put_call_oi_ratio(*, put_oi: float, call_oi: float) -> float | None:
    if call_oi <= 0:
        return None
    return put_oi/call_oi
