#!/usr/bin/env python3
"""Validate workflow visual composition contract evidence.

This validator is intentionally mechanical. It does not generate copy, choose
assets, infer storyboard intent, or render video. It checks that an authored
HyperFrames project exposes the evidence needed for workflow visual gates: audience
text hygiene, internal process-title blocking, dialogue-caption/editorial-overlay
separation, caption fit, PiP cue binding, layered video assembly, and batch
diversity ledger consistency.
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
    re.compile(r"\bworkflow\b", re.IGNORECASE),
    re.compile(r"文案\s*\d+"),
)

INTERNAL_PROCESS_LABEL_PATTERNS = (
    re.compile(r"工作流程"),
    re.compile(r"(?:执行流程|操作流程|项目流程|内部流程|流程步骤|流程说明|流程验证|流程复盘|流程图)"),
    re.compile(r"(?:内部)?(?:学习交流|内部学习|团队复盘|项目复盘|内部培训)"),
    re.compile(r"(?:证据推进|痛点爆破|创作节点|审查话术|参考节奏)"),
    re.compile(r"\bpipeline\b", re.IGNORECASE),
    re.compile(r"\bN[1-9]\s*[-_]", re.IGNORECASE),
    re.compile(r"\b(?:hook_opening|content_body|private_traffic_cta|semantic_pip|dialogue_caption|editorial_overlay)\b", re.IGNORECASE),
)

CAPTION_BAD_TEXT_PATTERNS = (
    re.compile(r"…"),
    re.compile(r"\.\.\."),
    re.compile(r"\n"),
)

DEFAULT_MAX_CAPTION_UNITS = 42.0
DEFAULT_MAX_OVERLAY_UNITS = 28.0
DEFAULT_MIN_PIP_WIDTH_PX = 260.0
DEFAULT_MIN_PIP_HEIGHT_PX = 146.0
DEFAULT_MIN_SIMULTANEOUS_PIPS = 2
OPENING_MATERIAL_MIN_DURATION = 5.0
OPENING_MATERIAL_MAX_DURATION = 10.0

BRANCH_EVIDENCE_KEYS = (
    "asset",
    "branch",
    "category",
    "file",
    "material",
    "path",
    "pool",
    "source",
)

FULL_DISPLAY_TOKENS = {
    "contain",
    "fit_contain",
    "scale_down",
    "full",
    "full_frame",
    "fullframe",
    "no_crop",
    "native",
    "native_scale",
    "letterbox",
    "complete",
    "完整",
    "完整展示",
    "全貌",
    "不裁剪",
    "原始比例",
}

CROP_OR_UPSCALE_TOKENS = {
    "cover",
    "fill",
    "crop",
    "cropped",
    "pan_scan",
    "panscan",
    "zoom",
    "zoom_in",
    "punch_in",
    "upscale",
    "enlarge",
    "fill_canvas",
    "background_cover",
    "裁剪",
    "填满",
    "放大",
}

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


def opacity_is_full(value: Any) -> bool:
    if value in (None, ""):
        return True
    if isinstance(value, bool):
        return value is True
    token = normalize_ws(str(value)).lower()
    if token in {"1", "1.0", "100", "100%", "full", "opaque", "none", "normal", "default", "不透明"}:
        return True
    if token in {"0", "0%", "false", "transparent", "translucent", "semi_transparent", "半透明", "透明"}:
        return False
    try:
        if token.endswith("%"):
            return float(token[:-1].strip()) >= 99.9
        return float(token) >= 0.999
    except ValueError:
        return False


def transparency_is_none(value: Any) -> bool:
    if value in (None, "", False):
        return True
    token = normalize_ws(str(value)).lower()
    if token in {"none", "0", "0.0", "0%", "false", "disabled", "off", "无", "不透明"}:
        return True
    try:
        if token.endswith("%"):
            return float(token[:-1].strip()) <= 0.1
        return float(token) <= 0.001
    except ValueError:
        return False


def style_value(style: str, property_name: str) -> str | None:
    pattern = re.compile(rf"(?:^|;)\s*{re.escape(property_name)}\s*:\s*([^;]+)", re.IGNORECASE)
    match = pattern.search(style or "")
    if not match:
        return None
    return normalize_ws(match.group(1))


def parse_time_seconds(value: Any) -> float | None:
    number = parse_float(value)
    if number is not None:
        return number
    if not isinstance(value, str):
        return None
    text = normalize_ws(value)
    match = re.fullmatch(r"(?:(\d+):)?(\d+):(\d+(?:\.\d+)?)", text)
    if not match:
        return None
    hours = float(match.group(1) or 0)
    minutes = float(match.group(2))
    seconds = float(match.group(3))
    return hours * 3600 + minutes * 60 + seconds


def duration_from_payload(value: Any) -> float | None:
    if not isinstance(value, dict):
        return None
    for key in ("duration_sec", "duration", "clip_duration", "selected_duration", "source_duration", "display_duration"):
        duration = parse_time_seconds(value.get(key))
        if duration is not None:
            return duration
    start = parse_time_seconds(value.get("start") or value.get("start_sec") or value.get("in"))
    end = parse_time_seconds(value.get("end") or value.get("end_sec") or value.get("out"))
    if start is not None and end is not None and end >= start:
        return end - start
    time_range = value.get("time_range") or value.get("range")
    if isinstance(time_range, dict):
        start = parse_time_seconds(time_range.get("start"))
        end = parse_time_seconds(time_range.get("end"))
        if start is not None and end is not None and end >= start:
            return end - start
        return parse_time_seconds(time_range.get("duration"))
    return None


def parse_dimension(value: Any, viewport_px: float) -> float | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        number = float(value)
        return number if not math.isnan(number) and not math.isinf(number) else None
    text = normalize_ws(str(value)).lower()
    if text.endswith("%"):
        try:
            return viewport_px * float(text[:-1].strip()) / 100.0
        except ValueError:
            return None
    match = re.search(r"(-?\d+(?:\.\d+)?)\s*(?:px)?", text)
    if not match:
        return None
    return float(match.group(1))


def parse_transform_scale(style_or_transform: str) -> list[float]:
    scales: list[float] = []
    text = style_or_transform or ""
    for match in re.finditer(r"scale(?:3d|x|y)?\s*\(([^)]+)\)", text, re.IGNORECASE):
        first = match.group(1).split(",")[0].strip()
        number = parse_float(first)
        if number is not None:
            scales.append(number)
    return scales


def extract_scale_values(value: Any) -> list[tuple[str, float]]:
    values: list[tuple[str, float]] = []
    if not isinstance(value, dict):
        return values
    for key in ("scale", "max_scale", "zoom", "upscale", "upscale_factor", "resize_scale", "render_scale"):
        if key in value:
            number = parse_float(value.get(key))
            if number is not None:
                values.append((key, number))
    style = value.get("style") or value.get("css") or value.get("transform")
    if isinstance(style, str):
        for number in parse_transform_scale(style):
            values.append(("style.transform.scale", number))
        zoom_value = style_value(style, "zoom")
        if zoom_value is not None:
            number = parse_float(zoom_value)
            if number is not None:
                values.append(("style.zoom", number))
        transform_value = style_value(style, "transform")
        if transform_value:
            for number in parse_transform_scale(transform_value):
                values.append(("style.transform.scale", number))
    return values


def extract_fit_values(value: Any) -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []
    if not isinstance(value, dict):
        return values
    for key in (
        "fit",
        "object_fit",
        "objectFit",
        "background_size",
        "backgroundSize",
        "display_mode",
        "crop_mode",
        "framing",
        "show_mode",
        "resize_mode",
        "render_mode",
    ):
        if key in value:
            values.append((key, normalize_token(value.get(key))))
    style = value.get("style") or value.get("css")
    if isinstance(style, str):
        for property_name in ("object-fit", "background-size"):
            item = style_value(style, property_name)
            if item is not None:
                values.append((f"style.{property_name}", normalize_token(item)))
    return values


def has_full_display_evidence(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    for key in ("full_display", "full_frame", "show_full_frame", "no_crop", "complete_display"):
        if key in value and truthy_layer(value.get(key)):
            return True
    for field, token in extract_fit_values(value):
        if token in FULL_DISPLAY_TOKENS:
            return True
        if field in {"crop_mode", "framing", "display_mode"} and token in {"none", "no", "false", "off", "disabled", "无", "不裁剪"}:
            return True
    return False


def has_no_upscale_evidence(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    for key in ("no_upscale", "avoid_upscale", "native_scale", "preserve_native_resolution"):
        if key in value and truthy_layer(value.get(key)):
            return True
    for key in ("upscale", "allow_upscale"):
        if key in value and not truthy_layer(value.get(key)):
            return True
    scales = extract_scale_values(value)
    if scales and all(number <= 1.001 for _, number in scales):
        return True
    for _, token in extract_fit_values(value):
        if token in {"contain", "scale_down", "native", "native_scale", "no_upscale", "原始比例", "不放大"}:
            return True
    return False


def validate_no_upscale(value: Any, path: str, scope: str) -> list[Finding]:
    findings: list[Finding] = []
    if not isinstance(value, dict):
        return findings
    for field, number in extract_scale_values(value):
        if number > 1.001:
            findings.append(Finding("fail", f"{scope}_uses_upscale", "traffic/opening material must not be enlarged above native scale", f"{path}.{field}"))
    for field, token in extract_fit_values(value):
        if token in CROP_OR_UPSCALE_TOKENS:
            findings.append(Finding("fail", f"{scope}_uses_cover_or_crop", "material must use contain/full-frame framing, not cover/crop/zoom", f"{path}.{field}"))
    return findings


def iter_branch_evidence_values(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return []
    result: list[str] = []
    for key, item in value.items():
        key_token = normalize_token(key)
        if any(part in key_token for part in BRANCH_EVIDENCE_KEYS):
            result.extend(iter_text_values(item))
        if isinstance(item, dict):
            result.extend(iter_branch_evidence_values(item))
        elif isinstance(item, list):
            for child in item:
                if isinstance(child, dict):
                    result.extend(iter_branch_evidence_values(child))
    return result


def has_opening_material_evidence(value: Any) -> bool:
    text = " ".join(iter_branch_evidence_values(value))
    return bool(re.search(r"projects/素材/开头素材|素材/开头素材|开头素材|\bopening_hook\b", text, re.IGNORECASE))


def has_private_traffic_material_evidence(value: Any) -> bool:
    text = " ".join(iter_branch_evidence_values(value))
    return bool(re.search(r"projects/素材/引流素材|素材/引流素材|引流素材|\bprivate_traffic_cta\b|\btraffic_cta\b|\bcta_material\b", text, re.IGNORECASE))


def representative_payloads(segment: dict[str, Any], details: dict[str, Any], *extra_keys: str) -> list[tuple[str, Any]]:
    payloads: list[tuple[str, Any]] = [("segment", segment)]
    for layer_name, item in details.items():
        payloads.append((f"layers.{layer_name}", item))
    for key in extra_keys:
        if key in segment:
            payloads.append((key, segment.get(key)))
    return payloads


def element_branch_text(element: Element) -> str:
    parts: list[str] = []
    for key, value in element.attrs.items():
        key_token = normalize_token(key)
        if any(part in key_token for part in BRANCH_EVIDENCE_KEYS):
            parts.append(value)
    return " ".join(parts)


def element_has_private_traffic_evidence(element: Element) -> bool:
    return bool(re.search(r"projects/素材/引流素材|素材/引流素材|引流素材|\bprivate_traffic_cta\b|\btraffic_cta\b|\bcta_material\b", element_branch_text(element), re.IGNORECASE))


def element_scale_values(element: Element) -> list[tuple[str, float]]:
    values: list[tuple[str, float]] = []
    for key in ("data-scale", "data-max-scale", "scale", "data-zoom", "zoom"):
        number = parse_float(element.attrs.get(key))
        if number is not None:
            values.append((key, number))
    style = element.attrs.get("style", "")
    for number in parse_transform_scale(style):
        values.append(("style.transform.scale", number))
    transform_value = style_value(style, "transform")
    if transform_value:
        for number in parse_transform_scale(transform_value):
            values.append(("style.transform.scale", number))
    zoom_value = style_value(style, "zoom")
    if zoom_value is not None:
        number = parse_float(zoom_value)
        if number is not None:
            values.append(("style.zoom", number))
    return values


def element_fit_values(element: Element) -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []
    for key in ("data-fit", "data-object-fit", "data-display-mode", "data-crop-mode", "object-fit"):
        if element.attrs.get(key):
            values.append((key, normalize_token(element.attrs.get(key))))
    style = element.attrs.get("style", "")
    for property_name in ("object-fit", "background-size"):
        item = style_value(style, property_name)
        if item is not None:
            values.append((f"style.{property_name}", normalize_token(item)))
    return values


def element_has_no_upscale_evidence(element: Element) -> bool:
    for key in ("data-no-upscale", "data-native-scale", "data-preserve-native-resolution"):
        if truthy_layer(element.attrs.get(key)):
            return True
    scales = element_scale_values(element)
    if scales and all(number <= 1.001 for _, number in scales):
        return True
    return any(token in {"contain", "scale_down", "native", "native_scale", "no_upscale", "不放大"} for _, token in element_fit_values(element))


def validate_element_no_upscale(element: Element, html_path: Path, scope: str) -> list[Finding]:
    findings: list[Finding] = []
    locator = element.locator(html_path)
    for field, number in element_scale_values(element):
        if number > 1.001:
            findings.append(Finding("fail", f"{scope}_html_uses_upscale", "traffic material must not be enlarged above native scale", f"{locator}.{field}"))
    for field, token in element_fit_values(element):
        if token in CROP_OR_UPSCALE_TOKENS:
            findings.append(Finding("fail", f"{scope}_html_uses_cover_or_crop", "traffic material must use contain/native framing, not cover/crop/zoom", f"{locator}.{field}"))
    if not element_has_no_upscale_evidence(element):
        findings.append(Finding("fail", f"{scope}_html_missing_no_upscale", "traffic material must declare no-upscale/native-scale evidence", locator))
    return findings


def element_dimensions(element: Element) -> tuple[float | None, float | None]:
    style = element.attrs.get("style", "")
    width = (
        parse_dimension(element.attrs.get("data-width"), 1920)
        or parse_dimension(element.attrs.get("width"), 1920)
        or parse_dimension(style_value(style, "width"), 1920)
    )
    height = (
        parse_dimension(element.attrs.get("data-height"), 1080)
        or parse_dimension(element.attrs.get("height"), 1080)
        or parse_dimension(style_value(style, "height"), 1080)
    )
    return width, height


def max_simultaneous_elements(elements: list[Element]) -> int:
    timed = [(item.start, item.end) for item in elements if item.start is not None and item.end is not None]
    if not timed:
        return 0
    points = sorted({point for interval in timed for point in interval if point is not None})
    if len(points) < 2:
        return len(timed)
    max_count = 0
    for left, right in zip(points, points[1:]):
        mid = (left + right) / 2
        count = sum(1 for start, end in timed if start is not None and end is not None and start <= mid < end)
        max_count = max(max_count, count)
    return max_count


def pip_has_grid_evidence(element: Element) -> bool:
    if normalize_token(element.attrs.get("data-layout")) == "grid":
        return True
    if element.attrs.get("data-grid-slot") or element.attrs.get("data-grid-index"):
        return True
    return bool(
        (element.attrs.get("data-grid-row") or element.attrs.get("data-row"))
        and (element.attrs.get("data-grid-col") or element.attrs.get("data-col"))
    )


def extract_opacity_values(value: Any) -> list[tuple[str, Any]]:
    values: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for key in ("opacity", "alpha", "background_opacity", "layer_opacity", "video_opacity"):
            if key in value:
                values.append((key, value.get(key)))
        for key in ("transparency", "background_transparency", "layer_transparency"):
            if key in value and not transparency_is_none(value.get(key)):
                values.append((key, f"transparency={value.get(key)}"))
        style = value.get("style") or value.get("css")
        if isinstance(style, str):
            opacity = style_value(style, "opacity")
            if opacity is not None:
                values.append(("style.opacity", opacity))
            filter_value = style_value(style, "filter")
            if filter_value:
                match = re.search(r"opacity\(([^)]+)\)", filter_value, re.IGNORECASE)
                if match:
                    values.append(("style.filter.opacity", match.group(1)))
        for key in ("effects", "filters", "background_effects"):
            nested = value.get(key)
            if isinstance(nested, dict):
                values.extend((f"{key}.{name}", item) for name, item in extract_opacity_values(nested))
    return values


def extract_mask_values(value: Any) -> list[tuple[str, Any]]:
    values: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for key in ("mask", "mask_mode", "masking", "clip_path", "clipPath"):
            if key in value:
                values.append((key, value.get(key)))
        style = value.get("style") or value.get("css")
        if isinstance(style, str):
            for property_name in ("mask", "-webkit-mask", "mask-image", "-webkit-mask-image", "clip-path"):
                mask_value = style_value(style, property_name)
                if mask_value is not None:
                    values.append((f"style.{property_name}", mask_value))
    return values


def validate_background_surface(value: Any, path: str, scope: str) -> list[Finding]:
    findings: list[Finding] = []
    for field, mask_value in extract_mask_values(value):
        if not mask_is_none(mask_value):
            findings.append(Finding("fail", f"{scope}_uses_mask", "background video must not use a mask", f"{path}.{field}"))
    for field, opacity_value in extract_opacity_values(value):
        if not opacity_is_full(opacity_value):
            findings.append(
                Finding(
                    "fail",
                    f"{scope}_uses_opacity",
                    "background video must be fully opaque; opacity/transparency effects are not allowed",
                    f"{path}.{field}",
                )
            )
    return findings


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
        for key in ("core_title", "core_word", "core_phrase", "summary", "display_text", "text", "copy"):
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


def overlay_has_segment_source(overlay: Any) -> bool:
    def has_cue_source_and_reason(item: dict[str, Any]) -> bool:
        source_cues = (
            item.get("source_cue_ids")
            or item.get("cue_ids")
            or item.get("source_cues")
            or item.get("source_cue_id")
            or item.get("cue_id")
        )
        source_text = (
            item.get("source_text")
            or item.get("source_excerpt")
            or item.get("source_paragraph")
            or item.get("matched_copy")
            or item.get("matched_script_text")
            or item.get("script_text")
        )
        reason = item.get("match_reason") or item.get("extraction_reason") or item.get("selection_reason")
        has_cue = bool(source_cues) if not isinstance(source_cues, list) else bool(source_cues)
        return has_cue and bool(normalize_ws(str(source_text or ""))) and bool(normalize_ws(str(reason or "")))

    if isinstance(overlay, dict):
        return has_cue_source_and_reason(overlay)
    if isinstance(overlay, list):
        return any(overlay_has_segment_source(item) for item in overlay)
    return False


def internal_process_label_match(text: str) -> str | None:
    for pattern in INTERNAL_PROCESS_LABEL_PATTERNS:
        if pattern.search(text):
            return pattern.pattern
    return None


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


def is_background_video(element: Element) -> bool:
    if element.purpose == "background_video":
        return True
    class_text = " ".join(element.classes).lower()
    ident = element.element_id.lower()
    return (
        "background_video" in class_text
        or "background-video" in class_text
        or "video_background" in class_text
        or "video-bg" in class_text
        or ident.startswith("background")
        or ident.startswith("bg-video")
    )


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
        process_match = internal_process_label_match(text)
        if process_match:
            findings.append(
                Finding(
                    "fail",
                    "internal_process_title_visible",
                    f"audience-visible text contains an internal process or learning label: {text[:120]}",
                    element.locator(html_path),
                )
            )
    return findings


def validate_background_html(backgrounds: list[Element], html_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    for element in backgrounds:
        locator = element.locator(html_path)
        payload = {
            "mask": element.attrs.get("data-mask") or element.attrs.get("mask"),
            "mask_mode": element.attrs.get("data-mask-mode"),
            "clip_path": element.attrs.get("data-clip-path"),
            "opacity": element.attrs.get("data-opacity") or element.attrs.get("opacity"),
            "alpha": element.attrs.get("data-alpha"),
            "transparency": element.attrs.get("data-transparency"),
            "style": element.attrs.get("style", ""),
        }
        findings.extend(validate_background_surface(payload, locator, "background_html"))
    return findings


def validate_private_traffic_html(elements: list[Element], html_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    for element in elements:
        if element_has_private_traffic_evidence(element):
            findings.extend(validate_element_no_upscale(element, html_path, "private_traffic"))
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


def validate_pip_html(
    pips: list[Element],
    html_path: Path,
    *,
    min_pip_slots: int,
    min_simultaneous_pips: int,
    min_pip_width_px: float,
    min_pip_height_px: float,
    strict_social_ad: bool,
) -> list[Finding]:
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
    if strict_social_ad and pips:
        simultaneous = max_simultaneous_elements(pips)
        if simultaneous < min_simultaneous_pips:
            findings.append(
                Finding(
                    "fail",
                    "pip_no_simultaneous_group",
                    f"semantic PiP must appear in aligned groups; max simultaneous count {simultaneous} is below {min_simultaneous_pips}",
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
        if strict_social_ad:
            if not pip.attrs.get("data-pip-group") and not pip.attrs.get("data-grid-group") and not pip.attrs.get("data-group-id"):
                findings.append(Finding("fail", "pip_missing_grid_group", "PiP must declare a grid/group id for aligned multi-window layout", locator))
            if not pip_has_grid_evidence(pip):
                findings.append(Finding("fail", "pip_missing_grid_position", "PiP must expose grid row/column or grid slot evidence", locator))
            width, height = element_dimensions(pip)
            if width is None or height is None:
                findings.append(Finding("fail", "pip_missing_size", "PiP must expose rendered width and height", locator))
            else:
                if width < min_pip_width_px or height < min_pip_height_px:
                    findings.append(
                        Finding(
                            "fail",
                            "pip_too_small",
                            f"PiP size {width:.0f}x{height:.0f}px is below minimum {min_pip_width_px:.0f}x{min_pip_height_px:.0f}px",
                            locator,
                        )
                    )
    return findings


def validate_assignment(
    assignment_path: Path,
    *,
    min_pip_slots: int,
    min_simultaneous_pips: int,
    min_pip_width_px: float,
    min_pip_height_px: float,
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

    timed_slots: list[tuple[float, float]] = []
    group_counts: dict[str, int] = {}
    for index, slot in enumerate(pip_slots if isinstance(pip_slots, list) else []):
        if not isinstance(slot, dict):
            findings.append(Finding("fail", "invalid_pip_slot", "pip_slots entries must be objects", f"{assignment_path}:pip_slots[{index}]"))
            continue
        path = f"{assignment_path}:pip_slots[{index}]"
        start = parse_time_seconds(slot.get("start") or slot.get("start_sec") or slot.get("trigger_time"))
        duration = duration_from_payload(slot)
        end = parse_time_seconds(slot.get("end") or slot.get("end_sec"))
        if start is not None and end is None and duration is not None:
            end = start + duration
        if start is not None and end is not None and end >= start:
            timed_slots.append((start, end))
        group_id = normalize_ws(str(slot.get("group_id") or slot.get("pip_group") or slot.get("grid_group") or slot.get("layout_group") or ""))
        if group_id:
            group_counts[group_id] = group_counts.get(group_id, 0) + 1

        if not slot.get("cue_id") or not slot.get("cue_text"):
            findings.append(Finding("fail", "pip_slot_missing_cue", "PiP slot must include cue_id and cue_text", path))
        image = slot.get("image") if isinstance(slot.get("image"), dict) else {}
        if not image.get("image_id") or not image.get("role"):
            findings.append(Finding("fail", "pip_slot_missing_image_role", "PiP slot must include image_id and role", path))
        if not slot.get("match_reason"):
            findings.append(Finding("fail", "pip_slot_missing_reason", "PiP slot must include match_reason", path))
        if strict_social_ad:
            if not group_id:
                findings.append(Finding("fail", "pip_slot_missing_group", "PiP slot must declare a group_id/grid_group for simultaneous grid layout", path))
            grid = slot.get("grid") if isinstance(slot.get("grid"), dict) else {}
            layout = normalize_token(slot.get("layout") or slot.get("layout_mode") or grid.get("layout"))
            has_grid_position = bool(
                layout == "grid"
                or slot.get("grid_slot")
                or slot.get("grid_index")
                or ((slot.get("row") or grid.get("row")) and (slot.get("col") or slot.get("column") or grid.get("col") or grid.get("column")))
            )
            if not has_grid_position:
                findings.append(Finding("fail", "pip_slot_missing_grid_position", "PiP slot must expose grid row/column or grid_slot evidence", path))
            size = slot.get("size") if isinstance(slot.get("size"), dict) else {}
            bounds = slot.get("bounds") if isinstance(slot.get("bounds"), dict) else {}
            width = (
                parse_dimension(slot.get("width"), 1920)
                or parse_dimension(size.get("width"), 1920)
                or parse_dimension(bounds.get("width") or bounds.get("w"), 1920)
            )
            height = (
                parse_dimension(slot.get("height"), 1080)
                or parse_dimension(size.get("height"), 1080)
                or parse_dimension(bounds.get("height") or bounds.get("h"), 1080)
            )
            if width is None or height is None:
                findings.append(Finding("fail", "pip_slot_missing_size", "PiP slot must expose width and height", path))
            elif width < min_pip_width_px or height < min_pip_height_px:
                findings.append(
                    Finding(
                        "fail",
                        "pip_slot_too_small",
                        f"PiP slot size {width:.0f}x{height:.0f}px is below minimum {min_pip_width_px:.0f}x{min_pip_height_px:.0f}px",
                        path,
                    )
                )
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
        if has_private_traffic_material_evidence(slot):
            if not has_no_upscale_evidence(slot):
                findings.append(Finding("fail", "private_traffic_slot_missing_no_upscale", "traffic PiP slot must declare no-upscale/native-scale evidence", path))
            findings.extend(validate_no_upscale(slot, path, "private_traffic_slot"))

    if strict_social_ad and isinstance(pip_slots, list) and pip_slots:
        max_group = max(group_counts.values(), default=0)
        max_time = 0
        if timed_slots:
            points = sorted({point for interval in timed_slots for point in interval})
            for left, right in zip(points, points[1:]):
                mid = (left + right) / 2
                max_time = max(max_time, sum(1 for start, end in timed_slots if start <= mid < end))
        if max(max_group, max_time) < min_simultaneous_pips:
            findings.append(
                Finding(
                    "fail",
                    "assignment_pip_no_simultaneous_group",
                    f"assignment PiP must include at least {min_simultaneous_pips} simultaneous/grid-grouped slots",
                    str(assignment_path),
                )
            )
    return metrics, findings


def validate_hook_opening_plan(segment: dict[str, Any], details: dict[str, Any], path: str) -> list[Finding]:
    findings: list[Finding] = []
    payloads = representative_payloads(segment, details, "opening_asset", "hook_asset", "hook_visual", "selected_opening_material")
    if not any(isinstance(payload, dict) and has_opening_material_evidence(payload) for _, payload in payloads):
        findings.append(
            Finding(
                "fail",
                "hook_opening_missing_opening_asset",
                "hook_opening must select real material from projects/素材/开头素材",
                path,
            )
        )

    durations = [duration_from_payload(payload) for _, payload in payloads if isinstance(payload, dict)]
    duration = next((item for item in durations if item is not None), None)
    if duration is None:
        findings.append(
            Finding(
                "fail",
                "hook_opening_missing_duration",
                "selected opening material must record a 5-10 second display/crop duration",
                path,
            )
        )
    elif duration < OPENING_MATERIAL_MIN_DURATION or duration > OPENING_MATERIAL_MAX_DURATION:
        findings.append(
            Finding(
                "fail",
                "hook_opening_duration_out_of_range",
                f"selected opening material duration {duration:.2f}s must be between {OPENING_MATERIAL_MIN_DURATION:.0f}s and {OPENING_MATERIAL_MAX_DURATION:.0f}s",
                path,
            )
        )

    if not any(isinstance(payload, dict) and has_full_display_evidence(payload) for _, payload in payloads):
        findings.append(
            Finding(
                "fail",
                "hook_opening_missing_full_display",
                "selected opening material must declare full-frame/no-crop/contain display evidence",
                path,
            )
        )
    for label, payload in payloads:
        if isinstance(payload, dict):
            findings.extend(validate_no_upscale(payload, f"{path}.{label}", "hook_opening"))
    return findings


def validate_private_traffic_plan(segment: dict[str, Any], details: dict[str, Any], path: str) -> list[Finding]:
    findings: list[Finding] = []
    payloads = representative_payloads(segment, details, "traffic_asset", "private_traffic_asset", "cta_asset", "selected_traffic_material")
    relevant_payloads = [(label, payload) for label, payload in payloads if isinstance(payload, dict)]
    has_branch_evidence = any(has_private_traffic_material_evidence(payload) for _, payload in relevant_payloads)
    if not has_branch_evidence:
        findings.append(
            Finding(
                "warn",
                "private_traffic_missing_branch_evidence",
                "private_traffic_cta should point to projects/素材/引流素材 or equivalent CTA material evidence",
                path,
            )
        )
    if not any(has_no_upscale_evidence(payload) for _, payload in relevant_payloads):
        findings.append(
            Finding(
                "fail",
                "private_traffic_missing_no_upscale",
                "traffic/CTA material must declare no-upscale/native-scale/contain evidence to avoid amplifying blur",
                path,
            )
        )
    for label, payload in relevant_payloads:
        findings.extend(validate_no_upscale(payload, f"{path}.{label}", "private_traffic"))
    return findings


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
        findings.extend(validate_background_surface(throughline, str(plan_path), "background_throughline"))
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
            findings.extend(validate_background_surface(background, path, "background_video"))

        if strict_social_ad and role == "hook_opening":
            findings.extend(validate_hook_opening_plan(segment, details, path))
        if strict_social_ad and role == "private_traffic_cta":
            findings.extend(validate_private_traffic_plan(segment, details, path))

        overlay_data = details.get("editorial_overlay") or segment.get("editorial_overlay") or segment.get("big_text")
        overlay_text = overlay_summary_text(overlay_data)
        if strict_social_ad and "editorial_overlay" in layers and not overlay_text:
            findings.append(
                Finding(
                    "fail",
                    "editorial_overlay_missing_summary",
                    "editorial overlay must contain a core word, phrase, or one-sentence summary",
                    path,
                )
            )
        if strict_social_ad and overlay_text and not overlay_has_segment_source(overlay_data):
            findings.append(
                Finding(
                    "fail",
                    "editorial_overlay_missing_segment_source",
                    "editorial overlay must record matched source_cue_ids, source_text, and match_reason for paragraph-level title extraction",
                    path,
                )
            )
        process_match = internal_process_label_match(overlay_text)
        if overlay_text and process_match:
            findings.append(
                Finding(
                    "fail",
                    "editorial_overlay_internal_process_title",
                    "editorial overlay title must summarize matched audience copy, not expose workflow/process/learning labels",
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
    min_simultaneous_pips: int,
    min_pip_width_px: float,
    min_pip_height_px: float,
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
    backgrounds = [item for item in elements if is_background_video(item)]
    metrics = {
        "project_root": str(project_root),
        "dialogue_caption_count": len(captions),
        "editorial_overlay_count": len(overlays),
        "semantic_pip_count": len(pips),
        "background_video_element_count": len(backgrounds),
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
    findings.extend(
        validate_pip_html(
            pips,
            html_path,
            min_pip_slots=min_pip_slots,
            min_simultaneous_pips=min_simultaneous_pips,
            min_pip_width_px=min_pip_width_px,
            min_pip_height_px=min_pip_height_px,
            strict_social_ad=strict_social_ad,
        )
    )
    findings.extend(validate_background_html(backgrounds, html_path))
    findings.extend(validate_private_traffic_html(elements, html_path))

    assignment_path = project_root / "workflow_assignment.json"
    if not assignment_path.exists():
        legacy_assignment_path = project_root / "f2_assignment.json"
        if legacy_assignment_path.exists():
            assignment_path = legacy_assignment_path
    if assignment_path.exists():
        assignment_metrics, assignment_findings = validate_assignment(
            assignment_path,
            min_pip_slots=min_pip_slots,
            min_simultaneous_pips=min_simultaneous_pips,
            min_pip_width_px=min_pip_width_px,
            min_pip_height_px=min_pip_height_px,
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
    parser.add_argument("--min-simultaneous-pips", type=int, default=DEFAULT_MIN_SIMULTANEOUS_PIPS, help="minimum PiP windows that must appear together in strict mode")
    parser.add_argument("--min-pip-width-px", type=float, default=DEFAULT_MIN_PIP_WIDTH_PX, help="minimum rendered PiP width in strict mode")
    parser.add_argument("--min-pip-height-px", type=float, default=DEFAULT_MIN_PIP_HEIGHT_PX, help="minimum rendered PiP height in strict mode")
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
            min_simultaneous_pips=args.min_simultaneous_pips,
            min_pip_width_px=args.min_pip_width_px,
            min_pip_height_px=args.min_pip_height_px,
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
