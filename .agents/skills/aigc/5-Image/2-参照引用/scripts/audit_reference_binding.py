#!/usr/bin/env python3
"""Audit 5-Image reference binding outputs.

This script catches the failure class where broad string matching binds too many
ambiguous local assets while the provider-specific slots still look valid.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


GENERIC_TOKENS = {
    "门",
    "灯",
    "墙",
    "水",
    "床",
    "地面",
    "卫生间",
    "吊顶",
    "楼道",
    "洗手池",
    "门板",
}


def load_json(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def strip_prop_prefix(name: str) -> str:
    return re.sub(r"^prop-\d+-", "", name)


def is_probably_base64(value: str) -> bool:
    if not value:
        return False
    if value.startswith("data:image/"):
        return True
    if len(value) < 128:
        return False
    return bool(re.fullmatch(r"[A-Za-z0-9+/=\s]+", value))


def rel_or_abs_exists(path_value: str, root: Path) -> bool:
    path = Path(path_value)
    if path.is_absolute():
        return path.exists()
    return (root / path).exists()


def audit_packet(packet: dict[str, Any], root: Path, max_refs_per_group: int) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    meta = packet.get("meta") if isinstance(packet.get("meta"), dict) else {}
    group_id = meta.get("group_id", "<unknown-group>")
    model = packet.get("model") if isinstance(packet.get("model"), dict) else {}
    refs = model.get("reference_images") if isinstance(model.get("reference_images"), list) else []
    markers = model.get("image_markers") if isinstance(model.get("image_markers"), list) else []

    if len(refs) != len(markers):
        errors.append(f"{group_id}: reference_images/image_markers count mismatch {len(refs)} != {len(markers)}")

    if len(refs) > max_refs_per_group:
        warnings.append(f"{group_id}: high reference count {len(refs)} > {max_refs_per_group}")

    ref_paths = [item.get("image_ref") for item in refs if isinstance(item, dict)]
    marker_paths = [item.get("image_ref") for item in markers if isinstance(item, dict)]
    if ref_paths != marker_paths:
        errors.append(f"{group_id}: image_ref order or values do not match between reference_images and image_markers")

    exact_generic: list[str] = []
    token_hits: dict[str, list[str]] = {}

    for ref in refs:
        if not isinstance(ref, dict):
            errors.append(f"{group_id}: reference item is not object")
            continue
        image_ref = str(ref.get("image_ref") or "")
        subject = str(ref.get("related_subject") or ref.get("source_asset_name") or "")
        subject_no_prefix = strip_prop_prefix(subject)

        if not image_ref:
            errors.append(f"{group_id}: reference missing image_ref")
        elif not rel_or_abs_exists(image_ref, root):
            errors.append(f"{group_id}: reference path does not exist: {image_ref}")

        if subject_no_prefix in GENERIC_TOKENS:
            exact_generic.append(subject)
        for token in GENERIC_TOKENS:
            if token in subject_no_prefix:
                token_hits.setdefault(token, []).append(subject)

    for token, subjects in sorted(token_hits.items()):
        unique_subjects = sorted(set(subjects))
        if len(unique_subjects) > 1:
            warnings.append(f"{group_id}: ambiguous token `{token}` matched {unique_subjects}")

    if exact_generic:
        warnings.append(f"{group_id}: generic exact subjects bound directly: {sorted(set(exact_generic))}")

    for marker in markers:
        if not isinstance(marker, dict):
            errors.append(f"{group_id}: marker item is not object")
            continue
        image_ref = str(marker.get("image_ref") or "")
        variants = marker.get("provider_variants") if isinstance(marker.get("provider_variants"), dict) else {}
        jimeng = variants.get("jimeng_cli") if isinstance(variants.get("jimeng_cli"), dict) else {}
        nano = variants.get("nano_banana") if isinstance(variants.get("nano_banana"), dict) else {}

        resolved = str(jimeng.get("resolved_input") or "")
        if jimeng.get("input_mode") != "local_path":
            errors.append(f"{group_id}: jimeng_cli input_mode is not local_path for {image_ref}")
        if jimeng.get("resolution_status") != "ready":
            errors.append(f"{group_id}: jimeng_cli resolution_status is not ready for {image_ref}")
        if not resolved or not Path(resolved).is_absolute() or not Path(resolved).exists():
            errors.append(f"{group_id}: jimeng_cli resolved_input is not an existing absolute path for {image_ref}")

        if nano.get("input_mode") != "base64":
            errors.append(f"{group_id}: nano_banana input_mode is not base64 for {image_ref}")
        nano_resolved = str(nano.get("resolved_input") or "")
        nano_status = str(nano.get("resolution_status") or "")
        if nano_status == "pending_encode" and nano_resolved:
            errors.append(f"{group_id}: nano_banana pending_encode must not carry resolved_input for {image_ref}")
        if nano_status != "pending_encode" and is_probably_base64(nano_resolved):
            warnings.append(f"{group_id}: nano_banana already carries base64-like data for {image_ref}")

    return errors, warnings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit aigc 5-Image/2-参照引用 binding outputs")
    parser.add_argument("--bound-json", required=True, help="Bound 第N集.json path")
    parser.add_argument("--manifest", help="Optional _manifest.json path")
    parser.add_argument("--assets", help="Optional selected-4-design-assets.json path")
    parser.add_argument("--root", default=".", help="Repository root for resolving relative paths")
    parser.add_argument("--max-refs-per-group", type=int, default=6, help="Warn when a group binds more refs")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(args.root).resolve()
    bound_path = Path(args.bound_json)
    manifest_path = Path(args.manifest) if args.manifest else None
    assets_path = Path(args.assets) if args.assets else None

    errors: list[str] = []
    warnings: list[str] = []

    try:
        bound = load_json(bound_path)
    except Exception as exc:
        print(f"ERROR: cannot read bound json: {exc}")
        return 2

    packets = bound.get("request_packets") if isinstance(bound.get("request_packets"), list) else []
    if not packets:
        errors.append("bound json has no request_packets[]")

    if not bound.get("next_entry"):
        errors.append("bound json missing top-level next_entry")

    if manifest_path:
        try:
            manifest = load_json(manifest_path)
            if not manifest.get("next_entry"):
                errors.append("manifest missing next_entry")
        except Exception as exc:
            errors.append(f"cannot read manifest: {exc}")

    if assets_path:
        try:
            assets_doc = load_json(assets_path)
            assets = assets_doc.get("assets") if isinstance(assets_doc, dict) else []
            missing_assets = [
                item.get("asset_path")
                for item in assets
                if isinstance(item, dict)
                and item.get("selected")
                and item.get("asset_path")
                and not rel_or_abs_exists(str(item["asset_path"]), root)
            ]
            if missing_assets:
                errors.append(f"selected assets missing on disk: {missing_assets[:8]}")
        except Exception as exc:
            warnings.append(f"cannot read assets manifest: {exc}")

    for packet in packets:
        packet_errors, packet_warnings = audit_packet(packet, root, args.max_refs_per_group)
        errors.extend(packet_errors)
        warnings.extend(packet_warnings)

    for item in warnings:
        print(f"WARNING: {item}")
    for item in errors:
        print(f"ERROR: {item}")

    if errors or (args.strict and warnings):
        print(
            json.dumps(
                {
                    "status": "fail",
                    "error_count": len(errors),
                    "warning_count": len(warnings),
                    "strict": args.strict,
                },
                ensure_ascii=False,
            )
        )
        return 1

    print(
        json.dumps(
            {
                "status": "pass",
                "error_count": 0,
                "warning_count": len(warnings),
                "strict": args.strict,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
