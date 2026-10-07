from __future__ import annotations

from datetime import datetime, timedelta

def data_is_stale(*, event_time: datetime, now: datetime, max_age: timedelta) -> bool:
    return now - event_time > max_age
