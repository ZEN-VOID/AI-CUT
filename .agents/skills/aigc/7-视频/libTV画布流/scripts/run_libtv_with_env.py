#!/usr/bin/env python3
"""Load the repository .env, then run an official LibTV CLI script unchanged."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


OFFICIAL_SCRIPT_NAMES = {
    "create_session.py",
    "query_session.py",
    "change_project.py",
    "upload_file.py",
    "download_results.py",
}


def find_repo_root() -> Path:
    candidates = [Path.cwd(), *Path(__file__).resolve().parents]
    for candidate in candidates:
        if (candidate / ".agents/skills/cli/libTV/scripts").is_dir():
            return candidate
    raise SystemExit("错误：无法定位仓库根目录或官方 libTV scripts 目录")


def load_dotenv(dotenv_path: Path, env: dict[str, str]) -> None:
    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key:
            env.setdefault(key, value)


def resolve_official_script(repo_root: Path, script_arg: str) -> Path:
    candidate = Path(script_arg)
    if candidate.name not in OFFICIAL_SCRIPT_NAMES:
        allowed = ", ".join(sorted(OFFICIAL_SCRIPT_NAMES))
        raise SystemExit(f"错误：不允许的 libTV 官方脚本：{script_arg}。允许值：{allowed}")

    scripts_dir = repo_root / ".agents/skills/cli/libTV/scripts"
    if candidate.is_absolute():
        script_path = candidate
    elif candidate.parent == Path("."):
        script_path = scripts_dir / candidate.name
    else:
        script_path = repo_root / candidate

    script_path = script_path.resolve()
    scripts_root = scripts_dir.resolve()
    if scripts_root not in script_path.parents or not script_path.exists():
        raise SystemExit(f"错误：脚本不在官方 libTV scripts 目录内或不存在：{script_arg}")
    return script_path


def main(argv: list[str]) -> int:
    if not argv:
        print(
            "用法：run_libtv_with_env.py <official_script.py> [args...]\n"
            "示例：run_libtv_with_env.py create_session.py \"把全部工作流和结果都放在画布上。...\"",
            file=sys.stderr,
        )
        return 2

    repo_root = find_repo_root()
    env = os.environ.copy()
    load_dotenv(repo_root / ".env", env)

    if not env.get("LIBTV_ACCESS_KEY"):
        print("错误：仓库根 .env 或当前环境中缺少 LIBTV_ACCESS_KEY", file=sys.stderr)
        return 1

    script_path = resolve_official_script(repo_root, argv[0])
    result = subprocess.run(
        [sys.executable, str(script_path), *argv[1:]],
        cwd=str(repo_root),
        env=env,
        check=False,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
