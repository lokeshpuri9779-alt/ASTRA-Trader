from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class Alert:
    severity: str
    title: str
    message: str

def drawdown_alert(drawdown_pct: float, threshold_pct: float=5.0) -> Alert | None:
    if abs(drawdown_pct) < threshold_pct:
        return None
    return Alert("HIGH","Paper drawdown threshold breached",f"Drawdown {drawdown_pct:.2f}% exceeds {threshold_pct:.2f}%")
