#!/usr/bin/env python3
"""
Mechanical helper for `story/3-Drafting/A-GPT原生`.

It assembles the chapter context pack and validates/writes back a Markdown
chapter already authored by the current GPT/LLM session. It does not generate
chapter prose by rule or template.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

import yaml


SCRIPT_PATH = Path(__file__).resolve()
DRAFTING_DIR = SCRIPT_PATH.parents[1]
STORY_ROOT = SCRIPT_PATH.parents[3]
STORY_SCRIPTS_DIR = STORY_ROOT / "scripts"
SYSTEM_PROMPT_PATH = DRAFTING_DIR / "templates" / "gpt-native-system-prompt.md"
CHAPTER_TEMPLATE_PATH = DRAFTING_DIR / "templates" / "chapter-root.template.md"

if str(STORY_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(STORY_SCRIPTS_DIR))

from chapter_paths import drafting_root_md_path, extract_chapter_title, find_chapter_file
from planning_paths import (
    canonical_book_plan_path,
    canonical_chapter_plan_path,
    canonical_volume_plan_path,
    planning_volume_num_for_chapter,
)
from project_locator import resolve_project_root


REQUIRED_OUTPUT_MARKERS = (
    "story_name:",
    "volume_num:",
    "chapter_num:",
    "chapter_title:",
    "planning_global_ref:",
    "planning_volume_ref:",
    "planning_chapter_ref:",
    "写作模型:",
    "rhythm_type:",
    "global_card_refs:",
    "style_card_refs:",
    "north_star_ref:",
    "project_context_refs:",
    "previous_chapter_ref:",
    "global_context:",
    "style_context:",
    "north_star_chapter_brief:",
)

REQUIRED_SCALAR_FIELDS = (
    "story_name",
    "chapter_title",
    "planning_global_ref",
    "planning_volume_ref",
    "planning_chapter_ref",
    "写作模型",
    "rhythm_type",
    "north_star_ref",
)

EXPECTED_WRITING_MODEL = "GPT"

REQUIRED_GLOBAL_CONTEXT_FIELDS = (
    "worldview_summary",
    "rule_pressure",
    "faction_or_system_pressure",
)

REQUIRED_STYLE_CONTEXT_FIELDS = (
    "tone_summary",
    "prose_summary",
    "dialogue_summary",
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+\n", "\n", text.replace("\r\n", "\n")).strip()


def _excerpt(text: str, max_chars: int) -> str:
    normalized = _normalize_text(text)
    if len(normalized) <= max_chars:
        return normalized
    return normalized[:max_chars].rstrip() + "\n...[truncated]"


def _rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _find_refs(root: Path, relative_glob: str) -> list[Path]:
    return sorted(root.glob(relative_glob))


def _select_project_context_files(project_root: Path, volume_num: int, chapter_num: int) -> list[Path]:
    context_dir = project_root / "CONTEXT"
    if not context_dir.is_dir():
        return []

    chapter_tokens = (
        f"第{chapter_num}章",
        f"chapter-{chapter_num}",
        f"chapter_{chapter_num}",
        f"ch{chapter_num:04d}",
        f"ch{chapter_num:03d}",
        f"ch{chapter_num}",
    )
    volume_tokens = (
        f"第{volume_num}卷",
        f"volume-{volume_num}",
        f"volume_{volume_num}",
        f"vol{volume_num}",
    )
    global_tokens = ("global", "全局", "世界", "设定", "角色", "风格", "continuity", "承接")

    scored: list[tuple[int, str, Path]] = []
    for path in sorted(context_dir.rglob("*.md")):
        rel_text = path.relative_to(context_dir).as_posix().lower()
        score = 0
        if any(token.lower() in rel_text for token in chapter_tokens):
            score += 100
        if any(token.lower() in rel_text for token in volume_tokens):
            score += 60
        if any(token.lower() in rel_text for token in global_tokens):
            score += 20
        scored.append((score, str(path), path))

    scored.sort(key=lambda item: (-item[0], item[1]))
    return [path for score, _, path in scored if score >= 20][:6]


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
        r'global_card_refs:\n(?:  - "1-Cards/0-全局卡/\.\.\."\n?)?',
        f"global_card_refs:\n{_yaml_list(global_card_refs, indent=2)}\n",
        rendered,
        count=1,
    )
    rendered = re.sub(
        r'style_card_refs:\n(?:  - "1-Cards/1-风格卡/\.\.\."\n?)?',
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
    rendered = rendered.replace("{{chapter_body}}", "[由当前 GPT/LLM 会话创作完整章节正文]")
    return rendered


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

    if previous_path and previous_path.exists():
        sections.append(f"上一章正文（{_rel(previous_path, project_root)}）：\n" + _excerpt(_read_text(previous_path), 9000))

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
    return stripped.strip().replace("\r\n", "\n").replace("\r", "\n")


def _split_frontmatter(text: str) -> tuple[dict, str]:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not match:
        raise ValueError("GPT 原生输出缺少完整 YAML frontmatter。")
    try:
        payload = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"GPT 原生输出 YAML frontmatter 无法解析：{exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("GPT 原生输出 YAML frontmatter 必须是映射对象。")
    return payload, text[match.end() :]


def _require_non_empty_text(payload: dict, field: str) -> None:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"GPT 原生输出 frontmatter 字段 `{field}` 不能为空。")


def _require_path_list(payload: dict, field: str, *, allow_empty: bool = False) -> None:
    value = payload.get(field)
    if not isinstance(value, list):
        raise ValueError(f"GPT 原生输出 frontmatter 字段 `{field}` 必须是列表。")
    if not allow_empty and not value:
        raise ValueError(f"GPT 原生输出 frontmatter 字段 `{field}` 不能为空列表。")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"GPT 原生输出 frontmatter 字段 `{field}` 只能包含非空路径字符串。")


def _require_context_block(payload: dict, field: str, required_keys: tuple[str, ...]) -> None:
    value = payload.get(field)
    if not isinstance(value, dict):
        raise ValueError(f"GPT 原生输出 frontmatter 字段 `{field}` 必须是对象。")
    for key in required_keys:
        item = value.get(key)
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"GPT 原生输出 frontmatter 字段 `{field}.{key}` 不能为空。")


def _validate_generated_markdown(text: str, chapter_num: int) -> None:
    for marker in REQUIRED_OUTPUT_MARKERS:
        if marker not in text:
            raise ValueError(f"GPT 原生输出缺少必需字段：{marker}")
    frontmatter, body_with_heading = _split_frontmatter(text)
    for field in REQUIRED_SCALAR_FIELDS:
        _require_non_empty_text(frontmatter, field)
    if frontmatter.get("写作模型") != EXPECTED_WRITING_MODEL:
        raise ValueError(f"GPT 原生输出 frontmatter 字段 `写作模型` 必须是 `{EXPECTED_WRITING_MODEL}`。")
    if frontmatter.get("chapter_num") != chapter_num:
        raise ValueError(f"GPT 原生输出 chapter_num 必须等于 {chapter_num}。")
    if not isinstance(frontmatter.get("volume_num"), int) or frontmatter["volume_num"] <= 0:
        raise ValueError("GPT 原生输出 volume_num 必须是正整数。")
    _require_path_list(frontmatter, "global_card_refs")
    _require_path_list(frontmatter, "style_card_refs")
    _require_path_list(frontmatter, "project_context_refs", allow_empty=True)
    previous_ref = frontmatter.get("previous_chapter_ref")
    if not isinstance(previous_ref, str):
        raise ValueError("GPT 原生输出 previous_chapter_ref 必须是字符串。")
    _require_context_block(frontmatter, "global_context", REQUIRED_GLOBAL_CONTEXT_FIELDS)
    _require_context_block(frontmatter, "style_context", REQUIRED_STYLE_CONTEXT_FIELDS)
    _require_non_empty_text(frontmatter, "north_star_chapter_brief")

    heading = f"# 第{chapter_num}章｜"
    if heading not in body_with_heading:
        raise ValueError(f"GPT 原生输出缺少章节标题行：{heading}")
    if "[由当前 GPT/LLM 会话创作完整章节正文]" in text or "[请填充完整章节正文]" in text:
        raise ValueError("GPT 原生输出仍包含模板占位正文，禁止写回。")

    body = body_with_heading.split(heading, 1)[-1].strip()
    if len(body) < 800:
        raise ValueError("GPT 原生输出正文过短，疑似不是完整章节。")


def _resolve_drafting_mode(requested_mode: str, chapter_path: Path) -> str:
    if requested_mode != "auto":
        return requested_mode
    if not chapter_path.exists():
        return "chapter_draft"
    raise SystemExit(
        "目标章已存在，auto 模式无法判断应续写、重写还是局部修复；"
        "请显式传入 --mode chapter_rewrite、--mode chapter_continue 或 --mode local_repair。"
    )


def _default_output_dir(project_root: Path, volume_num: int, chapter_num: int) -> Path:
    return project_root / "reports" / "3-Drafting" / "gpt-native" / f"第{volume_num}卷" / f"第{chapter_num}章"


def _load_authored_draft(args: argparse.Namespace) -> str:
    if args.from_stdin:
        return sys.stdin.read()
    if args.draft_file:
        return Path(args.draft_file).read_text(encoding="utf-8")
    raise SystemExit(
        "请由当前 GPT/LLM 会话创作 Markdown 后，通过 --draft-file 或 --from-stdin "
        "交给脚本校验落盘；若只需上下文包，请使用 --dry-run。"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate and write a GPT-native chapter manuscript")
    parser.add_argument("--project-root", help="explicit project root; defaults to active story project")
    parser.add_argument("--chapter", type=int, required=True, help="target chapter number")
    parser.add_argument("--output-dir", help="GPT-native artifact output dir")
    parser.add_argument(
        "--mode",
        choices=("auto", "chapter_draft", "chapter_rewrite", "chapter_continue", "local_repair"),
        default="auto",
        help="drafting mode; auto rewrites existing chapters and drafts missing chapters",
    )
    parser.add_argument("--dry-run", action="store_true", help="only emit the context pack without writing a chapter")
    parser.add_argument("--draft-file", help="Markdown file already authored by the current GPT/LLM session")
    parser.add_argument("--from-stdin", action="store_true", help="read the GPT-authored Markdown from stdin")
    parser.add_argument("--no-writeback", action="store_true", help="validate and save sidecar without writing canonical chapter")
    return parser


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
    north_star_path = project_root / "0-Init" / "north_star.yaml"
    memory_path = project_root / "MEMORY.md"
    chapter_path = drafting_root_md_path(project_root, chapter_num)
    previous_path = find_chapter_file(project_root, chapter_num - 1) if chapter_num > 1 else None
    drafting_mode = _resolve_drafting_mode(args.mode, chapter_path)

    required_files = [book_plan_path, volume_plan_path, chapter_plan_path, north_star_path]
    missing = [str(path) for path in required_files if not path.is_file()]
    if missing:
        raise SystemExit("缺少必需输入：\n- " + "\n- ".join(missing))

    global_cards = _find_refs(project_root, "1-Cards/0-全局卡/**/*.json")
    style_cards = _find_refs(project_root, "1-Cards/1-风格卡/**/*.json")
    if not global_cards:
        raise SystemExit("缺少全局卡：1-Cards/0-全局卡/**/*.json")
    if not style_cards:
        raise SystemExit("缺少风格卡：1-Cards/1-风格卡/**/*.json")

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
    )

    output_dir = Path(args.output_dir) if args.output_dir else _default_output_dir(project_root, volume_num, chapter_num)
    output_dir.mkdir(parents=True, exist_ok=True)
    messages_path = output_dir / f"chapter_{chapter_num}_gpt_native_messages.json"
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
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    generated = _strip_code_fence(_load_authored_draft(args))
    _validate_generated_markdown(generated, chapter_num)

    raw_path = output_dir / f"chapter_{chapter_num}_gpt_authored.md"
    raw_path.write_text(generated + "\n", encoding="utf-8")

    if not args.no_writeback:
        chapter_path.parent.mkdir(parents=True, exist_ok=True)
        chapter_path.write_text(generated + "\n", encoding="utf-8")

    summary = {
        "ok": True,
        "project_root": str(project_root),
        "chapter_path": str(chapter_path),
        "drafting_mode": drafting_mode,
        "messages_path": str(messages_path),
        "gpt_native_output_dir": str(output_dir),
        "authored_draft_path": str(raw_path),
        "writeback": not args.no_writeback,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
