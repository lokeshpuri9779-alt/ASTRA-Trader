from __future__ import annotations

from dataclasses import asdict, dataclass

@dataclass(frozen=True)
class CandidateDossier:
    hypothesis_id: str
    strategy_name: str
    trial_count: int
    oos_metrics: dict
    robustness: dict
    known_failure_modes: tuple[str,...]
    data_manifest_hash: str
    code_commit: str

    def to_dict(self) -> dict:
        return asdict(self)
