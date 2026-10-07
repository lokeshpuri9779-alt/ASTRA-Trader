from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import json

@dataclass(frozen=True)
class ExperimentManifest:
    experiment_id: str
    hypothesis_id: str
    strategy_name: str
    strategy_version: str
    code_commit: str
    dataset_id: str
    dataset_hash: str
    start_time: str
    end_time: str
    parameters: dict
    cost_model: dict
    slippage_model: dict
    seed: int
    created_at: str

    def canonical_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))

    def manifest_hash(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()

    @classmethod
    def create(
        cls,
        *,
        experiment_id: str,
        hypothesis_id: str,
        strategy_name: str,
        strategy_version: str,
        code_commit: str,
        dataset_id: str,
        dataset_hash: str,
        start_time: str,
        end_time: str,
        parameters: dict,
        cost_model: dict,
        slippage_model: dict,
        seed: int,
    ) -> "ExperimentManifest":
        return cls(
            experiment_id=experiment_id,
            hypothesis_id=hypothesis_id,
            strategy_name=strategy_name,
            strategy_version=strategy_version,
            code_commit=code_commit,
            dataset_id=dataset_id,
            dataset_hash=dataset_hash,
            start_time=start_time,
            end_time=end_time,
            parameters=parameters,
            cost_model=cost_model,
            slippage_model=slippage_model,
            seed=seed,
            created_at=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        )
