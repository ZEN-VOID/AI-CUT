#!/usr/bin/env python3
"""Validate `1-Planning/2-格式` outputs for standard and explainer variants."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


YAML_FRONTMATTER_RE = re.compile(r"(?s)^---\n(?P<header>.*?)\n---\n(?P<body>.*)$")
HEADER_LINE_RE = re.compile(r"^\s*([^：:]+)\s*[：:]\s*(.*?)\s*$")
SCRIPT_BODY_RE = re.compile(r"(?m)^【剧本正文】\s*$")
SCENE_HEADER_RE = re.compile(r"^###\s*场景(?P<label>[^：:]+)\s*[：:]\s*(?P<title>.+?)\s*$")
NOTE_HEADER_RE = re.compile(
    r"^(?:#{1,6}\s*)?(?:【)?(?:附加执行备注|执行备注|风险备注|规划交接|执行报告)(?:】)?\s*(?:[：:].*)?$"
)
TEXT_PATTERNS = {
    "dialogue": re.compile(r"^对白（(?P<speaker>[^）]+)）\s*[：:]\s*(?P<body>.+?)\s*$"),
    "inner": re.compile(r"^内心独白（(?P<speaker>[^）]+)）\s*[：:]\s*(?P<body>.+?)\s*$"),
    "narration": re.compile(r"^旁白（(?P<speaker>[^）]+)）\s*[：:]\s*(?P<body>.+?)\s*$"),
}
VISUAL_PATTERNS = {
    "dialogue_visual": re.compile(r"^对白画面\s*[：:]\s*(?P<body>.+?)\s*$"),
    "inner_visual": re.compile(r"^内心独白画面\s*[：:]\s*(?P<body>.+?)\s*$"),
    "narration_visual": re.compile(r"^旁白画面\s*[：:]\s*(?P<body>.+?)\s*$"),
    "action_visual": re.compile(r"^动作画面\s*[：:]\s*(?P<body>.+?)\s*$"),
    "camera_preset": re.compile(r"^镜头语言预设\s*[：:]\s*(?P<body>.+?)\s*$"),
}
UPSTREAM_QUOTE_RE = re.compile(r"[“\"](?P<text>[^”\"\n]+)[”\"]")
INLINE_ATTRIBUTION_RE = re.compile(
    r"(?:笑着|哭着|低声|轻声|沉声|冷声|怒声|怒吼|喊着|喊道|吼道|叹道|哽咽着|看着|盯着|望着|转身|抬手|伸手|后退|上前|走向).{0,8}(?:说|问|道|喊)$"
)
STANDARD_WARNING_NARRATION_RATIO = 0.45
VARIANT_LABELS = {"standard": "标准剧", "explainer": "解说剧"}


@dataclass
class Finding:
    level: str
    code: str
    file: str
    detail: str
    line_no: int | None = None
    scene: str | None = None


@dataclass
class Entry:
    kind: str
    line_no: int
    raw: str
    speaker: str | None = None
    body: str | None = None


@dataclass
class Scene:
    title: str
    line_no: int
    entries: list[Entry]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="校验 `1-Planning/2-格式` 输出契约")
    parser.add_argument("--input", required=True, help="待校验的第N集 Markdown 文件")
    parser.add_argument("--variant", choices=("standard", "explainer"), required=True, help="技能变体")
    parser.add_argument("--upstream", help="可选：`1-分集` 上游输入文件，用于对白冻结校验")
    parser.add_argument("--allow-inner", action="store_true", help="仅用于解说剧：显式允许内心独白")
    parser.add_argument("--json", help="可选：将校验结果写入 JSON 文件")
    return parser.parse_args()


def add_finding(
    findings: list[Finding],
    *,
    level: str,
    code: str,
    file_path: Path,
    detail: str,
    line_no: int | None = None,
    scene: str | None = None,
) -> None:
    findings.append(
        Finding(
            level=level,
            code=code,
            file=file_path.as_posix(),
            detail=detail,
            line_no=line_no,
            scene=scene,
        )
    )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = YAML_FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    header = {}
    for raw_line in match.group("header").splitlines():
        parsed = HEADER_LINE_RE.match(raw_line)
        if not parsed:
            continue
        header[parsed.group(1).strip()] = parsed.group(2).strip()
    return header, match.group("body")


def extract_script_body(text: str) -> str | None:
    match = SCRIPT_BODY_RE.search(text)
    if not match:
        return None
    return text[match.end() :].lstrip("\n")


def classify_line(raw_line: str) -> tuple[str | None, str | None, str | None]:
    for kind, pattern in TEXT_PATTERNS.items():
        match = pattern.match(raw_line)
        if match:
            return kind, match.group("speaker").strip(), match.group("body").strip()
    for kind, pattern in VISUAL_PATTERNS.items():
        match = pattern.match(raw_line)
        if match:
            return kind, None, match.group("body").strip()
    return None, None, None


def parse_scenes(body: str, *, file_path: Path, findings: list[Finding]) -> list[Scene]:
    scenes: list[Scene] = []
    current_scene: Scene | None = None
    note_mode = False

    for index, raw_line in enumerate(body.splitlines(), start=1):
        stripped = raw_line.strip()
        if not stripped:
            continue
        if NOTE_HEADER_RE.match(stripped):
            note_mode = True
            continue
        if note_mode:
            continue

        scene_match = SCENE_HEADER_RE.match(stripped)
        if scene_match:
            current_scene = Scene(title=scene_match.group("title").strip(), line_no=index, entries=[])
            scenes.append(current_scene)
            continue

        if current_scene is None:
            add_finding(
                findings,
                level="error",
                code="FAIL-SCENE-MISSING",
                file_path=file_path,
                detail="`【剧本正文】` 内存在未归属到任何 `### 场景X：...` 标题的正文行。",
                line_no=index,
            )
            continue

        kind, speaker, content = classify_line(stripped)
        if kind is None:
            add_finding(
                findings,
                level="error",
                code="FAIL-UNKNOWN-LINE",
                file_path=file_path,
                detail=f"发现未结构化正文行：{stripped}",
                line_no=index,
                scene=current_scene.title,
            )
            continue
        current_scene.entries.append(Entry(kind=kind, line_no=index, raw=stripped, speaker=speaker, body=content))

    if not scenes:
        add_finding(
            findings,
            level="error",
            code="FAIL-SCENE-MISSING",
            file_path=file_path,
            detail="`【剧本正文】` 未发现任何合法场景标题。",
        )
    return scenes


def extract_quote_content(body: str) -> tuple[str | None, str | None]:
    if len(body) < 2:
        return None, "文本内容为空。"
    if not (body.startswith("“") and body.endswith("”")):
        return None, "正文必须使用中文双引号包裹。"
    inner = body[1:-1].strip()
    if not inner:
        return None, "引号内正文为空。"
    return inner, None


def compute_word_count(script_body: str) -> int:
    return len(script_body.strip())


def extract_upstream_dialogues(upstream_text: str) -> set[str]:
    return {match.group("text").strip() for match in UPSTREAM_QUOTE_RE.finditer(upstream_text) if match.group("text").strip()}


def validate_variant(
    path: Path,
    *,
    variant: str,
    allow_inner: bool,
    upstream_text: str | None,
) -> tuple[list[Finding], dict[str, Any]]:
    findings: list[Finding] = []
    text = read_text(path)
    header, remainder = parse_frontmatter(text)
    script_body = extract_script_body(remainder)

    if script_body is None:
        add_finding(findings, level="error", code="FAIL-FORMAT", file_path=path, detail="缺少 `【剧本正文】` 区块。")
        return findings, {"variant": variant, "scenes": 0}

    expected_variant = VARIANT_LABELS[variant]
    if header.get("剧本变体") != expected_variant:
        add_finding(
            findings,
            level="error",
            code="FAIL-VARIANT-MISMATCH",
            file_path=path,
            detail=f"`剧本变体` 应为 `{expected_variant}`，实际为 `{header.get('剧本变体') or '缺失'}`。",
        )

    actual_word_count = compute_word_count(script_body)
    expected_word_count = header.get("总字数")
    if expected_word_count is None:
        add_finding(findings, level="error", code="FAIL-WORDCOUNT-STALE", file_path=path, detail="YAML 缺少 `总字数` 字段。")
    else:
        try:
            if int(expected_word_count) != actual_word_count:
                add_finding(
                    findings,
                    level="error",
                    code="FAIL-WORDCOUNT-STALE",
                    file_path=path,
                    detail=f"`总字数`={expected_word_count}，但当前 `【剧本正文】` 实算为 {actual_word_count}。",
                )
        except ValueError:
            add_finding(
                findings,
                level="error",
                code="FAIL-WORDCOUNT-STALE",
                file_path=path,
                detail=f"`总字数` 不是合法整数：{expected_word_count}",
            )

    scenes = parse_scenes(script_body, file_path=path, findings=findings)
    upstream_quotes = extract_upstream_dialogues(upstream_text) if upstream_text else set()
    narration_count = 0
    dialogue_count = 0
    narration_speakers: set[str] = set()

    for scene in scenes:
        action_count = 0
        awaiting_visual: tuple[str, int] | None = None

        for entry in scene.entries:
            if entry.kind in {"dialogue", "inner", "narration"}:
                quote, error = extract_quote_content(entry.body or "")
                if error:
                    add_finding(findings, level="error", code="FAIL-QUOTE", file_path=path, detail=error, line_no=entry.line_no, scene=scene.title)
                if entry.speaker is None or not entry.speaker.strip():
                    add_finding(findings, level="error", code="FAIL-SPEAKER-MISSING", file_path=path, detail="说话主体缺失。", line_no=entry.line_no, scene=scene.title)
                if quote and INLINE_ATTRIBUTION_RE.search(quote):
                    add_finding(
                        findings,
                        level="error",
                        code="FAIL-ACTION-MIXED",
                        file_path=path,
                        detail="引号内疑似混入动作描写，请下沉到对应 `*画面` 字段。",
                        line_no=entry.line_no,
                        scene=scene.title,
                    )
                if entry.kind == "dialogue":
                    dialogue_count += 1
                    if quote and upstream_quotes and quote not in upstream_quotes:
                        add_finding(
                            findings,
                            level="warning",
                            code="WARN-DIALOGUE-FREEZE",
                            file_path=path,
                            detail="当前对白未在上游引号文本中直接命中，请人工确认是否仍满足逐字保真。",
                            line_no=entry.line_no,
                            scene=scene.title,
                        )
                if entry.kind == "narration":
                    narration_count += 1
                    if entry.speaker:
                        narration_speakers.add(entry.speaker.strip())
                if entry.kind == "inner" and variant == "explainer" and not allow_inner:
                    add_finding(
                        findings,
                        level="error",
                        code="FAIL-INNER-MODE",
                        file_path=path,
                        detail="解说剧默认不允许 `内心独白`，除非显式传入 `--allow-inner`。",
                        line_no=entry.line_no,
                        scene=scene.title,
                    )
                awaiting_visual = (entry.kind, entry.line_no)
                continue

            if entry.kind == "action_visual":
                action_count += 1
                continue
            if entry.kind == "camera_preset":
                continue

            if entry.kind in {"dialogue_visual", "inner_visual", "narration_visual"}:
                visual_target = {
                    "dialogue_visual": "dialogue",
                    "inner_visual": "inner",
                    "narration_visual": "narration",
                }[entry.kind]
                if awaiting_visual is None or awaiting_visual[0] != visual_target:
                    add_finding(
                        findings,
                        level="error",
                        code="FAIL-VISUAL-MISSING",
                        file_path=path,
                        detail="`*画面` 没有和最近的文本条目同命题配对。",
                        line_no=entry.line_no,
                        scene=scene.title,
                    )
                awaiting_visual = None

        if awaiting_visual is not None:
            add_finding(
                findings,
                level="error",
                code="FAIL-VISUAL-MISSING",
                file_path=path,
                detail=f"文本条目 `{awaiting_visual[0]}` 缺少就近 `*画面` 配对。",
                line_no=awaiting_visual[1],
                scene=scene.title,
            )
        if action_count == 0:
            add_finding(
                findings,
                level="error",
                code="FAIL-SILENT-MISSING",
                file_path=path,
                detail="每个场景至少需要 1 条 `动作画面：` 承载无台词推进。",
                line_no=scene.line_no,
                scene=scene.title,
            )

    if variant == "explainer" and narration_count == 0:
        add_finding(
            findings,
            level="error",
            code="FAIL-NARRATIONIZATION",
            file_path=path,
            detail="解说剧至少应存在 1 条 `旁白`，否则无法证明已完成旁白主导整理。",
        )
    if narration_count > 1 and len(narration_speakers) > 1:
        add_finding(
            findings,
            level="error",
            code="FAIL-NARRATOR-DRIFT",
            file_path=path,
            detail=f"发现多个旁白主体：{', '.join(sorted(narration_speakers))}；同一集旁白主体必须保持一致。",
        )
    if variant == "standard" and dialogue_count > 0:
        narration_ratio = narration_count / max(dialogue_count + narration_count, 1)
        if narration_ratio > STANDARD_WARNING_NARRATION_RATIO:
            add_finding(
                findings,
                level="warning",
                code="WARN-NARRATION-RATIO",
                file_path=path,
                detail=f"标准剧 `旁白` 占比约为 {narration_ratio:.0%}，请人工确认是否仍满足“表演优先、旁白从严”。",
            )

    summary = {
        "variant": variant,
        "variant_label": expected_variant,
        "scenes": len(scenes),
        "dialogue_count": dialogue_count,
        "narration_count": narration_count,
        "narration_speakers": sorted(narration_speakers),
        "actual_word_count": actual_word_count,
    }
    return findings, summary


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    upstream_text = read_text(Path(args.upstream)) if args.upstream else None
    findings, summary = validate_variant(
        input_path,
        variant=args.variant,
        allow_inner=args.allow_inner,
        upstream_text=upstream_text,
    )

    payload = {
        "ok": not any(item.level == "error" for item in findings),
        "summary": summary,
        "findings": [asdict(item) for item in findings],
    }

    if args.json:
        Path(args.json).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    for item in findings:
        location = f"{item.file}:{item.line_no}" if item.line_no else item.file
        scene = f" [{item.scene}]" if item.scene else ""
        print(f"{item.level.upper()} {item.code} {location}{scene} - {item.detail}")

    if payload["ok"]:
        print(f"OK - {input_path.as_posix()} ({summary['variant_label']}, scenes={summary['scenes']})")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
