from __future__ import annotations

from pathlib import Path
import shutil

def backup_file(source: str | Path, destination_dir: str | Path) -> Path:
    src=Path(source)
    dest=Path(destination_dir)
    dest.mkdir(parents=True,exist_ok=True)
    target=dest/src.name
    shutil.copy2(src,target)
    return target

def restore_file(backup: str | Path, destination: str | Path) -> Path:
    src=Path(backup)
    dest=Path(destination)
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src,dest)
    return dest
