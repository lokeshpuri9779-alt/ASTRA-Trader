from __future__ import annotations

def iv_minus_realized(*, implied_vol: float, realized_vol: float) -> float:
    return implied_vol-realized_vol

def term_structure(front_iv: float, back_iv: float) -> float:
    return back_iv-front_iv

def skew_difference(put_iv: float, call_iv: float) -> float:
    return put_iv-call_iv
