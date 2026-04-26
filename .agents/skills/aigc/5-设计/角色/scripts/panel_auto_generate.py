#!/usr/bin/env python3
"""SMART bridge from panel layout JSON packets to built-in imagegen requests."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable, Sequence


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
SMART_MODE_CHOICES = ("auto", "continuous-batch", "single-doc-t2i", "natural-language-t2i", "off")
MAX_DISCOVERED_REFS = 4
MAX_SCAN_DEPTH = 4


def _repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / ".codex").exists():
            return parent
    return Path.cwd()


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _dedupe_strings(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value or "").strip()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result


def _ref_value(item: Any) -> str:
    if isinstance(item, dict):
        return str(item.get("url") or item.get("path") or item.get("image") or "").strip()
    return str(item or "").strip()


def _load_manifest_packet_paths(manifest_path: Path) -> list[Path]:
    payload = _read_json(manifest_path)
    parent = manifest_path.parent
    packet_files: list[str] = []

    outputs = payload.get("outputs")
    if isinstance(outputs, dict):
        packet_files = [str(item) for item in outputs.get("packet_files", []) if str(item).strip()]
        packet_files.extend(str(item) for item in outputs.get("layout_files", []) if str(item).strip())
    elif isinstance(outputs, list):
        packet_files = [str(item) for item in outputs if str(item).strip()]
    if not packet_files:
        packet_files = [str(item) for item in payload.get("output_files", []) if str(item).strip().endswith("-layout.json")]

    resolved: list[Path] = []
    for item in packet_files:
        candidate = Path(item)
        if not candidate.is_absolute():
            candidate = (parent / item).resolve()
        resolved.append(candidate)
    return resolved


def _normalize_token(value: str) -> str:
    return re.sub(r"[\s_\-]+", "", value.strip().lower())


def _subject_tokens(packet: dict[str, Any]) -> list[str]:
    subject = packet.get("subject")
    if not isinstance(subject, dict):
        return []
    keys = (
        "scene_id",
        "scene_key",
        "scene_name",
        "role_id",
        "role_name",
        "costume_id",
        "canonical_label",
        "prop_id",
        "prop_name",
        "identity_badge",
        "canonical_name",
        "output_filename",
    )
    tokens: list[str] = []
    for key in keys:
        value = str(subject.get(key, "")).strip()
        if not value:
            continue
        tokens.append(value)
        normalized = _normalize_token(value)
        if normalized and normalized != value:
            tokens.append(normalized)
    return _dedupe_strings(tokens)


def _resolve_source_path(path_value: str, repo_root: Path) -> Path | None:
    text = str(path_value or "").strip()
    if not text:
        return None
    candidate = Path(text)
    if not candidate.is_absolute():
        candidate = repo_root / candidate
    return candidate if candidate.exists() else None


def _project_name(packet: dict[str, Any]) -> str:
    meta = packet.get("meta")
    if isinstance(meta, dict):
        project_name = str(meta.get("project_name", "")).strip()
        if project_name:
            return project_name
    return str(packet.get("project_name") or "测试")


def _domain_from_packet(packet: dict[str, Any], packet_path: Path) -> str:
    meta = packet.get("meta")
    skill_id = ""
    if isinstance(meta, dict):
        skill_id = str(meta.get("skill_id") or "").strip()
    for domain in ("场景", "角色", "道具", "服装"):
        if f"/{domain}" in skill_id or skill_id.endswith(domain):
            return domain

    parts = packet_path.as_posix().split("/")
    for index, part in enumerate(parts):
        if part == "5-设计" and index + 1 < len(parts):
            return parts[index + 1]
    return ""


def _continuity_roots(packet: dict[str, Any], packet_path: Path, repo_root: Path) -> list[Path]:
    roots: list[Path] = []
    image_generation = packet.get("image_generation")
    if isinstance(image_generation, dict):
        for item in image_generation.get("continuity_source_roots", []) or []:
            resolved = _resolve_source_path(str(item), repo_root)
            if resolved is not None:
                roots.append(resolved if resolved.is_dir() else resolved.parent)

    meta = packet.get("meta")
    if isinstance(meta, dict):
        for key, value in meta.items():
            if not key.startswith("source_"):
                continue
            resolved = _resolve_source_path(str(value), repo_root)
            if resolved is not None:
                roots.append(resolved if resolved.is_dir() else resolved.parent)

    domain = _domain_from_packet(packet, packet_path)
    if domain:
        assets_root = repo_root / "projects" / "aigc" / _project_name(packet) / "Assets" / domain
        if assets_root.exists():
            roots.append(assets_root)

    deduped: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        key = root.resolve().as_posix()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(root)
    return deduped


def _discover_continuity_refs(packet: dict[str, Any], packet_path: Path, repo_root: Path) -> list[str]:
    tokens = _subject_tokens(packet)
    if not tokens:
        return []

    candidates: list[tuple[int, int, str]] = []
    for root in _continuity_roots(packet, packet_path, repo_root):
        if not root.exists():
            continue
        for candidate in root.rglob("*"):
            if not candidate.is_file() or candidate.suffix.lower() not in IMAGE_EXTENSIONS:
                continue
            try:
                depth = len(candidate.relative_to(root).parts)
            except ValueError:
                continue
            if depth > MAX_SCAN_DEPTH:
                continue
            candidate_posix = candidate.as_posix()
            if "/3-面板/" in candidate_posix or "/generated/" in candidate_posix:
                continue
            stem = candidate.stem
            normalized_stem = _normalize_token(stem)
            score = 0
            for token in tokens:
                normalized_token = _normalize_token(token)
                if token and token.lower() in stem.lower():
                    score += 40
                if normalized_token and normalized_token in normalized_stem:
                    score += 60
            if score <= 0:
                continue
            candidates.append((score, depth, candidate.resolve().as_posix()))

    candidates.sort(key=lambda item: (-item[0], item[1], item[2]))
    return _dedupe_strings(item[2] for item in candidates[:MAX_DISCOVERED_REFS])


def _extract_prompt(packet: dict[str, Any]) -> tuple[str, str]:
    image_generation = packet.get("image_generation")
    if isinstance(image_generation, dict):
        prompt_text = str(image_generation.get("prompt_text", "")).strip()
        if prompt_text:
            return prompt_text, "image_generation.prompt_text"

    prompt = str(packet.get("prompt", "")).strip()
    if prompt:
        return prompt, "prompt"

    prompt_payload = packet.get("prompt_payload")
    if isinstance(prompt_payload, dict):
        prompt_text = str(prompt_payload.get("prompt_text", "")).strip()
        if prompt_text:
            return prompt_text, "prompt_payload.prompt_text"

    raise ValueError(f"无法从 packet 提取 prompt: {packet.get('meta', {})}")


def _resolve_requested_mode(requested_mode: str, *, pipeline_context: str, packet_count: int) -> str:
    if requested_mode != "auto":
        return requested_mode
    if pipeline_context == "panel-stage":
        return "continuous-batch"
    return "single-doc-t2i"


def _is_continuity_mode(resolved_mode: str) -> bool:
    return resolved_mode == "continuous-batch"


def _packet_reference_lists(packet: dict[str, Any]) -> tuple[list[str], list[str]]:
    image_generation = packet.get("image_generation")
    packet_refs: list[str] = []
    explicit_refs: list[str] = []
    if isinstance(image_generation, dict):
        packet_refs.extend(_ref_value(item) for item in image_generation.get("reference_images", []) or [])
        explicit_refs.extend(_ref_value(item) for item in image_generation.get("explicit_references", []) or [])
    refs = packet.get("references")
    if isinstance(refs, dict):
        packet_refs.extend(_ref_value(item) for item in refs.get("reference_images", []) or [])
        explicit_refs.extend(_ref_value(item) for item in refs.get("explicit_references", []) or [])
    images = packet.get("images")
    if isinstance(images, list):
        packet_refs.extend(_ref_value(item) for item in images)
    return _dedupe_strings(packet_refs), _dedupe_strings(explicit_refs)


def _request_id(packet: dict[str, Any], packet_path: Path) -> str:
    image_generation = packet.get("image_generation")
    if isinstance(image_generation, dict):
        request_id = str(image_generation.get("request_id", "")).strip()
        if request_id:
            return request_id
    return re.sub(r"[^A-Za-z0-9._-]+", "-", packet_path.stem).strip("-") or "panel-request"


def _output_filename(packet: dict[str, Any], packet_path: Path) -> str:
    image_generation = packet.get("image_generation")
    if isinstance(image_generation, dict):
        output_filename = str(image_generation.get("output_filename", "")).strip()
        if output_filename:
            return output_filename
    output = packet.get("output")
    if isinstance(output, dict):
        for key in ("target_image_filename", "output_filename"):
            output_filename = str(output.get(key, "")).strip()
            if output_filename:
                return output_filename
    return f"{packet_path.stem}.png"


def _output_dir(packet: dict[str, Any], packet_path: Path) -> Path:
    image_generation = packet.get("image_generation")
    if isinstance(image_generation, dict):
        output_dir = str(image_generation.get("output_dir", "")).strip()
        if output_dir:
            return Path(output_dir)
    output_dir = str(packet.get("output_dir", "")).strip()
    if output_dir:
        return Path(output_dir)
    return packet_path.parent / "generated" / _request_id(packet, packet_path)


def _prompt_reference_sections(packet: dict[str, Any], prompt_field: str) -> list[str]:
    image_generation = packet.get("image_generation")
    if isinstance(image_generation, dict):
        sections = [str(item).strip() for item in image_generation.get("prompt_reference_sections", []) or [] if str(item).strip()]
        if sections:
            return sections
    return [prompt_field]


def build_generation_requests(
    packet_paths: Sequence[Path],
    *,
    repo_root: Path,
    smart_mode: str,
    explicit_references: Sequence[str],
    pipeline_context: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    requested_mode = smart_mode
    resolved_mode = _resolve_requested_mode(requested_mode, pipeline_context=pipeline_context, packet_count=len(packet_paths))
    request_docs: list[dict[str, Any]] = []
    trace_tasks: list[dict[str, Any]] = []

    for packet_path in packet_paths:
        packet = _read_json(packet_path)
        prompt_text, prompt_field = _extract_prompt(packet)
        packet_reference_images, packet_explicit_references = _packet_reference_lists(packet)
        continuity_reference_images = (
            _discover_continuity_refs(packet, packet_path, repo_root)
            if _is_continuity_mode(resolved_mode)
            else []
        )
        merged_references = _dedupe_strings(
            [
                *(packet_reference_images if _is_continuity_mode(resolved_mode) else []),
                *packet_explicit_references,
                *explicit_references,
                *continuity_reference_images,
            ]
        )
        images = [{"url": item} for item in merged_references]
        output_dir = _output_dir(packet, packet_path)
        request_doc = {
            "prompt": prompt_text,
            "images": images,
            "project_name": _project_name(packet),
            "task_kind": "project",
            "request_id": _request_id(packet, packet_path),
            "provider_skill": "imagegen",
            "provider_mode": "built-in image_gen",
            "default_model": "GPT-IMAGE-2",
            "output_dir": output_dir.as_posix(),
            "output_filename": _output_filename(packet, packet_path),
            "aspect_ratio": packet.get("aspect_ratio", "16:9"),
            "image_size": packet.get("image_size", "4K"),
            "save_policy": "Generate with built-in image_gen, then copy the selected output from $CODEX_HOME/generated_images into output_dir/output_filename. Leave the original generated image in place.",
            "prompt_reference": {
                "smart_mode_requested": requested_mode,
                "smart_mode_resolved": resolved_mode,
                "prompt_field": prompt_field,
                "prompt_reference_sections": _prompt_reference_sections(packet, prompt_field),
                "source_layout_json": packet_path.as_posix(),
                "packet_reference_images": packet_reference_images,
                "continuity_reference_images": continuity_reference_images,
                "explicit_references": _dedupe_strings([*packet_explicit_references, *explicit_references]),
            },
        }
        request_docs.append(request_doc)
        trace_tasks.append(
            {
                "packet_path": packet_path.as_posix(),
                "request_id": request_doc["request_id"],
                "resolved_mode": resolved_mode,
                "task_mode": "i2i" if images else "t2i",
                "reference_count": len(images),
                "continuity_reference_count": len(continuity_reference_images),
                "explicit_reference_count": len(_dedupe_strings([*packet_explicit_references, *explicit_references])),
                "output_dir": output_dir.as_posix(),
                "request_json": "",
            }
        )

    trace = {
        "smart_mode_requested": requested_mode,
        "smart_mode_resolved": resolved_mode,
        "pipeline_context": pipeline_context,
        "tasks": trace_tasks,
    }
    return request_docs, trace


def run_panel_auto_generate(
    packet_paths: Sequence[Path],
    *,
    manifest_path: Path | None = None,
    smart_mode: str = "auto",
    explicit_references: Sequence[str] = (),
    dry_run: bool = False,
    print_payload: bool = False,
    max_concurrent: int = 100,
    timeout: int = 180,
    save_images: bool = True,
    no_report: bool = False,
    generate: bool = True,
    background: bool = True,
    pipeline_context: str = "direct-request",
) -> dict[str, Any]:
    if smart_mode == "off":
        return {"success": True, "task_count": 0, "success_count": 0, "failed_count": 0, "skipped": True, "reason": "smart-mode-off"}

    repo_root = _repo_root()
    resolved_packets = [path.resolve() for path in packet_paths]
    if manifest_path is not None and not resolved_packets:
        resolved_packets = _load_manifest_packet_paths(manifest_path.resolve())
    if not resolved_packets:
        raise ValueError("未提供任何可消费的 panel packet")

    request_docs, trace = build_generation_requests(
        resolved_packets,
        repo_root=repo_root,
        smart_mode=smart_mode,
        explicit_references=explicit_references,
        pipeline_context=pipeline_context,
    )

    request_root = resolved_packets[0].parent / "generated" / "requests"
    request_root.mkdir(parents=True, exist_ok=True)
    for task, request_doc in zip(trace["tasks"], request_docs):
        request_path = request_root / f"{request_doc['request_id']}-request.json"
        _write_json(request_path, request_doc)
        task["request_json"] = request_path.as_posix()
    batch_request_path = request_root / "panel_auto_generate_batch.json"
    _write_json(batch_request_path, {"tasks": request_docs})

    bridge_report_path = request_root / "panel_auto_generate_report.json"
    imagegen_result = {
        "success": True,
        "status": "request_sidecar_only" if not generate else "request_ready",
        "execution_mode": "codex-builtin-imagegen",
        "provider_skill": "imagegen",
        "provider_mode": "built-in image_gen",
        "default_model": "GPT-IMAGE-2",
        "task_count": len(request_docs),
        "success_count": 0,
        "failed_count": 0,
        "skipped": not generate,
        "reason": "request-sidecar-only" if not generate else "",
        "effective_max_concurrent": 1,
        "foreground": not background,
        "dry_run": dry_run,
        "save_images": save_images,
        "no_report": no_report,
        "print_payload": print_payload,
        "timeout_seconds": timeout,
        "next_step": "Call built-in image_gen once per task, using images[] as visible conversation references when applicable, then copy selected generated images into output_dir/output_filename.",
    }
    bridge_report = {
        "request_batch_path": batch_request_path.as_posix(),
        "manifest_path": manifest_path.resolve().as_posix() if manifest_path else "",
        "trace": trace,
        "imagegen_result": imagegen_result,
    }
    _write_json(bridge_report_path, bridge_report)
    imagegen_result["request_batch_path"] = batch_request_path.as_posix()
    imagegen_result["bridge_report_path"] = bridge_report_path.as_posix()
    imagegen_result["smart_mode_requested"] = trace["smart_mode_requested"]
    imagegen_result["smart_mode_resolved"] = trace["smart_mode_resolved"]
    imagegen_result["trace"] = trace
    return imagegen_result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="把 3-面板 layout packet 按 SMART 合同桥接到内置 imagegen 请求侧车。")
    parser.add_argument("--manifest", help="面板 manifest 路径；若未传 layout-json，可从中解析 packet 列表")
    parser.add_argument("--layout-json", action="append", default=[], help="显式指定 panel layout JSON，可重复传入")
    parser.add_argument("--smart-mode", choices=SMART_MODE_CHOICES, default="auto", help="SMART 模式")
    parser.add_argument("--reference", action="append", default=[], help="显式追加参考图，可重复传入")
    parser.add_argument("--max-concurrent", type=int, default=1, help="兼容旧参数；内置 imagegen 逐资产调用")
    parser.add_argument("--timeout", type=int, default=180, help="兼容旧参数；内置 imagegen 不由本脚本等待 provider")
    parser.add_argument("--no-save-images", action="store_true", help="只保留请求与报告，不落 PNG")
    parser.add_argument("--no-report", action="store_true", help="兼容旧参数；本 bridge 始终写 imagegen bridge report")
    parser.add_argument("--request-only", action="store_true", help="只写 request sidecar 和 bridge report")
    parser.add_argument("--foreground", action="store_true", help="兼容旧参数；内置 imagegen 由 Codex 会话前台执行")
    parser.add_argument("--dry-run", action="store_true", help="只生成 request sidecar，不代表已经调用内置 imagegen")
    parser.add_argument("--print-payload", action="store_true", help="打印内置 imagegen 请求侧车摘要")
    parser.add_argument("--pipeline-context", choices=("panel-stage", "direct-request"), default="direct-request", help="auto 模式判型所需上下文")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    packet_paths = [Path(item) for item in args.layout_json]
    manifest_path = Path(args.manifest) if args.manifest else None
    result = run_panel_auto_generate(
        packet_paths,
        manifest_path=manifest_path,
        smart_mode=args.smart_mode,
        explicit_references=args.reference,
        dry_run=args.dry_run,
        print_payload=args.print_payload,
        max_concurrent=args.max_concurrent,
        timeout=args.timeout,
        save_images=not args.no_save_images,
        no_report=args.no_report,
        generate=not args.request_only,
        background=not args.foreground,
        pipeline_context=args.pipeline_context,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("success", False) else 1


if __name__ == "__main__":
    raise SystemExit(main())
