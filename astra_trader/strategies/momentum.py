from __future__ import annotations

def relative_strength_rank(returns_by_symbol: dict[str,float]) -> list[tuple[str,float]]:
    return sorted(returns_by_symbol.items(),key=lambda x:x[1],reverse=True)
