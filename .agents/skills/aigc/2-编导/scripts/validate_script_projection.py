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
    "场面调度",
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
    "心理反应",
    "表演提示",
}
PLACEHOLDER_LEAK_PATTERNS = [
    "本场按上游原文顺序承接",
    "不新增事件结果",
    "说话者的视线",
    "手部动作、身体距离",
    "对手反应就近承托对白",
    "引号内不加入动作",
    "普通人、追兵、女卫、船工或村民",
    "<可见空间",
    "<说话时的表演",
    "<逐字保真的上游对白",
]
DIALOGUE_PLACEHOLDER_ROLES = {
    "原文角色",
    "角色",
    "角色名",
    "某人",
    "说话者",
    "[原文角色]",
}
DIALOGUE_FIELD_RE = re.compile(r"^对白（([^，）]+)，([^）]+)）$")
ENVIRONMENT_ACTION_PATTERNS = [
    "小声说",
    "低声说",
    "沉声",
    "说：",
    "吐出日语",
    "咬了一口",
    "咬下",
    "凑到",
    "攥住",
    "握住",
    "别过头",
    "别过脸",
    "指尖叩",
    "收进了袖中",
    "灌一口酒",
    "望着他",
]
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
    "权力关系",
    "掌控全场",
    "不信任",
    "试探",
    "潜台词",
    "他意识到",
    "她意识到",
    "他们意识到",
    "意识到自己",
    "他觉得",
    "她觉得",
    "他们觉得",
    "他明白",
    "她明白",
    "众人都明白",
    "这象征",
    "这预示",
    "这说明",
    "命运的阴影",
    "关系发生改变",
    "信任发生变化",
    "内心崩塌",
    "内心深处",
    "心里明白",
    "心里觉得",
    "心里像",
    "感到恶心",
    "感到难受",
    "感到愤怒",
    "感到害怕",
    "感到崩溃",
    "她是在试探",
    "他是在试探",
    "对方在撒谎",
    "早有准备",
    "早已熟悉",
    "早已习惯",
    "每天都",
    "每次都",
    "一直以来",
    "往日",
    "无数次",
    "灵魂",
    "无边黑暗",
    "证明了他",
    "证明了她",
    "本场按上游原文顺序承接",
    "说话者的视线",
]
SUBJECTIVE_INTENT_PATTERNS = [
    "试图",
    "想要",
    "打算",
    "意图",
    "准备借此",
    "想借此",
    "为了掩饰",
    "为了让",
]
UNRELATED_BACKSTORY_PATTERNS = [
    "多年前",
    "从小",
    "小时候",
    "过去曾",
    "当年",
    "来历",
    "祖传",
    "旧事",
]
CINEMATOGRAPHY_OVERREACH_PATTERNS = [
    "分镜明细预设",
    "机位",
    "景别",
    "推镜",
    "拉镜",
    "摇镜",
    "移镜",
    "跟拍",
    "特写镜头",
    "中景",
    "全景",
    "分镜",
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
SUMMARY_ONLY_FIELDS = {"表演提示", "场面调度"}


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
        if fields and field_base(fields[-1]) in SUMMARY_ONLY_FIELDS:
            findings.append(
                f"[ERROR] Scene {number} ends with summary-only field '{fields[-1]}'. Integrate performance/blocking details into the relevant beat fields."
            )
            ok = False

        for field, line in field_lines:
            base = field_base(field)
            value = field_value(line)
            if base == "对白":
                dialogue_match = DIALOGUE_FIELD_RE.match(field)
                if not dialogue_match:
                    findings.append(
                        f"[ERROR] Scene {number} dialogue field '{field}' must use format '对白（角色名，语态/状态短语）'."
                    )
                    ok = False
                else:
                    role = dialogue_match.group(1).strip()
                    manner = dialogue_match.group(2).strip()
                    if role in DIALOGUE_PLACEHOLDER_ROLES:
                        findings.append(
                            f"[ERROR] Scene {number} dialogue field '{field}' uses a template placeholder as speaker name."
                        )
                        ok = False
                    if not manner:
                        findings.append(
                            f"[ERROR] Scene {number} dialogue field '{field}' lacks a speaking manner/state phrase."
                        )
                        ok = False
            for pattern in PLACEHOLDER_LEAK_PATTERNS:
                if pattern in value:
                    findings.append(
                        f"[ERROR] Scene {number} field '{field}' leaks an instruction/template placeholder into the script: {pattern}"
                    )
                    ok = False
            if base in CONCRETE_CHECK_FIELDS:
                for pattern in ABSTRACT_VISUAL_PATTERNS:
                    if pattern in value:
                        findings.append(
                            f"[ERROR] Scene {number} field '{field}' contains abstract/non-visual wording: {pattern}"
                        )
                        ok = False
            if base in {"角色动作", "动作画面"}:
                for pattern in SUBJECTIVE_INTENT_PATTERNS:
                    if pattern in value:
                        findings.append(
                            f"[ERROR] Scene {number} action field '{field}' contains subjective intent wording instead of objective filmable action: {pattern}"
                        )
                        ok = False
            for pattern in UNRELATED_BACKSTORY_PATTERNS:
                if pattern in value:
                    findings.append(
                        f"[ERROR] Scene {number} field '{field}' may add unrelated backstory/object-origin/recollection detail: {pattern}"
                    )
                    ok = False
            if base == "环境描写":
                for pattern in ENVIRONMENT_ACTION_PATTERNS:
                    if pattern in value:
                        findings.append(
                            f"[ERROR] Scene {number} environment field mixes character action/dialogue cue into setting description: {pattern}"
                        )
                        ok = False
            if base == "音效":
                for pattern in DESCRIPTIVE_SOUND_PATTERNS:
                    if pattern in value:
                        findings.append(
                            f"[ERROR] Scene {number} sound field '{field}' describes the sound instead of writing sound body: {pattern}"
                        )
                        ok = False
            if base == "分镜明细预设":
                findings.append(
                    f"[ERROR] Scene {number} uses removed field '分镜明细预设'. Use visual/action/performance fields instead."
                )
                ok = False
            if base == "场面调度":
                for pattern in CINEMATOGRAPHY_OVERREACH_PATTERNS:
                    if pattern in value:
                        findings.append(
                            f"[ERROR] Scene {number} staging field '{field}' contains cinematography-overreach wording: {pattern}"
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
