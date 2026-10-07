from dataclasses import dataclass

@dataclass(frozen=True)
class Scenario:
    name: str
    spot_shock_pct: float = 0.0
    vol_shock_points: float = 0.0

@dataclass(frozen=True)
class ScenarioResult:
    name: str
    pnl: float

def linear_delta_stress(*, position_delta_rupees: float, scenario: Scenario) -> ScenarioResult:
    pnl = position_delta_rupees * (scenario.spot_shock_pct / 100.0)
    return ScenarioResult(scenario.name, pnl)
