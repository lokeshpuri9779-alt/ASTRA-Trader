from __future__ import annotations

from dataclasses import dataclass
import os

@dataclass(frozen=True)
class ReleaseStamp:
    commit_sha: str
    release_tag: str
    build_id: str

def current_release_stamp() -> ReleaseStamp:
    return ReleaseStamp(
        commit_sha=os.getenv("ASTRA_COMMIT_SHA","UNKNOWN"),
        release_tag=os.getenv("ASTRA_RELEASE_TAG","UNRELEASED"),
        build_id=os.getenv("ASTRA_BUILD_ID","LOCAL"),
    )
