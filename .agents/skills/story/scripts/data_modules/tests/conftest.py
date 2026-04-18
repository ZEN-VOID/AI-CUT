#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path


def _ensure_story2026_scripts_on_path() -> None:
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))


def bootstrap_project_root(project_root: Path):
    from data_modules.config import DataModulesConfig

    cfg = DataModulesConfig.from_project_root(project_root)
    cfg.ensure_dirs()
    if not cfg.state_file.exists():
        cfg.state_file.write_text(json.dumps({"project_info": {}}, ensure_ascii=False), encoding="utf-8")
    return cfg


_ensure_story2026_scripts_on_path()
