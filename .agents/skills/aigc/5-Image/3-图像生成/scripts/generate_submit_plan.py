#!/usr/bin/env python3
"""Generate canonical submit-plan / submit-brief for aigc 5-Image/3-图像生成."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tif", ".tiff"}


def find_repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "AGENTS.md").exists():
            return parent
    raise RuntimeError("无法定位仓库根目录。")


ROOT = find_repo_root()
PROJECTS_ROOT = ROOT / "projects" / "aigc"
BUILTIN_ENTRY = "$imagegen / built-in image_gen"
JIMENG_ENTRY = ".agents/skills/cli/dreamina-cli/SKILL.md"
NANO_ENTRY = ".agents/skills/api/anyfast/image/nano-banana/SKILL.md"
REWORK_REF_BINDING = ".agents/skills/aigc/5-Image/2-参照引用/SKILL.md"
REWORK_PROMPT = ".agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def require_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} 必须是对象。")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{label} 必须是数组。")
    return value


def require_non_empty_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} 不能为空。")
    return value.strip()


def has_local_assets(assets_root: Path) -> bool:
    if not assets_root.exists():
        return False
    for path in assets_root.rglob("*"):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
            return True
    return False


def default_input_path(project_root: Path, source_tranche: str, episode: str, provider: str) -> Path:
    provider_candidates = [provider, "dual_mode", "jimeng_cli", "nano_banana"]
    seen: set[Path] = set()
    candidates: list[Path] = []
    for mode in provider_candidates:
        candidate = project_root / "5-Image" / "2-参照引用" / mode / source_tranche / episode / f"{episode}.json"
        if candidate not in seen:
            candidates.append(candidate)
            seen.add(candidate)
    raw_request = project_root / "5-Image" / source_tranche / episode / f"{episode}.json"
    candidates.append(raw_request)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"未找到可提交的请求 JSON：{candidates[-1]}")


def provider_entry(provider: str) -> str:
    if provider == "builtin_image_gen":
        return BUILTIN_ENTRY
    if provider == "jimeng_cli":
        return JIMENG_ENTRY
    if provider == "nano_banana":
        return NANO_ENTRY
    raise ValueError(f"未知 provider: {provider}")


def provider_model_hint(provider: str) -> str:
    if provider == "builtin_image_gen":
        return "GPT-IMAGE-2"
    if provider == "nano_banana":
        return "gemini-3.1-flash-image-preview"
    if provider == "jimeng_cli":
        return "dreamina-cli default"
    return ""


def classify_input_mode(
    packets: list[dict[str, Any]],
    assets_root: Path,
    allow_prompt_only: bool,
) -> tuple[str, dict[str, Any], list[str]]:
    total_refs = 0
    packets_with_refs = 0
    empty_packets = 0
    assumptions: list[str] = []
    for packet in packets:
        model = require_dict(packet.get("model"), "packet.model")
        refs = model.get("reference_images")
        if not isinstance(refs, list):
            raise ValueError("请求对象缺少 `model.reference_images` 数组。")
        total_refs += len(refs)
        if refs:
            packets_with_refs += 1
        else:
            empty_packets += 1

    assets_present = has_local_assets(assets_root)
    if total_refs > 0:
        return (
            "reference_driven",
            {
                "reference_status": "bound",
                "total_reference_count": total_refs,
                "packets_with_refs": packets_with_refs,
                "empty_packets": empty_packets,
                "assets_present": assets_present,
            },
            assumptions,
        )

    if assets_present and not allow_prompt_only:
        raise ValueError(
            "项目 Assets 非空，但当前请求对象没有任何绑定引用。"
            "按 5-Image/3-图像生成 合同，这应先视为 unresolved；"
            "请先完成严格参照绑定，或显式传入 `--allow-prompt-only` 作为人工覆盖。"
        )

    if assets_present and allow_prompt_only:
        assumptions.append("严格参照绑定执行后仍为零引用；本轮以显式 prompt-only override 继续 handoff。")

    return (
        "prompt_only",
        {
            "reference_status": "empty",
            "total_reference_count": 0,
            "packets_with_refs": 0,
            "empty_packets": empty_packets,
            "assets_present": assets_present,
        },
        assumptions,
    )


def summarize_resolution(
    packets: list[dict[str, Any]],
    provider: str,
    input_mode: str,
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for packet in packets:
        meta = require_dict(packet.get("meta"), "packet.meta")
        model = require_dict(packet.get("model"), "packet.model")
        refs = require_list(model.get("reference_images"), "packet.model.reference_images")
        markers = require_list(model.get("image_markers"), "packet.model.image_markers")
        packet_key = str(meta.get("source_shot_ids") or meta.get("group_id") or "<unknown>")
        if input_mode == "prompt_only":
            items.append(
                {
                    "packet_key": packet_key,
                    "reference_count": 0,
                    "resolution_status": "prompt_only",
                    "provider_inputs": [],
                }
            )
            continue

        provider_inputs: list[dict[str, Any]] = []
        for ref, marker in zip(refs, markers):
            ref_obj = require_dict(ref, "reference_images[]")
            marker_obj = require_dict(marker, "image_markers[]")
            variants = require_dict(marker_obj.get("provider_variants"), "provider_variants")
            provider_variant = require_dict(variants.get(provider), f"provider_variants.{provider}")
            provider_inputs.append(
                {
                    "image_ref": ref_obj.get("image_ref", ""),
                    "related_subject": ref_obj.get("related_subject", ""),
                    "input_mode": provider_variant.get("input_mode", ""),
                    "resolution_status": provider_variant.get("resolution_status", ""),
                    "resolved_input": provider_variant.get("resolved_input", ""),
                }
            )
        if provider == "jimeng_cli":
            resolution_status = "ready"
        elif provider == "builtin_image_gen":
            resolution_status = "visible_reference_required"
        else:
            resolution_status = "pending_encode_allowed"
        items.append(
            {
                "packet_key": packet_key,
                "reference_count": len(provider_inputs),
                "resolution_status": resolution_status,
                "provider_inputs": provider_inputs,
            }
        )
    return items


def expected_output_name(packet: dict[str, Any], index: int) -> str:
    meta = require_dict(packet.get("meta"), "packet.meta")
    shot_ids = meta.get("source_shot_ids")
    if isinstance(shot_ids, list) and shot_ids:
        base = str(shot_ids[0])
    else:
        group_id = str(meta.get("group_id") or f"group-{index:03d}")
        display = str(meta.get("shot_display_index") or index)
        base = f"{group_id}-{display}"
    return f"{base}.png"


def build_batch_task(
    packet: dict[str, Any],
    provider: str,
    output_dir: Path,
    index: int,
    input_mode: str,
) -> dict[str, Any]:
    meta = require_dict(packet.get("meta"), "packet.meta")
    model = require_dict(packet.get("model"), "packet.model")
    prompt = require_non_empty_text(packet.get("prompt"), "packet.prompt")
    output_name = expected_output_name(packet, index)
    task_id = output_name.rsplit(".", 1)[0]
    task: dict[str, Any] = {
        "task_id": task_id,
        "provider": provider,
        "provider_model_hint": provider_model_hint(provider),
        "group_id": meta.get("group_id", ""),
        "source_shot_ids": meta.get("source_shot_ids", []),
        "prompt": prompt,
        "prompt_char_count": packet.get("prompt_char_count", len(prompt)),
        "ratio": model.get("ratio", ""),
        "image_size": model.get("image_size", ""),
        "output_format": model.get("output_format", "png"),
        "num_images": model.get("num_images", 1),
        "output_path": str((output_dir / output_name).resolve()),
        "input_mode": input_mode,
        "reference_images": [],
    }
    if provider == "builtin_image_gen":
        task["provider_mode"] = "built-in image_gen"
        task["default_model"] = "GPT-IMAGE-2"

    if input_mode == "reference_driven":
        refs = require_list(model.get("reference_images"), "packet.model.reference_images")
        markers = require_list(model.get("image_markers"), "packet.model.image_markers")
        for ref, marker in zip(refs, markers):
            ref_obj = require_dict(ref, "reference_images[]")
            marker_obj = require_dict(marker, "image_markers[]")
            variants = require_dict(marker_obj.get("provider_variants"), "provider_variants")
            provider_variant = require_dict(variants.get(provider), f"provider_variants.{provider}")
            task["reference_images"].append(
                {
                    "image_ref": ref_obj.get("image_ref", ""),
                    "related_subject": ref_obj.get("related_subject", ""),
                    "input_mode": provider_variant.get("input_mode", ""),
                    "resolution_status": provider_variant.get("resolution_status", ""),
                    "resolved_input": provider_variant.get("resolved_input", ""),
                }
            )
    return task


def build_submit_brief(
    project: str,
    episode: str,
    source_tranche: str,
    provider: str,
    input_mode: str,
    input_path: Path,
    next_entry: str,
    rework_entry: str,
    assumptions: list[str],
    risk_notes: list[str],
) -> str:
    lines = [
        "# 5-Image / 3-图像生成 / submit-brief",
        "",
        f"- project: {project}",
        f"- episode: {episode}",
        f"- source_tranche: {source_tranche}",
        f"- provider: {provider}",
        f"- input_mode: {input_mode}",
        f"- source_request: `{rel(input_path)}`",
        f"- next_entry: `{next_entry}`",
        f"- rework_entry: `{rework_entry}`",
        "",
        "## Boundary",
        "",
        "- 本轮只生成 provider handoff 包，不改 prompt、不重绑引用、不伪装产图成功。",
        "",
        "## Decision",
        "",
        f"- 已锁定 provider=`{provider}`。",
        f"- 本轮执行模式=`{input_mode}`。",
    ]
    if assumptions:
        lines.extend(["", "## Assumptions", ""])
        lines.extend(f"- {item}" for item in assumptions)
    lines.extend(["", "## Risks", ""])
    if risk_notes:
        lines.extend(f"- {item}" for item in risk_notes)
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Next Entry",
            "",
            f"- `{next_entry}`",
            "",
        ]
    )
    return "\n".join(lines)


def run(
    project: str,
    episode: str,
    source_tranche: str,
    provider: str,
    input_path: Path | None,
    allow_prompt_only: bool,
    dry_run: bool,
) -> dict[str, Any]:
    project_root = PROJECTS_ROOT / project
    if not project_root.exists():
        raise FileNotFoundError(f"未找到项目根：{project_root}")

    if input_path is None:
        input_path = default_input_path(project_root, source_tranche, episode, provider)
    if not input_path.exists():
        raise FileNotFoundError(f"输入请求不存在：{input_path}")

    payload = require_dict(read_json(input_path), str(input_path))
    packets = [require_dict(item, "request_packets[]") for item in require_list(payload.get("request_packets"), "request_packets")]
    if not packets:
        raise ValueError("请求对象没有 `request_packets[]`，无法生成 submit-plan。")

    for packet in packets:
        require_dict(packet.get("meta"), "packet.meta")
        require_dict(packet.get("prompt_style"), "packet.prompt_style")
        require_dict(packet.get("model"), "packet.model")
        require_non_empty_text(packet.get("prompt"), "packet.prompt")

    assets_root = project_root / "Assets"
    input_mode, reference_state, assumptions = classify_input_mode(
        packets=packets,
        assets_root=assets_root,
        allow_prompt_only=allow_prompt_only,
    )

    output_dir = project_root / "5-Image" / "3-图像生成" / provider / source_tranche / episode
    batch_path = output_dir / "request-batch.json"
    tasks = [
        build_batch_task(packet, provider, output_dir, index + 1, input_mode)
        for index, packet in enumerate(packets)
    ]
    request_batch = {
        "provider": provider,
        "provider_model_hint": provider_model_hint(provider),
        "project_name": project,
        "episode_id": episode,
        "source_tranche": source_tranche,
        "source_request": rel(input_path),
        "input_mode": input_mode,
        "tasks": tasks,
    }

    next_entry = provider_entry(provider)
    rework_entry = REWORK_REF_BINDING if reference_state["assets_present"] else REWORK_PROMPT
    risk_notes: list[str] = []
    if input_mode == "prompt_only":
        risk_notes.append("当前 handoff 不消费本地参照图；生成一致性将完全依赖 prompt。")
    if provider == "nano_banana" and input_mode == "reference_driven":
        risk_notes.append("nano_banana 引用若仍为 pending_encode，执行层需在提交前完成 BASE64 编码。")
    if provider == "jimeng_cli" and input_mode == "reference_driven":
        risk_notes.append("Dreamina CLI 执行前需保证所有 resolved_input 绝对路径仍可读。")
    if provider == "builtin_image_gen":
        risk_notes.append("内置 image_gen 不走 API / CLI；生成后必须把 `$CODEX_HOME/generated_images/...` 原始文件复制回 output_dir。")

    resolution_summary = summarize_resolution(packets, provider, input_mode)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    expected_outputs = [str((output_dir / expected_output_name(packet, index + 1)).resolve()) for index, packet in enumerate(packets)]
    submit_plan = {
        "project_name": project,
        "episode_id": episode,
        "source_tranche": source_tranche,
        "generated_at": generated_at,
        "provider": provider,
        "provider_entry": next_entry,
        "source_request": {
            "path": rel(input_path),
            "request_kind": "reference_bound_request" if "/2-参照引用/" in rel(input_path) else "prompt_request",
            "packet_count": len(packets),
            "readiness_verdict": "ready",
        },
        "input_mode": input_mode,
        "reference_status": reference_state["reference_status"],
        "provider_input_resolution": {
            "provider": provider,
            "input_mode": input_mode,
            "resolution_summary": resolution_summary,
            "note": "prompt-only handoff" if input_mode == "prompt_only" else "provider-specific references resolved from bound request",
        },
        "execution": (
            {
                "execution_mode": "codex-builtin-imagegen",
                "max_concurrent": 1,
                "provider_skill": "imagegen",
                "provider_mode": "built-in image_gen",
                "default_model": "GPT-IMAGE-2",
                "status": "request_ready",
                "request_sidecar_required": True,
                "project_copy_required": True,
                "generated_source_path": "",
                "request_batch_path": str(batch_path.resolve()),
            }
            if provider == "builtin_image_gen"
            else {
                "execution_mode": "background-batch-concurrent",
                "max_concurrent": 100,
                "status_after_submit": "background_submitted",
                "foreground_override": "--foreground",
                "request_batch_path": str(batch_path.resolve()),
            }
        ),
        "output_dir": str(output_dir.resolve()),
        "expected_outputs": expected_outputs,
        "result_outputs": [],
        "request_batch_path": str(batch_path.resolve()),
        "status": "request_ready" if provider == "builtin_image_gen" else "planned",
        "next_entry": next_entry,
        "rework_entry": rework_entry,
        "risk_notes": risk_notes,
        "operator_assumptions": assumptions,
    }
    brief = build_submit_brief(
        project=project,
        episode=episode,
        source_tranche=source_tranche,
        provider=provider,
        input_mode=input_mode,
        input_path=input_path,
        next_entry=next_entry,
        rework_entry=rework_entry,
        assumptions=assumptions,
        risk_notes=risk_notes,
    )

    summary = {
        "project": project,
        "episode": episode,
        "provider": provider,
        "input_mode": input_mode,
        "packet_count": len(packets),
        "reference_status": reference_state["reference_status"],
        "allow_prompt_only": allow_prompt_only,
        "input_request": rel(input_path),
        "output_dir": str(output_dir.resolve()),
        "next_entry": next_entry,
    }
    if dry_run:
        return summary | {"request_batch_path": str(batch_path.resolve())}

    write_json(batch_path, request_batch)
    write_json(output_dir / "submit-plan.json", submit_plan)
    write_text(output_dir / "submit-brief.md", brief)
    return summary | {
        "request_batch_path": str(batch_path.resolve()),
        "submit_plan": str((output_dir / "submit-plan.json").resolve()),
        "submit_brief": str((output_dir / "submit-brief.md").resolve()),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="为 5-Image/3-图像生成 生成 canonical submit-plan / submit-brief。")
    parser.add_argument("--project", required=True, help="项目名")
    parser.add_argument("--episode", required=True, help="集名，例如 第1集")
    parser.add_argument(
        "--source-tranche",
        required=True,
        choices=["分镜故事板", "分镜帧", "漫画"],
        help="当前请求对象来自哪个 5-Image 子路径",
    )
    parser.add_argument(
        "--provider",
        default="builtin_image_gen",
        choices=["builtin_image_gen", "jimeng_cli", "nano_banana"],
        help="锁定唯一 provider；默认 builtin_image_gen（内置 image_gen / GPT-IMAGE-2）",
    )
    parser.add_argument("--input", type=Path, help="可选，直接指定输入请求 JSON")
    parser.add_argument("--allow-prompt-only", action="store_true", help="在 Assets 非空但严格绑定为空时，显式允许 prompt-only handoff")
    parser.add_argument("--dry-run", action="store_true", help="只打印计划摘要，不写回文件")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        summary = run(
            project=args.project,
            episode=args.episode,
            source_tranche=args.source_tranche,
            provider=args.provider,
            input_path=args.input,
            allow_prompt_only=args.allow_prompt_only,
            dry_run=args.dry_run,
        )
    except Exception as exc:  # noqa: BLE001
        print(str(exc))
        return 1
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
