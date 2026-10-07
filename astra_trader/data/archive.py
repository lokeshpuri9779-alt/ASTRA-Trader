from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

def extract_zip_safe(path: str | Path, destination: str | Path) -> list[Path]:
    src = Path(path)
    dest = Path(destination)
    dest.mkdir(parents=True, exist_ok=True)
    extracted: list[Path] = []

    with ZipFile(src) as zf:
        for member in zf.infolist():
            target = (dest / member.filename).resolve()
            if not str(target).startswith(str(dest.resolve())):
                raise ValueError("Unsafe archive path.")
            zf.extract(member, dest)
            if not member.is_dir():
                extracted.append(target)
    return extracted
