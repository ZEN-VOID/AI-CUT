#!/usr/bin/env python3
"""Validate grouped manga script markdown files for comic stage 1 handoff."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
TITLE_RE = re.compile(r"^#\s*第(\d+)组\s*$", re.MULTILINE)
FILENAME_RE = re.compile(r"^第(\d+)组\.md$")
SECTION_RE = re.compile(
    r"^【(?P<name>[^】]+)】\n(?P<body>.*?)(?=^【[^】]+】\n|\Z)",
    re.MULTILINE | re.DOTALL,
)

REQUIRED_FRONTMATTER = {
    "项目名",
    "组号",
    "分组口径",
    "估算原文字数",
    "尾组决议",
    "source_type",
    "truth_boundary",
    "adaptation_posture",
    "type_stack_summary",
    "type_stack_active_packs",
    "type_pack_projection_script_adaptation",
    "type_pack_projection_nine_blade",
}

REQUIRED_SECTIONS = {
    "本组跨度",
    "边界判定",
    "漫剧正文",
    "组末钩子",
}

ALLOWED_TAIL_DECISIONS = {
    "single_group",
    "normal",
    "merged_into_previous",
    "standalone_tail",
}

ALLOWED_SOURCE_TYPES = {
    "text",
    "image",
    "video",
    "news_event",
    "hot_search",
    "mixed",
}

ALLOWED_TRUTH_BOUNDARIES = {
    "faithful",
    "inspired_by",
    "free_reimagining",
}

ALLOWED_ADAPTATION_POSTURES = {
    "faithful-core",
    "comic-first",
    "spectacle-first",
}


def _parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, ["missing frontmatter block delimited by ---"]
    frontmatter: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            errors.append(f"invalid frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip()
    return frontmatter, errors


def _parse_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    for match in SECTION_RE.finditer(text):
        sections[match.group("name").strip()] = match.group("body").strip()
    return sections


def _non_ws_len(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"{path}: file does not exist"]
    if not path.is_file():
        return [f"{path}: path is not a file"]

    text = path.read_text(encoding="utf-8")
    frontmatter, fm_errors = _parse_frontmatter(text)
    errors.extend(f"{path}: {msg}" for msg in fm_errors)
    sections = _parse_sections(text)

    filename_match = FILENAME_RE.match(path.name)
    if not filename_match:
        errors.append(f"{path}: filename must match 第N组.md")
        file_group_number = None
    else:
        file_group_number = filename_match.group(1)

    title_match = TITLE_RE.search(text)
    if not title_match:
        errors.append(f"{path}: missing markdown title '# 第N组'")
        title_group_number = None
    else:
        title_group_number = title_match.group(1)

    missing_frontmatter = REQUIRED_FRONTMATTER - set(frontmatter)
    for key in sorted(missing_frontmatter):
        errors.append(f"{path}: missing frontmatter field '{key}'")

    missing_sections = REQUIRED_SECTIONS - set(sections)
    for section in sorted(missing_sections):
        errors.append(f"{path}: missing section '【{section}】'")

    if "组号" in frontmatter:
        group_value = frontmatter["组号"]
        match = re.fullmatch(r"第(\d+)组", group_value)
        if not match:
            errors.append(f"{path}: frontmatter 组号 must match 第N组")
            fm_group_number = None
        else:
            fm_group_number = match.group(1)
    else:
        fm_group_number = None

    group_numbers = [n for n in (file_group_number, title_group_number, fm_group_number) if n is not None]
    if group_numbers and len(set(group_numbers)) != 1:
        errors.append(f"{path}: filename, title, and frontmatter 组号 must agree")

    estimated_chars = frontmatter.get("估算原文字数")
    if estimated_chars:
        if not estimated_chars.isdigit() or int(estimated_chars) < 1:
            errors.append(f"{path}: 估算原文字数 must be a positive integer")

    tail_decision = frontmatter.get("尾组决议")
    if tail_decision and tail_decision not in ALLOWED_TAIL_DECISIONS:
        errors.append(
            f"{path}: 尾组决议 must be one of {', '.join(sorted(ALLOWED_TAIL_DECISIONS))}"
        )

    source_type = frontmatter.get("source_type")
    if source_type and source_type not in ALLOWED_SOURCE_TYPES:
        errors.append(f"{path}: source_type must be one of {', '.join(sorted(ALLOWED_SOURCE_TYPES))}")

    truth_boundary = frontmatter.get("truth_boundary")
    if truth_boundary and truth_boundary not in ALLOWED_TRUTH_BOUNDARIES:
        errors.append(
            f"{path}: truth_boundary must be one of {', '.join(sorted(ALLOWED_TRUTH_BOUNDARIES))}"
        )

    adaptation_posture = frontmatter.get("adaptation_posture")
    if adaptation_posture and adaptation_posture not in ALLOWED_ADAPTATION_POSTURES:
        errors.append(
            f"{path}: adaptation_posture must be one of {', '.join(sorted(ALLOWED_ADAPTATION_POSTURES))}"
        )

    type_stack_summary = frontmatter.get("type_stack_summary", "")
    if type_stack_summary and _non_ws_len(type_stack_summary) < 4:
        errors.append(f"{path}: type_stack_summary is too short to be useful")

    active_packs = frontmatter.get("type_stack_active_packs", "")
    if active_packs:
        packs = [item.strip() for item in active_packs.split("|") if item.strip()]
        if len(packs) < 2:
            errors.append(f"{path}: type_stack_active_packs must contain at least 2 packs separated by '|'")

    for key in ("type_pack_projection_script_adaptation", "type_pack_projection_nine_blade"):
        value = frontmatter.get(key, "")
        if value and _non_ws_len(value) < 8:
            errors.append(f"{path}: {key} is too short to be useful")

    for section_name in REQUIRED_SECTIONS:
        body = sections.get(section_name, "")
        if body and _non_ws_len(body) < 4:
            errors.append(f"{path}: section '【{section_name}】' is too short")

    body = sections.get("漫剧正文", "")
    if body and _non_ws_len(body) < 80:
        errors.append(f"{path}: section '【漫剧正文】' must contain substantive script content")

    boundary = sections.get("边界判定", "")
    if boundary and frontmatter.get("尾组决议") in {"merged_into_previous", "standalone_tail"}:
        lower_boundary = boundary.lower()
        if "尾组" not in boundary and "并入" not in boundary and "独立" not in boundary:
            errors.append(f"{path}: 边界判定 must explain the tail-group decision")
        if frontmatter.get("尾组决议") == "merged_into_previous" and "并" not in boundary:
            errors.append(f"{path}: 边界判定 should explain why the tail group merged into previous")
        if frontmatter.get("尾组决议") == "standalone_tail" and "独立" not in boundary:
            errors.append(f"{path}: 边界判定 should explain why the tail group stands alone")

    return errors


def _collect_targets(inputs: list[str]) -> list[Path]:
    targets: list[Path] = []
    for raw in inputs:
        path = Path(raw)
        if path.is_dir():
            targets.extend(sorted(path.glob("第*组.md")))
        else:
            targets.append(path)
    return targets


def validate_bundle(targets: list[Path]) -> list[str]:
    errors: list[str] = []
    if not targets:
        return errors

    numbered: list[tuple[int, Path, dict[str, str]]] = []
    for path in targets:
        text = path.read_text(encoding="utf-8")
        frontmatter, _ = _parse_frontmatter(text)
        match = FILENAME_RE.match(path.name)
        if not match:
            continue
        numbered.append((int(match.group(1)), path, frontmatter))

    numbered.sort(key=lambda item: item[0])
    if not numbered:
        return errors

    expected = list(range(1, len(numbered) + 1))
    actual = [item[0] for item in numbered]
    if actual != expected:
        errors.append(
            "bundle: group numbers must be continuous starting at 第1组 "
            f"(found: {', '.join(f'第{n}组' for n in actual)})"
        )

    if len(numbered) == 1:
        _, path, frontmatter = numbered[0]
        if frontmatter.get("尾组决议") != "single_group":
            errors.append(f"{path}: single-file bundle must use 尾组决议=single_group")
        return errors

    for index, (group_number, path, frontmatter) in enumerate(numbered):
        tail_decision = frontmatter.get("尾组决议", "")
        estimated_chars = frontmatter.get("估算原文字数", "")
        estimated_value = int(estimated_chars) if estimated_chars.isdigit() else None
        is_last = index == len(numbered) - 1

        if not is_last and tail_decision != "normal":
            errors.append(f"{path}: non-final groups must use 尾组决议=normal")

        if is_last:
            if tail_decision == "single_group":
                errors.append(f"{path}: final group in a multi-file bundle cannot use 尾组决议=single_group")
            if tail_decision == "standalone_tail" and estimated_value is not None and estimated_value < 700:
                errors.append(f"{path}: standalone_tail requires 估算原文字数 >= 700")
            if tail_decision == "merged_into_previous":
                boundary_text = _parse_sections(path.read_text(encoding='utf-8')).get("边界判定", "")
                if "并" not in boundary_text:
                    errors.append(f"{path}: merged_into_previous must be justified in 【边界判定】")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate grouped manga script markdown files.")
    parser.add_argument("paths", nargs="+", help="One or more grouped script files or directories.")
    args = parser.parse_args()

    targets = _collect_targets(args.paths)
    if not targets:
        print("No grouped manga script files found.", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    for path in targets:
        all_errors.extend(validate_file(path))
    all_errors.extend(validate_bundle(targets))

    if all_errors:
        for error in all_errors:
            print(error, file=sys.stderr)
        return 1

    for path in targets:
        print(f"OK: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
