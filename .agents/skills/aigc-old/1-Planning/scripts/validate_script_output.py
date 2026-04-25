#!/usr/bin/env python3
"""Validate `1-Planning/2-剧本` outputs from the legacy `2-格式/` runtime path."""

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
SCENE_SLUGLINE_RE = re.compile(r"^(?:内景|外景|内外景)\s+.+?\s+-\s+(?:日|夜)$")
NOTE_HEADER_RE = re.compile(
    r"^(?:#{1,6}\s*)?(?:【)?(?:附加执行备注|执行备注|风险备注|规划交接|执行报告)(?:】)?\s*(?:[：:].*)?$"
)
TEXT_PATTERNS = {
    "dialogue": re.compile(r"^对白（(?P<speaker>[^）]+)）\s*[：:]\s*(?P<body>.+?)\s*$"),
    "inner": re.compile(r"^(?:独白|内心独白)（(?P<speaker>[^）]+)）\s*[：:]\s*(?P<body>.+?)\s*$"),
    "narration": re.compile(r"^旁白（(?P<speaker>[^）]+)）\s*[：:]\s*(?P<body>.+?)\s*$"),
}
VISUAL_PATTERNS = {
    "dialogue_visual": re.compile(r"^对白画面\s*[：:]\s*(?P<body>.+?)\s*$"),
    "inner_visual": re.compile(r"^(?:独白画面|内心独白画面)\s*[：:]\s*(?P<body>.+?)\s*$"),
    "narration_visual": re.compile(r"^旁白画面\s*[：:]\s*(?P<body>.+?)\s*$"),
    "action_visual": re.compile(r"^动作画面\s*[：:]\s*(?P<body>.+?)\s*$"),
    "character_action": re.compile(r"^角色动作\s*[：:]\s*(?P<body>.+?)\s*$"),
    "environment": re.compile(r"^环境描写\s*[：:]\s*(?P<body>.+?)\s*$"),
    "sound": re.compile(r"^音效\s*[：:]\s*(?P<body>.+?)\s*$"),
    "sound_visual": re.compile(r"^音效画面\s*[：:]\s*(?P<body>.+?)\s*$"),
    "transition": re.compile(r"^转场\s*[：:]\s*(?P<body>.+?)\s*$"),
    "character_design": re.compile(r"^角色造型\s*[：:]\s*(?P<body>.+?)\s*$"),
    "prop_closeup": re.compile(r"^道具特写\s*[：:]\s*(?P<body>.+?)\s*$"),
    "expression_closeup": re.compile(r"^(?:表情特写|特写画面)\s*[：:]\s*(?P<body>.+?)\s*$"),
    "group_visual": re.compile(r"^群像画面\s*[：:]\s*(?P<body>.+?)\s*$"),
    "system_visual": re.compile(r"^系统画面\s*[：:]\s*(?P<body>.+?)\s*$"),
    "rule_visual": re.compile(r"^规则显影\s*[：:]\s*(?P<body>.+?)\s*$"),
    "disaster_visual": re.compile(r"^现实灾难画面\s*[：:]\s*(?P<body>.+?)\s*$"),
    "performance_note": re.compile(r"^(?:表演提示|心理反应)\s*[：:]\s*(?P<body>.+?)\s*$"),
    "camera_preset": re.compile(r"^镜头语言预设\s*[：:]\s*(?P<body>.+?)\s*$"),
}
SCENE_FIELD_KINDS = {
    "action_visual",
    "character_action",
    "environment",
    "sound",
    "transition",
    "character_design",
    "prop_closeup",
    "expression_closeup",
    "group_visual",
    "system_visual",
    "rule_visual",
    "disaster_visual",
    "performance_note",
}
PROSE_LIKE_ACTION_RE = re.compile(
    r"(?:第[一二三四五六七八九十百0-9]+[章节]|感觉|意识到|记起来|想起|没有人知道|不知道|他明明记得|"
    r"大概是|像是在等|像是接到了|这是什么能力|为什么只有)"
)
UPSTREAM_QUOTE_RE = re.compile(r"[“\"](?P<text>[^”\"\n]+)[”\"]")
UPSTREAM_ATTRIBUTION_RE = re.compile(
    r"(?P<speaker>[\u4e00-\u9fffA-Za-z0-9·]{1,12})(?:（[^）\n]*）)?\s*[：:]\s*(?P<body>.*?)(?="
    r"[\u4e00-\u9fffA-Za-z0-9·]{1,12}(?:（[^）\n]*）)?\s*[：:]"
        r"|画面\s*[：:]|时长\s*[：:]|音效(?:画面)?\s*[：:]|景别\s*[：:]|环境\s*[：:]|$)",
    re.S,
)
UPSTREAM_NON_DIALOGUE_LABELS = {
    "场景",
    "环境",
    "景别",
    "画面",
    "音效",
    "时长",
    "特写",
    "近景",
    "中景",
    "全景",
    "正反打",
    "交叉切",
    "转场",
    "剧本类型",
    "人物",
    "总镜数",
    "源文件",
    "项目名",
    "集数",
}
INLINE_ATTRIBUTION_RE = re.compile(
    r"(?:笑着|哭着|低声|轻声|沉声|冷声|怒声|怒吼|喊着|喊道|吼道|叹道|哽咽着|看着|盯着|望着|转身|抬手|伸手|后退|上前|走向).{0,8}(?:说|问|道|喊)$"
)
STANDARD_WARNING_NARRATION_RATIO = 0.45
STANDARD_VARIANT = "standard"
STANDARD_VARIANT_LABEL = "标准剧"


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
    parser = argparse.ArgumentParser(description="校验 `1-Planning/2-剧本` 输出契约；runtime 路径仍为 `2-格式/`")
    parser.add_argument("--input", required=True, help="待校验的第N集 Markdown 文件")
    parser.add_argument(
        "--variant",
        default=STANDARD_VARIANT,
        help="兼容旧命令；当前统一按 standard/标准剧 校验",
    )
    parser.add_argument("--upstream", help="可选：`1-分集` 上游输入文件，用于对白冻结校验")
    parser.add_argument("--allow-inner", action="store_true", help="兼容旧参数；当前无特殊效果")
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
    slugline_to_label: dict[str, str] = {}
    label_to_slugline: dict[str, str] = {}
    previous_scene_title: str | None = None

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
            scene_label = scene_match.group("label").strip()
            scene_title = scene_match.group("title").strip()
            if not scene_label.isdigit():
                add_finding(
                    findings,
                    level="error",
                    code="FAIL-SCENE-LABEL",
                    file_path=file_path,
                    detail="场景编号必须使用阿拉伯数字，例如 `场景1`。",
                    line_no=index,
                )
            if not SCENE_SLUGLINE_RE.match(scene_title):
                add_finding(
                    findings,
                    level="error",
                    code="FAIL-SCENE-SLUGLINE",
                    file_path=file_path,
                    detail="场景标题必须使用好莱坞标准剧本 slugline：`内景/外景 场所 - 日/夜`，不得写成剧情摘要。",
                    line_no=index,
                )
            previous_label = slugline_to_label.get(scene_title)
            if previous_label is not None and previous_label != scene_label:
                add_finding(
                    findings,
                    level="error",
                    code="FAIL-SCENE-DUPLICATE-SLUGLINE",
                    file_path=file_path,
                    detail=(
                        f"相同 slugline `{scene_title}` 必须沿用同一个场景编号："
                        f"首次为 `场景{previous_label}`，此处为 `场景{scene_label}`。"
                    ),
                    line_no=index,
                )
            previous_title = label_to_slugline.get(scene_label)
            if previous_title is not None and previous_title != scene_title:
                add_finding(
                    findings,
                    level="error",
                    code="FAIL-SCENE-LABEL-COLLISION",
                    file_path=file_path,
                    detail=(
                        f"`场景{scene_label}` 已绑定 `{previous_title}`，不得复用到不同 slugline `{scene_title}`。"
                    ),
                    line_no=index,
                )
            if previous_scene_title == scene_title:
                add_finding(
                    findings,
                    level="error",
                    code="FAIL-SCENE-REPEATED-HEADING",
                    file_path=file_path,
                    detail=(
                        f"同一连续场景 `{scene_title}` 的标题只能出现一次；"
                        "叙事 beat 不应重复打印相同场景标题。"
                    ),
                    line_no=index,
                )
            slugline_to_label.setdefault(scene_title, scene_label)
            label_to_slugline.setdefault(scene_label, scene_title)
            previous_scene_title = scene_title
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


