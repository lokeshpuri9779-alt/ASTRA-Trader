from __future__ import annotations

from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Iterable, Any

class ParquetStore:
    """Small adapter around pandas/pyarrow parquet persistence."""

    def write(self, records: Iterable[Any], path: str | Path) -> Path:
        import pandas as pd

        rows = []
        for record in records:
            rows.append(asdict(record) if is_dataclass(record) else dict(record))
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(rows).to_parquet(out, index=False)
        return out

    def read(self, path: str | Path):
        import pandas as pd
        return pd.read_parquet(path)
