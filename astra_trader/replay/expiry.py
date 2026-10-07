from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class OptionSettlement:
    intrinsic_value: float
    cashflow_per_unit: float
    expires_worthless: bool

def settle_option(*, option_type: str, strike: float, settlement_underlying: float) -> OptionSettlement:
    kind = option_type.upper()
    if kind == "CE":
        intrinsic = max(0.0, settlement_underlying - strike)
    elif kind == "PE":
        intrinsic = max(0.0, strike - settlement_underlying)
    else:
        raise ValueError("option_type must be CE or PE")
    return OptionSettlement(
        intrinsic_value=intrinsic,
        cashflow_per_unit=intrinsic,
        expires_worthless=intrinsic == 0.0,
    )