def normalize_preservation_text(text: str) -> str:
    text = re.sub(r"(?s)^---\n.*?\n---\n", "", text)
    text = re.sub(r"(?m)^#{1,6}\s*.*$", "", text)
    text = re.sub(r"(?m)^【剧本正文】\s*$", "", text)
    text = re.sub(r"(?m)^###\s*场景[^：:]+[：:].*$", "", text)
    text = re.sub(
        r"(?m)^(?:对白|独白|内心独白|旁白)(?:（[^）]+）)?\s*[：:]\s*[“\"]?(.*?)[”\"]?\s*$",
        r"\1",
        text,
    )
    text = re.sub(
        r"(?m)^(?:对白画面|独白画面|内心独白画面|旁白画面|音效画面|动作画面|角色动作|环境描写|音效|"
        r"转场|角色造型|道具特写|表情特写|特写画面|群像画面|系统画面|规则显影|现实灾难画面|表演提示|心理反应|镜头语言预设)\s*[：:]\s*",
        "",
        text,
    )
    text = re.sub(r"\s+", "", text)
    return text


def split_upstream_paragraphs(upstream_text: str) -> list[str]:
    body = extract_script_body(parse_frontmatter(upstream_text)[1])
    source = body if body is not None else upstream_text
    paragraphs: list[str] = []
    for raw_block in re.split(r"\n\s*\n", source):
        block = normalize_preservation_text(raw_block)
        if len(block) >= 12:
            paragraphs.append(block)
    return paragraphs


