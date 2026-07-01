#!/usr/bin/env python3
"""Validate workflow visual composition contract evidence.

This validator is intentionally mechanical. It does not generate copy, choose
assets, infer storyboard intent, or render video. It checks that an authored
HyperFrames project exposes the evidence needed for workflow visual gates: audience
text hygiene, dialogue-caption/editorial-overlay separation, caption fit, PiP
cue binding, layered video assembly, and batch diversity ledger consistency.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


INTERNAL_TEXT_PATTERNS = (
    re.compile(r"[（(][^）)]*(?:人称|痛点|激昂|亢奋|恐吓|情绪|口吻|风格|节奏|类型|标签|提示)[^）)]*[）)]"),
    re.compile(r"文案正文\s*[：:]"),
    re.compile(r"【[^】]*(?:第\s*\d+\s*条|文案|标题|钩子)[^】]*】"),
)

WORKFLOW_WATERMARK_PATTERNS = (
    # Legacy labels should not leak into audience-visible output after the F1/F2 merge.
    re.compile(r"\bF2\b", re.IGNORECASE),
    re.compile(r"\bHyperFrames\b", re.IGNORECASE),
    re.compile(r"文案\s*\d+"),
)

CAPTION_BAD_TEXT_PATTERNS = (
    re.compile(r"…"),
    re.compile(r"\.\.\."),
    re.compile(r"\n"),
)

DEFAULT_MAX_CAPTION_UNITS = 42.0
DEFAULT_MAX_OVERLAY_UNITS = 28.0

SEGMENT_ROLE_ALIASES = {
    "hook_opening": {
        "hook_opening",
        "opening_hook",
        "opening",
        "opener",
        "hook",
        "爆款开头",
        "开头",
        "开头部分",
    },
    "content_body": {
        "content_body",
        "body",
        "content",
        "main_content",
        "内容",
        "内容部分",
        "正片",
    },
    "private_traffic_cta": {
        "private_traffic_cta",
        "traffic_cta",
        "cta",
        "conversion",
        "private_traffic",
        "引流",
        "引流部分",
        "私域",
        "私域引流",
    },
}

CONTENT_SUBTYPE_ALIASES = {
    "comic_drama": {"comic_drama", "drama", "manju", "漫剧", "漫剧素材", "纯漫剧"},
    "tool_demo": {"tool_demo", "tool", "workflow", "operation_demo", "工具", "工作流", "操作演示"},
    "revenue_proof": {"revenue_proof", "revenue", "income", "result", "收益", "收益素材", "结果证明"},
}

REQUIRED_SEGMENT_LAYERS = {
    "background_video",
    "semantic_pip",
    "dialogue_caption",
    "editorial_overlay",
}


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    path: str = ""


@dataclass
class Element:
    tag: str
    attrs: dict[str, str]
    text: str

    @property
    def element_id(self) -> str:
        return self.attrs.get("id", "")

    @property
    def classes(self) -> set[str]:
        return set((self.attrs.get("class") or "").split())

    @property
    def purpose(self) -> str:
        return self.attrs.get("data-layer-purpose", "")

    @property
    def start(self) -> float | None:
        return parse_float(self.attrs.get("data-start"))

    @property
    def duration(self) -> float | None:
        return parse_float(self.attrs.get("data-duration"))

    @property
    def end(self) -> float | None:
        if self.start is None or self.duration is None:
            return None
        return self.start + self.duration

    @property
    def track(self) -> str:
        return self.attrs.get("data-track-index", "")

    def locator(self, html_path: Path) -> str:
        ident = self.element_id or self.tag
        return f"{html_path}:{ident}"


class ProjectHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stack: list[dict[str, Any]] = []
        self.elements: list[Element] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        self.stack.append({"tag": tag, "attrs": {key: value or "" for key, value in attrs}, "text_parts": []})

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self.skip_depth:
            self.skip_depth -= 1
            return
        if self.skip_depth or not self.stack:
            return
        current = self.stack.pop()
        text = normalize_ws("".join(current["text_parts"]))
        self.elements.append(Element(current["tag"], current["attrs"], text))

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        for item in self.stack:
            item["text_parts"].append(data)


def parse_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return number


def normalize_ws(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def normalize_text(value: str) -> str:
    value = normalize_ws(value)
    return re.sub(r"[\s，。！？、,.!?；;：:（）()《》<>\"'“”‘’+\-·/|]", "", value).lower()


def display_units(text: str) -> float:
    total = 0.0
    for ch in text:
        if ch.isspace():
            total += 0.5
        elif "\u4e00" <= ch <= "\u9fff" or ch in "，。！？；、：":
            total += 2.0
        else:
            total += 1.0
    return total


def text_match_score(left: str, right: str) -> float:
    a = normalize_text(left)
    b = normalize_text(right)
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    if a in b or b in a:
        return min(len(a), len(b)) / max(len(a), len(b))
    a_chars = set(a)
    b_chars = set(b)
    return len(a_chars & b_chars) / max(len(a_chars | b_chars), 1)


def normalize_token(value: Any) -> str:
    return normalize_ws(str(value or "")).lower().replace("-", "_").replace(" ", "_")


def canonical_from_aliases(value: Any, aliases: dict[str, set[str]]) -> str | None:
    token = normalize_token(value)
    if not token:
        return None
    for canonical, options in aliases.items():
        normalized_options = {normalize_token(option) for option in options}
        if token in normalized_options:
            return canonical
        if any(option and option in token for option in normalized_options):
            return canonical
    return None


def iter_text_values(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, (int, float, bool)):
        return [str(value)]
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            result.extend(iter_text_values(item))
        return result
    if isinstance(value, dict):
        result = []
        for item in value.values():
            result.extend(iter_text_values(item))
        return result
    return []


def truthy_layer(value: Any) -> bool:
    if value in (None, False):
        return False
    if isinstance(value, str) and normalize_token(value) in {"", "none", "false", "disabled", "off", "n/a", "na"}:
        return False
    return True


def mask_is_none(value: Any) -> bool:
    if value in (None, "", False):
        return True
    token = normalize_token(value)
    return token in {"none", "no_mask", "disabled", "off", "false", "transparent_none", "无", "不用", "不加蒙版"}


def collect_segment_layers(segment: dict[str, Any]) -> tuple[set[str], dict[str, Any]]:
    layers: set[str] = set()
    details: dict[str, Any] = {}

    for container_key in ("layers", "layer_plan", "required_layers", "visual_layers"):
        container = segment.get(container_key)
        if isinstance(container, dict):
            for key, value in container.items():
                canonical = canonical_layer_name(key, value)
                if canonical and truthy_layer(value):
                    layers.add(canonical)
                    details.setdefault(canonical, value)
        elif isinstance(container, list):
            for item in container:
                if not isinstance(item, dict):
                    continue
                raw_name = (
                    item.get("layer")
                    or item.get("type")
                    or item.get("kind")
                    or item.get("purpose")
                    or item.get("data-layer-purpose")
                )
                canonical = canonical_layer_name(raw_name, item)
                if canonical and truthy_layer(item.get("enabled", True)):
                    layers.add(canonical)
                    details.setdefault(canonical, item)

    for key, canonical in (
        ("background_video", "background_video"),
        ("background_layer", "background_video"),
        ("pip_asset", "semantic_pip"),
        ("semantic_pip", "semantic_pip"),
        ("dialogue_caption", "dialogue_caption"),
        ("captions", "dialogue_caption"),
        ("editorial_overlay", "editorial_overlay"),
        ("big_text", "editorial_overlay"),
        ("poster_text", "editorial_overlay"),
    ):
        if truthy_layer(segment.get(key)):
            layers.add(canonical)
            details.setdefault(canonical, segment.get(key))
    return layers, details


def canonical_layer_name(raw_name: Any, value: Any = None) -> str | None:
    token = normalize_token(raw_name)
    if token in {"background_video", "video_background", "background", "background_layer", "背景视频", "背景层"}:
        return "background_video"
    if token in {"semantic_pip", "pip", "pip_asset", "picture_in_picture", "画中画", "证据窗"}:
        return "semantic_pip"
    if token in {"dialogue_caption", "caption", "captions", "subtitle", "subtitles", "字幕", "台词字幕"}:
        return "dialogue_caption"
    if token in {"editorial_overlay", "overlay", "big_text", "poster_text", "title_card", "大字报", "核心词"}:
        return "editorial_overlay"
    if isinstance(value, dict):
        nested = value.get("data-layer-purpose") or value.get("purpose") or value.get("type")
        if nested and nested != raw_name:
            return canonical_layer_name(nested)
    return None


def overlay_summary_text(overlay: Any) -> str:
    candidates: list[Any] = []
    if isinstance(overlay, dict):
        for key in ("core_word", "core_phrase", "summary", "display_text", "text", "copy"):
            candidates.append(overlay.get(key))
    elif isinstance(overlay, list):
        for item in overlay:
            candidates.append(overlay_summary_text(item))
    else:
        candidates.append(overlay)
    for item in candidates:
        text = normalize_ws(str(item or ""))
        if text:
            return text
    return ""


def content_subtypes_from_segment(segment: dict[str, Any]) -> set[str]:
    values: list[str] = []
    for key in ("content_subtype", "content_type", "material_type", "asset_category", "section_type", "purpose"):
        values.extend(iter_text_values(segment.get(key)))
    for container_key in ("layers", "layer_plan", "required_layers", "visual_layers"):
        values.extend(iter_text_values(segment.get(container_key)))
    return {
        canonical
        for value in values
        if (canonical := canonical_from_aliases(value, CONTENT_SUBTYPE_ALIASES)) is not None
    }


def load_json(path: Path) -> tuple[Any | None, list[Finding]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except FileNotFoundError:
        return None, [Finding("warn", "missing_json", f"JSON file not found: {path}", str(path))]
    except json.JSONDecodeError as exc:
        return None, [Finding("fail", "invalid_json", f"invalid JSON: {exc}", str(path))]


def parse_html(path: Path) -> tuple[list[Element], list[Finding]]:
    if not path.exists():
        return [], [Finding("fail", "missing_html", f"index.html not found: {path}", str(path))]
    parser = ProjectHTMLParser()
    try:
        parser.feed(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError as exc:
        return [], [Finding("fail", "html_read_error", f"cannot read HTML as UTF-8: {exc}", str(path))]
    return parser.elements, []


def is_dialogue_caption(element: Element) -> bool:
    return element.purpose == "dialogue_caption" or "caption" in element.classes


def is_editorial_overlay(element: Element) -> bool:
    return element.purpose == "editorial_overlay"


def is_semantic_pip(element: Element) -> bool:
    return element.purpose == "semantic_pip" or "pip" in element.classes or element.element_id.lower().startswith("pip")


def is_visible_text_candidate(element: Element) -> bool:
    if not element.text:
        return False
    if element.tag in {"html", "body", "head", "title"}:
        return False
    return bool(element.purpose or element.classes or element.tag in {"h1", "h2", "h3", "p", "span", "strong"})


def find_project_roots(root: Path) -> list[Path]:
    if (root / "index.html").exists():
        return [root]
    roots = sorted({path.parent for path in root.glob("**/index.html") if "node_modules" not in path.parts})
    return roots


def validate_text_hygiene(elements: list[Element], html_path: Path, *, allow_workflow_labels: bool) -> list[Finding]:
    findings: list[Finding] = []
    for element in elements:
        if not is_visible_text_candidate(element):
            continue
        text = element.text
        for pattern in INTERNAL_TEXT_PATTERNS:
            if pattern.search(text):
                findings.append(
                    Finding(
                        "fail",
                        "internal_prompt_visible",
                        f"audience-visible text contains internal prompt metadata: {text[:120]}",
                        element.locator(html_path),
                    )
                )
        if not allow_workflow_labels:
            for pattern in WORKFLOW_WATERMARK_PATTERNS:
                if pattern.search(text):
                    findings.append(
                        Finding(
                            "fail",
                            "workflow_label_visible",
                            f"audience-visible text contains workflow label/watermark: {text[:120]}",
                            element.locator(html_path),
                        )
                    )
    return findings


def validate_captions(
    captions: list[Element],
    overlays: list[Element],
    html_path: Path,
    *,
    max_caption_units: float,
    require_dialogue_captions: bool,
) -> list[Finding]:
    findings: list[Finding] = []
    if require_dialogue_captions and not captions:
        findings.append(Finding("fail", "missing_dialogue_captions", "no dialogue_caption elements found", str(html_path)))
        return findings

    sorted_captions = sorted(captions, key=lambda item: item.start if item.start is not None else -1)
    previous_end: float | None = None
    tracks = {caption.track for caption in sorted_captions if caption.track}
    if len(tracks) > 1:
        findings.append(Finding("warn", "multiple_caption_tracks", f"dialogue captions use multiple tracks: {sorted(tracks)}", str(html_path)))

    for caption in sorted_captions:
        locator = caption.locator(html_path)
        if caption.start is None or caption.duration is None:
            findings.append(Finding("fail", "missing_caption_timing", "caption must have data-start and data-duration", locator))
        elif previous_end is not None and caption.start < previous_end - 0.02:
            findings.append(Finding("fail", "overlapping_dialogue_captions", "dialogue captions overlap in time", locator))
        if caption.end is not None:
            previous_end = max(previous_end if previous_end is not None else caption.end, caption.end)

        for pattern in CAPTION_BAD_TEXT_PATTERNS:
            if pattern.search(caption.text):
                findings.append(Finding("fail", "caption_truncated_or_wrapped", f"caption contains ellipsis or newline: {caption.text}", locator))
        if display_units(caption.text) > max_caption_units:
            findings.append(
                Finding(
                    "fail",
                    "caption_overwide",
                    f"caption display width {display_units(caption.text):.1f} exceeds max {max_caption_units:.1f}: {caption.text}",
                    locator,
                )
            )

    for overlay in overlays:
        if not overlay.text:
            continue
        for caption in sorted_captions:
            if caption.start is None or caption.end is None or overlay.start is None or overlay.end is None:
                continue
            if overlay.start >= caption.end or caption.start >= overlay.end:
                continue
            score = text_match_score(overlay.text, caption.text)
            if score >= 0.82 and min(len(normalize_text(overlay.text)), len(normalize_text(caption.text))) >= 8:
                findings.append(
                    Finding(
                        "fail",
                        "overlay_duplicates_caption",
                        f"editorial overlay duplicates current dialogue caption (score {score:.2f})",
                        overlay.locator(html_path),
                    )
                )
    return findings


def validate_pip_html(pips: list[Element], html_path: Path, *, min_pip_slots: int, strict_social_ad: bool) -> list[Finding]:
    findings: list[Finding] = []
    if strict_social_ad and len(pips) < min_pip_slots:
        findings.append(
            Finding(
                "fail",
                "pip_underfilled",
                f"semantic PiP slot count {len(pips)} is below required minimum {min_pip_slots}",
                str(html_path),
            )
        )
    for pip in pips:
        locator = pip.locator(html_path)
        if pip.start is None or pip.duration is None:
            findings.append(Finding("fail", "pip_missing_timing", "PiP must have data-start and data-duration", locator))
        if pip.purpose != "semantic_pip":
            findings.append(Finding("fail", "pip_missing_semantic_purpose", "PiP must declare data-layer-purpose=semantic_pip", locator))
        if not pip.attrs.get("data-cue-id"):
            findings.append(Finding("fail", "pip_missing_cue_id", "PiP must reference a cue id", locator))
        if not pip.attrs.get("data-match-reason"):
            findings.append(Finding("fail", "pip_missing_match_reason", "PiP must expose a match reason", locator))
    return findings


def validate_assignment(
    assignment_path: Path,
    *,
    min_pip_slots: int,
    min_pip_match_score: float,
    require_manifest_hint: bool,
    strict_social_ad: bool,
) -> tuple[dict[str, Any], list[Finding]]:
    data, findings = load_json(assignment_path)
    metrics: dict[str, Any] = {}
    if not isinstance(data, dict):
        return metrics, findings

    captions = data.get("caption_cues") or []
    pip_slots = data.get("pip_slots") or []
    metrics["assignment_caption_count"] = len(captions) if isinstance(captions, list) else 0
    metrics["assignment_pip_slot_count"] = len(pip_slots) if isinstance(pip_slots, list) else 0

    if strict_social_ad and len(pip_slots) < min_pip_slots:
        findings.append(
            Finding(
                "fail",
                "assignment_pip_underfilled",
                f"assignment PiP slot count {len(pip_slots)} is below required minimum {min_pip_slots}",
                str(assignment_path),
            )
        )

    for index, slot in enumerate(pip_slots if isinstance(pip_slots, list) else []):
        if not isinstance(slot, dict):
            findings.append(Finding("fail", "invalid_pip_slot", "pip_slots entries must be objects", f"{assignment_path}:pip_slots[{index}]"))
            continue
        path = f"{assignment_path}:pip_slots[{index}]"
        if not slot.get("cue_id") or not slot.get("cue_text"):
            findings.append(Finding("fail", "pip_slot_missing_cue", "PiP slot must include cue_id and cue_text", path))
        image = slot.get("image") if isinstance(slot.get("image"), dict) else {}
        if not image.get("image_id") or not image.get("role"):
            findings.append(Finding("fail", "pip_slot_missing_image_role", "PiP slot must include image_id and role", path))
        if not slot.get("match_reason"):
            findings.append(Finding("fail", "pip_slot_missing_reason", "PiP slot must include match_reason", path))
        hint = slot.get("video_manifest_hint") if isinstance(slot.get("video_manifest_hint"), dict) else {}
        if require_manifest_hint and not hint.get("segment_id"):
            findings.append(Finding("fail", "pip_missing_manifest_hint", "PiP slot must include video manifest segment hint", path))
        score = parse_float(hint.get("match_score"))
        if require_manifest_hint and score is None:
            findings.append(Finding("fail", "pip_missing_match_score", "PiP manifest hint must include match_score", path))
        elif score is not None and score < min_pip_match_score:
            findings.append(
                Finding(
                    "fail",
                    "pip_weak_manifest_match",
                    f"PiP manifest hint match_score {score:.1f} is below minimum {min_pip_match_score:.1f}",
                    path,
                )
            )
    return metrics, findings


def validate_composition_plan(
    plan_path: Path,
    *,
    strict_social_ad: bool,
    max_overlay_units: float,
) -> tuple[dict[str, Any], list[Finding]]:
    data, findings = load_json(plan_path)
    metrics: dict[str, Any] = {}
    if not isinstance(data, dict):
        if strict_social_ad and not any(item.code == "invalid_json" for item in findings):
            findings.append(Finding("fail", "missing_composition_plan", "workflow_composition_plan.json is required", str(plan_path)))
        return metrics, findings

    segments = (
        data.get("timeline_segments")
        or data.get("content_segments")
        or data.get("storyboard_segments")
        or data.get("segments")
        or []
    )
    if not isinstance(segments, list):
        findings.append(Finding("fail", "invalid_timeline_segments", "timeline_segments must be a list", str(plan_path)))
        segments = []

    role_counts = {key: 0 for key in SEGMENT_ROLE_ALIASES}
    observed_subtypes: set[str] = set()
    metrics["composition_segment_count"] = len(segments)

    throughline = (
        data.get("background_throughline")
        or data.get("background_video_throughline")
        or data.get("background_continuity")
        or data.get("background_continuity_map")
    )
    if strict_social_ad and not isinstance(throughline, dict):
        findings.append(
            Finding(
                "fail",
                "missing_background_throughline",
                "composition plan must declare continuous background video throughline",
                str(plan_path),
            )
        )
    elif isinstance(throughline, dict):
        mode_values = " ".join(iter_text_values(throughline.get("mode") or throughline.get("continuity") or throughline.get("strategy")))
        if not re.search(r"continuous|throughline|full_span|拉通|贯穿", mode_values, re.IGNORECASE):
            findings.append(
                Finding(
                    "fail",
                    "background_throughline_not_continuous",
                    "background video throughline must be continuous/throughline",
                    str(plan_path),
                )
            )
        mask_value = throughline.get("mask") or throughline.get("mask_mode") or throughline.get("masking")
        if not mask_is_none(mask_value):
            findings.append(Finding("fail", "background_throughline_uses_mask", "background throughline must not use a mask", str(plan_path)))
        source_hint = " ".join(iter_text_values(throughline))
        if source_hint and not re.search(r"漫剧素材|纯漫剧素材|comic_drama|pure_comic", source_hint, re.IGNORECASE):
            findings.append(
                Finding(
                    "warn",
                    "background_throughline_not_comic_drama_hint",
                    "background throughline should usually point to projects/素材/漫剧素材/纯漫剧素材 or equivalent evidence",
                    str(plan_path),
                )
            )

    for index, segment in enumerate(segments):
        if not isinstance(segment, dict):
            findings.append(Finding("fail", "invalid_timeline_segment", "timeline segment must be an object", f"{plan_path}:timeline_segments[{index}]"))
            continue
        path = f"{plan_path}:timeline_segments[{index}]"
        raw_role = segment.get("segment_role") or segment.get("role") or segment.get("section") or segment.get("phase") or segment.get("type")
        role = canonical_from_aliases(raw_role, SEGMENT_ROLE_ALIASES)
        if role:
            role_counts[role] += 1
        elif strict_social_ad:
            findings.append(Finding("fail", "unknown_video_segment_role", "segment must declare hook/content/traffic role", path))

        layers, details = collect_segment_layers(segment)
        if strict_social_ad:
            for layer in sorted(REQUIRED_SEGMENT_LAYERS - layers):
                findings.append(Finding("fail", "segment_missing_layer", f"segment is missing required layer: {layer}", path))

        background = details.get("background_video")
        if isinstance(background, dict):
            mask_value = background.get("mask") or background.get("mask_mode") or background.get("masking")
            if not mask_is_none(mask_value):
                findings.append(Finding("fail", "background_video_uses_mask", "background video layer must not use a mask", path))

        overlay_text = overlay_summary_text(details.get("editorial_overlay") or segment.get("editorial_overlay") or segment.get("big_text"))
        if strict_social_ad and "editorial_overlay" in layers and not overlay_text:
            findings.append(
                Finding(
                    "fail",
                    "editorial_overlay_missing_summary",
                    "editorial overlay must contain a core word, phrase, or one-sentence summary",
                    path,
                )
            )
        if overlay_text and display_units(overlay_text) > max_overlay_units:
            findings.append(
                Finding(
                    "fail",
                    "editorial_overlay_too_long",
                    f"editorial overlay display width {display_units(overlay_text):.1f} exceeds max {max_overlay_units:.1f}: {overlay_text}",
                    path,
                )
            )

        if role == "content_body":
            observed_subtypes.update(content_subtypes_from_segment(segment))

    metrics["composition_segment_roles"] = role_counts
    metrics["composition_content_subtypes"] = sorted(observed_subtypes)
    if strict_social_ad:
        for role, count in role_counts.items():
            if count == 0:
                findings.append(Finding("fail", "missing_video_segment_role", f"composition plan missing segment role: {role}", str(plan_path)))
        for subtype in CONTENT_SUBTYPE_ALIASES:
            if subtype not in observed_subtypes:
                exception_map = data.get("content_mix_exceptions") if isinstance(data.get("content_mix_exceptions"), dict) else {}
                if not exception_map.get(subtype):
                    findings.append(
                        Finding(
                            "fail",
                            "missing_content_subtype",
                            f"content body missing required material subtype: {subtype}",
                            str(plan_path),
                        )
                    )
    return metrics, findings


def validate_batch_audit(root: Path, *, min_pip_slots: int, require_manifest_hint: bool) -> tuple[dict[str, Any], list[Finding]]:
    metrics: dict[str, Any] = {}
    findings: list[Finding] = []
    audit_path = root / "asset_diversity_audit.json"
    ledger_path = root / "asset_usage_ledger.json"
    audit, audit_findings = load_json(audit_path)
    ledger, ledger_findings = load_json(ledger_path)
    findings.extend(item for item in audit_findings if item.severity == "fail")
    findings.extend(item for item in ledger_findings if item.severity == "fail")

    if isinstance(audit, dict):
        checks = audit.get("checks") if isinstance(audit.get("checks"), dict) else {}
        metrics["batch_audit_verdict"] = audit.get("verdict")
        metrics.update({f"audit_{key}": value for key, value in checks.items()})
        if audit.get("verdict") != "pass":
            findings.append(Finding("fail", "asset_diversity_audit_not_pass", "asset_diversity_audit verdict must be pass", str(audit_path)))
        if checks.get("pip_min_per_target", min_pip_slots) < min_pip_slots:
            findings.append(Finding("fail", "batch_pip_underfilled", "batch audit reports too few PiP slots per target", str(audit_path)))
        if require_manifest_hint and checks.get("pip_manifest_hint_count") != checks.get("pip_image_placement_count"):
            findings.append(Finding("fail", "batch_pip_manifest_hint_gap", "not every PiP placement has manifest hint", str(audit_path)))
        if audit.get("pip_underfilled_targets"):
            findings.append(Finding("fail", "batch_pip_underfilled_targets", "batch audit lists underfilled targets", str(audit_path)))
        if audit.get("pip_missing_manifest_hint"):
            findings.append(Finding("fail", "batch_pip_missing_manifest_hint", "batch audit lists PiP without manifest hints", str(audit_path)))

    if isinstance(ledger, dict):
        records = ledger.get("usage_records") or []
        metrics["ledger_usage_record_count"] = len(records) if isinstance(records, list) else 0
    return metrics, findings


def validate_project(
    project_root: Path,
    *,
    max_caption_units: float,
    max_overlay_units: float,
    min_pip_slots: int,
    min_pip_match_score: float,
    strict_social_ad: bool,
    require_manifest_hint: bool,
    allow_workflow_labels: bool,
) -> tuple[dict[str, Any], list[Finding]]:
    html_path = project_root / "index.html"
    elements, findings = parse_html(html_path)
    captions = [item for item in elements if is_dialogue_caption(item)]
    overlays = [item for item in elements if is_editorial_overlay(item)]
    pips = [item for item in elements if is_semantic_pip(item)]
    metrics = {
        "project_root": str(project_root),
        "dialogue_caption_count": len(captions),
        "editorial_overlay_count": len(overlays),
        "semantic_pip_count": len(pips),
    }

    findings.extend(validate_text_hygiene(elements, html_path, allow_workflow_labels=allow_workflow_labels))
    findings.extend(
        validate_captions(
            captions,
            overlays,
            html_path,
            max_caption_units=max_caption_units,
            require_dialogue_captions=True,
        )
    )
    findings.extend(validate_pip_html(pips, html_path, min_pip_slots=min_pip_slots, strict_social_ad=strict_social_ad))

    assignment_path = project_root / "workflow_assignment.json"
    if not assignment_path.exists():
        legacy_assignment_path = project_root / "f2_assignment.json"
        if legacy_assignment_path.exists():
            assignment_path = legacy_assignment_path
    if assignment_path.exists():
        assignment_metrics, assignment_findings = validate_assignment(
            assignment_path,
            min_pip_slots=min_pip_slots,
            min_pip_match_score=min_pip_match_score,
            require_manifest_hint=require_manifest_hint,
            strict_social_ad=strict_social_ad,
        )
        metrics.update(assignment_metrics)
        findings.extend(assignment_findings)
    elif strict_social_ad:
        findings.append(Finding("warn", "missing_assignment", "workflow_assignment.json missing; PiP manifest evidence cannot be fully checked", str(project_root)))

    plan_path = project_root / "workflow_composition_plan.json"
    plan_metrics, plan_findings = validate_composition_plan(
        plan_path,
        strict_social_ad=strict_social_ad,
        max_overlay_units=max_overlay_units,
    )
    metrics.update(plan_metrics)
    findings.extend(plan_findings)

    return metrics, findings


def finding_to_dict(finding: Finding) -> dict[str, str]:
    data = {"severity": finding.severity, "code": finding.code, "message": finding.message}
    if finding.path:
        data["path"] = finding.path
    return data


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate workflow visual composition contract evidence.")
    parser.add_argument("root", type=Path, help="workflow project root or batch root")
    parser.add_argument("--strict-social-ad", action="store_true", help="enforce social-ad/batch PiP and diversity gates")
    parser.add_argument("--min-pip-slots", type=int, default=4, help="minimum cue-bound PiP slots per project in strict mode")
    parser.add_argument("--min-pip-match-score", type=float, default=1.0, help="minimum manifest match_score for PiP slots")
    parser.add_argument("--max-caption-units", type=float, default=DEFAULT_MAX_CAPTION_UNITS, help="single-line caption display unit limit")
    parser.add_argument("--max-overlay-units", type=float, default=DEFAULT_MAX_OVERLAY_UNITS, help="editorial overlay display unit limit")
    parser.add_argument("--allow-workflow-labels", action="store_true", help="allow visible workflow/HyperFrames labels")
    parser.add_argument("--allow-missing-manifest-hint", action="store_true", help="do not fail PiP slots without video manifest hints")
    parser.add_argument("--write-report", type=Path, help="write JSON validation report")
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    root = args.root.resolve()
    project_roots = find_project_roots(root)
    all_findings: list[Finding] = []
    project_metrics: list[dict[str, Any]] = []

    if not project_roots:
        all_findings.append(Finding("fail", "no_hyperframes_projects", f"no index.html files found below {root}", str(root)))

    for project_root in project_roots:
        metrics, findings = validate_project(
            project_root,
            max_caption_units=args.max_caption_units,
            max_overlay_units=args.max_overlay_units,
            min_pip_slots=args.min_pip_slots,
            min_pip_match_score=args.min_pip_match_score,
            strict_social_ad=args.strict_social_ad,
            require_manifest_hint=not args.allow_missing_manifest_hint,
            allow_workflow_labels=args.allow_workflow_labels,
        )
        project_metrics.append(metrics)
        all_findings.extend(findings)

    batch_metrics: dict[str, Any] = {}
    if (root / "asset_diversity_audit.json").exists() or (root / "asset_usage_ledger.json").exists():
        batch_metrics, batch_findings = validate_batch_audit(root, min_pip_slots=args.min_pip_slots, require_manifest_hint=not args.allow_missing_manifest_hint)
        all_findings.extend(batch_findings)

    fail_count = sum(1 for item in all_findings if item.severity == "fail")
    warn_count = sum(1 for item in all_findings if item.severity == "warn")
    report = {
        "validator": "validate_visual_contract.py",
        "root": str(root),
        "verdict": "pass" if fail_count == 0 else "fail",
        "summary": {
            "project_count": len(project_roots),
            "fail_count": fail_count,
            "warn_count": warn_count,
        },
        "project_metrics": project_metrics,
        "batch_metrics": batch_metrics,
        "findings": [finding_to_dict(item) for item in all_findings],
    }

    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.write_report:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(output, encoding="utf-8")
    print(output, end="")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
