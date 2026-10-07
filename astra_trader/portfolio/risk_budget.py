from __future__ import annotations

def normalize_strategy_budgets(raw: dict[str,float]) -> dict[str,float]:
    cleaned={k:max(0.0,float(v)) for k,v in raw.items()}
    total=sum(cleaned.values())
    if total<=0:
        return {k:0.0 for k in cleaned}
    return {k:v/total for k,v in cleaned.items()}
