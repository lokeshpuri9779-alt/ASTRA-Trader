from __future__ import annotations

from dataclasses import dataclass, field

@dataclass
class QualityReport:
    accepted: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

def quarantine_if_invalid(*, duplicate_count: int = 0, timestamp_errors: int = 0, schema_errors: int = 0) -> QualityReport:
    errors = []
    if duplicate_count:
        errors.append(f"DUPLICATES:{duplicate_count}")
    if timestamp_errors:
        errors.append(f"TIMESTAMP_ERRORS:{timestamp_errors}")
    if schema_errors:
        errors.append(f"SCHEMA_ERRORS:{schema_errors}")
    return QualityReport(accepted=not errors, errors=errors)
