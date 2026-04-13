#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build an episode-level scene catalog from a director episode JSON."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


EPISODE_FILE_RE = re.compile(r"^第0*(?P<ep>\d+)集\.json$")
EPISODE_IN_STEM_RE = re.compile(r"第0*(?P<ep>\d+)集")
TRIM_PUNCTUATION = " \t\r\n，,。；;、"
SCENE_SPLIT_MARKERS = (
    "左后侧",
    "右后侧",
    "左前侧",
    "右前侧",
    "西端",
    "东端",
    "南端",
    "北端",
    "东侧",
    "西侧",
    "南侧",
    "北侧",
    "左侧",
    "右侧",
    "门内",
    "门外",
    "门口",
    "窗边",
    "柜台",
    "近景",
    "远景",
    "内侧",
    "外侧",
    "前方",
    "后方",
    "高处",
    "低处",
    "入口",
    "出口",
)
SCENE_NOISE_ONLY = {
    "镜头",
    "画面",
    "前景",
    "中景",
    "后景",
}


@dataclass
class VariantAggregate:
    label: str
    first_order: int
    raw_examples: List[str] = field(default_factory=list)
    group_ids: List[str] = field(default_factory=list)
    shot_ids: List[str] = field(default_factory=list)

    def add(self, raw_scene: str, group_id: str, shot_id: str) -> None:
        if raw_scene not in self.raw_examples:
            self.raw_examples.append(raw_scene)
        if group_id not in self.group_ids:
            self.group_ids.append(group_id)
        if shot_id not in self.shot_ids:
            self.shot_ids.append(shot_id)


