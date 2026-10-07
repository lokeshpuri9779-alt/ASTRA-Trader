from __future__ import annotations

from dataclasses import dataclass
from ipaddress import ip_address

@dataclass(frozen=True)
class StaticIpValidation:
    ok: bool
    errors: tuple[str,...]

def validate_static_ips(primary: str | None, secondary: str | None = None) -> StaticIpValidation:
    errors: list[str]=[]
    if not primary:
        errors.append("PRIMARY_STATIC_IP_REQUIRED")
    else:
        try:
            p=ip_address(primary)
            if p.is_private or p.is_loopback or p.is_unspecified:
                errors.append("PRIMARY_MUST_BE_PUBLIC")
        except ValueError:
            errors.append("PRIMARY_INVALID_IP")

    if secondary:
        try:
            s=ip_address(secondary)
            if s.is_private or s.is_loopback or s.is_unspecified:
                errors.append("SECONDARY_MUST_BE_PUBLIC")
            if primary and secondary == primary:
                errors.append("SECONDARY_MUST_DIFFER")
        except ValueError:
            errors.append("SECONDARY_INVALID_IP")

    return StaticIpValidation(ok=not errors,errors=tuple(errors))
