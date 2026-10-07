from __future__ import annotations

from dataclasses import dataclass, field

@dataclass(frozen=True)
class ShadowIntent:
    symbol: str
    side: str
    quantity: int
    reference_price: float
    metadata: dict = field(default_factory=dict)

class ShadowGateway:
    """Records hypothetical orders but never transmits them externally."""

    def __init__(self):
        self.intents: list[ShadowIntent] = []

    def submit(self, intent: ShadowIntent) -> None:
        self.intents.append(intent)
