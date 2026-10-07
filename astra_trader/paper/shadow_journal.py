from __future__ import annotations

from astra_trader.paper.journal import PaperJournal
from astra_trader.paper.shadow_runtime import ShadowRunResult

def journal_shadow_run(journal: PaperJournal, result: ShadowRunResult) -> None:
    for item in result.assessments:
        journal.append(
            "SHADOW_ASSESSMENT",
            f"{item.symbol}: {item.action}",
            {
                "reference_price": item.reference_price,
                "reason": item.reason,
                "execution": "NONE",
            },
        )
