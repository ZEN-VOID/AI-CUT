#!/usr/bin/env python3
"""Validate F1 cue-to-audio/script dialogue alignment manifests."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

STRICT_SOURCE_RE = re.compile(r"(asr|whisper|word|manual|human|听看|逐字)", re.IGNORECASE)
FALLBACK_SOURCE_RE = re.compile(r"(silence|silent|fallback|ratio|length|speech_interval|停顿|比例)", re.IGNORECASE)
STRICT_EVIDENCE_RE = re.compile(r"(asr|word|whisper|manual|human|listening|听看|逐字)", re.IGNORECASE)
DEFAULT_MIN_MATCH_RATIO = 0.65
MATCH_RATIO_KEYS = (
    "match_ratio",
    "content_match_ratio",
    "asr_script_match_ratio",
    "transcript_match_ratio",
)
MANUAL_VERIFICATION_KEYS = (
    "manual_listening_verified",
    "human_qc_verified",
    "manual_qc_verified",
    "manual_spot_check_verified",
)


def parse_srt_count(path: Path) -> int:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return 0
    return len(re.split(r"\n\s*\n", text))


def span_values(value: object) -> tuple[float, float] | None:
    if isinstance(value, list) and len(value) == 2:
        return float(value[0]), float(value[1])
    if isinstance(value, dict) and "start" in value and "end" in value:
        return float(value["start"]), float(value["end"])
    return None


def truthy(value: object) -> bool:
    return value is True or (isinstance(value, str) and value.strip().lower() in {"true", "yes", "pass", "verified"})


def manually_verified(record: dict) -> bool:
    return any(truthy(record.get(name)) for name in MANUAL_VERIFICATION_KEYS)


def ratio_value(value: object) -> float | None:
    try:
        ratio = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    if 0 <= ratio <= 1:
        return ratio
    return None


def extract_match_ratio(record: dict) -> float | None:
    for key in MATCH_RATIO_KEYS:
        ratio = ratio_value(record.get(key))
        if ratio is not None:
            return ratio
    nested = record.get("match_report")
    if isinstance(nested, dict):
        for key in MATCH_RATIO_KEYS:
            ratio = ratio_value(nested.get(key))
            if ratio is not None:
                return ratio
    return None


def cue_has_strict_evidence(cue: dict, root_evidence: object) -> bool:
    source_method = str(cue.get("source_method", ""))
    evidence_fields = [
        cue.get("strict_sync_evidence"),
        cue.get("sync_evidence"),
        cue.get("alignment_evidence"),
        root_evidence,
    ]
    evidence_text = " ".join(str(value) for value in evidence_fields if value is not None)

    if manually_verified(cue):
        return True
    if any(cue.get(name) is not None for name in ("asr_word_span", "word_span", "asr_char_span", "asr_text_span", "asr_words")):
        return True
    if STRICT_EVIDENCE_RE.search(evidence_text):
        return True
    return STRICT_SOURCE_RE.search(source_method) is not None and FALLBACK_SOURCE_RE.search(source_method) is None


def validate(
    path: Path,
    srt_path: Path | None = None,
    strict: bool = False,
    min_match_ratio: float = DEFAULT_MIN_MATCH_RATIO,
) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    cues = data.get("cues")
    errors: list[str] = []
    previous_audio_end = -1.0
    root_evidence = data.get("strict_sync_evidence") or data.get("sync_evidence")
    root_match_ratio = extract_match_ratio(data) if isinstance(data, dict) else None
    root_manual_verified = manually_verified(data) if isinstance(data, dict) else False

    if not isinstance(cues, list) or not cues:
        return {"path": str(path), "ok": False, "errors": ["missing or empty cues"]}

    all_cues_manually_verified = all(isinstance(cue, dict) and manually_verified(cue) for cue in cues)
    if strict and root_match_ratio is not None and root_match_ratio < min_match_ratio and not (
        root_manual_verified or all_cues_manually_verified
    ):
        errors.append(
            f"global ASR/script match_ratio {root_match_ratio:.4f} < required {min_match_ratio:.4f}; "
            "manual listening verification required"
        )

    for expected, cue in enumerate(cues, 1):
        if not isinstance(cue, dict):
            errors.append(f"cue {expected}: not an object")
            continue
        cue_manual_verified = manually_verified(cue)
        cue_match_ratio = extract_match_ratio(cue)
        if cue.get("index") != expected:
            errors.append(f"cue {expected}: bad index {cue.get('index')!r}")
        if not str(cue.get("text", "")).strip():
            errors.append(f"cue {expected}: missing text")
        audio_span = span_values(cue.get("audio_span"))
        if audio_span is None:
            errors.append(f"cue {expected}: missing audio_span")
        else:
            start, end = audio_span
            if end <= start:
                errors.append(f"cue {expected}: non-positive audio_span")
            if start < previous_audio_end - 0.02:
                errors.append(f"cue {expected}: audio_span overlaps or moves backward")
            previous_audio_end = max(previous_audio_end, end)
        if cue.get("script_span") is None:
            errors.append(f"cue {expected}: missing script_span")
        if not str(cue.get("source_method", "")).strip():
            errors.append(f"cue {expected}: missing source_method")
        if strict:
            source_method = str(cue.get("source_method", ""))
            if FALLBACK_SOURCE_RE.search(source_method) and not (
                cue_manual_verified or root_manual_verified
            ):
                errors.append(
                    f"cue {expected}: fallback source_method {source_method!r} is not strict sync evidence"
                )
            if not cue_has_strict_evidence(cue, root_evidence):
                errors.append(
                    f"cue {expected}: missing strict sync evidence "
                    "(ASR word/char span or manual listening verification required)"
                )
            if cue_match_ratio is None and root_match_ratio is None and not (
                cue_manual_verified or root_manual_verified
            ):
                errors.append(
                    f"cue {expected}: missing ASR/script content match ratio "
                    "or manual listening verification"
                )
            if cue_match_ratio is not None and cue_match_ratio < min_match_ratio and not (
                cue_manual_verified or root_manual_verified
            ):
                errors.append(
                    f"cue {expected}: ASR/script match_ratio {cue_match_ratio:.4f} "
                    f"< required {min_match_ratio:.4f}; manual listening verification required"
                )
        if cue.get("verdict") != "pass":
            errors.append(f"cue {expected}: verdict is {cue.get('verdict')!r}")

    srt_count = None
    if srt_path is not None:
        srt_count = parse_srt_count(srt_path)
        if srt_count != len(cues):
            errors.append(f"srt cue count {srt_count} != alignment cue count {len(cues)}")

    return {
        "path": str(path),
        "srt_path": str(srt_path) if srt_path else None,
        "ok": not errors,
        "strict": strict,
        "min_match_ratio": min_match_ratio if strict else None,
        "cue_count": len(cues),
        "srt_cue_count": srt_count,
        "errors": errors,
    }


def main(argv: list[str]) -> int:
    strict = False
    args = argv[1:]
    if "--strict" in args:
        strict = True
        args.remove("--strict")
    min_match_ratio = DEFAULT_MIN_MATCH_RATIO
    for arg in list(args):
        if arg.startswith("--min-match-ratio="):
            min_match_ratio = float(arg.split("=", 1)[1])
            args.remove(arg)
    if "--min-match-ratio" in args:
        index = args.index("--min-match-ratio")
        try:
            min_match_ratio = float(args[index + 1])
        except (IndexError, ValueError):
            print("error: --min-match-ratio requires a numeric value", file=sys.stderr)
            return 2
        del args[index:index + 2]
    if len(args) not in (1, 2):
        print(
            "usage: validate_dialogue_alignment.py [--strict] [--min-match-ratio 0.65] "
            "<dialogue_alignment.json> [master.srt]",
            file=sys.stderr,
        )
        return 2
    report = validate(
        Path(args[0]),
        Path(args[1]) if len(args) == 2 else None,
        strict=strict,
        min_match_ratio=min_match_ratio,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
