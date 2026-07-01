#!/usr/bin/env python3
"""Update the project-wide material usage monitor CSV.

This helper is intentionally mechanical. It reads final usage evidence from
workflow ledgers or explicit file arguments, then maintains the simple CSV the
operator reviews:

素材名,文件路径,使用次数,使用程度

`使用程度` is restricted to `全片` or `部分切片`.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


HEADER = ["素材名", "文件路径", "使用次数", "使用程度"]
USAGE_DEGREES = {"全片", "部分切片"}

PATH_KEYS = (
    "source_file",
    "source_path",
    "file_path",
    "asset_path",
    "path",
    "video_path",
    "image_path",
    "audio_path",
    "script_path",
    "source_audio",
    "source_script",
)
NAME_KEYS = ("asset_name", "name", "素材名", "source_video_id", "image_id", "asset_id")
DEGREE_KEYS = ("usage_degree", "使用程度", "usage_extent", "extent", "scope", "usage_mode")
PARTIAL_HINT_KEYS = (
    "segment_id",
    "analysis_slice_id",
    "start",
    "end",
    "in",
    "out",
    "source_start",
    "source_end",
    "clip_start",
    "clip_end",
    "time_range",
    "duration_sec",
)
FULL_VALUES = {"全片", "full", "whole", "entire", "entire_file", "complete", "all", "full_asset"}
PARTIAL_VALUES = {"部分切片", "partial", "slice", "clip", "segment", "part", "trim", "cut", "range"}


class MonitorError(RuntimeError):
    pass


def normalize_token(value: Any) -> str:
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def normalize_path(value: Any, repo_root: Path) -> str:
    raw = str(value or "").strip()
    if not raw:
        return ""
    path = Path(raw).expanduser()
    if path.is_absolute():
        try:
            return path.resolve().relative_to(repo_root.resolve()).as_posix()
        except ValueError:
            return path.as_posix()
    return path.as_posix()


def material_name(path_value: str, record: dict[str, Any] | None = None) -> str:
    record = record or {}
    for key in NAME_KEYS:
        value = record.get(key)
        if value:
            return str(value).strip()
    return Path(path_value).name


def infer_usage_degree(record: dict[str, Any], default_usage_degree: str) -> str:
    for key in DEGREE_KEYS:
        value = record.get(key)
        token = normalize_token(value)
        if not token:
            continue
        if value in USAGE_DEGREES:
            return str(value)
        if token in FULL_VALUES:
            return "全片"
        if token in PARTIAL_VALUES:
            return "部分切片"

    for key in PARTIAL_HINT_KEYS:
        value = record.get(key)
        if value not in (None, "", [], {}):
            return "部分切片"

    return default_usage_degree


def usage_record_from_dict(record: dict[str, Any], repo_root: Path, default_usage_degree: str) -> tuple[str, str, str] | None:
    path_value = ""
    for key in PATH_KEYS:
        if record.get(key):
            path_value = normalize_path(record[key], repo_root)
            break
    if not path_value:
        return None
    degree = infer_usage_degree(record, default_usage_degree)
    if degree not in USAGE_DEGREES:
        raise MonitorError(f"invalid usage degree for {path_value}: {degree}")
    return (material_name(path_value, record), path_value, degree)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise MonitorError(f"invalid JSON: {path}: {exc}") from exc


def list_from_mapping(mapping: dict[str, Any], key: str) -> list[Any]:
    value = mapping.get(key)
    if isinstance(value, list):
        return value
    return []


def collect_usage_records(data: Any, repo_root: Path, default_usage_degree: str, include_planned: bool) -> list[tuple[str, str, str]]:
    records: list[dict[str, Any]] = []
    usage_keys = ["used_assets", "actual_usage", "actual_used_assets"]
    if include_planned:
        usage_keys.append("planned_usage")

    if isinstance(data, dict):
        for key in usage_keys:
            records.extend(item for item in list_from_mapping(data, key) if isinstance(item, dict))
        for output in list_from_mapping(data, "outputs"):
            if not isinstance(output, dict):
                continue
            for key in usage_keys:
                records.extend(item for item in list_from_mapping(output, key) if isinstance(item, dict))
    elif isinstance(data, list):
        records.extend(item for item in data if isinstance(item, dict))

    usage_rows: list[tuple[str, str, str]] = []
    for record in records:
        row = usage_record_from_dict(record, repo_root, default_usage_degree)
        if row:
            usage_rows.append(row)
    return usage_rows


def find_usage_json_sources(paths: list[Path]) -> list[Path]:
    sources: list[Path] = []
    for path in paths:
        if path.is_file():
            sources.append(path)
            continue
        if path.is_dir():
            direct = path / "asset_usage_ledger.json"
            if direct.exists():
                sources.append(direct)
            sources.extend(sorted(path.rglob("asset_usage_ledger.json")))
    return sorted(dict.fromkeys(sources))


def read_monitor(path: Path) -> Counter[tuple[str, str]]:
    counter: Counter[tuple[str, str]] = Counter()
    if not path.exists() or path.stat().st_size == 0:
        return counter

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != HEADER:
            raise MonitorError(f"CSV header must be exactly: {','.join(HEADER)}")
        for index, row in enumerate(reader, start=2):
            file_path = str(row.get("文件路径") or "").strip()
            degree = str(row.get("使用程度") or "").strip()
            count_text = str(row.get("使用次数") or "").strip()
            if not file_path:
                raise MonitorError(f"row {index}: 文件路径 is required")
            if degree not in USAGE_DEGREES:
                raise MonitorError(f"row {index}: 使用程度 must be 全片 or 部分切片")
            try:
                count = int(count_text)
            except ValueError as exc:
                raise MonitorError(f"row {index}: 使用次数 must be an integer") from exc
            if count < 0:
                raise MonitorError(f"row {index}: 使用次数 must not be negative")
            counter[(file_path, degree)] += count
    return counter


def write_monitor(path: Path, counter: Counter[tuple[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(HEADER)
        for file_path, degree in sorted(counter):
            writer.writerow([material_name(file_path), file_path, counter[(file_path, degree)], degree])


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Maintain projects/素材使用监控.csv from final workflow asset usage evidence."
    )
    parser.add_argument("sources", nargs="*", help="asset_usage_ledger.json files or directories containing them.")
    parser.add_argument(
        "--monitor",
        default="projects/素材使用监控.csv",
        help="Path to the global usage monitor CSV.",
    )
    parser.add_argument("--repo-root", default=".", help="Repository root for relative path normalization.")
    parser.add_argument("--asset", action="append", default=[], help="Explicit asset path to count once.")
    parser.add_argument(
        "--usage-degree",
        choices=sorted(USAGE_DEGREES),
        default="部分切片",
        help="Usage degree for explicit --asset entries and records without enough evidence.",
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Rebuild the monitor from the provided sources instead of adding to existing counts.",
    )
    parser.add_argument(
        "--include-planned",
        action="store_true",
        help="Also count planned_usage entries. Final close should normally omit this.",
    )
    parser.add_argument("--validate-only", action="store_true", help="Validate the existing monitor CSV without writing.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    monitor_path = Path(args.monitor)
    if not monitor_path.is_absolute():
        monitor_path = repo_root / monitor_path

    try:
        existing = read_monitor(monitor_path)
        if args.validate_only:
            print(json.dumps({"verdict": "pass", "monitor_path": str(monitor_path), "rows": len(existing)}, ensure_ascii=False))
            return 0

        source_paths: list[Path] = []
        for value in args.sources:
            source_path = Path(value)
            if not source_path.is_absolute():
                source_path = repo_root / source_path
            source_paths.append(source_path)

        new_rows: list[tuple[str, str, str]] = []
        for source in find_usage_json_sources(source_paths):
            new_rows.extend(collect_usage_records(load_json(source), repo_root, args.usage_degree, args.include_planned))

        for asset in args.asset:
            path_value = normalize_path(asset, repo_root)
            if not path_value:
                raise MonitorError("--asset cannot be empty")
            new_rows.append((material_name(path_value), path_value, args.usage_degree))

        counter: Counter[tuple[str, str]] = Counter() if args.rebuild else existing
        added = 0
        for _name, file_path, degree in new_rows:
            counter[(file_path, degree)] += 1
            added += 1

        write_monitor(monitor_path, counter)
        print(
            json.dumps(
                {
                    "verdict": "pass",
                    "monitor_path": str(monitor_path),
                    "mode": "rebuild" if args.rebuild else "merge",
                    "rows": len(counter),
                    "added_usage_count": added,
                },
                ensure_ascii=False,
            )
        )
        return 0
    except MonitorError as exc:
        print(json.dumps({"verdict": "fail", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
