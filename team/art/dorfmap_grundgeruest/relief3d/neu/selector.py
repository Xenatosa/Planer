"""Small environment selector shared by the legacy entry points and tests."""
from __future__ import annotations

import os
from collections.abc import Mapping


def new_pipeline_enabled(env: Mapping[str, str] | None = None) -> bool:
    values = os.environ if env is None else env
    return values.get("RELIEF_NEU") == "1"
