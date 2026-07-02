#!/usr/bin/env python3
"""Validate workflow dialogue caption timing evidence.

This script is intentionally mechanical. It does not generate subtitles, infer
creative grouping, or perform ASR. It verifies that an workflow final-ready project has
structured per-cue timing evidence and that the HyperFrames caption timeline
matches that evidence.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


DISALLOWED_METHOD_MARKERS = (
    "manual_script_audio_duration",
    "duration_ratio",
    "total_duration",
    "equal_split",
    "proportional",
    "blind_manual",
)

PREVIEW_MARKERS = (
    "preview",
    "草稿",
    "不宣称",
    "建议补跑",
    "not machine word timestamps",
    "not strict",
)

ALLOWED_CAPTION_TYPES = {"dialogue_caption", "editorial_overlay"}

SCRIPT_SOURCE_KEYS = (
    "source_script",
    "script_path",
    "content_truth",
    "content_truth_path",
    "script_source",
)
AUDIO_SOURCE_KEYS = (
    "source_audio",
    "audio_clock_path",
    "paired_audio",
    "paired_audio_path",
)
STEM_SOURCE_KEYS = (
    "script_audio_stem",
    "batch_stem",
    "content_stem",
    "stem",
)

SCRIPT_ORDER_KEYS = (
    "script_order",
    "source_order",
    "caption_order",
    "sequence",
    "script_index",
    "source_index",
    "sentence_index",
    "line_index",
    "line_no",
    "line",
    "start_char",
    "char_start",
    "start_index",
    "offset_start",
)


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    path: str = ""


@dataclass
class NormalizedCue:
    raw: dict[str, Any]
    index: int
    cue_id: str
    start: float | None
    end: float | None
    caption_type: str | None
    spoken_text: str
    display_text: str
    script_anchor: Any
    script_order: float | None
    sync_method: str
    audio_anchor: Any
    tolerance_ms: float | None


@dataclass
class HtmlCaption:
    element_id: str
    cue_id: str
    start: float
    end: float
    text: str


class CaptionHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._stack: list[dict[str, Any]] = []
        self.captions: list[HtmlCaption] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        class_value = attr.get("class", "")
        element_id = attr.get("id", "")
        is_caption = "caption" in class_value.split() or "caption" in element_id.lower() or re.match(r"cap[-_\d]", element_id.lower() or "")
        if is_caption and "data-start" in attr and "data-duration" in attr:
            self._stack.append(
                {
                    "depth": 1,
                    "id": element_id,
                    "cue_id": first_present(attr, ("data-cue-id", "data-cue", "data-caption-id", "data-id"), ""),
                    "start": attr.get("data-start", ""),
                    "duration": attr.get("data-duration", ""),
                    "text_parts": [],
                }
            )
        elif self._stack:
            self._stack[-1]["depth"] += 1

    def handle_endtag(self, tag: str) -> None:
        if not self._stack:
            return
        self._stack[-1]["depth"] -= 1
        if self._stack[-1]["depth"] > 0:
            return
        current = self._stack.pop()
        start = parse_float(current["start"])
        duration = parse_float(current["duration"])
        if start is None or duration is None:
            return
        text = normalize_ws("".join(current["text_parts"]))
        self.captions.append(HtmlCaption(current["id"], current["cue_id"], start, start + duration, text))

    def handle_data(self, data: str) -> None:
        if self._stack:
            self._stack[-1]["text_parts"].append(data)


def normalize_ws(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def normalize_text(value: str) -> str:
    value = normalize_ws(value)
    return re.sub(r"[\s，。！？、,.!?；;：:（）()《》<>\"'“”‘’+\-·]", "", value).lower()


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return number


def deep_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(deep_text(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(deep_text(item) for item in value)
    return str(value)


def first_present(mapping: dict[str, Any], keys: tuple[str, ...], default: Any = None) -> Any:
    for key in keys:
        if key in mapping and mapping[key] not in (None, ""):
            return mapping[key]
    return default


def load_json(path: Path) -> tuple[dict[str, Any] | None, list[Finding]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except FileNotFoundError:
        return None, [Finding("fail", "missing_alignment", f"dialogue alignment file not found: {path}", str(path))]
    except json.JSONDecodeError as exc:
        return None, [Finding("fail", "invalid_json", f"invalid JSON: {exc}", str(path))]


def collect_cue_items(data: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("cues", "cue_groups", "caption_cues", "dialogue_cues"):
        value = data.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def collect_duration(data: dict[str, Any]) -> float | None:
    direct = first_present(data, ("duration_s", "clock_duration_s", "audio_duration_s"))
    duration = parse_float(direct)
    if duration is not None:
        return duration
    basis = data.get("alignment_basis")
    if isinstance(basis, dict):
        return parse_float(first_present(basis, ("duration_s", "clock_duration_s", "audio_duration_s")))
    return None


def collect_audio_path(data: dict[str, Any]) -> str:
    direct = first_present(data, ("audio_path", "clock_source", "primary_audio", "project_audio"), "")
    if direct:
        return str(direct)
    basis = data.get("alignment_basis")
    if isinstance(basis, dict):
        return str(first_present(basis, ("audio_path", "clock_source", "primary_audio", "project_audio"), ""))
    return ""


def collect_source_field(data: dict[str, Any], keys: tuple[str, ...]) -> str:
    direct = first_present(data, keys, "")
    if direct:
        return str(direct)
    for container_key in ("alignment_basis", "source_pair", "script_audio_pair", "source"):
        container = data.get(container_key)
        if isinstance(container, dict):
            value = first_present(container, keys, "")
            if value:
                return str(value)
    return ""


def path_stem(value: str) -> str:
    if not value:
        return ""
    return Path(value).stem.strip()


def is_bgm_path(value: str) -> bool:
    if not value:
        return False
    return path_stem(value).lower() == "bgm"


def path_mentions_material_pool(value: str) -> bool:
    if not value:
        return False
    normalized = value.replace("\\", "/")
    return "projects/内容/文案/" in normalized or "projects/内容/音频/" in normalized


def collect_pair_map(data: dict[str, Any]) -> Any:
    for key in ("script_audio_pair_map", "script_audio_pairs", "batch_pairs"):
        value = data.get(key)
        if value:
            return value
    basis = data.get("alignment_basis")
    if isinstance(basis, dict):
        for key in ("script_audio_pair_map", "script_audio_pairs", "batch_pairs"):
            value = basis.get(key)
            if value:
                return value
    return None


def validate_script_audio_pair(
    data: dict[str, Any],
    *,
    audio_path: str,
    strict_final: bool,
    require_script_audio_pair: bool,
) -> tuple[list[Finding], dict[str, Any]]:
    findings: list[Finding] = []
    metrics: dict[str, Any] = {}
    source_script = collect_source_field(data, SCRIPT_SOURCE_KEYS)
    source_audio = collect_source_field(data, AUDIO_SOURCE_KEYS)
    declared_stem = collect_source_field(data, STEM_SOURCE_KEYS)
    pair_map = collect_pair_map(data)
    pair_required = (
        require_script_audio_pair
        or isinstance(pair_map, (dict, list))
        or path_mentions_material_pool(source_script)
        or path_mentions_material_pool(source_audio)
        or path_mentions_material_pool(audio_path)
    )

    metrics["source_script"] = source_script
    metrics["source_audio"] = source_audio
    metrics["script_audio_stem"] = declared_stem
    metrics["script_audio_pair_required"] = pair_required

    if strict_final and is_bgm_path(audio_path):
        findings.append(Finding("fail", "bgm_as_audio_clock", "BGM.* must not be used as the dialogue audio clock", "audio_path"))
    if strict_final and is_bgm_path(source_audio):
        findings.append(Finding("fail", "bgm_as_source_audio", "BGM.* must not be used as source_audio for dialogue", "source_audio"))

    if not pair_required:
        return findings, metrics

    if not source_script:
        findings.append(
            Finding(
                "fail",
                "missing_source_script",
                "script/audio pair route must record source_script from projects/内容/文案/",
            )
        )
    if not source_audio:
        findings.append(
            Finding(
                "fail",
                "missing_source_audio",
                "script/audio pair route must record source_audio from projects/内容/音频/",
            )
        )
    if not declared_stem:
        findings.append(
            Finding(
                "fail",
                "missing_script_audio_stem",
                "script/audio pair route must record the shared source stem",
            )
        )

    script_stem = path_stem(source_script)
    audio_stem = path_stem(source_audio)
    if script_stem and audio_stem and script_stem != audio_stem:
        findings.append(
            Finding(
                "fail",
                "script_audio_stem_mismatch",
                f"source_script stem {script_stem!r} does not match source_audio stem {audio_stem!r}",
            )
        )
    if declared_stem and script_stem and declared_stem != script_stem:
        findings.append(
            Finding(
                "fail",
                "declared_stem_mismatch",
                f"script_audio_stem {declared_stem!r} does not match source_script stem {script_stem!r}",
            )
        )
    if declared_stem and audio_stem and declared_stem != audio_stem:
        findings.append(
            Finding(
                "fail",
                "declared_stem_audio_mismatch",
                f"script_audio_stem {declared_stem!r} does not match source_audio stem {audio_stem!r}",
            )
        )
    return findings, metrics


def normalize_cue(raw: dict[str, Any], index: int, global_method: str, default_tolerance_ms: float) -> NormalizedCue:
    start = parse_float(first_present(raw, ("start_s", "start", "from_s", "from")))
    end = parse_float(first_present(raw, ("end_s", "end", "to_s", "to")))
    if end is None:
        duration = parse_float(first_present(raw, ("duration_s", "duration")))
        if start is not None and duration is not None:
            end = start + duration

    spoken_text = str(first_present(raw, ("spoken_text", "transcript_text", "voice_text", "text"), ""))
    display_text = str(first_present(raw, ("display_text", "caption", "subtitle", "text"), ""))
    caption_type = first_present(raw, ("caption_type", "type", "cue_type"), None)
    script_anchor = first_present(raw, ("script_span", "script_anchor", "script_source_span", "source_span"), None)
    script_order = script_order_from(first_present(raw, SCRIPT_ORDER_KEYS, None))
    if script_order is None:
        script_order = script_order_from(script_anchor)
    sync_method = str(first_present(raw, ("sync_method", "clock_method", "method"), global_method or ""))
    audio_anchor = first_present(raw, ("audio_anchor", "audio_anchors", "transcript_anchor", "transcript_segment", "anchor"), None)
    tolerance = parse_float(first_present(raw, ("tolerance_ms", "sync_tolerance_ms", "max_offset_ms"), default_tolerance_ms))
    cue_id = str(first_present(raw, ("id", "cue_id"), f"cue-{index + 1:02d}"))

    return NormalizedCue(
        raw=raw,
        index=index,
        cue_id=cue_id,
        start=start,
        end=end,
        caption_type=str(caption_type) if caption_type is not None else None,
        spoken_text=spoken_text,
        display_text=display_text,
        script_anchor=script_anchor,
        script_order=script_order,
        sync_method=sync_method,
        audio_anchor=audio_anchor,
        tolerance_ms=tolerance,
    )


def collect_global_method(data: dict[str, Any]) -> str:
    pieces = [
        data.get("clock_method"),
        data.get("sync_method"),
        data.get("cue_policy"),
        data.get("status"),
    ]
    for key in ("asr_status", "transcription_status", "alignment_basis"):
        value = data.get(key)
        if isinstance(value, dict):
            pieces.append(value.get("result"))
            pieces.append(value.get("status"))
            pieces.append(value.get("fallback_disclosure"))
            pieces.append(value.get("note"))
            pieces.append(value.get("transcription_status"))
    return " ".join(str(piece) for piece in pieces if piece not in (None, ""))


def is_disallowed_method(value: str) -> bool:
    lowered = value.lower()
    return any(marker in lowered for marker in DISALLOWED_METHOD_MARKERS)


def is_preview_only(value: str) -> bool:
    lowered = value.lower()
    return any(marker.lower() in lowered for marker in PREVIEW_MARKERS)


def anchor_window(anchor: Any) -> tuple[float | None, float | None]:
    if isinstance(anchor, list):
        starts: list[float] = []
        ends: list[float] = []
        for item in anchor:
            item_start, item_end = anchor_window(item)
            if item_start is not None:
                starts.append(item_start)
            if item_end is not None:
                ends.append(item_end)
        return (min(starts) if starts else None, max(ends) if ends else None)
    if not isinstance(anchor, dict):
        return None, None
    start = parse_float(first_present(anchor, ("start_s", "start", "audio_start_s", "from_s", "from")))
    end = parse_float(first_present(anchor, ("end_s", "end", "audio_end_s", "to_s", "to")))
    if end is None:
        duration = parse_float(first_present(anchor, ("duration_s", "duration")))
        if start is not None and duration is not None:
            end = start + duration
    return start, end


def script_order_from(value: Any) -> float | None:
    if isinstance(value, list):
        orders = [script_order_from(item) for item in value]
        numeric_orders = [item for item in orders if item is not None]
        return min(numeric_orders) if numeric_orders else None
    if isinstance(value, dict):
        direct = first_present(value, SCRIPT_ORDER_KEYS, None)
        order = parse_float(direct)
        if order is not None:
            return order
        for nested_key in ("span", "script_span", "source_span", "anchor", "range"):
            order = script_order_from(value.get(nested_key))
            if order is not None:
                return order
    return parse_float(value)


def text_match_score(a: str, b: str) -> float:
    left = normalize_text(a)
    right = normalize_text(b)
    if not left or not right:
        return 0.0
    if left == right:
        return 1.0
    if left in right or right in left:
        return min(len(left), len(right)) / max(len(left), len(right))
    left_chars = set(left)
    right_chars = set(right)
    return len(left_chars & right_chars) / max(len(left_chars | right_chars), 1)


def validate_alignment(
    data: dict[str, Any],
    *,
    strict_final: bool,
    default_tolerance_ms: float,
    require_dialogue_captions: bool,
    require_script_audio_pair: bool,
) -> tuple[list[NormalizedCue], list[Finding], dict[str, Any]]:
    findings: list[Finding] = []
    metrics: dict[str, Any] = {}
    global_method = collect_global_method(data)
    duration = collect_duration(data)
    audio_path = collect_audio_path(data)
    cue_items = collect_cue_items(data)
    global_tolerance = parse_float(first_present(data, ("sync_tolerance_ms", "tolerance_ms"), default_tolerance_ms)) or default_tolerance_ms
    cues = [normalize_cue(item, index, global_method, global_tolerance) for index, item in enumerate(cue_items)]

    metrics["cue_count"] = len(cues)
    metrics["duration_s"] = duration
    metrics["audio_path"] = audio_path
    pair_findings, pair_metrics = validate_script_audio_pair(
        data,
        audio_path=audio_path,
        strict_final=strict_final,
        require_script_audio_pair=require_script_audio_pair,
    )
    metrics.update(pair_metrics)
    findings.extend(pair_findings)

    if not audio_path:
        findings.append(Finding("fail", "missing_audio_clock", "missing audio clock path/source"))
    if duration is None:
        findings.append(Finding("fail", "missing_audio_duration", "missing audio duration"))
    if not cues:
        findings.append(Finding("fail", "missing_cues", "no cue list found; expected cues/cue_groups/caption_cues"))
    if is_disallowed_method(global_method):
        findings.append(Finding("fail", "disallowed_clock_method", "global clock method indicates total-duration/proportional timing"))
    if strict_final and is_preview_only(global_method):
        findings.append(Finding("fail", "preview_only_timing", "alignment metadata says timing is preview/draft or not strict"))

    seen_cue_ids: dict[str, int] = {}
    for cue in cues:
        if cue.cue_id in seen_cue_ids:
            findings.append(
                Finding(
                    "fail",
                    "duplicate_cue_id",
                    f"cue id {cue.cue_id!r} duplicates cue[{seen_cue_ids[cue.cue_id]}]",
                    f"cue[{cue.index}]/{cue.cue_id}",
                )
            )
        else:
            seen_cue_ids[cue.cue_id] = cue.index

    previous_end: float | None = None
    previous_dialogue_script_order: float | None = None
    previous_audio_anchor_end: float | None = None
    dialogue_count = 0
    editorial_count = 0
    script_order_count = 0
    audio_anchor_count = 0
    for cue in cues:
        path = f"cue[{cue.index}]/{cue.cue_id}"
        if cue.start is None or cue.end is None:
            findings.append(Finding("fail", "missing_cue_time", "cue must have numeric start/end", path))
            continue
        if cue.end <= cue.start:
            findings.append(Finding("fail", "invalid_cue_window", "cue end must be greater than start", path))
        if previous_end is not None and cue.start < previous_end - 0.02:
            findings.append(Finding("fail", "overlapping_cues", "cue overlaps previous cue by more than 20ms", path))
        previous_end = max(previous_end if previous_end is not None else cue.end, cue.end)

        if cue.caption_type not in ALLOWED_CAPTION_TYPES:
            findings.append(Finding("fail", "missing_caption_type", "cue must declare caption_type=dialogue_caption or editorial_overlay", path))
            inferred_dialogue = True
        else:
            inferred_dialogue = cue.caption_type == "dialogue_caption"

        if inferred_dialogue:
            dialogue_count += 1
            if cue.script_order is None:
                if strict_final:
                    findings.append(
                        Finding(
                            "fail",
                            "missing_script_order",
                            "strict dialogue cue must include sortable script order evidence such as script_order or script_span.start_char",
                            path,
                        )
                    )
            else:
                script_order_count += 1
                if previous_dialogue_script_order is not None and cue.script_order < previous_dialogue_script_order - 0.001:
                    findings.append(
                        Finding(
                            "fail",
                            "script_order_regression",
                            f"dialogue cue script order regresses from {previous_dialogue_script_order:g} to {cue.script_order:g}",
                            path,
                        )
                    )
                previous_dialogue_script_order = cue.script_order
            if not normalize_ws(cue.spoken_text):
                findings.append(Finding("fail", "missing_spoken_text", "dialogue cue must include spoken_text/text", path))
            if not normalize_ws(cue.display_text):
                findings.append(Finding("fail", "missing_display_text", "dialogue cue must include display_text/caption/text", path))
            if cue.script_anchor in (None, ""):
                findings.append(Finding("fail", "missing_script_anchor", "dialogue cue must include script_span or script_anchor", path))
            if is_disallowed_method(cue.sync_method):
                findings.append(Finding("fail", "disallowed_cue_method", "cue method indicates total-duration/proportional timing", path))
            if strict_final and is_preview_only(deep_text(cue.raw)):
                findings.append(Finding("fail", "preview_only_cue", "cue contains preview/draft timing language", path))
            if cue.audio_anchor in (None, ""):
                findings.append(Finding("fail", "missing_audio_anchor", "dialogue cue must include per-cue audio_anchor/transcript_anchor", path))
            else:
                anchor_start, anchor_end = anchor_window(cue.audio_anchor)
                if anchor_start is None or anchor_end is None:
                    findings.append(Finding("fail", "missing_audio_anchor_time", "audio anchor must include numeric start/end", path))
                else:
                    audio_anchor_count += 1
                    if previous_audio_anchor_end is not None and anchor_start < previous_audio_anchor_end - 0.02:
                        findings.append(
                            Finding(
                                "fail",
                                "audio_anchor_order_regression",
                                f"audio anchor starts before the previous dialogue audio anchor ended ({anchor_start:.3f}s < {previous_audio_anchor_end:.3f}s)",
                                path,
                            )
                        )
                    previous_audio_anchor_end = max(previous_audio_anchor_end if previous_audio_anchor_end is not None else anchor_end, anchor_end)
                    tolerance = cue.tolerance_ms or (100.0 if (cue.end - cue.start) <= 1.5 else default_tolerance_ms)
                    start_delta = abs((cue.start - anchor_start) * 1000.0)
                    end_delta = abs((cue.end - anchor_end) * 1000.0)
                    if start_delta > tolerance or end_delta > tolerance:
                        findings.append(
                            Finding(
                                "fail",
                                "anchor_tolerance_exceeded",
                                f"cue differs from audio anchor by {start_delta:.0f}ms/{end_delta:.0f}ms, tolerance {tolerance:.0f}ms",
                                path,
                            )
                        )
            if cue.spoken_text and cue.display_text:
                score = text_match_score(cue.spoken_text, cue.display_text)
                if score < 0.55:
                    findings.append(
                        Finding(
                            "fail",
                            "dialogue_display_mismatch",
                            f"display text does not appear to be a dialogue subtitle for spoken text (score {score:.2f})",
                            path,
                        )
                    )
        else:
            editorial_count += 1

    if duration is not None and previous_end is not None and abs(duration - previous_end) > 0.5:
        findings.append(Finding("fail", "duration_mismatch", f"last cue ends at {previous_end:.3f}s, audio duration is {duration:.3f}s"))
    if require_dialogue_captions and dialogue_count == 0:
        findings.append(Finding("fail", "no_dialogue_captions", "no dialogue_caption cue found"))

    metrics["dialogue_caption_count"] = dialogue_count
    metrics["editorial_overlay_count"] = editorial_count
    metrics["cue_ids"] = [cue.cue_id for cue in cues]
    metrics["script_order_count"] = script_order_count
    metrics["audio_anchor_count"] = audio_anchor_count
    return cues, findings, metrics


def parse_html_captions(path: Path) -> tuple[list[HtmlCaption], list[Finding]]:
    if not path.exists():
        return [], [Finding("fail", "missing_html", f"HyperFrames HTML not found: {path}", str(path))]
    parser = CaptionHTMLParser()
    try:
        parser.feed(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError as exc:
        return [], [Finding("fail", "html_read_error", f"cannot read HTML as UTF-8: {exc}", str(path))]
    return parser.captions, []


def validate_html_timeline(
    cues: list[NormalizedCue],
    html_captions: list[HtmlCaption],
    dom_tolerance_ms: float,
    *,
    require_html_cue_ids: bool,
) -> list[Finding]:
    findings: list[Finding] = []
    dialogue_cues = [cue for cue in cues if cue.caption_type == "dialogue_caption"]
    if not dialogue_cues:
        return findings
    if not html_captions:
        findings.append(Finding("fail", "missing_html_captions", "no caption elements with data-start/data-duration found in index.html"))
        return findings
    if len(html_captions) != len(dialogue_cues):
        findings.append(
            Finding(
                "fail",
                "html_caption_count_mismatch",
                f"HTML caption count {len(html_captions)} does not match dialogue cue count {len(dialogue_cues)}",
            )
        )

    previous_html_start: float | None = None
    seen_html_cue_ids: dict[str, str] = {}
    for caption in html_captions:
        locator = f"html/{caption.element_id or caption.cue_id or 'caption'}"
        if previous_html_start is not None and caption.start < previous_html_start - 0.02:
            findings.append(
                Finding(
                    "fail",
                    "html_caption_order_regression",
                    "HTML caption DOM order is not monotonic by data-start; render order may scramble subtitles",
                    locator,
                )
            )
        previous_html_start = max(previous_html_start if previous_html_start is not None else caption.start, caption.start)
        if require_html_cue_ids and not caption.cue_id:
            findings.append(Finding("fail", "html_missing_cue_id", "strict final captions must include data-cue-id", locator))
        if caption.cue_id:
            if caption.cue_id in seen_html_cue_ids:
                findings.append(
                    Finding(
                        "fail",
                        "duplicate_html_cue_id",
                        f"HTML cue id {caption.cue_id!r} duplicates {seen_html_cue_ids[caption.cue_id]}",
                        locator,
                    )
                )
            else:
                seen_html_cue_ids[caption.cue_id] = locator

    timeline_cues = sorted(
        [cue for cue in dialogue_cues if cue.start is not None and cue.end is not None],
        key=lambda cue: (cue.start or 0.0, cue.end or 0.0, cue.index),
    )
    timeline_captions = sorted(html_captions, key=lambda caption: (caption.start, caption.end, caption.element_id))

    for cue, caption in zip(timeline_cues, timeline_captions):
        path = f"html/{caption.element_id or cue.cue_id}"
        if cue.start is None or cue.end is None:
            continue
        if caption.cue_id and caption.cue_id != cue.cue_id:
            findings.append(
                Finding(
                    "fail",
                    "html_cue_id_mismatch",
                    f"HTML data-cue-id {caption.cue_id!r} does not match timeline cue id {cue.cue_id!r}",
                    path,
                )
            )
        start_delta = abs((cue.start - caption.start) * 1000.0)
        end_delta = abs((cue.end - caption.end) * 1000.0)
        if start_delta > dom_tolerance_ms or end_delta > dom_tolerance_ms:
            findings.append(
                Finding(
                    "fail",
                    "html_timing_mismatch",
                    f"HTML timing differs from dialogue_alignment by {start_delta:.0f}ms/{end_delta:.0f}ms",
                    path,
                )
            )
        score = text_match_score(cue.display_text or cue.spoken_text, caption.text)
        if score < 0.55:
            findings.append(
                Finding(
                    "fail",
                    "html_text_mismatch",
                    f"HTML caption text does not match dialogue cue display text (score {score:.2f})",
                    path,
                )
            )
    return findings


def ffprobe_duration(path: Path) -> float | None:
    if not path.exists():
        return None
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return parse_float(result.stdout.strip())


def validate_audio_duration(project_root: Path, audio_path: str, declared_duration: float | None) -> list[Finding]:
    if not audio_path or declared_duration is None:
        return []
    candidates = [Path(audio_path)]
    if not Path(audio_path).is_absolute():
        candidates.insert(0, project_root / audio_path)
    actual_path = next((candidate for candidate in candidates if candidate.exists()), None)
    if actual_path is None:
        return [Finding("warn", "audio_file_not_found", f"audio file not found for duration probe: {audio_path}")]
    actual_duration = ffprobe_duration(actual_path)
    if actual_duration is None:
        return [Finding("warn", "ffprobe_unavailable", f"could not ffprobe audio duration: {actual_path}")]
    if abs(actual_duration - declared_duration) > 0.25:
        return [
            Finding(
                "fail",
                "audio_duration_probe_mismatch",
                f"declared audio duration {declared_duration:.3f}s differs from ffprobe {actual_duration:.3f}s",
                str(actual_path),
            )
        ]
    return []


def finding_to_dict(finding: Finding) -> dict[str, str]:
    data = {"severity": finding.severity, "code": finding.code, "message": finding.message}
    if finding.path:
        data["path"] = finding.path
    return data


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate workflow dialogue synchronization evidence.")
    parser.add_argument("project_root", type=Path, help="workflow/HyperFrames project root")
    parser.add_argument("--alignment", type=Path, help="dialogue_alignment.json path; defaults to project_root/dialogue_alignment.json")
    parser.add_argument("--html", type=Path, help="HyperFrames HTML path; defaults to project_root/index.html")
    parser.add_argument("--strict-final", action="store_true", help="fail preview/draft or total-duration timing evidence")
    parser.add_argument(
        "--require-script-audio-pair",
        action="store_true",
        help="require source_script/source_audio/shared stem evidence for projects/内容/文案 + projects/内容/音频 routes",
    )
    parser.add_argument("--no-html", action="store_true", help="skip HTML caption timeline comparison")
    parser.add_argument("--require-dialogue-captions", action="store_true", default=True, help="require at least one dialogue_caption cue")
    parser.add_argument("--allow-no-dialogue-captions", action="store_false", dest="require_dialogue_captions")
    parser.add_argument("--tolerance-ms", type=float, default=150.0, help="default audio-anchor tolerance in milliseconds")
    parser.add_argument("--dom-tolerance-ms", type=float, default=80.0, help="HTML-vs-alignment timing tolerance in milliseconds")
    parser.add_argument("--write-report", type=Path, help="write JSON validation report")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    project_root = args.project_root.resolve()
    alignment_path = args.alignment.resolve() if args.alignment else project_root / "dialogue_alignment.json"
    html_path = args.html.resolve() if args.html else project_root / "index.html"

    data, findings = load_json(alignment_path)
    metrics: dict[str, Any] = {}
    cues: list[NormalizedCue] = []
    if data is not None:
        cues, alignment_findings, metrics = validate_alignment(
            data,
            strict_final=args.strict_final,
            default_tolerance_ms=args.tolerance_ms,
            require_dialogue_captions=args.require_dialogue_captions,
            require_script_audio_pair=args.require_script_audio_pair,
        )
        findings.extend(alignment_findings)
        findings.extend(validate_audio_duration(project_root, metrics.get("audio_path", ""), metrics.get("duration_s")))

    if data is not None and not args.no_html:
        html_captions, html_findings = parse_html_captions(html_path)
        findings.extend(html_findings)
        if not html_findings:
            findings.extend(
                validate_html_timeline(
                    cues,
                    html_captions,
                    args.dom_tolerance_ms,
                    require_html_cue_ids=args.strict_final,
                )
            )
            metrics["html_caption_count"] = len(html_captions)

    fail_count = sum(1 for finding in findings if finding.severity == "fail")
    warn_count = sum(1 for finding in findings if finding.severity == "warn")
    report = {
        "schema": "workflow_dialogue_sync_validation.v2",
        "project_root": str(project_root),
        "alignment_path": str(alignment_path),
        "html_path": str(html_path) if not args.no_html else None,
        "strict_final": args.strict_final,
        "require_script_audio_pair": args.require_script_audio_pair,
        "verdict": "pass" if fail_count == 0 else "fail",
        "fail_count": fail_count,
        "warn_count": warn_count,
        "metrics": metrics,
        "findings": [finding_to_dict(finding) for finding in findings],
    }

    if args.write_report:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
