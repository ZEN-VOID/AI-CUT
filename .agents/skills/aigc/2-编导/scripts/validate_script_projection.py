#!/usr/bin/env python3
"""Validate mechanical structure of a 2-编导 episode script.

This checker is intentionally conservative. It verifies structure, field
presence, and nearby audio-visual pairs, but it does not prove creative
faithfulness to the upstream episode source.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SCENE_RE = re.compile(r"^###\s+场景(\d+)：(内景|外景)\s+.+\s+-\s+(日|夜)\s*$")
FIELD_RE = re.compile(r"^([^：\n]+)：")
AUDIO_PAIRS = {
    "对白": "对白画面",
    "独白": "独白画面",
    "内心独白": "内心独白画面",
    "旁白": "旁白画面",
    "音效": "音效画面",
}
VISUAL_FIELDS = {
    "环境描写",
    "角色动作",
    "动作画面",
    "群像画面",
    "表情特写",
    "角色造型",
    "道具特写",
    "系统画面",
    "规则显影",
    "现实灾难画面",
    "对白画面",
    "独白画面",
    "内心独白画面",
    "旁白画面",
    "音效画面",
}
CONCRETE_CHECK_FIELDS = VISUAL_FIELDS | {
    "环境描写",
    "道具特写",
    "表演提示",
}
ABSTRACT_VISUAL_PATTERNS = [
    "规则测试开始",
    "压抑气氛",
    "第二节课是",
    "没有字数限制",
    "他从来不",
    "底牌",
    "幸运还是诅咒",
    "正面摊牌",
    "爽快",
    "小型审判",
    "不做灾害奇观",
    "因为没有人",
    "没有人知道",
    "缺席的代价是什么",
    "现实身份",
    "人数压力",
    "队友候选",
    "等式补完",
]
DESCRIPTIVE_SOUND_PATTERNS = [
    "铃声",
    "一声",
    "声音",
    "读书声",
    "尖叫声",
    "哭声",
    "响起",
    "传来",
    "闷响",
]


def field_base(field: str) -> str:
    return re.sub(r"（.*?）", "", field).strip()


def field_value(line: str) -> str:
    return line.split("：", 1)[1].strip() if "：" in line else ""


def split_scenes(lines: list[str]) -> list[tuple[int, str, list[str]]]:
    scenes: list[tuple[int, str, list[str]]] = []
    current_number: int | None = None
    current_title = ""
    current_lines: list[str] = []
    for line in lines:
        match = SCENE_RE.match(line)
        if match:
            if current_number is not None:
                scenes.append((current_number, current_title, current_lines))
            current_number = int(match.group(1))
            current_title = line
            current_lines = []
            continue
        if current_number is not None:
            current_lines.append(line)
    if current_number is not None:
        scenes.append((current_number, current_title, current_lines))
    return scenes


def validate(path: Path) -> tuple[bool, list[str]]:
    findings: list[str] = []
    if not path.is_file():
        return False, [f"[ERROR] File not found: {path}"]

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    ok = True

    if not text.startswith("---\n"):
        findings.append("[ERROR] Missing YAML frontmatter.")
        ok = False
    for marker in ("source_episode_path:", "adaptation_mode:", "dialogue_lock:", "audio_visual_pairing:"):
        if marker not in text:
            findings.append(f"[ERROR] Missing frontmatter marker: {marker}")
            ok = False
    if "【剧本正文】" not in text:
        findings.append("[ERROR] Missing body marker: 【剧本正文】")
        ok = False

    scenes = split_scenes(lines)
    if not scenes:
        findings.append("[ERROR] No valid scene slugline found.")
        ok = False

    sluglines: dict[str, int] = {}
    for number, title, scene_lines in scenes:
        slug = title.split("：", 1)[1].strip()
        if slug in sluglines and sluglines[slug] != number:
            findings.append(f"[ERROR] Duplicate slugline with different scene number: {slug}")
            ok = False
        sluglines[slug] = number

        fields: list[str] = []
        field_lines: list[tuple[str, str]] = []
        for line in scene_lines:
            match = FIELD_RE.match(line)
            if match:
                field = match.group(1).strip()
                fields.append(field)
                field_lines.append((field, line))
        if not any(field_base(field) in VISUAL_FIELDS for field in fields):
            findings.append(f"[ERROR] Scene {number} has no formal visual field.")
            ok = False

        for field, line in field_lines:
            base = field_base(field)
            value = field_value(line)
            if base in CONCRETE_CHECK_FIELDS:
                for pattern in ABSTRACT_VISUAL_PATTERNS:
                    if pattern in value:
                        findings.append(
                            f"[ERROR] Scene {number} field '{field}' contains abstract/non-visual wording: {pattern}"
                        )
                        ok = False
            if base == "音效":
                for pattern in DESCRIPTIVE_SOUND_PATTERNS:
                    if pattern in value:
                        findings.append(
                            f"[ERROR] Scene {number} sound field '{field}' describes the sound instead of writing sound body: {pattern}"
                        )
                        ok = False
            if base == "镜头语言预设":
                findings.append(
                    f"[ERROR] Scene {number} uses removed field '镜头语言预设'. Use visual/action/performance fields instead."
                )
                ok = False

        for index, field in enumerate(fields):
            base = field_base(field)
            if base not in AUDIO_PAIRS:
                continue
            expected = AUDIO_PAIRS[base]
            nearby = [field_base(item) for item in fields[index + 1 : index + 4]]
            if expected not in nearby:
                findings.append(
                    f"[ERROR] Scene {number} audio field '{field}' lacks nearby '{expected}'."
                )
                ok = False

    if ok:
        findings.append("[OK] Mechanical script projection checks passed.")
    return ok, findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode_script", help="Path to projects/aigc/<项目名>/2-编导/第N集.md")
    args = parser.parse_args()
    ok, findings = validate(Path(args.episode_script))
    for finding in findings:
        print(finding)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
