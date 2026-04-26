#!/usr/bin/env python3
"""Load project-scoped 5-设计 fallback registry from project CONTEXT/."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REGISTRY_FILENAME = "4-design-fallback-registry.json"


def project_registry_path(project_root: Path | None) -> Path | None:
    if project_root is None:
        return None
    return project_root / "CONTEXT" / REGISTRY_FILENAME


def load_project_design_fallbacks(project_root: Path | None) -> dict[str, Any]:
    path = project_registry_path(project_root)
    if path is None or not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def nested_get(mapping: dict[str, Any] | None, *keys: str, default: Any = None) -> Any:
    current: Any = mapping or {}
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current