def validate_upstream_preservation(
    *,
    file_path: Path,
    script_body: str,
    upstream_text: str,
    findings: list[Finding],
) -> dict[str, Any]:
    upstream_normalized = normalize_preservation_text(extract_script_body(parse_frontmatter(upstream_text)[1]) or upstream_text)
    output_normalized = normalize_preservation_text(script_body)
    if not upstream_normalized:
        return {"upstream_preservation_ratio": None, "upstream_paragraph_coverage": None}

    length_ratio = len(output_normalized) / max(len(upstream_normalized), 1)
    paragraphs = split_upstream_paragraphs(upstream_text)
    covered = sum(1 for item in paragraphs if item in output_normalized)
    paragraph_coverage = covered / max(len(paragraphs), 1)

    if length_ratio < 0.9:
        add_finding(
            findings,
            level="error",
            code="FAIL-UPSTREAM-PRESERVATION",
            file_path=file_path,
            detail=(
                "`2-剧本` 不得压缩或摘要 `1-分集` 正文；"
                f"当前正文保留长度比为 {length_ratio:.0%}，低于 90%。"
            ),
        )
    if paragraphs and paragraph_coverage < 0.6:
        add_finding(
            findings,
            level="warning",
            code="WARN-UPSTREAM-PARAGRAPH-COVERAGE",
            file_path=file_path,
            detail=(
                "`2-剧本` 已通过长度保真硬门，但原文长段可能被拆成字段或剧本化改写为画面字段；"
                f"当前整段覆盖率为 {paragraph_coverage:.0%}，请人工抽查是否存在删改。"
            ),
        )

    return {
        "upstream_preservation_ratio": round(length_ratio, 4),
        "upstream_paragraph_coverage": round(paragraph_coverage, 4),
        "upstream_paragraphs": len(paragraphs),
        "upstream_paragraphs_covered": covered,
    }


