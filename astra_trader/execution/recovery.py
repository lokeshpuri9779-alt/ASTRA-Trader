from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

class RecoveryAction(str, Enum):
    WAIT_FOR_STATUS = "WAIT_FOR_STATUS"
    QUERY_BY_CLIENT_ID = "QUERY_BY_CLIENT_ID"
    BLOCK_NEW_RISK = "BLOCK_NEW_RISK"
    MANUAL_REVIEW = "MANUAL_REVIEW"

@dataclass(frozen=True)
class UnknownSubmissionRecovery:
    actions: tuple[RecoveryAction, ...]

def recovery_plan(*, broker_supports_client_id_query: bool, age_seconds: int) -> UnknownSubmissionRecovery:
    actions: list[RecoveryAction] = [RecoveryAction.BLOCK_NEW_RISK]
    if broker_supports_client_id_query:
        actions.append(RecoveryAction.QUERY_BY_CLIENT_ID)
    elif age_seconds < 30:
        actions.append(RecoveryAction.WAIT_FOR_STATUS)
    else:
        actions.append(RecoveryAction.MANUAL_REVIEW)
    return UnknownSubmissionRecovery(tuple(actions))
