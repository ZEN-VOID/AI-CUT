#!/usr/bin/env python3
"""Bind conservative Assets references for 5-Image request JSON files."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[6]
AIGC_SHARED_DIR = ROOT / ".agents" / "skills" / "aigc" / "_shared"
if str(AIGC_SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(AIGC_SHARED_DIR))

from detail_root_adapter import ensure_legacy_detail_payload  # noqa: E402

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tif", ".tiff"}
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


@dataclass(frozen=True)
class AssetRecord:
    path: Path
    rel_path: str
    category: str
    source_name: str
    comparable_name: str


@dataclass(frozen=True)
class MatchRequest:
    token: str
    related_subject: str
    category: str
    evidence_level: str
    evidence_field: str


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def normalize_text(text: str) -> str:
    lowered = text.strip().lower()
    return re.sub(r"[\s_\-—－·,，。:：;；/\\|()\[\]{}<>《》“”‘’'\"`]+", "", lowered)


def strip_prop_prefix(name: str) -> str:
    return re.sub(r"^prop-\d+-", "", name)


def is_generic_token(token: str) -> bool:
    comparable = normalize_text(strip_prop_prefix(token))
    return comparable in {normalize_text(item) for item in GENERIC_TOKENS} or len(comparable) <= 1


def list_assets(assets_root: Path) -> list[AssetRecord]:
    records: list[AssetRecord] = []
    if not assets_root.exists():
        return records
    for path in sorted(assets_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in IMAGE_EXTS:
            continue
        rel_parts = path.relative_to(assets_root).parts
        category = rel_parts[0] if rel_parts else ""
        source_name = path.stem
        records.append(
            AssetRecord(
                path=path,
                rel_path=str(path.relative_to(ROOT)),
                category=category,
                source_name=source_name,
                comparable_name=strip_prop_prefix(source_name),
            )
        )
    return records


def parse_subject_entries(outfit_text: str) -> list[str]:
    names: list[str] = []
    for raw in re.split(r"[；;]", outfit_text or ""):
        item = re.sub(r"（.*?）|\(.*?\)", "", raw).strip()
        if not item:
            continue
        name = re.split(r"[-—－]", item, maxsplit=1)[0].strip()
        if name and name not in names:
            names.append(name)
    return names


def build_group_index(source_data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    payload = ensure_legacy_detail_payload(source_data)
    groups = payload["final_output"]["main_content"]["分镜组列表"]
    return {group["分镜组ID"]: group for group in groups}


def explicit_marker_requests(packet: dict[str, Any]) -> list[MatchRequest]:
    model = packet.get("model") if isinstance(packet.get("model"), dict) else {}
    markers = model.get("image_markers") if isinstance(model.get("image_markers"), list) else []
    requests: list[MatchRequest] = []
    for marker in markers:
        if not isinstance(marker, dict):
            continue
        subject = str(marker.get("related_subject") or "").strip()
        if not subject or "<" in subject or ">" in subject or is_generic_token(subject):
            continue
        requests.append(
            MatchRequest(
                token=subject,
                related_subject=subject,
                category=str(marker.get("ref_kind") or ""),
                evidence_level="provider_required_ref",
                evidence_field="model.image_markers[].related_subject",
            )
        )
    return requests


def build_match_requests(packet: dict[str, Any], group: dict[str, Any]) -> list[MatchRequest]:
    requests: list[MatchRequest] = []
    meta = packet.get("meta") if isinstance(packet.get("meta"), dict) else {}
    shot_level = str(meta.get("shot_level") or "")
    group_id = str(meta.get("group_id") or "")
    source_shot_ids = meta.get("source_shot_ids") if isinstance(meta.get("source_shot_ids"), list) else []

    if shot_level == "storyboard_group" and group_id:
        requests.append(
            MatchRequest(
                token=group_id,
                related_subject=f"分镜组 {group_id}",
                category="分镜画板",
                evidence_level="explicit_group_id",
                evidence_field="meta.group_id",
            )
        )
    if shot_level == "storyboard_frame":
        for shot_id in source_shot_ids:
            requests.append(
                MatchRequest(
                    token=str(shot_id),
                    related_subject=f"分镜 {shot_id}",
                    category="分镜画板",
                    evidence_level="explicit_shot_id",
                    evidence_field="meta.source_shot_ids[]",
                )
            )

    outfit_text = group.get("组间设计", {}).get("出场角色及穿搭", "")
    for name in parse_subject_entries(outfit_text):
        requests.append(
            MatchRequest(
                token=name,
                related_subject=name,
                category="角色",
                evidence_level="explicit_subject",
                evidence_field="组间设计.出场角色及穿搭",
            )
        )

    requests.extend(explicit_marker_requests(packet))
    deduped: list[MatchRequest] = []
    seen: set[tuple[str, str, str]] = set()
    for request in requests:
        key = (normalize_text(request.token), request.category, request.evidence_field)
        if key not in seen:
            deduped.append(request)
            seen.add(key)
    return deduped


def category_matches(asset: AssetRecord, request: MatchRequest) -> bool:
    if request.category == "分镜画板":
        return asset.category == "分镜画板"
    if request.category in {"角色", "场景", "道具"}:
        return asset.category == request.category
    return asset.category in {"角色", "场景", "道具", "分镜画板"}


def resolve_match(
    assets: list[AssetRecord],
    request: MatchRequest,
    selected_paths: set[Path],
) -> tuple[AssetRecord | None, str | None]:
    token_norm = normalize_text(request.token)
    if not token_norm:
        return None, None
    if request.category != "分镜画板" and is_generic_token(request.token):
        return None, f"{request.related_subject} 是泛词，禁止自动绑定"

    exact = [
        asset
        for asset in assets
        if category_matches(asset, request) and normalize_text(asset.comparable_name) == token_norm
    ]
    if not exact and request.category == "分镜画板":
        exact = [
            asset
            for asset in assets
            if category_matches(asset, request) and token_norm in normalize_text(asset.source_name)
        ]
    if not exact:
        return None, None

    exact = sorted(exact, key=lambda item: item.rel_path)
    if len(exact) > 1:
        return None, f"{request.related_subject} 命中多个候选: {', '.join(item.rel_path for item in exact[:6])}"
    selected = exact[0]
    if selected.path in selected_paths:
        return None, f"{request.related_subject} 重复使用同一路径: {selected.rel_path}"
    return selected, None


def provider_variants(abs_path: Path, provider_mode: str) -> dict[str, Any]:
    variants: dict[str, Any] = {}
    if provider_mode in {"jimeng_cli", "dual_mode"}:
        variants["jimeng_cli"] = {
            "input_mode": "local_path",
            "resolution_status": "ready",
            "resolved_input": str(abs_path),
        }
    if provider_mode in {"nano_banana", "dual_mode"}:
        variants["nano_banana"] = {
            "input_mode": "base64",
            "resolution_status": "pending_encode",
            "resolved_input": "",
        }
    return variants


def validate_packet(packet: dict[str, Any], root: Path) -> list[str]:
    issues: list[str] = []
    model = packet.get("model") if isinstance(packet.get("model"), dict) else {}
    refs = model.get("reference_images")
    markers = model.get("image_markers")
    if not isinstance(refs, list) or not isinstance(markers, list):
        return ["reference_images/image_markers 必须都是数组"]
    if len(refs) != len(markers):
        issues.append("reference_images 与 image_markers 长度不一致")
    for index, (ref, marker) in enumerate(zip(refs, markers), start=1):
        image_no = f"图{index}"
        if not isinstance(ref, dict) or not isinstance(marker, dict):
            issues.append(f"{image_no} 引用或 marker 不是对象")
            continue
        image_ref = str(ref.get("image_ref") or "")
        if marker.get("image_ref") != image_ref:
            issues.append(f"{image_no} image_ref 不一致")
        if marker.get("image_no") != image_no or ref.get("image_no") != image_no:
            issues.append(f"{image_no} 顺序位不连续")
        if not image_ref or not (root / image_ref).exists():
            issues.append(f"{image_no} 路径不存在: {image_ref}")
    return issues


def request_key(packet: dict[str, Any]) -> str:
    meta = packet.get("meta") if isinstance(packet.get("meta"), dict) else {}
    return str(meta.get("group_id") or meta.get("source_shot_ids") or "<unknown>")


def build_report(
    episode: str,
    provider_mode: str,
    source_request: str,
    packet_reports: list[dict[str, Any]],
    hard_failures: list[str],
    next_entry: str,
) -> str:
    lines = [
        "# 5-Image / 2-参照引用 / match-report",
        "",
        f"- episode: {episode}",
        f"- provider_mode: {provider_mode}",
        f"- source_request: {source_request}",
        f"- next_entry: `{next_entry}`",
        f"- hard_fail_count: {len(hard_failures)}",
        "",
    ]
    if hard_failures:
        lines.extend(["## Hard Failures", ""])
        lines.extend(f"- {issue}" for issue in hard_failures)
        lines.append("")

    lines.extend(["## Packet Summary", ""])
    for report in packet_reports:
        lines.append(f"### {report['packet_key']}")
        lines.append("")
        lines.append(f"- bound_count: {len(report['bound_assets'])}")
        lines.append(f"- skipped_count: {len(report['skipped_candidates'])}")
        lines.append(f"- ambiguous_count: {len(report['ambiguous_candidates'])}")
        lines.append("- bound_assets:")
        if report["bound_assets"]:
            for item in report["bound_assets"]:
                lines.append(
                    f"  - {item['image_no']} {item['related_subject']} -> `{item['image_ref']}` "
                    f"({item['evidence_level']}, {item['evidence_field']})"
                )
        else:
            lines.append("  - none")
        lines.append("- ambiguous_candidates:")
        if report["ambiguous_candidates"]:
            lines.extend(f"  - {item}" for item in report["ambiguous_candidates"])
        else:
            lines.append("  - none")
        lines.append("- rejected_candidates:")
        if report["rejected_candidates"]:
            lines.extend(f"  - {item}" for item in report["rejected_candidates"])
        else:
            lines.append("  - none")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def run(
    project: str,
    episode: str,
    source_tranche: str,
    provider_mode: str,
    input_path: Path | None,
    output_dir: Path | None,
    dry_run: bool,
) -> dict[str, Any]:
    project_root = ROOT / "projects" / "aigc" / project
    assets_root = project_root / "Assets"
    if input_path is None:
        input_path = project_root / "5-Image" / source_tranche / episode / f"{episode}.json"
    if not input_path.exists():
        raise FileNotFoundError(f"输入请求 JSON 不存在: {input_path}")

    source_request = read_json(input_path)
    source_request_rel = str(input_path.relative_to(ROOT))
    source_detail = read_json(ROOT / source_request["source_file"])
    group_index = build_group_index(source_detail)
    assets = list_assets(assets_root)
    output_payload = copy.deepcopy(source_request)
    output_payload["tranche"] = f"5-Image/2-参照引用/{provider_mode}/{source_tranche}"
    output_payload["source_request_file"] = source_request_rel
    output_payload["provider_mode"] = provider_mode
    output_payload["generated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    next_entry = ".agents/skills/aigc/5-Image/3-图像生成/SKILL.md"
    output_payload["next_entry"] = next_entry

    hard_failures: list[str] = []
    packet_reports: list[dict[str, Any]] = []
    for packet in output_payload.get("request_packets", []):
        meta = packet.get("meta") if isinstance(packet.get("meta"), dict) else {}
        group_id = str(meta.get("group_id") or "")
        group = group_index.get(group_id, {})
        selected_paths: set[Path] = set()
        bound_assets: list[dict[str, Any]] = []
        skipped: list[str] = []
        ambiguous: list[str] = []

        for request in build_match_requests(packet, group):
            asset, issue = resolve_match(assets, request, selected_paths)
            if issue:
                ambiguous.append(issue)
                continue
            if asset is None:
                skipped.append(f"{request.related_subject} 未命中唯一可用资产")
                continue
            selected_paths.add(asset.path)
            image_no = f"图{len(bound_assets) + 1}"
            bound_assets.append(
                {
                    "image_ref": asset.rel_path,
                    "ref_kind": asset.category,
                    "related_subject": request.related_subject,
                    "image_no": image_no,
                    "source_asset_name": asset.source_name,
                    "evidence_level": request.evidence_level,
                    "evidence_field": request.evidence_field,
                    "provider_variants": provider_variants(asset.path, provider_mode),
                }
            )

        model = packet.setdefault("model", {})
        model["reference_images"] = [
            {
                key: item[key]
                for key in ("image_ref", "ref_kind", "related_subject", "image_no", "source_asset_name")
            }
            for item in bound_assets
        ]
        model["image_markers"] = [
            {
                key: item[key]
                for key in (
                    "image_ref",
                    "ref_kind",
                    "related_subject",
                    "image_no",
                    "provider_variants",
                )
            }
            for item in bound_assets
        ]
        meta["reference_mode"] = "bound" if bound_assets else "empty"
        meta["provider_mode"] = provider_mode

        packet_issues = validate_packet(packet, ROOT)
        packet_key_value = request_key(packet)
        if ambiguous:
            hard_failures.extend(f"{packet_key_value}: {issue}" for issue in ambiguous)
        if packet_issues:
            hard_failures.extend(f"{packet_key_value}: {issue}" for issue in packet_issues)

        packet_reports.append(
            {
                "packet_key": packet_key_value,
                "bound_assets": bound_assets,
                "skipped_candidates": skipped,
                "ambiguous_candidates": ambiguous,
                "rejected_candidates": [],
            }
        )

    summary = {
        "project": project,
        "episode": episode,
        "source_tranche": source_tranche,
        "provider_mode": provider_mode,
        "input_request": source_request_rel,
        "assets_root": str(assets_root.relative_to(ROOT)),
        "packet_count": len(packet_reports),
        "matched_packet_count": sum(1 for report in packet_reports if report["bound_assets"]),
        "total_reference_count": sum(len(report["bound_assets"]) for report in packet_reports),
        "hard_fail_count": len(hard_failures),
        "status": "failed" if hard_failures else "ok",
        "next_entry": next_entry,
        "packet_reports": packet_reports,
    }
    if dry_run:
        return summary
    if hard_failures:
        raise ValueError("\n".join(hard_failures))

    if output_dir is None:
        output_dir = project_root / "5-Image" / "2-参照引用" / provider_mode / source_tranche / episode
    output_json = output_dir / f"{episode}.json"
    output_manifest = output_dir / "_manifest.json"
    output_report = output_dir / "match-report.md"
    manifest = {
        "episode_id": episode,
        "project_name": project,
        "source_request_file": source_request_rel,
        "json_file": str(output_json.relative_to(ROOT)) if output_json.is_relative_to(ROOT) else str(output_json),
        "provider_mode": provider_mode,
        "source_tranche": source_tranche,
        "reference_total": summary["total_reference_count"],
        "validation_status": "passed",
        "next_entry": next_entry,
        "generated_at": output_payload["generated_at"],
        "packet_reports": packet_reports,
    }
    write_json(output_json, output_payload)
    write_json(output_manifest, manifest)
    write_text(output_report, build_report(episode, provider_mode, source_request_rel, packet_reports, hard_failures, next_entry))
    return summary | {"output_json": str(output_json), "output_manifest": str(output_manifest)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="为现有 5-Image 请求 JSON 保守绑定 Assets 参照图。")
    parser.add_argument("--project", required=True, help="项目名")
    parser.add_argument("--episode", required=True, help="集名，例如 第1集")
    parser.add_argument(
        "--source-tranche",
        required=True,
        choices=["分镜故事板", "分镜帧", "漫画"],
        help="输入请求对象来自哪个 5-Image 子路径",
    )
    parser.add_argument(
        "--provider-mode",
        default="dual_mode",
        choices=["jimeng_cli", "nano_banana", "dual_mode"],
        help="引用解析模式",
    )
    parser.add_argument("--input", type=Path, help="可选，直接指定输入请求 JSON 路径")
    parser.add_argument("--output-dir", type=Path, help="可选，覆盖输出目录；主要用于测试")
    parser.add_argument("--dry-run", action="store_true", help="仅打印匹配摘要，不写回文件")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        summary = run(
            project=args.project,
            episode=args.episode,
            source_tranche=args.source_tranche,
            provider_mode=args.provider_mode,
            input_path=args.input,
            output_dir=args.output_dir,
            dry_run=args.dry_run,
        )
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
