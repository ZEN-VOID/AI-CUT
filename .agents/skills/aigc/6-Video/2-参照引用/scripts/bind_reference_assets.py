#!/usr/bin/env python3
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


@dataclass(frozen=True)
class MatchRequest:
    token: str
    related_subject: str
    preferred_dirs: tuple[str, ...]
    category: str


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


def list_asset_files(assets_root: Path) -> list[Path]:
    if not assets_root.exists():
        return []
    return sorted(path for path in assets_root.rglob("*") if path.is_file() and path.suffix.lower() in IMAGE_EXTS)


def build_group_index(source_data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    payload = ensure_legacy_detail_payload(source_data)
    groups = payload["final_output"]["main_content"]["分镜组列表"]
    return {group["分镜组ID"]: group for group in groups}


def parse_subject_entries(outfit_text: str) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for raw in re.split(r"[；;]", outfit_text or ""):
        item = raw.strip()
        if not item:
            continue
        item = re.sub(r"（.*?）|\(.*?\)", "", item).strip()
        if not item:
            continue
        parts = re.split(r"[-—－]", item, maxsplit=1)
        name = parts[0].strip()
        if name:
            entries.append((name, item))
    return entries


def request_key(packet: dict[str, Any]) -> str:
    shot_ids = packet["meta"].get("source_shot_ids", [])
    if packet["meta"].get("shot_level") == "storyboard_frame" and shot_ids:
        return f"分镜 {shot_ids[0]}"
    return f"分镜组 {packet['meta'].get('group_id', '')}"


def build_match_requests(packet: dict[str, Any], group: dict[str, Any]) -> list[MatchRequest]:
    requests: list[MatchRequest] = []
    group_id = packet["meta"]["group_id"]
    shot_level = packet["meta"]["shot_level"]
    shot_ids = packet["meta"].get("source_shot_ids", [])

    if shot_level == "storyboard_group":
        requests.append(
            MatchRequest(
                token=group_id,
                related_subject=f"分镜组 {group_id}",
                preferred_dirs=("分镜画板/分镜故事板", "分镜画板/漫画"),
                category="storyboard_group",
            )
        )
    if shot_level == "storyboard_frame":
        for shot_id in shot_ids:
            requests.append(
                MatchRequest(
                    token=shot_id,
                    related_subject=f"分镜 {shot_id}",
                    preferred_dirs=("分镜画板/分镜帧",),
                    category="storyboard_frame",
                )
            )

    outfit_text = group.get("组间设计", {}).get("出场角色及穿搭", "")
    seen_keys: set[tuple[str, tuple[str, ...]]] = set()
    for name, full_entry in parse_subject_entries(outfit_text):
        character_request = MatchRequest(
            token=name,
            related_subject=name,
            preferred_dirs=("角色",),
            category="character",
        )
        if (character_request.token, character_request.preferred_dirs) not in seen_keys:
            requests.append(character_request)
            seen_keys.add((character_request.token, character_request.preferred_dirs))

        if full_entry != name:
            costume_request = MatchRequest(
                token=full_entry,
                related_subject=full_entry,
                preferred_dirs=("服装",),
                category="costume",
            )
            if (costume_request.token, costume_request.preferred_dirs) not in seen_keys:
                requests.append(costume_request)
                seen_keys.add((costume_request.token, costume_request.preferred_dirs))

    return requests


def score_candidate(path: Path, assets_root: Path, match_request: MatchRequest) -> int:
    stem_norm = normalize_text(path.stem)
    token_norm = normalize_text(match_request.token)
    if not stem_norm or not token_norm:
        return 0

    score = 0
    if stem_norm == token_norm:
        score = 100
    elif stem_norm.startswith(token_norm) or stem_norm.endswith(token_norm):
        score = 90
    elif token_norm in stem_norm:
        score = 80
    else:
        return 0

    rel_posix = path.relative_to(assets_root).as_posix()
    if any(rel_posix.startswith(prefix) for prefix in match_request.preferred_dirs):
        score += 20
    if match_request.token in path.stem:
        score += 5
    return score


def resolve_match(
    assets_root: Path,
    asset_files: list[Path],
    match_request: MatchRequest,
    selected_paths: set[Path],
) -> tuple[Path | None, str | None]:
    scored: list[tuple[int, Path]] = []
    for asset in asset_files:
        score = score_candidate(asset, assets_root, match_request)
        if score >= 100:
            scored.append((score, asset))

    if not scored:
        return None, None

    scored.sort(key=lambda item: (-item[0], str(item[1])))
    best_score = scored[0][0]
    top_candidates = [path for score, path in scored if score == best_score]
    if len(top_candidates) > 1:
        return None, f"{match_request.related_subject} 命中多个同分候选: {', '.join(path.name for path in top_candidates)}"

    selected = top_candidates[0]
    if selected in selected_paths:
        return None, f"{match_request.related_subject} 命中了已被其他槽位使用的同一路径: {selected.name}"

    return selected, None


def validate_bound_packet(model_payload: dict[str, Any], assets_root: Path) -> list[str]:
    issues: list[str] = []
    refs = model_payload.get("reference_images")
    markers = model_payload.get("image_markers")

    if not isinstance(refs, list):
        issues.append("reference_images 不是数组。")
        return issues
    if not isinstance(markers, list):
        issues.append("image_markers 不是数组。")
        return issues
    if len(refs) != len(markers):
        issues.append("reference_images 与 image_markers 长度不一致。")
        return issues

    seen_refs: set[str] = set()
    for index, (ref, marker) in enumerate(zip(refs, markers), start=1):
        expected_no = f"图{index}"
        if not isinstance(ref, str) or not ref.strip():
            issues.append(f"{expected_no} 的 reference_images 路径为空。")
            continue
        if ref in seen_refs:
            issues.append(f"{expected_no} 的 reference_images 路径重复：{ref}")
        seen_refs.add(ref)
        if not isinstance(marker, dict):
            issues.append(f"{expected_no} 的 marker 不是对象。")
            continue
        expected_keys = ["image_no", "image_ref", "ref_kind", "related_subject"]
        if sorted(marker.keys()) != expected_keys:
            issues.append(f"{expected_no} 的 marker 字段不符合共享模板骨架。")
            continue
        if marker["image_no"] != expected_no:
            issues.append(f"{expected_no} 的 image_no 不连续。")
        if marker["image_ref"] != ref:
            issues.append(f"{expected_no} 的 image_ref 与 reference_images 不一致。")
        if marker["ref_kind"] != "local_path":
            issues.append(f"{expected_no} 的 ref_kind 必须为 local_path。")
        if not str(marker["related_subject"]).strip():
            issues.append(f"{expected_no} 的 related_subject 为空。")

        ref_path = ROOT / ref
        if not ref_path.exists():
            issues.append(f"{expected_no} 的路径不存在：{ref}")
        else:
            try:
                ref_path.relative_to(assets_root)
            except ValueError:
                issues.append(f"{expected_no} 的路径不位于 Assets 内：{ref}")

    return issues


def build_report(
    episode_id: str,
    source_tranche: str,
    packet_reports: list[dict[str, Any]],
    fail_issues: list[str],
) -> str:
    lines = [
        f"# {episode_id} 参照引用报告",
        "",
        f"- source_tranche: {source_tranche}",
        f"- packet_count: {len(packet_reports)}",
        f"- hard_fail_count: {len(fail_issues)}",
        "",
    ]
    if fail_issues:
        lines.extend(["## Hard Failures", ""])
        lines.extend([f"- {issue}" for issue in fail_issues])
        lines.append("")

    lines.append("## Packet Summary")
    lines.append("")
    for packet_report in packet_reports:
        lines.append(f"### {packet_report['packet_key']}")
        lines.append("")
        lines.append(f"- matched_count: {packet_report['matched_count']}")
        lines.append(f"- skipped_count: {packet_report['skipped_count']}")
        lines.append(f"- ambiguous_count: {packet_report['ambiguous_count']}")
        if packet_report["matched"]:
            lines.append("- matched:")
            for item in packet_report["matched"]:
                lines.append(f"  - {item['related_subject']} -> {item['image_ref']}")
        if packet_report["skipped"]:
            lines.append("- skipped:")
            for item in packet_report["skipped"]:
                lines.append(f"  - {item}")
        if packet_report["ambiguous"]:
            lines.append("- ambiguous:")
            for item in packet_report["ambiguous"]:
                lines.append(f"  - {item}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def run(project: str, episode: str, source_tranche: str, input_path: Path | None, dry_run: bool) -> dict[str, Any]:
    project_root = ROOT / "projects" / "aigc" / project
    assets_root = project_root / "Assets"
    if input_path is None:
        input_path = project_root / "6-Video" / source_tranche / episode / f"{episode}.json"
    if not input_path.exists():
        raise FileNotFoundError(f"输入请求 JSON 不存在：{input_path}")

    source_request = read_json(input_path)
    source_request_rel = str(input_path.relative_to(ROOT))
    source_detail_path = ROOT / source_request["source_file"]
    source_detail = read_json(source_detail_path)
    group_index = build_group_index(source_detail)
    asset_files = list_asset_files(assets_root)

    output_payload = copy.deepcopy(source_request)
    output_payload["tranche"] = f"6-Video/2-参照引用/{source_tranche}"
    output_payload["generated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    output_payload["reference_binding"] = {
        "source_request": source_request_rel,
        "assets_root": str(assets_root.relative_to(ROOT)),
        "source_tranche": source_tranche,
        "strict_mode": True,
    }

    packet_reports: list[dict[str, Any]] = []
    hard_failures: list[str] = []

    for packet in output_payload.get("request_packets", []):
        group_id = packet["meta"]["group_id"]
        group = group_index[group_id]
        selected_paths: set[Path] = set()
        match_requests = build_match_requests(packet, group)
        matched: list[dict[str, str]] = []
        skipped: list[str] = []
        ambiguous: list[str] = []

        for match_request in match_requests:
            selected, issue = resolve_match(assets_root, asset_files, match_request, selected_paths)
            if issue:
                ambiguous.append(issue)
                continue
            if selected is None:
                skipped.append(f"{match_request.related_subject} 未命中可用资产")
                continue
            selected_paths.add(selected)
            rel_path = str(selected.relative_to(ROOT))
            matched.append(
                {
                    "image_ref": rel_path,
                    "related_subject": match_request.related_subject,
                    "category": match_request.category,
                }
            )

        packet["model"]["reference_images"] = [item["image_ref"] for item in matched]
        packet["model"]["image_markers"] = [
            {
                "image_ref": item["image_ref"],
                "ref_kind": "local_path",
                "related_subject": item["related_subject"],
                "image_no": f"图{index}",
            }
            for index, item in enumerate(matched, start=1)
        ]

        packet_issue_list = validate_bound_packet(packet["model"], assets_root)
        packet_key_value = request_key(packet)
        if ambiguous:
            hard_failures.extend([f"{packet_key_value}: {issue}" for issue in ambiguous])
        if packet_issue_list:
            hard_failures.extend([f"{packet_key_value}: {issue}" for issue in packet_issue_list])

        packet_reports.append(
            {
                "packet_key": packet_key_value,
                "matched_count": len(matched),
                "skipped_count": len(skipped),
                "ambiguous_count": len(ambiguous),
                "matched": matched,
                "skipped": skipped,
                "ambiguous": ambiguous,
            }
        )

    summary = {
        "project": project,
        "episode": episode,
        "source_tranche": source_tranche,
        "input_request": source_request_rel,
        "assets_root": str(assets_root.relative_to(ROOT)),
        "packet_count": len(packet_reports),
        "matched_packet_count": sum(1 for report in packet_reports if report["matched_count"] > 0),
        "total_reference_count": sum(report["matched_count"] for report in packet_reports),
        "hard_fail_count": len(hard_failures),
        "status": "failed" if hard_failures else "ok",
        "packet_reports": packet_reports,
    }

    if dry_run:
        return summary

    if hard_failures:
        raise ValueError("\n".join(hard_failures))

    output_dir = project_root / "6-Video" / "2-参照引用" / source_tranche / episode
    output_json = output_dir / f"{episode}.json"
    output_manifest = output_dir / "_manifest.json"
    output_report = output_dir / "match-report.md"

    output_payload["reference_binding"]["validation_status"] = "passed"
    output_payload["reference_binding"]["output_report"] = str(output_report.relative_to(ROOT))

    manifest = {
        "episode_id": episode,
        "project_name": project,
        "source_request": source_request_rel,
        "source_tranche": source_tranche,
        "output_json": str(output_json.relative_to(ROOT)),
        "output_report": str(output_report.relative_to(ROOT)),
        "assets_root": str(assets_root.relative_to(ROOT)),
        "packet_count": summary["packet_count"],
        "matched_packet_count": summary["matched_packet_count"],
        "total_reference_count": summary["total_reference_count"],
        "validation_status": "passed",
        "generated_at": output_payload["generated_at"],
        "packet_reports": packet_reports,
    }
    report = build_report(episode, source_tranche, packet_reports, hard_failures)

    write_json(output_json, output_payload)
    write_json(output_manifest, manifest)
    write_text(output_report, report)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="为现有 6-Video 请求 JSON 绑定 Assets 参照图。")
    parser.add_argument("--project", required=True, help="项目名，例如 2049退休老头的快乐生活")
    parser.add_argument("--episode", required=True, help="集名，例如 第1集")
    parser.add_argument(
        "--source-tranche",
        required=True,
        choices=["全能参照", "首帧参照"],
        help="输入请求对象来自哪个 6-Video 子路径",
    )
    parser.add_argument("--input", type=Path, help="可选，直接指定输入请求 JSON 路径")
    parser.add_argument("--dry-run", action="store_true", help="仅打印匹配摘要，不写回文件")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        summary = run(
            project=args.project,
            episode=args.episode,
            source_tranche=args.source_tranche,
            input_path=args.input,
            dry_run=args.dry_run,
        )
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        return 1

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
