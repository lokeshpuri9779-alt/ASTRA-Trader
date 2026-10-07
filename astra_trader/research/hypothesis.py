from __future__ import annotations

from dataclasses import dataclass, field

@dataclass(frozen=True)
class Hypothesis:
    hypothesis_id: str
    rationale: str
    market: str
    horizon: str
    parameters: dict
    pass_criteria: dict
    max_trials: int
    tags: tuple[str, ...] = field(default_factory=tuple)
