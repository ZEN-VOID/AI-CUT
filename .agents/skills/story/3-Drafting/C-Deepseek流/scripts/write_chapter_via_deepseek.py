#!/usr/bin/env python3
"""
Bridge script for `story/3-Drafting/C-Deepseek流`.

It assembles the chapter context pack locally, then delegates the actual
chapter-file creation to `.agents/skills/api/deepseek`.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
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
DEEPSEEK_SCRIPT = SKILLS_ROOT / "api" / "deepseek" / "scripts" / "deepseek_chat.py"
SYSTEM_PROMPT_PATH = DRAFTING_DIR / "templates" / "deepseek-system-prompt.md"
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
    "story_name",
    "volume_num",
    "chapter_num",
    "chapter_title",
    "planning_global_ref",
    "planning_volume_ref",
    "planning_chapter_ref",
    "写作模型",
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
REQUIRED_GLOBAL_CONTEXT_KEYS = ("worldview_summary", "rule_pressure", "faction_or_system_pressure")
REQUIRED_STYLE_CONTEXT_KEYS = ("tone_summary", "prose_summary", "dialogue_summary")
EXPECTED_WRITING_MODEL = "Deepseek"
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
    rendered = rendered.replace("{{chapter_body}}", "[请填充完整章节正文]")
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
        "请根据以下导入上下文，生成符合项目风格与当前章规划的完整小说章节 Markdown 文件。"
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
    if not text.startswith("---\n"):
        raise ValueError("DeepSeek 返回内容缺少 YAML frontmatter 起始 `---`。")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, flags=re.S)
    if not match:
        raise ValueError("DeepSeek 返回内容缺少完整 YAML frontmatter 闭合 `---`。")
    try:
        payload = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"DeepSeek 返回 frontmatter 不是合法 YAML：{exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("DeepSeek 返回 frontmatter 必须是 YAML 对象。")
    return payload, match.group(2)


def _require_non_empty(value: object, field_name: str) -> None:
    if value is None:
        raise ValueError(f"DeepSeek 返回 frontmatter 字段为空：{field_name}")
    if isinstance(value, str) and not value.strip():
        raise ValueError(f"DeepSeek 返回 frontmatter 字段为空：{field_name}")
    if isinstance(value, (list, dict)) and not value:
        raise ValueError(f"DeepSeek 返回 frontmatter 字段为空：{field_name}")


def _validate_path_list(payload: dict, field_name: str, *, allow_empty: bool = False) -> None:
    value = payload.get(field_name)
    if not isinstance(value, list):
        raise ValueError(f"DeepSeek 返回 frontmatter 字段必须是列表：{field_name}")
    if not allow_empty and not value:
        raise ValueError(f"DeepSeek 返回 frontmatter 字段不能为空列表：{field_name}")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"DeepSeek 返回 frontmatter 字段只能包含非空路径字符串：{field_name}")


def _validate_nested_context(payload: dict, field_name: str, keys: Iterable[str]) -> None:
    value = payload.get(field_name)
    if not isinstance(value, dict):
        raise ValueError(f"DeepSeek 返回 frontmatter 字段必须是对象：{field_name}")
    for key in keys:
        _require_non_empty(value.get(key), f"{field_name}.{key}")


def _validate_generated_markdown(text: str, chapter_num: int) -> None:
    payload, body = _split_frontmatter(text)
    for marker in REQUIRED_OUTPUT_MARKERS:
        if marker not in payload:
            raise ValueError(f"DeepSeek 返回内容缺少必需字段：{marker}")
        if marker not in {"project_context_refs", "previous_chapter_ref"}:
            _require_non_empty(payload.get(marker), marker)

    if int(payload.get("chapter_num") or 0) != chapter_num:
        raise ValueError(f"DeepSeek 返回 chapter_num 与目标章不一致：{payload.get('chapter_num')}")
    if payload.get("写作模型") != EXPECTED_WRITING_MODEL:
        raise ValueError(f"DeepSeek 返回 frontmatter 字段 `写作模型` 必须是 `{EXPECTED_WRITING_MODEL}`。")
    if not isinstance(payload.get("volume_num"), int) or payload["volume_num"] <= 0:
        raise ValueError("DeepSeek 返回 volume_num 必须是正整数。")
    if not isinstance(payload.get("previous_chapter_ref"), str):
        raise ValueError("DeepSeek 返回 previous_chapter_ref 必须是字符串。")

    _validate_path_list(payload, "global_card_refs")
    _validate_path_list(payload, "style_card_refs")
    _validate_path_list(payload, "project_context_refs", allow_empty=True)
    _validate_nested_context(payload, "global_context", REQUIRED_GLOBAL_CONTEXT_KEYS)
    _validate_nested_context(payload, "style_context", REQUIRED_STYLE_CONTEXT_KEYS)
    _require_non_empty(payload.get("north_star_chapter_brief"), "north_star_chapter_brief")

    heading = f"# 第{chapter_num}章｜"
    if heading not in body:
        raise ValueError(f"DeepSeek 返回内容缺少章节标题行：{heading}")
    body_after_heading = body.split(heading, 1)[1]
    if len(re.sub(r"\s+", "", body_after_heading)) < MIN_BODY_CHARS:
        raise ValueError(f"DeepSeek 返回正文过短，低于最小完整度门槛 {MIN_BODY_CHARS} 字。")
    for marker in PLACEHOLDER_MARKERS:
        if marker in text:
            raise ValueError(f"DeepSeek 返回内容仍包含模板占位符：{marker}")
    for pattern in PLANNING_LANGUAGE_PATTERNS:
        if pattern in body_after_heading:
            raise ValueError(f"DeepSeek 返回正文仍保留 planning 语言：{pattern}")


def _default_output_dir(project_root: Path, volume_num: int, chapter_num: int) -> Path:
    return project_root / "reports" / "3-Drafting" / "deepseek" / f"第{volume_num}卷" / f"第{chapter_num}章"


def _run_deepseek(messages_path: Path, output_dir: Path, *, max_tokens: int, stream: bool, timeout: int) -> str:
    cmd = [
        sys.executable,
        str(DEEPSEEK_SCRIPT),
        "--messages-file",
        str(messages_path),
        "--task-kind",
        "temp",
        "--project-name",
        "story-drafting-deepseek",
        "--output-dir",
        str(output_dir),
        "--thinking",
        "enabled",
        "--reasoning-effort",
        "high",
        "--max-tokens",
        str(max_tokens),
        "--timeout",
        str(timeout),
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
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "DeepSeek 调用失败。")
    return proc.stdout.strip()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write chapter manuscript via DeepSeek")
    parser.add_argument("--project-root", help="explicit project root; defaults to active story project")
    parser.add_argument("--chapter", type=int, required=True, help="target chapter number")
    parser.add_argument("--output-dir", help="provider artifact output dir")
    parser.add_argument("--max-tokens", type=int, default=12000)
    parser.add_argument("--timeout", type=int, default=240, help="DeepSeek request timeout in seconds")
    parser.add_argument(
        "--mode",
        choices=("auto", "chapter_draft", "chapter_rewrite", "chapter_continue", "local_repair"),
        default="auto",
        help="drafting mode; auto rewrites existing chapters and drafts missing chapters",
    )
    parser.add_argument("--stream", action="store_true", help="use stream mode when calling provider")
    parser.add_argument("--dry-run", action="store_true", help="only emit the messages pack without calling DeepSeek")
    parser.add_argument("--no-writeback", action="store_true", help="call DeepSeek but do not write back the chapter file")
    parser.add_argument("--force", action="store_true", help="allow writeback over an existing canonical chapter file")
    return parser


def _resolve_drafting_mode(args: argparse.Namespace, chapter_path: Path) -> str:
    target_exists = chapter_path.exists()
    writeback_enabled = not (args.dry_run or args.no_writeback)
    if args.mode == "auto":
        if target_exists and writeback_enabled:
            raise SystemExit(
                "目标章已存在，auto 模式禁止直接覆盖。请显式传入 "
                "--mode chapter_rewrite / chapter_continue / local_repair，并加 --force；"
                "或使用 --dry-run / --no-writeback。"
            )
        return "chapter_rewrite" if target_exists else "chapter_draft"

    if args.mode == "chapter_draft" and target_exists and writeback_enabled:
        raise SystemExit("目标章已存在，不能用 chapter_draft 覆盖；请改用 rewrite/continue/local_repair 并加 --force。")
    if args.mode in {"chapter_rewrite", "chapter_continue", "local_repair"} and not target_exists:
        raise SystemExit(f"目标章不存在，不能执行 {args.mode}；请改用 chapter_draft。")
    if target_exists and writeback_enabled and not args.force:
        raise SystemExit("目标章已存在，正式写回必须显式传入 --force。")
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
    north_star_path = project_root / "0-Init" / "north_star.yaml"
    memory_path = project_root / "MEMORY.md"
    chapter_path = drafting_root_md_path(project_root, chapter_num)
    previous_path = find_chapter_file(project_root, chapter_num - 1) if chapter_num > 1 else None
    drafting_mode = _resolve_drafting_mode(args, chapter_path)

    required_files = [book_plan_path, volume_plan_path, chapter_plan_path, north_star_path, memory_path]
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
        memory_path=memory_path,
        global_cards=global_cards,
        style_cards=style_cards,
        project_context_files=project_context_files,
        previous_path=previous_path,
        current_path=chapter_path,
    )

    output_dir = Path(args.output_dir) if args.output_dir else _default_output_dir(project_root, volume_num, chapter_num)
    output_dir.mkdir(parents=True, exist_ok=True)
    messages_path = output_dir / f"chapter_{chapter_num}_deepseek_messages.json"
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
            "memory_ref": _rel(memory_path, project_root),
            "project_context_refs": [_rel(path, project_root) for path in project_context_files],
            "provider": "deepseek-v4-pro",
            "thinking": "enabled",
            "reasoning_effort": "high",
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    generated = _strip_code_fence(
        _run_deepseek(
            messages_path,
            output_dir,
            max_tokens=args.max_tokens,
            stream=args.stream,
            timeout=args.timeout,
        )
    )
    _validate_generated_markdown(generated, chapter_num)

    raw_path = output_dir / f"chapter_{chapter_num}_generated.md"
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
        "provider_output_dir": str(output_dir),
        "generated_preview_path": str(raw_path),
        "writeback": not args.no_writeback,
        "provider": "deepseek-v4-pro",
        "thinking": "enabled",
        "reasoning_effort": "high",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
