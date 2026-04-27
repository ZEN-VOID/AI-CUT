#!/usr/bin/env python3
"""
Bridge script for `story/3-初稿/B-Doubao流`.

It assembles the chapter context pack locally, then delegates the actual
chapter-file creation to AnyFast `doubao-seed-2.0-pro`.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable

import yaml


SCRIPT_PATH = Path(__file__).resolve()
DRAFTING_DIR = SCRIPT_PATH.parents[1]
STORY_STAGE_DIR = SCRIPT_PATH.parents[2]
STORY_ROOT = SCRIPT_PATH.parents[3]
SKILLS_ROOT = SCRIPT_PATH.parents[4]
REPO_ROOT = SCRIPT_PATH.parents[6]
STORY_SCRIPTS_DIR = STORY_ROOT / "scripts"
DOUBAO_SCRIPT = (
    SKILLS_ROOT
    / "api"
    / "anyfast"
    / "llm"
    / "doubao-seed-2.0-pro"
    / "scripts"
    / "doubao_seed_chat.py"
)
SYSTEM_PROMPT_PATH = DRAFTING_DIR / "templates" / "doubao-system-prompt.md"
CHAPTER_TEMPLATE_PATH = DRAFTING_DIR / "templates" / "chapter-root.template.md"

if str(STORY_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(STORY_SCRIPTS_DIR))

from chapter_paths import drafting_root_md_path, extract_chapter_title, find_chapter_file
from planning_paths import (
    canonical_book_plan_path,
    canonical_book_plan_relpath,
    canonical_chapter_plan_path,
    canonical_chapter_plan_relpath,
    canonical_volume_plan_path,
    canonical_volume_plan_relpath,
    planning_volume_num_for_chapter,
)
from project_locator import resolve_project_root


REQUIRED_OUTPUT_MARKERS = (
    "写作模型",
)
EXPECTED_WRITING_MODEL = "Doubao"
FORBIDDEN_FRONTMATTER_FIELDS = (
    "story_name",
    "volume_num",
    "chapter_num",
    "chapter_title",
    "planning_global_ref",
    "planning_volume_ref",
    "planning_chapter_ref",
    "rhythm_type",
    "global_card_refs",
    "style_card_refs",
    "north_star_ref",
    "project_context_refs",
    "previous_chapter_ref",
    "global_context",
    "style_context",
    "north_star_chapter_brief",
)
PLACEHOLDER_MARKERS = ("[请填充完整章节正文]", "{{chapter_body}}", "{{", "}}")
PLANNING_LANGUAGE_PATTERNS = (
    "本章故事概要",
    "本章冲突",
    "本章任务线",
    "章末达成",
    "七步职责映射",
    "selected_mode",
    "exit_hook",
)
MIN_BODY_CHARS = 800


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+\n", "\n", text.replace("\r\n", "\n")).strip()


def _excerpt(text: str, max_chars: int) -> str:
    normalized = _normalize_text(text)
    if len(normalized) <= max_chars:
        return normalized
    return normalized[:max_chars].rstrip() + "\n...[truncated]"


def _tail_excerpt(text: str, max_chars: int) -> str:
    normalized = _normalize_text(text)
    if len(normalized) <= max_chars:
        return normalized
    return "[truncated]...\n" + normalized[-max_chars:].lstrip()


def _rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _find_refs(root: Path, relative_glob: str) -> list[Path]:
    return sorted(root.glob(relative_glob))


def _select_project_context_files(project_root: Path, volume_num: int, chapter_num: int) -> list[Path]:
    context_dir = project_root / "CONTEXT"
    if not context_dir.is_dir():
        return []

    scored: list[tuple[int, str, Path]] = []
    for path in sorted(context_dir.rglob("*.md")):
        name = path.name
        stem = path.stem
        score = 0
        if f"第{chapter_num}章" in stem:
            score += 100
        if f"第{volume_num}卷" in stem:
            score += 60
        if any(token in stem for token in ("global", "全局", "世界", "设定", "角色", "风格", "continuity", "承接")):
            score += 20
        if path.parent == context_dir:
            score += 10
        scored.append((score, str(path), path))

    scored.sort(key=lambda item: (-item[0], item[1]))
    selected = [path for score, _, path in scored if score > 0][:6]
    if selected:
        return selected
    return [path for _, _, path in scored[:3]]


def _yaml_list(paths: Iterable[str], indent: int = 0) -> str:
    items = list(paths)
    prefix = " " * indent
    if not items:
        return prefix + "[]"
    return "\n".join(f'{prefix}- "{item}"' for item in items)


def _extract_rhythm_type_from_planning_text(text: str) -> str:
    match = re.search(r"`selected_mode`：([^\n]+)", text)
    if match:
        return match.group(1).strip().strip("`").strip()
    match = re.search(r"rhythm_type[:：]\s*\"?([^\n\"]+)\"?", text)
    if match:
        return match.group(1).strip()
    return ""


def _render_output_template(
    *,
    story_name: str,
    volume_num: int,
    chapter_num: int,
    chapter_title: str,
    rhythm_type: str,
    global_card_refs: list[str],
    style_card_refs: list[str],
    project_context_refs: list[str],
    previous_chapter_ref: str,
) -> str:
    template = _read_text(CHAPTER_TEMPLATE_PATH)
    rendered = template.replace("{{story_name}}", story_name)
    rendered = rendered.replace("{{volume_num}}", str(volume_num))
    rendered = rendered.replace("{{chapter_num}}", str(chapter_num))
    rendered = rendered.replace("{{chapter_title}}", chapter_title)
    rendered = rendered.replace("{{rhythm_type}}", rhythm_type)

    rendered = re.sub(
        r'global_card_refs:\n(?:  - "1-设定/0-全局卡/\.\.\."\n?)?',
        f"global_card_refs:\n{_yaml_list(global_card_refs, indent=2)}\n",
        rendered,
        count=1,
    )
    rendered = re.sub(
        r'style_card_refs:\n(?:  - "1-设定/1-风格卡/\.\.\."\n?)?',
        f"style_card_refs:\n{_yaml_list(style_card_refs, indent=2)}\n",
        rendered,
        count=1,
    )

    if project_context_refs:
        rendered = rendered.replace(
            "project_context_refs: []",
            f"project_context_refs:\n{_yaml_list(project_context_refs, indent=2)}",
        )
    rendered = rendered.replace('previous_chapter_ref: ""', f'previous_chapter_ref: "{previous_chapter_ref}"')
    rendered = rendered.replace("{{chapter_body}}", "[请填充完整章节正文]")
    return rendered


def _read_optional_instruction_file(path: str | None) -> str:
    if not path:
        return ""
    return _read_text(Path(path)).strip()


def _build_branch_instruction_section(
    *,
    drafting_mode: str,
    user_instructions: list[str],
    instruction_file_text: str,
    repair_finding: str,
    continue_from: str,
) -> str:
    lines: list[str] = []
    if drafting_mode == "chapter_rewrite":
        lines.append("重写分支：必须先吸收现稿中已经成立的事实，再按当前 planning 与用户约束重构完整章节。")
    elif drafting_mode == "chapter_continue":
        lines.append("续写分支：必须保留现稿已成立段落、文气和承接，只补足未完成的推进与章末牵引。")
        if continue_from:
            lines.append(f"续写边界：{continue_from}")
    elif drafting_mode == "local_repair":
        lines.append("局部修复分支：必须优先定位问题段落和源层约束，不得扩大改写未受影响的正文。")
        if repair_finding:
            lines.append("修复 finding：\n" + repair_finding)

    if user_instructions:
        lines.append("用户补充约束：\n" + "\n".join(f"- {item}" for item in user_instructions))
    if instruction_file_text:
        lines.append("外部约束文件：\n" + instruction_file_text)
    return "\n\n".join(lines)


def _build_continuity_bridge_section(previous_path: Path | None, project_root: Path) -> str:
    if previous_path and previous_path.exists():
        previous_ref = _rel(previous_path, project_root)
        previous_text = _read_text(previous_path)
        return (
            f"连续性桥（必须优先吸收，来源：{previous_ref}）：\n"
            "1. 本章开篇必须承接上一章末尾已经发生的事实、人物所在位置、情绪余波、未完成动作和悬念压力。\n"
            "2. 不得把本章写成重新开局；允许自然跳时，但必须用叙事细节交代上一章到本章之间的因果过渡。\n"
            "3. 当前章 planning 是推进方向，上一章末尾是入场姿态；两者冲突时，先保留上一章既成事实，再用本章事件完成推进。\n"
            "4. 章末必须形成对下一章的牵引，不要在本章内把所有压力清空。\n\n"
            "上一章末尾摘录（优先用于开章承接）：\n"
            + _tail_excerpt(previous_text, 6000)
            + "\n\n上一章整体摘录（用于人物状态、事实与文气校准）：\n"
            + _excerpt(previous_text, 9000)
        )

    return (
        "连续性桥：上一章正文未找到；本章不得停工，必须改用当前卷规划与当前章 planning "
        "建立开章入场、推进因果和章末牵引。"
    )


def _build_messages(
    *,
    project_root: Path,
    story_name: str,
    volume_num: int,
    chapter_num: int,
    chapter_title: str,
    drafting_mode: str,
    target_path: Path,
    book_plan_path: Path,
    volume_plan_path: Path,
    chapter_plan_path: Path,
    north_star_path: Path,
    memory_path: Path | None,
    global_cards: list[Path],
    style_cards: list[Path],
    project_context_files: list[Path],
    previous_path: Path | None,
    current_path: Path,
    user_instructions: list[str],
    instruction_file_text: str,
    repair_finding: str,
    continue_from: str,
    supervision_packet_text: str,
) -> list[dict[str, str]]:
    system_prompt = _read_text(SYSTEM_PROMPT_PATH).strip()
    global_card_refs = [_rel(path, project_root) for path in global_cards]
    style_card_refs = [_rel(path, project_root) for path in style_cards]
    project_context_refs = [_rel(path, project_root) for path in project_context_files]
    previous_ref = _rel(previous_path, project_root) if previous_path else ""

    output_template = _render_output_template(
        story_name=story_name,
        volume_num=volume_num,
        chapter_num=chapter_num,
        chapter_title=chapter_title,
        rhythm_type=_extract_rhythm_type_from_planning_text(_read_text(chapter_plan_path)),
        global_card_refs=global_card_refs,
        style_card_refs=style_card_refs,
        project_context_refs=project_context_refs,
        previous_chapter_ref=previous_ref,
    )

    sections = [
        f"目标输出路径：{_rel(target_path, project_root)}",
        f"当前模式：{drafting_mode}",
        "输出模板（必须按此 schema 返回完整文件）：\n" + output_template,
        "整书规划：\n" + _excerpt(_read_text(book_plan_path), 5000),
        "当前卷规划：\n" + _excerpt(_read_text(volume_plan_path), 5000),
        "当前章规划：\n" + _excerpt(_read_text(chapter_plan_path), 7000),
        "north_star：\n" + _excerpt(_read_text(north_star_path), 3000),
    ]

    sections.append(_build_continuity_bridge_section(previous_path, project_root))

    branch_instruction_section = _build_branch_instruction_section(
        drafting_mode=drafting_mode,
        user_instructions=user_instructions,
        instruction_file_text=instruction_file_text,
        repair_finding=repair_finding,
        continue_from=continue_from,
    )
    if branch_instruction_section:
        sections.append("分支执行约束：\n" + branch_instruction_section)

    if memory_path and memory_path.is_file():
        sections.append(f"项目 MEMORY（{_rel(memory_path, project_root)}）：\n" + _excerpt(_read_text(memory_path), 3000))

    if global_cards:
        global_payload = []
        for path in global_cards:
            global_payload.append(f"[{_rel(path, project_root)}]\n{_excerpt(_read_text(path), 2200)}")
        sections.append("全局卡摘录：\n" + "\n\n".join(global_payload))

    if style_cards:
        style_payload = []
        for path in style_cards:
            style_payload.append(f"[{_rel(path, project_root)}]\n{_excerpt(_read_text(path), 2200)}")
        sections.append("风格卡摘录：\n" + "\n\n".join(style_payload))

    if project_context_files:
        context_payload = []
        for path in project_context_files:
            context_payload.append(f"[{_rel(path, project_root)}]\n{_excerpt(_read_text(path), 1800)}")
        sections.append("项目 CONTEXT 摘录：\n" + "\n\n".join(context_payload))

    if supervision_packet_text:
        sections.append("监制组 supervision_packet（必须吸收为创作约束，不得写入 frontmatter）：\n" + supervision_packet_text)

    if current_path.exists():
        sections.append(
            f"当前目标章现稿（必须先吸收后再按当前模式处理，{_rel(current_path, project_root)}）：\n"
            + _excerpt(_read_text(current_path), 9000)
        )

    user_prompt = (
        "请根据以下上下文直接创作并返回完整章节 Markdown 文件。"
        "不要解释过程，不要输出多个版本。\n\n" + "\n\n".join(sections)
    )
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def _strip_code_fence(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```[a-zA-Z0-9_-]*\n", "", stripped)
        stripped = re.sub(r"\n```$", "", stripped)
    return stripped.strip()


def _split_frontmatter(text: str) -> tuple[dict, str]:
    normalized = text.replace("\r\n", "\n").strip()
    if not normalized.startswith("---\n"):
        raise ValueError("豆包返回内容缺少 YAML frontmatter 起始 `---`。")
    end_match = re.search(r"\n---\s*\n", normalized)
    if not end_match:
        raise ValueError("豆包返回内容缺少 YAML frontmatter 结束 `---`。")
    yaml_text = normalized[4:end_match.start()]
    body = normalized[end_match.end():].strip()
    try:
        payload = yaml.safe_load(yaml_text)
    except yaml.YAMLError as exc:
        raise ValueError(f"豆包返回 YAML frontmatter 不合法：{exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("豆包返回 YAML frontmatter 必须是对象。")
    return payload, body


def _require_non_empty(value: object, field_name: str) -> None:
    if value is None:
        raise ValueError(f"豆包返回 frontmatter 字段为空：{field_name}")
    if isinstance(value, str) and not value.strip():
        raise ValueError(f"豆包返回 frontmatter 字段为空：{field_name}")
    if isinstance(value, (list, dict)) and not value:
        raise ValueError(f"豆包返回 frontmatter 字段为空：{field_name}")


def _validate_nested_context(payload: dict, field_name: str, keys: Iterable[str]) -> None:
    value = payload.get(field_name)
    if not isinstance(value, dict):
        raise ValueError(f"豆包返回 frontmatter 字段必须是对象：{field_name}")
    for key in keys:
        _require_non_empty(value.get(key), f"{field_name}.{key}")


def _validate_generated_markdown(text: str, chapter_num: int, expected_previous_ref: str = "") -> None:
    payload, body = _split_frontmatter(text)
    for marker in REQUIRED_OUTPUT_MARKERS:
        if marker not in payload:
            raise ValueError(f"豆包返回 frontmatter 缺少必需字段：{marker}")
        _require_non_empty(payload.get(marker), marker)

    if payload.get("写作模型") != EXPECTED_WRITING_MODEL:
        raise ValueError(f"豆包返回 frontmatter 字段 `写作模型` 必须是 `{EXPECTED_WRITING_MODEL}`。")
    for field in FORBIDDEN_FRONTMATTER_FIELDS:
        if field in payload:
            raise ValueError(f"豆包返回 frontmatter 不应重复写入 `{field}`，该信息由上下文加载与 sidecar 承载。")

    heading = f"# 第{chapter_num}章｜"
    if heading not in body:
        raise ValueError(f"豆包返回内容缺少章节标题行：{heading}")
    body_after_heading = body.split(heading, 1)[1]
    if len(re.sub(r"\s+", "", body_after_heading)) < MIN_BODY_CHARS:
        raise ValueError(f"豆包返回正文过短，低于最小完整度门槛 {MIN_BODY_CHARS} 字。")
    for marker in PLACEHOLDER_MARKERS:
        if marker in text:
            raise ValueError(f"豆包返回内容仍包含模板占位符：{marker}")
    for pattern in PLANNING_LANGUAGE_PATTERNS:
        if pattern in body_after_heading:
            raise ValueError(f"豆包返回正文仍保留 planning 语言：{pattern}")


def _default_output_dir(project_root: Path, volume_num: int, chapter_num: int) -> Path:
    return project_root / "reports" / "3-初稿" / "doubao" / f"第{volume_num}卷" / f"第{chapter_num}章"


def _run_doubao(messages_path: Path, output_dir: Path, *, temperature: float, top_p: float, max_tokens: int, stream: bool) -> str:
    cmd = [
        sys.executable,
        str(DOUBAO_SCRIPT),
        "--messages-file",
        str(messages_path),
        "--task-kind",
        "temp",
        "--project-name",
        "story-drafting-doubao",
        "--output-dir",
        str(output_dir),
        "--temperature",
        str(temperature),
        "--top-p",
        str(top_p),
        "--max-tokens",
        str(max_tokens),
    ]
    if stream:
        cmd.append("--stream")

    proc = subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "豆包调用失败。")
    return proc.stdout.strip()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write chapter manuscript via AnyFast Doubao")
    parser.add_argument("--project-root", help="explicit project root; defaults to active story project")
    parser.add_argument("--chapter", type=int, required=True, help="target chapter number")
    parser.add_argument("--output-dir", help="provider artifact output dir")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--max-tokens", type=int, default=12000)
    parser.add_argument(
        "--mode",
        choices=("auto", "chapter_draft", "chapter_rewrite", "chapter_continue", "local_repair"),
        default="auto",
        help="drafting mode; auto drafts missing chapters and blocks writeback over existing chapters",
    )
    parser.add_argument(
        "--instruction",
        action="append",
        default=[],
        help="extra user constraint for rewrite/continue/repair; can be repeated",
    )
    parser.add_argument("--instruction-file", help="file containing additional rewrite/continue/repair constraints")
    parser.add_argument("--supervision-packet", help="team supervision packet file produced by drafting subagents")
    parser.add_argument("--continue-from", help="explicit continuation boundary for chapter_continue")
    parser.add_argument("--repair-finding", help="review finding or local issue description for local_repair")
    parser.add_argument("--stream", action="store_true", help="use stream mode when calling provider")
    parser.add_argument("--dry-run", action="store_true", help="only emit the messages pack without calling Doubao")
    parser.add_argument("--no-writeback", action="store_true", help="call Doubao but do not write back the chapter file")
    parser.add_argument("--force", action="store_true", help="allow writeback over an existing canonical chapter file")
    return parser


def _resolve_drafting_mode(args: argparse.Namespace, chapter_path: Path) -> str:
    target_exists = chapter_path.exists()
    if args.mode == "auto":
        if target_exists and not (args.dry_run or args.no_writeback):
            raise SystemExit(
                "目标章已存在，auto 模式禁止直接覆盖。请显式传入 "
                "--mode chapter_rewrite / chapter_continue / local_repair，并加 --force；"
                "或使用 --dry-run / --no-writeback。"
            )
        return "chapter_rewrite" if target_exists else "chapter_draft"

    if args.mode == "chapter_draft" and target_exists and not (args.dry_run or args.no_writeback):
        raise SystemExit("目标章已存在，不能用 chapter_draft 覆盖；请改用 rewrite/continue/local_repair 并加 --force。")
    if args.mode in {"chapter_rewrite", "chapter_continue", "local_repair"} and not target_exists:
        raise SystemExit(f"目标章不存在，不能执行 {args.mode}；请改用 chapter_draft。")
    if target_exists and not (args.dry_run or args.no_writeback) and not args.force:
        raise SystemExit("目标章已存在，正式写回必须显式传入 --force。")
    if args.mode == "chapter_continue" and not (args.continue_from or args.instruction or args.instruction_file):
        raise SystemExit("chapter_continue 必须提供 --continue-from、--instruction 或 --instruction-file。")
    if args.mode == "local_repair" and not (args.repair_finding or args.instruction or args.instruction_file):
        raise SystemExit("local_repair 必须提供 --repair-finding、--instruction 或 --instruction-file。")
    return args.mode


def main() -> int:
    args = build_parser().parse_args()

    project_root = resolve_project_root(args.project_root)
    story_name = project_root.name
    chapter_num = args.chapter
    volume_num = planning_volume_num_for_chapter(chapter_num, project_root=project_root)
    chapter_title = extract_chapter_title(project_root, chapter_num) or f"第{chapter_num}章"

    book_plan_path = canonical_book_plan_path(project_root)
    volume_plan_path = canonical_volume_plan_path(project_root, volume_num)
    chapter_plan_path = canonical_chapter_plan_path(project_root, chapter_num, volume_num)
    north_star_path = project_root / "0-初始化" / "north_star.yaml"
    memory_path = project_root / "MEMORY.md"
    chapter_path = drafting_root_md_path(project_root, chapter_num)
    previous_path = find_chapter_file(project_root, chapter_num - 1) if chapter_num > 1 else None
    drafting_mode = _resolve_drafting_mode(args, chapter_path)
    instruction_file_text = _read_optional_instruction_file(args.instruction_file)
    supervision_packet_text = _read_text(Path(args.supervision_packet)).strip() if args.supervision_packet else ""

    required_files = [book_plan_path, volume_plan_path, chapter_plan_path, north_star_path]
    missing = [str(path) for path in required_files if not path.is_file()]
    if missing:
        raise SystemExit("缺少必需输入：\n- " + "\n- ".join(missing))

    global_cards = []
    style_cards = []

    project_context_files = _select_project_context_files(project_root, volume_num, chapter_num)
    messages = _build_messages(
        project_root=project_root,
        story_name=story_name,
        volume_num=volume_num,
        chapter_num=chapter_num,
        chapter_title=chapter_title,
        drafting_mode=drafting_mode,
        target_path=chapter_path,
        book_plan_path=book_plan_path,
        volume_plan_path=volume_plan_path,
        chapter_plan_path=chapter_plan_path,
        north_star_path=north_star_path,
        memory_path=memory_path if memory_path.is_file() else None,
        global_cards=global_cards,
        style_cards=style_cards,
        project_context_files=project_context_files,
        previous_path=previous_path,
        current_path=chapter_path,
        user_instructions=args.instruction,
        instruction_file_text=instruction_file_text,
        repair_finding=args.repair_finding or "",
        continue_from=args.continue_from or "",
        supervision_packet_text=supervision_packet_text,
    )

    output_dir = Path(args.output_dir) if args.output_dir else _default_output_dir(project_root, volume_num, chapter_num)
    output_dir.mkdir(parents=True, exist_ok=True)
    messages_path = output_dir / f"chapter_{chapter_num}_doubao_messages.json"
    messages_path.write_text(json.dumps(messages, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.dry_run:
        summary = {
            "ok": True,
            "mode": "dry_run",
            "project_root": str(project_root),
            "chapter_path": str(chapter_path),
            "drafting_mode": drafting_mode,
            "messages_path": str(messages_path),
            "output_dir": str(output_dir),
            "memory_ref": _rel(memory_path, project_root) if memory_path.is_file() else "",
            "project_context_refs": [_rel(path, project_root) for path in project_context_files],
            "previous_chapter_ref": _rel(previous_path, project_root) if previous_path and previous_path.exists() else "",
            "force_required_for_writeback": chapter_path.exists(),
            "supervision_packet_ref": args.supervision_packet or "",
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    generated = _strip_code_fence(
        _run_doubao(
            messages_path,
            output_dir,
            temperature=args.temperature,
            top_p=args.top_p,
            max_tokens=args.max_tokens,
            stream=args.stream,
        )
    )
    expected_previous_ref = _rel(previous_path, project_root) if previous_path and previous_path.exists() else ""
    _validate_generated_markdown(generated, chapter_num, expected_previous_ref)

    raw_path = output_dir / f"chapter_{chapter_num}_generated.md"
    raw_path.write_text(generated + "\n", encoding="utf-8")

    backup_path: Path | None = None
    if not args.no_writeback:
        chapter_path.parent.mkdir(parents=True, exist_ok=True)
        if chapter_path.exists():
            backup_path = output_dir / f"chapter_{chapter_num}_backup_before_writeback.md"
            backup_path.write_text(_read_text(chapter_path), encoding="utf-8")
        chapter_path.write_text(generated + "\n", encoding="utf-8")

    summary = {
        "ok": True,
        "project_root": str(project_root),
        "chapter_path": str(chapter_path),
        "drafting_mode": drafting_mode,
        "messages_path": str(messages_path),
        "provider_output_dir": str(output_dir),
        "generated_preview_path": str(raw_path),
        "writeback": not args.no_writeback,
        "backup_path": str(backup_path) if backup_path else "",
        "supervision_packet_ref": args.supervision_packet or "",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
