#!/usr/bin/env python3
"""Postprocess grouped-script outputs for `1-Planning/3-分组`.

Current contract:
1) no machine sidecar generation,
2) no agents-plan initialization,
3) report renderer + validator + quantizer are the default exit gate.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from grouping_quantizer import TAIL_HOOK_COMMENT_PREFIX, TAIL_HOOK_LABEL, strip_tail_hook_block

SCRIPT_DIR = Path(__file__).resolve().parent
VALIDATOR = SCRIPT_DIR / "validate_grouping_output.py"
REPORT_RENDERER = SCRIPT_DIR / "render_grouping_report.py"
GROUP_HEADER_RE = re.compile(r"^##\s*【(?P<group_id>\d+-\d+-\d+)】(?:\s+(?P<title>.+))?$")
SCENE_HEADER_RE = re.compile(r"^###\s*场景(?P<label>[^：:]+)\s*[：:]\s*(?P<title>.+?)\s*$")
VOICE_TEXT_RE = re.compile(r"^(对白|独白|内心独白|旁白)(?:（.*?）|\(.*?\))?\s*[：:]\s*(.*)$")
VOICE_VISUAL_RE = re.compile(r"^(对白画面|独白画面|内心独白画面|旁白画面)\s*[：:]\s*(.*)$")
ACTION_VISUAL_RE = re.compile(r"^动作画面\s*[：:]\s*(.*)$")


@dataclass
class GroupBlock:
    group_id: str
    title: str
    body_lines: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="校验 3-分组 grouped script 输出，并通过 quantizer/validator 执行量化门槛。")
    parser.add_argument("--input", required=True, help="输入文件或目录（第N集.md 或 3-分组 目录）")
    parser.add_argument("--include-pattern", default="第*集.md", help="目录模式匹配（默认: 第*集.md）")
    parser.add_argument("--skip-tail-hook", action="store_true", help=f"跳过默认的 `{TAIL_HOOK_LABEL}` 注入。")
    parser.add_argument("--skip-render-report", action="store_true", help="跳过默认的执行报告模板回写。")
    parser.add_argument("--dry-run", action="store_true", help="仅打印即将校验的文件，不执行 validator")
    return parser.parse_args()


def collect_files(input_path: Path, include_pattern: str) -> list[Path]:
    if not input_path.exists():
        raise FileNotFoundError(f"输入路径不存在: {input_path}")
    if input_path.is_file():
        return [input_path]
    files = sorted(path for path in input_path.glob(include_pattern) if path.is_file())
    if files:
        return files
    return sorted(path for path in input_path.glob("*.md") if path.is_file())


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("grouped script 必须以 frontmatter 开头。")
    try:
        _, rest = text.split("---\n", 1)
        block, body = rest.split("\n---\n", 1)
    except ValueError as exc:
        raise ValueError("frontmatter 结束分隔符缺失。") from exc
    return f"---\n{block}\n---\n", body


def split_group_blocks(body: str) -> tuple[list[str], list[GroupBlock]]:
    lines = body.splitlines()
    header_indexes: list[tuple[int, re.Match[str]]] = []
    for index, raw_line in enumerate(lines):
        match = GROUP_HEADER_RE.match(raw_line.strip())
        if match:
            header_indexes.append((index, match))
    if not header_indexes:
        return lines, []

    prefix_lines = lines[: header_indexes[0][0]]
    groups: list[GroupBlock] = []
    for position, (start_index, match) in enumerate(header_indexes):
        end_index = header_indexes[position + 1][0] if position + 1 < len(header_indexes) else len(lines)
        body_lines = lines[start_index + 1 : end_index]
        groups.append(
            GroupBlock(
                group_id=match.group("group_id"),
                title=(match.group("title") or "").strip(),
                body_lines=body_lines,
            )
        )
    return prefix_lines, groups


def strip_tail_hook_lines(body_lines: list[str]) -> list[str]:
    cleaned_text = strip_tail_hook_block("\n".join(body_lines))
    if not cleaned_text:
        return []
    return cleaned_text.splitlines()


def extract_opening_beat(body_lines: list[str]) -> tuple[str | None, list[str]]:
    current_scene: str | None = None
    for index, raw_line in enumerate(body_lines):
        line = raw_line.strip()
        if not line:
            continue
        scene_match = SCENE_HEADER_RE.match(line)
        if scene_match:
            current_scene = f"场景{scene_match.group('label')}：{scene_match.group('title')}"
            continue
        if line.startswith("#"):
            continue
        if ACTION_VISUAL_RE.match(line):
            return current_scene, [line]
        if VOICE_TEXT_RE.match(line):
            beat_lines = [line]
            for next_index in range(index + 1, len(body_lines)):
                next_line = body_lines[next_index].strip()
                if not next_line:
                    continue
                if VOICE_VISUAL_RE.match(next_line):
                    beat_lines.append(next_line)
                break
            return current_scene, beat_lines
        if VOICE_VISUAL_RE.match(line):
            return current_scene, [line]
        return current_scene, [line]
    return current_scene, []


def render_group_block(group: GroupBlock) -> list[str]:
    header = f"## 【{group.group_id}】"
    if group.title:
        header += f" {group.title}"
    return [header, *group.body_lines]


def apply_tail_hook_to_file(path: Path) -> bool:
    original_text = path.read_text(encoding="utf-8")
    frontmatter_block, body = split_frontmatter(original_text)
    prefix_lines, groups = split_group_blocks(body)
    if not groups:
        return False

    normalized_groups = [
        GroupBlock(group_id=group.group_id, title=group.title, body_lines=strip_tail_hook_lines(group.body_lines))
        for group in groups
    ]

    changed = False
    for index, group in enumerate(normalized_groups[:-1]):
        next_group = normalized_groups[index + 1]
        _next_scene, opening_beat = extract_opening_beat(next_group.body_lines)
        if not opening_beat:
            continue
        tail_hook_lines = ["", f"<!-- {TAIL_HOOK_COMMENT_PREFIX} from={next_group.group_id} -->", *opening_beat]
        candidate_lines = group.body_lines + tail_hook_lines
        if candidate_lines != groups[index].body_lines:
            changed = True
        group.body_lines = candidate_lines

    reconstructed_lines = prefix_lines[:]
    for position, group in enumerate(normalized_groups):
        if reconstructed_lines and reconstructed_lines[-1].strip():
            reconstructed_lines.append("")
        reconstructed_lines.extend(render_group_block(group))
        if position < len(normalized_groups) - 1:
            reconstructed_lines.append("")

    new_text = frontmatter_block + "\n".join(reconstructed_lines).rstrip() + "\n"
    if new_text != original_text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return changed


def main() -> int:
    args = parse_args()
    try:
        files = collect_files(Path(args.input), args.include_pattern)
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        return 1

    if not files:
        print("未找到可处理的 markdown 文件。", file=sys.stderr)
        return 1

    for path in files:
        print(f"准备校验 grouped script: {path}")
        if not args.skip_tail_hook:
            print(f"  - 将在校验前应用 `{TAIL_HOOK_LABEL}`")
        if not args.skip_render_report:
            print("  - 将在校验前按模板回写 `执行报告.md`")

    if args.dry_run:
        return 0

    if not args.skip_tail_hook:
        for path in files:
            updated = apply_tail_hook_to_file(path)
            if updated:
                print(f"已写入 `{TAIL_HOOK_LABEL}`: {path}")

    if not args.skip_render_report:
        for path in files:
            command = [sys.executable, str(REPORT_RENDERER), "--input", str(path)]
            result = subprocess.run(command, check=False)
            if result.returncode != 0:
                return result.returncode

    command = [sys.executable, str(VALIDATOR), "--input", args.input, "--include-pattern", args.include_pattern]
    result = subprocess.run(command, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
