#!/usr/bin/env python3
"""Validate the AIGC fine-tuning skill package without generating content."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "CONTEXT.md",
    "README.md",
    "CHANGELOG.md",
    "test-prompts.json",
    "agents/openai.yaml",
    "references/stage-tuning-schemes.md",
    "types/type-map.md",
    "types/stage-output-types.md",
    "templates/output-template.md",
    "review/review-contract.md",
    "scripts/README.md",
]

REQUIRED_STAGES = [
    "2-美学",
    "3-主体",
    "4-编剧",
    "5-导演",
    "6-分镜",
    "7-摄影",
    "8-分组",
    "9-图像",
    "10-画布",
]

REQUIRED_REPORT_SECTIONS = [
    "Target Stage Map",
    "Scheme Selection Matrix",
    "Source Anchor Table",
    "Reference Brief",
    "Iteration Ledger",
    "Comparison Acceptance Matrix",
    "Owner Boundary Check",
    "Owner Handoff Patch",
    "Execution Decision Trace",
    "Reference Execution Matrix",
    "Rule Evidence Map",
    "N/A Justification",
    "Repair Log",
    "Validation Result",
    "Final Verdict",
]

PLACEHOLDER_PATTERN = re.compile(r"\[" + "TO" + "DO" + r"(?::[^\]]*)?\]", re.IGNORECASE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    skill_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (skill_dir / relative).is_file():
            errors.append(f"missing required file: {relative}")

    for path in skill_dir.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".json", ".yaml", ".py"}:
            text = read_text(path)
            if PLACEHOLDER_PATTERN.search(text):
                errors.append(f"unresolved TODO placeholder: {path.relative_to(skill_dir)}")

    skill_md = read_text(skill_dir / "SKILL.md") if (skill_dir / "SKILL.md").is_file() else ""
    for stage in REQUIRED_STAGES:
        if stage not in skill_md:
            errors.append(f"SKILL.md missing stage index marker: {stage}")

    schemes = read_text(skill_dir / "references/stage-tuning-schemes.md") if (skill_dir / "references/stage-tuning-schemes.md").is_file() else ""
    for stage in REQUIRED_STAGES:
        if stage not in schemes:
            errors.append(f"stage-tuning-schemes.md missing stage scheme: {stage}")
    for marker in ["Multi-round plan", "Comparison acceptance", "Review Gate Mapping"]:
        if marker not in schemes:
            errors.append(f"stage-tuning-schemes.md missing marker: {marker}")

    template = read_text(skill_dir / "templates/output-template.md") if (skill_dir / "templates/output-template.md").is_file() else ""
    for section in REQUIRED_REPORT_SECTIONS:
        if f"## {section}" not in template:
            errors.append(f"output template missing section: {section}")

    prompts_path = skill_dir / "test-prompts.json"
    if prompts_path.is_file():
        try:
            prompts = json.loads(read_text(prompts_path))
        except json.JSONDecodeError as exc:
            errors.append(f"test-prompts.json invalid JSON: {exc}")
        else:
            if not isinstance(prompts, list) or len(prompts) < 3:
                errors.append("test-prompts.json must contain at least 3 prompts")
            for index, item in enumerate(prompts, start=1):
                if not isinstance(item, dict):
                    errors.append(f"test prompt {index} is not an object")
                    continue
                for key in ["id", "prompt", "expected"]:
                    if not isinstance(item.get(key), str) or not item[key].strip():
                        errors.append(f"test prompt {index} missing {key}")

    if errors:
        print(json.dumps({"ok": False, "errors": errors}, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps({"ok": True, "skill_dir": str(skill_dir)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
