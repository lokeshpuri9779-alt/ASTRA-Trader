from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class ExposureCaps:
    max_underlying_fraction: float = 0.35
    max_sector_fraction: float = 0.30
    max_cluster_fraction: float = 0.50

@dataclass(frozen=True)
class ExposureCheck:
    allowed: bool
    reason: str

def check_exposure_caps(
    *,
    total_equity: float,
    proposed_underlying_exposure: float,
    proposed_sector_exposure: float,
    proposed_cluster_exposure: float,
    caps: ExposureCaps,
) -> ExposureCheck:
    if total_equity <= 0:
        return ExposureCheck(False, "INVALID_EQUITY")
    if abs(proposed_underlying_exposure) > total_equity * caps.max_underlying_fraction:
        return ExposureCheck(False, "UNDERLYING_CAP")
    if abs(proposed_sector_exposure) > total_equity * caps.max_sector_fraction:
        return ExposureCheck(False, "SECTOR_CAP")
    if abs(proposed_cluster_exposure) > total_equity * caps.max_cluster_fraction:
        return ExposureCheck(False, "CORRELATION_CLUSTER_CAP")
    return ExposureCheck(True, "OK")