def normalize_upstream_dialogue(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().strip("。；;"))


def extract_upstream_dialogues(upstream_text: str) -> set[str]:
    dialogues = {
        normalize_upstream_dialogue(match.group("text"))
        for match in UPSTREAM_QUOTE_RE.finditer(upstream_text)
        if normalize_upstream_dialogue(match.group("text"))
    }
    for match in UPSTREAM_ATTRIBUTION_RE.finditer(upstream_text):
        speaker = match.group("speaker").strip()
        if speaker in UPSTREAM_NON_DIALOGUE_LABELS:
            continue
        body = normalize_upstream_dialogue(match.group("body"))
        if body:
            dialogues.add(body)
    return dialogues


def validate_standard_output(
    path: Path,
    *,
    allow_inner: bool,
    upstream_text: str | None,
) -> tuple[list[Finding], dict[str, Any]]:
    findings: list[Finding] = []
    text = read_text(path)
    header, remainder = parse_frontmatter(text)
    script_body = extract_script_body(remainder)

    if script_body is None:
        add_finding(findings, level="error", code="FAIL-FORMAT", file_path=path, detail="缺少 `【剧本正文】` 区块。")
        return findings, {"variant": STANDARD_VARIANT, "scenes": 0}

    expected_variant = STANDARD_VARIANT_LABEL
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
    preservation_summary: dict[str, Any] = {}
    if upstream_text:
        preservation_summary = validate_upstream_preservation(
            file_path=path,
            script_body=script_body,
            upstream_text=upstream_text,
            findings=findings,
        )

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
                    if quote and upstream_quotes and normalize_upstream_dialogue(quote) not in upstream_quotes:
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
                awaiting_visual = (entry.kind, entry.line_no)
                continue

            if entry.kind == "sound":
                action_count += 1
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
                awaiting_visual = ("sound", entry.line_no)
                continue

            if entry.kind in SCENE_FIELD_KINDS:
                action_count += 1
                if entry.kind == "action_visual" and entry.body and PROSE_LIKE_ACTION_RE.search(entry.body):
                    add_finding(
                        findings,
                        level="warning",
                        code="WARN-ACTION-PROSE-LIKE",
                        file_path=path,
                        detail=(
                            "`动作画面` 疑似承载小说叙述、认知解释或章节标题；"
                            "请优先改写为 `角色动作/环境描写/音效/道具特写/系统画面/规则显影/心理反应` 等正式剧本字段。"
                        ),
                        line_no=entry.line_no,
                        scene=scene.title,
                    )
                continue
            if entry.kind == "camera_preset":
                continue

            if entry.kind in {"dialogue_visual", "inner_visual", "narration_visual", "sound_visual"}:
                visual_target = {
                    "dialogue_visual": "dialogue",
                    "inner_visual": "inner",
                    "narration_visual": "narration",
                    "sound_visual": "sound",
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

    if narration_count > 1 and len(narration_speakers) > 1:
        add_finding(
            findings,
            level="error",
            code="FAIL-NARRATOR-DRIFT",
            file_path=path,
            detail=f"发现多个旁白主体：{', '.join(sorted(narration_speakers))}；同一集旁白主体必须保持一致。",
        )
    if dialogue_count > 0:
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
        "variant": STANDARD_VARIANT,
        "variant_label": expected_variant,
        "scenes": len({scene.title for scene in scenes}),
        "scene_sections": len(scenes),
        "dialogue_count": dialogue_count,
        "narration_count": narration_count,
        "narration_speakers": sorted(narration_speakers),
        "actual_word_count": actual_word_count,
        **preservation_summary,
    }
    return findings, summary


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    upstream_text = read_text(Path(args.upstream)) if args.upstream else None
    if args.variant != STANDARD_VARIANT:
        print(f"WARNING WARN-VARIANT-NORMALIZED - `--variant {args.variant}` 已废弃，本次统一按 `standard/标准剧` 校验。")
    findings, summary = validate_standard_output(
        input_path,
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