@dataclass
class SceneAggregate:
    scene_name: str
    scene_key: str
    first_order: int
    first_group_id: str
    first_shot_id: str
    group_ids: List[str] = field(default_factory=list)
    shot_ids: List[str] = field(default_factory=list)
    variants: Dict[str, VariantAggregate] = field(default_factory=dict)

    def add(self, group_id: str, shot_id: str, variant_label: str, raw_scene: str, order: int) -> None:
        if group_id not in self.group_ids:
            self.group_ids.append(group_id)
        if shot_id not in self.shot_ids:
            self.shot_ids.append(shot_id)
        variant_key = canonical_key(variant_label or self.scene_name)
        variant = self.variants.get(variant_key)
        if variant is None:
            variant = VariantAggregate(label=variant_label or self.scene_name, first_order=order)
            self.variants[variant_key] = variant
        variant.add(raw_scene=raw_scene, group_id=group_id, shot_id=shot_id)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从导演 episode JSON 提取场景清单")
    parser.add_argument(
        "--input",
        required=True,
        help="输入 episode JSON，例如 projects/<项目名>/3-Detail/第N集.json",
    )
    parser.add_argument(
        "--output-dir",
        help="输出目录；默认自动推断到 projects/<项目名>/4-Design/场景/1-清单/第N集/",
    )
    parser.add_argument(
        "--emit-manifest",
        action="store_true",
        help="附带输出 _manifest.json",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def find_project_root(input_path: Path) -> Optional[Path]:
    resolved = input_path.resolve()
    parts = resolved.parts
    if "projects" not in parts:
        return None
    index = parts.index("projects")
    if index + 1 >= len(parts):
        return None
    return Path(*parts[: index + 2])


def extract_episode_id(input_path: Path, payload: dict) -> str:
    metadata = payload.get("metadata", {})
    episode_id = metadata.get("episode_id")
    if isinstance(episode_id, str) and episode_id.strip():
        return episode_id.strip()

    match = EPISODE_FILE_RE.match(input_path.name)
    if match:
        return f"第{int(match.group('ep'))}集"

    stem_match = EPISODE_IN_STEM_RE.search(input_path.stem)
    if stem_match:
        return f"第{int(stem_match.group('ep'))}集"

    return input_path.stem


def infer_output_dir(input_path: Path, episode_id: str, explicit_output_dir: Optional[str]) -> Path:
    if explicit_output_dir:
        return Path(explicit_output_dir)

    project_root = find_project_root(input_path)
    if project_root is not None:
        return project_root / "4-Design" / "1-场景" / "1-清单" / episode_id

    return input_path.parent / "1-清单" / episode_id


def require_groups(payload: dict) -> List[dict]:
    try:
        groups = payload["final_output"]["main_content"]["分镜组列表"]
    except KeyError as exc:
        raise ValueError("输入缺少 `final_output.main_content.分镜组列表`，不符合最小 shared schema 壳。") from exc
    if not isinstance(groups, list):
        raise ValueError("`分镜组列表` 必须是数组。")
    return groups


def clean_scene_text(value: object) -> str:
    if not isinstance(value, str):
        return ""
    text = re.sub(r"\s+", " ", value).strip(TRIM_PUNCTUATION)
    return text


def resolve_scene_text(shot: object) -> str:
    if not isinstance(shot, dict):
        return ""
    for field in ("角色背景面", "场景及方位"):
        raw = clean_scene_text(shot.get(field, ""))
        if raw:
            return raw
    return ""


def canonical_key(value: str) -> str:
    normalized = re.sub(r"\s+", "", value).strip(TRIM_PUNCTUATION)
    normalized = re.sub(r"[^\w\u4e00-\u9fff]+", "", normalized.lower())
    return normalized or "unknown"


def normalize_primary(text: str) -> str:
    primary = text.strip(TRIM_PUNCTUATION)
    primary = re.sub(r"^(?:从|自)(?=[\u4e00-\u9fffA-Za-z0-9])", "", primary)
    primary = primary.strip(TRIM_PUNCTUATION)
    return primary or "unknown"


def split_scene(raw_scene: str) -> tuple[str, str]:
    text = clean_scene_text(raw_scene)
    if not text:
        return ("unknown", "")

    if text in SCENE_NOISE_ONLY:
        return ("unknown", "")

    head = re.split(r"[，,。；;、]", text, maxsplit=1)[0].strip(TRIM_PUNCTUATION)
    split_index: Optional[int] = None
    for marker in SCENE_SPLIT_MARKERS:
        position = head.find(marker)
        if position <= 0:
            continue
        if split_index is None or position < split_index:
            split_index = position

    if split_index is None:
        primary = normalize_primary(head or text)
        return (primary, "")

    raw_primary = head[:split_index].strip(TRIM_PUNCTUATION)
    primary = normalize_primary(raw_primary)
    variant = text[len(raw_primary):].strip(TRIM_PUNCTUATION)
    if not primary or primary == "unknown":
        return (clean_scene_text(text), "")
    return (primary, variant)


def build_scene_catalog(payload: dict, input_path: Path) -> dict:
    groups = require_groups(payload)
    episode_id = extract_episode_id(input_path=input_path, payload=payload)
    scene_map: Dict[str, SceneAggregate] = {}
    group_scene_map: List[dict] = []
    order = 0
    shot_count = 0

    for group in groups:
        group_id = str(group.get("分镜组ID", "")).strip() or "unknown-group"
        shots = group.get("分镜明细", [])
        if not isinstance(shots, list):
            continue

        for shot in shots:
            shot_count += 1
            order += 1
            shot_id = str(shot.get("分镜ID", "")).strip() or f"{group_id}-unknown-shot-{shot_count}"
            raw_scene = resolve_scene_text(shot)
            scene_name, scene_variant = split_scene(raw_scene)
            scene_key = canonical_key(scene_name)
            scene_record = scene_map.get(scene_key)
            if scene_record is None:
                scene_record = SceneAggregate(
                    scene_name=scene_name,
                    scene_key=scene_key,
                    first_order=order,
                    first_group_id=group_id,
                    first_shot_id=shot_id,
                )
                scene_map[scene_key] = scene_record
            scene_record.add(
                group_id=group_id,
                shot_id=shot_id,
                variant_label=scene_variant or scene_name,
                raw_scene=raw_scene or "unknown",
                order=order,
            )

            time_range = shot.get("时间段", {})
            if not isinstance(time_range, dict):
                time_range = {}

            group_scene_map.append(
                {
                    "order": order,
                    "group_id": group_id,
                    "shot_id": shot_id,
                    "scene_raw": raw_scene or "unknown",
                    "scene_name": scene_name,
                    "scene_variant": scene_variant,
                    "scene_key": scene_key,
                    "time_range": {
                        "start_sec": time_range.get("开始秒"),
                        "end_sec": time_range.get("结束秒"),
                    },
                }
            )

    sorted_scenes = sorted(scene_map.values(), key=lambda item: item.first_order)
    scene_rows: List[dict] = []
    variant_count = 0
    for index, scene in enumerate(sorted_scenes, start=1):
        scene_id = f"SCENE-{index:03d}"
        variants = sorted(scene.variants.values(), key=lambda item: item.first_order)
        variant_rows = []
        for variant_index, variant in enumerate(variants, start=1):
            variant_count += 1
            variant_rows.append(
                {
                    "variant_id": f"{scene_id}-V{variant_index:02d}",
                    "variant_label": variant.label,
                    "raw_examples": variant.raw_examples,
                    "group_ids": variant.group_ids,
                    "shot_ids": variant.shot_ids,
                }
            )

        scene_rows.append(
            {
                "scene_id": scene_id,
                "scene_name": scene.scene_name,
                "scene_key": scene.scene_key,
                "first_appearance": {
                    "group_id": scene.first_group_id,
                    "shot_id": scene.first_shot_id,
                },
                "coverage": {
                    "group_ids": scene.group_ids,
                    "shot_ids": scene.shot_ids,
                    "group_count": len(scene.group_ids),
                    "shot_count": len(scene.shot_ids),
                },
                "variants": variant_rows,
                "display_profile": {
                    "title": scene.scene_name,
                    "subtitle": f"{len(variant_rows)} 个变体 / {len(scene.shot_ids)} 个镜头",
                    "tags": ["scene-catalog", "4-Design", "from-3-Detail"],
                },
            }
        )

    return {
        "metadata": {
            "schema_version": "aigc/design-scene-catalog/v1",
            "skill_id": "aigc-design-scene-list",
            "source_episode_file": input_path.as_posix(),
            "source_schema": ".agents/skills/aigc/_shared/director_episode_output.schema.json",
            "source_route": "3-Detail -> 4-Design/场景/1-清单",
            "episode_id": episode_id,
            "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        },
        "summary": {
            "group_count": len(groups),
            "shot_count": shot_count,
            "scene_count": len(scene_rows),
            "variant_count": variant_count,
        },
        "scenes": scene_rows,
        "group_scene_map": group_scene_map,
        "acceptance_notes": [
            "scene_name 只来自上游 `角色背景面` 的保守抽取；旧 `场景及方位` 仅作兼容读取。",
            "group_scene_map 必须保持对 group_id / shot_id 的直接回链。",
            "当前产物只服务 4-Design 场景链，不承载研究稿或 bridge 字段。",
        ],
    }


def build_manifest(catalog: dict, output_file: Path) -> dict:
    scenes = catalog["scenes"]
    return {
        "episode_id": catalog["metadata"]["episode_id"],
        "source_file": catalog["metadata"]["source_episode_file"],
        "output_file": output_file.as_posix(),
        "output_mode": "full_trace",
        "scene_count": catalog["summary"]["scene_count"],
        "group_scene_count": len(catalog["group_scene_map"]),
        "scenes": [
            {
                "scene_id": item["scene_id"],
                "scene_name": item["scene_name"],
                "variant_count": len(item["variants"]),
                "shot_count": item["coverage"]["shot_count"],
            }
            for item in scenes
        ],
    }


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"输入不存在：{input_path.as_posix()}")

    payload = load_json(input_path)
    episode_id = extract_episode_id(input_path=input_path, payload=payload)
    output_dir = infer_output_dir(
        input_path=input_path,
        episode_id=episode_id,
        explicit_output_dir=args.output_dir,
    )
    catalog = build_scene_catalog(payload=payload, input_path=input_path)
    output_file = output_dir / f"{episode_id}.json"
    write_json(output_file, catalog)

    if args.emit_manifest:
        manifest_file = output_dir / "_manifest.json"
        write_json(manifest_file, build_manifest(catalog=catalog, output_file=output_file))

    print(output_file.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
