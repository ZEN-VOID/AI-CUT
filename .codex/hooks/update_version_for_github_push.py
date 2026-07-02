#!/usr/bin/env python3
"""Update VERSION.md for github-push runs."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


HISTORY_START = "<!-- version-hook:history:start -->"
HISTORY_END = "<!-- version-hook:history:end -->"

CURRENT_VERSION_RE = re.compile(r"(?m)^(当前版本[：:]\s*)`?(V\d+(?:\.\d+){1,2})`?(\s*)$")
LAST_UPDATED_RE = re.compile(r"(?m)^(最后更新[：:]\s*).*$")
VERSION_RE = re.compile(r"^V(?P<major>\d+)\.(?P<minor>\d+)(?:\.(?P<patch>\d+))?$")

LEVEL_ALIASES = {
    "none": "none",
    "baseline": "none",
    "no-bump": "none",
    "nobump": "none",
    "不升级": "none",
    "不递增": "none",
    "small": "small",
    "patch": "small",
    "小": "small",
    "小更新": "small",
    "medium": "medium",
    "minor": "medium",
    "中": "medium",
    "中更新": "medium",
    "large": "large",
    "major": "large",
    "大": "large",
    "大更新": "large",
}

LEVEL_LABELS = {
    "none": "不升级",
    "small": "小更新",
    "medium": "中更新",
    "large": "大更新",
}


def read_hook_input() -> dict[str, Any]:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def hook_response(message: str | None = None, *, suppress: bool = True) -> None:
    payload: dict[str, Any] = {"continue": True, "suppressOutput": suppress}
    if message:
        payload["systemMessage"] = message
    print(json.dumps(payload, ensure_ascii=False))


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


def resolve_root(args: argparse.Namespace, hook_input: dict[str, Any]) -> Path:
    if args.root:
        return Path(args.root).resolve()
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_dir:
        return git_root(Path(project_dir))
    hook_cwd = hook_input.get("cwd")
    if isinstance(hook_cwd, str) and hook_cwd:
        return git_root(Path(hook_cwd))
    return git_root(Path.cwd())


def prompt_requests_github_push(prompt: str) -> bool:
    if not prompt:
        return False
    direct_markers = ("[$github-push]", "$github-push", "/github-push")
    if any(marker in prompt for marker in direct_markers):
        return True
    if re.search(r"(^|[\s`])github-push([\s`]|$)", prompt):
        return bool(re.search(r"执行|运行|调用|启用|提交|推送|同步|commit|push", prompt, re.IGNORECASE))
    return False


def normalize_level(raw_level: str | None) -> str:
    if not raw_level:
        return "small"
    normalized = raw_level.strip().lower()
    return LEVEL_ALIASES.get(normalized, normalized if normalized in LEVEL_LABELS else "small")


def level_from_prompt(prompt: str) -> str | None:
    if not prompt:
        return None
    pattern = re.compile(
        r"(?:VERSION_BUMP_LEVEL|version[-_ ]?bump|版本(?:更新)?级别|升级级别)\s*[:=：]\s*"
        r"(none|baseline|no-bump|small|patch|medium|minor|large|major|不升级|小更新|中更新|大更新|小|中|大)",
        re.IGNORECASE,
    )
    match = pattern.search(prompt)
    if match:
        return normalize_level(match.group(1))
    return None


def choose_level(args: argparse.Namespace, hook_input: dict[str, Any]) -> str:
    prompt = hook_input.get("user_prompt") if isinstance(hook_input.get("user_prompt"), str) else ""
    raw_level = args.level or os.environ.get("VERSION_BUMP_LEVEL") or os.environ.get("GITHUB_PUSH_VERSION_BUMP")
    return normalize_level(raw_level or level_from_prompt(prompt))


def parse_version(version: str) -> tuple[int, int, int]:
    match = VERSION_RE.match(version.strip())
    if not match:
        raise ValueError(f"Unsupported version: {version}")
    major = int(match.group("major"))
    minor = int(match.group("minor"))
    patch = int(match.group("patch") or 0)
    return major, minor, patch


def format_version(parts: tuple[int, int, int]) -> str:
    major, minor, patch = parts
    if patch == 0:
        return f"V{major}.{minor}"
    return f"V{major}.{minor}.{patch}"


def bump_version(current: str, level: str) -> str:
    major, minor, patch = parse_version(current)
    if level == "none":
        return format_version((major, minor, patch))
    if level == "small":
        return format_version((major, minor, patch + 1))
    if level == "medium":
        return format_version((major, minor + 1, 0))
    if level == "large":
        return format_version((major + 1, 0, 0))
    raise ValueError(f"Unsupported bump level: {level}")


def current_version_from(text: str) -> str:
    match = CURRENT_VERSION_RE.search(text)
    if match:
        return match.group(2)
    match = re.search(r"V\d+\.\d+(?:\.\d+)?", text)
    if match:
        return match.group(0)
    raise ValueError("VERSION.md does not contain a supported current version line")


def changed_scope(root: Path) -> str:
    try:
        output = subprocess.check_output(
            ["git", "-C", str(root), "status", "--porcelain=v1", "-z"],
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "repository sync"
    paths = [item[3:].decode("utf-8", "replace") for item in output.split(b"\0") if len(item) > 3]
    if not paths:
        return "repository sync"
    if any(path.startswith(".agents/skills/workflow/") for path in paths):
        return "workflow skill update"
    if any(path.startswith(".codex/hooks/") for path in paths):
        return "codex hook update"
    return "repository update"


def update_text(text: str, old_version: str, new_version: str, level: str, timestamp: str, scope: str) -> str:
    def replace_current(match: re.Match[str]) -> str:
        return f"{match.group(1)}`{new_version}`{match.group(3)}"

    updated, count = CURRENT_VERSION_RE.subn(replace_current, text, count=1)
    if count == 0:
        updated = f"当前版本：`{new_version}`\n" + updated

    if LAST_UPDATED_RE.search(updated):
        updated = LAST_UPDATED_RE.sub(f"最后更新：{timestamp}", updated, count=1)
    else:
        updated = updated.replace(f"当前版本：`{new_version}`", f"当前版本：`{new_version}`\n最后更新：{timestamp}", 1)

    if old_version == new_version:
        entry = f"- {timestamp}：`{old_version}`（{LEVEL_LABELS[level]}；github-push 自动更新；scope: {scope}）。"
    else:
        entry = (
            f"- {timestamp}：`{old_version}` -> `{new_version}`"
            f"（{LEVEL_LABELS[level]}；github-push 自动更新；scope: {scope}）。"
        )

    if HISTORY_START in updated and HISTORY_END in updated:
        start_index = updated.index(HISTORY_START) + len(HISTORY_START)
        updated = updated[:start_index] + "\n" + entry + updated[start_index:]
    else:
        updated = updated.rstrip() + f"\n\n## 版本记录\n\n{HISTORY_START}\n{entry}\n{HISTORY_END}\n"

    return updated


def update_version_file(root: Path, level: str, *, dry_run: bool) -> tuple[str, str, Path]:
    version_path = root / "VERSION.md"
    if not version_path.exists():
        raise FileNotFoundError(f"VERSION.md not found: {version_path}")
    text = version_path.read_text(encoding="utf-8")
    old_version = current_version_from(text)
    new_version = bump_version(old_version, level)
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    new_text = update_text(text, old_version, new_version, level, timestamp, changed_scope(root))
    if not dry_run:
        version_path.write_text(new_text, encoding="utf-8")
    return old_version, new_version, version_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Update VERSION.md before github-push.")
    parser.add_argument("--hook", action="store_true", help="Read hook JSON from stdin and skip unless github-push is requested.")
    parser.add_argument("--force", action="store_true", help="Update VERSION.md regardless of hook prompt matching.")
    parser.add_argument("--dry-run", action="store_true", help="Compute the update without writing VERSION.md.")
    parser.add_argument("--level", choices=sorted(LEVEL_LABELS), help="Version bump level.")
    parser.add_argument("--root", help="Repository root. Defaults to CLAUDE_PROJECT_DIR, hook cwd, or git root.")
    args = parser.parse_args()

    hook_input = read_hook_input() if args.hook else {}
    prompt = hook_input.get("user_prompt") if isinstance(hook_input.get("user_prompt"), str) else ""

    if args.hook and not args.force and not prompt_requests_github_push(prompt):
        hook_response()
        return 0

    try:
        root = resolve_root(args, hook_input)
        level = choose_level(args, hook_input)
        old_version, new_version, version_path = update_version_file(root, level, dry_run=args.dry_run)
    except Exception as exc:  # noqa: BLE001 - hooks should report structured failure context.
        message = f"VERSION.md 自动更新失败：{exc}"
        if args.hook:
            hook_response(message, suppress=False)
            return 0
        print(message, file=sys.stderr)
        return 1

    message = f"VERSION.md 自动更新：{old_version} -> {new_version} ({LEVEL_LABELS[level]})"
    if args.dry_run:
        message += " [dry-run]"
    if args.hook:
        hook_response(message, suppress=False)
    else:
        print(f"{version_path}: {message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
