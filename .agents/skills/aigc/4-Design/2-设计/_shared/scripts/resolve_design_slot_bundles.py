#!/usr/bin/env python3
"""Resolve current-round 4-Design/2-设计 targets into slot bundles."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def find_repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "AGENTS.md").exists():
            return parent
    raise RuntimeError("无法定位仓库根目录。")


ROOT = find_repo_root()
CONTRACT_PATH = ROOT / ".agents/skills/aigc/4-Design/2-设计/_shared/design-slot-review-contract.md"

BUNDLE_REGISTRY = {
    "场景": [
        {
            "bundle_id": "SCENE-BUNDLE-01-story-world",
            "default_patch_target": "canonical_truth",
            "review_focus": "story-world",
        },
        {
            "bundle_id": "SCENE-BUNDLE-02-design-structure",
            "default_patch_target": "canonical_truth",
            "review_focus": "design-structure",
        },
        {
            "bundle_id": "SCENE-BUNDLE-03-cinematography",
            "default_patch_target": "canonical_truth",
            "review_focus": "cinematography",
        },
        {
            "bundle_id": "SCENE-BUNDLE-04-prompt-cleanliness",
            "default_patch_target": "canonical_prompt_slots",
            "review_focus": "prompt-cleanliness",
        },
    ],
    "角色": [
        {
            "bundle_id": "ROLE-BUNDLE-01-identity-pressure",
            "default_patch_target": "canonical_truth",
            "review_focus": "identity-pressure",
        },
        {
            "bundle_id": "ROLE-BUNDLE-02-visual-system",
            "default_patch_target": "canonical_truth",
            "review_focus": "visual-system",
        },
        {
            "bundle_id": "ROLE-BUNDLE-03-camera-readability",
            "default_patch_target": "canonical_truth",
            "review_focus": "camera-readability",
        },
        {
            "bundle_id": "ROLE-BUNDLE-04-prompt-cleanliness",
            "default_patch_target": "canonical_prompt_slots",
            "review_focus": "prompt-cleanliness",
        },
    ],
    "道具": [
        {
            "bundle_id": "PROP-BUNDLE-01-story-function",
            "default_patch_target": "canonical_truth",
            "review_focus": "story-function",
        },
        {
            "bundle_id": "PROP-BUNDLE-02-design-structure",
            "default_patch_target": "canonical_truth",
            "review_focus": "design-structure",
        },
        {
            "bundle_id": "PROP-BUNDLE-03-photography-readability",
            "default_patch_target": "canonical_truth",
            "review_focus": "photography-readability",
        },
        {
            "bundle_id": "PROP-BUNDLE-04-prompt-cleanliness",
            "default_patch_target": "canonical_prompt_slots",
            "review_focus": "prompt-cleanliness",
        },
    ],
}

DOMAIN_ALIASES = {
    "scene": "场景",
    "character": "角色",
    "prop": "道具",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="把 4-Design/2-设计 当前轮输出解析成 slot bundle。")
    parser.add_argument("--domain", required=True, help="场景 / 角色 / 道具，也接受 scene / character / prop")
    parser.add_argument("--canonical", required=True, help="canonical truth 文件路径")
    parser.add_argument("--projection", required=True, help="projection 文件路径")
    parser.add_argument("--manifest", required=True, help="_manifest.json 路径")
    parser.add_argument("--validation-report", help="可选，阶段 validation-report.md 路径")
    parser.add_argument("--allow-missing", action="store_true", help="允许 target files 尚未落盘，仅输出解析骨架")
    return parser.parse_args()


def normalize_domain(value: str) -> str:
    normalized = DOMAIN_ALIASES.get(value.strip().lower(), value.strip())
    if normalized not in BUNDLE_REGISTRY:
        raise ValueError(f"未知 domain: {value}")
    return normalized


def resolve_target_file(path_value: str, label: str, allow_missing: bool) -> str:
    path = Path(path_value)
    if not path.is_absolute():
        path = (ROOT / path).resolve()
    if not allow_missing and not path.exists():
        raise FileNotFoundError(f"{label} 不存在：{path}")
    return str(path)


def build_target_files(args: argparse.Namespace) -> dict[str, Any]:
    target_files: dict[str, Any] = {
        "canonical_truth": resolve_target_file(args.canonical, "canonical", args.allow_missing),
        "projection": resolve_target_file(args.projection, "projection", args.allow_missing),
        "manifest": resolve_target_file(args.manifest, "manifest", args.allow_missing),
    }
    if args.validation_report:
        target_files["validation_report"] = resolve_target_file(
            args.validation_report,
            "validation-report",
            args.allow_missing,
        )
    else:
        target_files["validation_report"] = None
    return target_files


def build_slot_bundles(domain: str, target_files: dict[str, Any]) -> list[dict[str, Any]]:
    resolved_targets = [
        target_files["canonical_truth"],
        target_files["projection"],
        target_files["manifest"],
    ]
    if target_files.get("validation_report"):
        resolved_targets.append(target_files["validation_report"])
    return [
        {
            "bundle_id": bundle["bundle_id"],
            "domain": domain,
            "default_patch_target": bundle["default_patch_target"],
            "review_focus": bundle["review_focus"],
            "target_files": resolved_targets,
        }
        for bundle in BUNDLE_REGISTRY[domain]
    ]


def main() -> int:
    args = parse_args()
    domain = normalize_domain(args.domain)
    target_files = build_target_files(args)
    payload = {
        "contract_path": str(CONTRACT_PATH),
        "domain": domain,
        "target_files": target_files,
        "slot_bundles": build_slot_bundles(domain, target_files),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
