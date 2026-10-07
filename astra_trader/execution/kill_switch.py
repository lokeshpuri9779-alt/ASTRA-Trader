from __future__ import annotations

from dataclasses import dataclass

@dataclass
class KillSwitch:
    engaged: bool = False
    reason: str = ""

    def engage(self, reason: str) -> None:
        self.engaged = True
        self.reason = reason or "UNSPECIFIED"

    def reset(self) -> None:
        self.engaged = False
        self.reason = ""

    def assert_can_submit(self) -> None:
        if self.engaged:
            raise RuntimeError(f"Execution kill switch engaged: {self.reason}")
