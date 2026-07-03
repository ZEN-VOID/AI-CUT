#!/usr/bin/env python3
"""Forward github-push version updates to the version-sync skill."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def git_root(start: Path) -> Path:
    try:
        output = subprocess.check_output(
            ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return start.resolve()
    return Path(output.strip()).resolve()


def main() -> int:
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    root = git_root(Path(project_dir) if project_dir else Path.cwd())
    script = root / ".agents" / "skills" / "version-sync" / "scripts" / "sync_version.py"
    if not script.exists():
        print(f"VERSION.md 版本同步失败：找不到 {script}", file=sys.stderr)
        return 1
    os.execv(sys.executable, [sys.executable, str(script), *sys.argv[1:]])
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
