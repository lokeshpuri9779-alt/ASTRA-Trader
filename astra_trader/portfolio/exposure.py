from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class Exposure:
    gross: float
    net: float
    by_underlying: dict[str, float]

def aggregate_exposure(positions: list[dict]) -> Exposure:
    gross=0.0; net=0.0; by={}
    for p in positions:
        notional=float(p.get("notional",0.0))
        signed=notional if str(p.get("side","BUY")).upper()=="BUY" else -notional
        gross += abs(signed)
        net += signed
        u=str(p.get("underlying",p.get("symbol","UNKNOWN")))
        by[u]=by.get(u,0.0)+signed
    return Exposure(gross,net,by)
