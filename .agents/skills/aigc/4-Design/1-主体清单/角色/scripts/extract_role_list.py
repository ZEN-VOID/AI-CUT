#!/usr/bin/env python3
"""Extract canonical role-list artifacts from director episode JSON."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


ROLE_FIELD = "角色站位走位"
LEGACY_ROLE_FIELD = "角色及站位和穿搭"
SCENE_FIELD = "角色背景面"
LEGACY_SCENE_FIELD = "场景及方位"
GROUP_COSTUME_FIELD = "出场角色及穿搭"
DIRECTOR_SCHEMA = ".agents/skills/aigc/_shared/director_episode_output.schema.json"
DEFAULT_JSON_NAME = "角色清单.json"
DEFAULT_MANIFEST_NAME = "_manifest.json"
DIRECTOR_INPUT_ALIASES = ("3-Detail", "编导")


def to_repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()

NON_CHARACTER_ROLE_KEYWORDS = (
    "无出场角色",
    "无角色出场",
    "无角色",
    "无人出场",
    "空镜",
    "空镜头",
    "环境画面",
    "环境镜头",
    "纯场景",
    "仅场景",
    "仅道具",
    "道具特写",
    "字幕画面",
    "纯字幕",
)
ROLE_BOUNDARY_KEYWORDS: Sequence[str] = (
    "位于",
    "站在",
    "站",
    "立",
    "坐",
    "跪",
    "蹲",
    "靠",
    "贴",
    "持",
    "举",
    "握",
    "拎",
    "撑",
    "扶",
    "向",
    "盯",
    "望",
    "看",
    "面朝",
    "背对",
    "身着",
    "穿着",
    "穿",
    "披",
    "戴",
    "别着",
    "系着",
    "前景",
    "后景",
    "左侧",
    "右侧",
    "中央",
    "居中",
)
COSTUME_HINT_TERMS: Sequence[str] = (
    "衣",
    "袍",
    "裙",
    "衫",
    "襦",
    "褙子",
    "斗篷",
    "披风",
    "甲",
    "冠",
    "簪",
    "佩",
    "靴",
    "鞋",
    "袖",
    "腰封",
    "护腕",
    "身着",
    "穿着",
    "一身",
    "换上",
    "披着",
    "戴着",
)
STATE_KEYWORDS: Sequence[Tuple[str, Tuple[str, ...]]] = (
    ("战损", ("战损", "染血", "沾血", "血迹", "破损", "撕裂", "残破")),
    ("夜行", ("夜行", "潜行", "夜色伪装", "暗行")),
    ("仪式", ("礼服", "仪式", "祭服", "朝服", "婚服", "冕服")),
    ("伪装", ("乔装", "伪装", "易容", "换装")),
    ("甲胄", ("甲", "铠", "战甲", "甲胄")),
)
CROWD_ROLE_KEYWORDS = (
    "侍卫",
    "仆从",
    "士兵",
    "兵卒",
    "百姓",
    "宫女",
    "太监",
    "官兵",
    "众人",
    "路人",
    "随从",
    "人群",
    "宾客",
    "群演",
)
RELATIONSHIP_ROLE_TOKENS = (
    "爸爸",
    "妈妈",
    "父亲",
    "母亲",
    "爷爷",
    "奶奶",
    "叔叔",
    "伯伯",
    "哥哥",
    "姐姐",
    "弟弟",
    "妹妹",
)
NON_ROLE_OBJECT_HINTS = (
    "石碑",
    "门把",
    "灯管",
    "房门",
    "窗纸",
    "画面",
    "前景",
    "后景",
    "走廊",
    "长廊",
    "墙边",
    "火光",
    "雨丝",
)
NON_ROLE_ACTION_HINTS = (
    "压近",
    "后退",
    "前倾",
    "回身",
    "骤然",
    "停住",
    "推门",
    "入画",
)
ROLE_TOKEN_RE = re.compile(r"^[\u4e00-\u9fffA-Za-z0-9·・_\-]{1,16}$")
EPISODE_STEM_RE = re.compile(r"第0*(?P<ep>\d+)集")
CROWD_PHRASE_RE = re.compile(r"[\u4e00-\u9fffA-Za-z0-9]{1,12}(?:群像|众人|路人|随从)")


@dataclass
class ShotRoleRecord:
    episode_label: str
    group_id: str
    shot_id: str
    role_text: str
    shot_scene: str
    role_names: List[str]
    costume_mentions: Dict[str, List[str]]
    source_file: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从导演 episode JSON 提取角色清单")
    parser.add_argument("--input", help="输入文件或目录")
    parser.add_argument("--project", help="项目名；配合 --episode 自动推断输入")
    parser.add_argument("--episode", help="集标识，例如 第1集")
    parser.add_argument("--output-dir", help="显式输出目录")
    parser.add_argument("--json-name", default=DEFAULT_JSON_NAME, help="主清单文件名")
    parser.add_argument("--manifest-name", default=DEFAULT_MANIFEST_NAME, help="manifest 文件名")
    parser.add_argument("--dry-run", action="store_true", help="仅打印统计，不落盘")
    return parser.parse_args()


def normalize_episode_label(raw: str) -> str:
    text = str(raw or "").strip()
    match = EPISODE_STEM_RE.search(text)
    if match:
        return f"第{int(match.group('ep'))}集"
    if text.isdigit():
        return f"第{int(text)}集"
    return text or "第1集"


def resolve_input_path(input_arg: Optional[str], project: Optional[str], episode: Optional[str]) -> Path:
    if input_arg:
        raw = Path(input_arg)
        if raw.exists():
            return raw
        if project is None and "projects" in raw.parts and len(raw.parts) >= 3:
            try:
                project = raw.parts[raw.parts.index("projects") + 1]
            except (ValueError, IndexError):
                project = None
        episode = episode or raw.stem

    if project and episode:
        episode_label = normalize_episode_label(episode)
        project_root = Path("projects") / "aigc" / project
        for stage_name in DIRECTOR_INPUT_ALIASES:
            candidate = project_root / stage_name / f"{episode_label}.json"
            if candidate.exists():
                return candidate

    raise FileNotFoundError("未找到输入文件；请提供 --input，或使用 --project + --episode。")


def collect_input_files(input_path: Path) -> List[Path]:
    if input_path.is_file():
        return [input_path]
    files = sorted(input_path.glob("第*集.json"))
    if not files:
        raise FileNotFoundError(f"目录下未找到 `第*集.json`: {input_path}")
    return files


def infer_project_name(path: Path) -> str:
    parts = path.resolve().parts
    if "projects" in parts:
        idx = parts.index("projects")
        if idx + 2 < len(parts) and parts[idx + 1] == "aigc":
            return parts[idx + 2]
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return "unknown-project"


def infer_output_dir(input_file: Path, explicit_output_dir: Optional[str], episode_label: str) -> Path:
    if explicit_output_dir:
        return Path(explicit_output_dir)
    parts = input_file.resolve().parts
    if "projects" in parts:
        idx = parts.index("projects")
        if idx + 2 < len(parts) and parts[idx + 1] == "aigc":
            project_root = Path(*parts[: idx + 3])
        elif idx + 1 < len(parts):
            project_root = Path(*parts[: idx + 2])
        else:
            project_root = input_file.parent
        return project_root / "4-Design" / "角色" / "1-清单" / episode_label
    return input_file.parent / "4-Design" / "角色" / "1-清单" / episode_label


def load_episode_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    try:
        data["final_output"]["main_content"]["分镜组列表"]
    except KeyError as exc:
        raise KeyError(f"{path} 缺少 shared director schema 主结构: {exc}") from exc
    return data


def normalize_role_token(token: str) -> str:
    text = token.strip().strip("，,；;。.!！?？:：")
    text = re.sub(r"^[\-•·\s]+", "", text)
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"^(?:前景|后景|左侧|右侧|中央|居中|远端|近端|门口|门边)", "", text)
    text = re.sub(r"(?:位于|站在|站|立|坐|跪|蹲|靠|贴|持|举|握|拎|撑|扶|盯|望|看|面朝|背对|身着|穿着|穿|披|戴|别着|系着).*$", "", text)
    text = re.sub(r"(?:左手|右手|双手|单手|双臂|手臂)$", "", text)
    text = text.rstrip("的之其")
    return text


def is_placeholder_role_token(token: str) -> bool:
    normalized = token.strip()
    return not normalized or any(keyword in normalized for keyword in NON_CHARACTER_ROLE_KEYWORDS)


def split_roles(role_text: str) -> List[str]:
    if not role_text.strip():
        return ["unknown"]
    normalized = role_text
    normalized = re.sub(r"\s*与\s*", "、", normalized)
    normalized = re.sub(r"\s*及\s*", "、", normalized)
    normalized = normalized.replace("；", "、").replace(";", "、")
    normalized = normalized.replace("，", "、").replace(",", "、")
    normalized = normalized.replace("/", "、").replace("|", "、").replace("｜", "、")
    parts = [normalize_role_token(item) for item in normalized.split("、")]
    result: List[str] = []
    for part in parts:
        if not part or is_placeholder_role_token(part):
            continue
        if part not in result:
            result.append(part)
    return result or ["unknown"]


def split_text_clauses(text: str) -> List[str]:
    return [item.strip() for item in re.split(r"[，,；;。！？!?]+", text) if item.strip()]


def is_valid_role_candidate(token: str) -> bool:
    normalized = normalize_role_token(token)
    if not normalized or is_placeholder_role_token(normalized):
        return False
    if any(hint in normalized for hint in NON_ROLE_OBJECT_HINTS):
        return False
    if any(hint in normalized for hint in NON_ROLE_ACTION_HINTS):
        return False
    if normalized.startswith(("被", "将", "把", "从", "向", "朝")):
        return False
    if normalized in {"共同", "画面"}:
        return False
    return bool(ROLE_TOKEN_RE.match(normalized)) or normalized in RELATIONSHIP_ROLE_TOKENS


def extract_role_chunk_from_clause(clause: str) -> str:
    text = clause.strip()
    cut_points = [text.find(keyword) for keyword in ROLE_BOUNDARY_KEYWORDS if text.find(keyword) > 0]
    if not cut_points:
        return text
    return text[: min(cut_points)].strip("：:，,；;。.!！?？ ")


def unique_preserve(values: Sequence[str]) -> List[str]:
    result: List[str] = []
    for value in values:
        text = str(value).strip()
        if text and text not in result:
            result.append(text)
    return result


def infer_costume_state(costume_texts: Sequence[str]) -> Tuple[str, List[str]]:
    state_hits: Counter[str] = Counter()
    tagged_rules: List[str] = []

    for raw_text in costume_texts:
        text = str(raw_text or "").strip()
        if not text:
            continue
        matched_state = "baseline"
        for state_name, keywords in STATE_KEYWORDS:
            if any(keyword in text for keyword in keywords):
                matched_state = state_name
                break
        state_hits[matched_state] += 1
        if matched_state != "baseline":
            tagged_rules.append(f"{matched_state}: {text}")

    if not state_hits:
        return "baseline", []

    primary_state = state_hits.most_common(1)[0][0]
    variation_rules = [
        rule
        for rule in unique_preserve(tagged_rules)
        if not rule.startswith(f"{primary_state}:")
    ]
    return primary_state, variation_rules


def pick_first_text(container: object, *fields: str) -> str:
    if not isinstance(container, dict):
        return ""
    for field in fields:
        value = container.get(field)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def extract_role_mentions_from_text(text: str) -> Tuple[List[str], Dict[str, List[str]]]:
    roles: List[str] = []
    costume_map: Dict[str, List[str]] = {}
    last_named_roles: List[str] = []
    costume_lead_markers = ("穿", "身着", "穿着", "披", "披着", "戴", "戴着", "一身", "换上")

    for clause in split_text_clauses(text):
        pair_match = re.match(
            r"^(?P<role>[\u4e00-\u9fffA-Za-z0-9·・_\\-]{1,16})\s*[-—:：]\s*(?P<costume>.+)$",
            clause,
        )
        if pair_match:
            role_name = normalize_role_token(pair_match.group("role"))
            if is_valid_role_candidate(role_name):
                last_named_roles = [role_name]
                roles.append(role_name)
                costume_map.setdefault(role_name, [])
                costume_map[role_name].append(clause)
                continue

        if clause.startswith(costume_lead_markers):
            current_roles = []
        else:
            role_chunk = extract_role_chunk_from_clause(clause)
            current_roles = [
                token
                for token in split_roles(role_chunk)
                if token != "unknown" and is_valid_role_candidate(token)
            ]

        if current_roles:
            last_named_roles = current_roles
            roles.extend(current_roles)

        target_roles = current_roles or (last_named_roles if len(last_named_roles) == 1 else [])
        if target_roles and any(term in clause for term in COSTUME_HINT_TERMS):
            for role_name in target_roles:
                costume_map.setdefault(role_name, [])
                costume_map[role_name].append(clause)

    relation_hits = [token for token in RELATIONSHIP_ROLE_TOKENS if token in text]
    normalized_roles = unique_preserve(roles + relation_hits)
    if not normalized_roles:
        fallback = [token for token in split_roles(text) if token != "unknown" and is_valid_role_candidate(token)]
        normalized_roles = unique_preserve(fallback)
    if not normalized_roles:
        normalized_roles = ["unknown"]
    return normalized_roles, {key: unique_preserve(value) for key, value in costume_map.items()}


def extract_group_role_costume_pairs(text: str) -> Tuple[List[str], Dict[str, List[str]]]:
    roles: List[str] = []
    costume_map: Dict[str, List[str]] = {}
    for clause in re.split(r"[；;]+", str(text or "").strip()):
        item = clause.strip()
        if not item:
            continue
        pair_match = re.match(
            r"^(?P<role>[\u4e00-\u9fffA-Za-z0-9·・_\-]{1,16})\s*[-—:：]\s*(?P<costume>.+)$",
            item,
        )
        if not pair_match:
            continue
        role_name = normalize_role_token(pair_match.group("role"))
        if not is_valid_role_candidate(role_name):
            continue
        roles.append(role_name)
        costume_map.setdefault(role_name, [])
        costume_map[role_name].append(item)
    normalized_roles = unique_preserve(roles)
    return normalized_roles or ["unknown"], {key: unique_preserve(value) for key, value in costume_map.items()}


def build_role_aliases(role_name: str) -> List[str]:
    aliases = [role_name]
    for suffix in ("全息投影", "群像"):
        if role_name.endswith(suffix):
            aliases.append(role_name[: -len(suffix)])
    return [alias for alias in unique_preserve(aliases) if alias]


def detect_roles_from_roster(role_text: str, roster_names: Sequence[str]) -> List[str]:
    text = str(role_text or "").strip()
    if not text:
        return ["unknown"]

    detected = [
        role_name
        for role_name in roster_names
        if role_name != "unknown" and any(alias in text for alias in build_role_aliases(role_name))
    ]
    if detected:
        return unique_preserve(detected)

    crowd_hits = [
        match.group(0)
        for match in CROWD_PHRASE_RE.finditer(text)
        if any(keyword in match.group(0) for keyword in CROWD_ROLE_KEYWORDS)
    ]
    if crowd_hits:
        return unique_preserve(crowd_hits)

    fallback = [
        token
        for token in split_roles(text)
        if token != "unknown" and is_valid_role_candidate(token) and len(token) <= 6
    ]
    return unique_preserve(fallback) or ["unknown"]


def infer_role_level(role_name: str, group_count: int, total_groups: int) -> str:
    if any(keyword in role_name for keyword in CROWD_ROLE_KEYWORDS):
        return "群像角色"
    if total_groups <= 0:
        return "功能角色"
    ratio = group_count / total_groups
    if group_count >= 6 or ratio >= 0.45:
        return "核心角色"
    if group_count >= 3 or ratio >= 0.2:
        return "重要角色"
    return "功能角色"


def extract_records_from_episode(input_file: Path) -> Tuple[str, List[ShotRoleRecord]]:
    data = load_episode_json(input_file)
    episode_label = normalize_episode_label(
        data.get("metadata", {}).get("episode_id") or input_file.stem
    )
    groups = data["final_output"]["main_content"]["分镜组列表"]
    records: List[ShotRoleRecord] = []

    for group in groups:
        group_id = str(group.get("分镜组ID") or "").strip()
        if not group_id:
            continue
        group_design = group.get("组间设计") if isinstance(group.get("组间设计"), dict) else {}
        group_costume_text = pick_first_text(group_design, GROUP_COSTUME_FIELD)
        group_role_names, group_costume_mentions = extract_group_role_costume_pairs(group_costume_text)
        shots = group.get("分镜明细") or []
        for index, shot in enumerate(shots, start=1):
            if not isinstance(shot, dict):
                continue
            shot_id = str(shot.get("分镜ID") or "").strip() or f"{group_id}-{index}"
            role_text = pick_first_text(shot, ROLE_FIELD, LEGACY_ROLE_FIELD)
            shot_scene = pick_first_text(shot, SCENE_FIELD, LEGACY_SCENE_FIELD)
            role_names = detect_roles_from_roster(role_text, group_role_names) if role_text else group_role_names
            costume_mentions: Dict[str, List[str]] = {}
            for role_name in role_names:
                for clause in group_costume_mentions.get(role_name, []):
                    costume_mentions.setdefault(role_name, [])
                    if clause not in costume_mentions[role_name]:
                        costume_mentions[role_name].append(clause)
            records.append(
                ShotRoleRecord(
                    episode_label=episode_label,
                    group_id=group_id,
                    shot_id=shot_id,
                    role_text=role_text,
                    shot_scene=shot_scene,
                    role_names=role_names,
                    costume_mentions=costume_mentions,
                    source_file=input_file.as_posix(),
                )
            )
    if not records:
        raise RuntimeError(f"{input_file} 未识别到任何合法分镜明细。")
    return episode_label, records


def build_roles(records: List[ShotRoleRecord]) -> List[dict]:
    role_map: Dict[str, dict] = {}
    total_groups = len({record.group_id for record in records})

    for record in records:
        for role_name in record.role_names:
            if role_name == "unknown":
                continue
            if role_name not in role_map:
                role_map[role_name] = {
                    "role_id": "",
                    "name": role_name,
                    "role_level": "功能角色",
                    "group_ids": [],
                    "shot_ids": [],
                    "shot_count": 0,
                    "first_appearance": {
                        "episode": record.episode_label,
                        "group_id": record.group_id,
                        "shot_id": record.shot_id,
                        "source_file": record.source_file,
                    },
                    "costume_mentions": [],
                    "evidence": [],
                }

            item = role_map[role_name]
            item["shot_count"] += 1
            if record.group_id not in item["group_ids"]:
                item["group_ids"].append(record.group_id)
            if record.shot_id not in item["shot_ids"]:
                item["shot_ids"].append(record.shot_id)
            for costume_text in record.costume_mentions.get(role_name, []):
                if costume_text not in item["costume_mentions"]:
                    item["costume_mentions"].append(costume_text)
            item["evidence"].append(
                {
                    "group_id": record.group_id,
                    "shot_id": record.shot_id,
                    "role_text": record.role_text,
                    "shot_scene": record.shot_scene,
                    "source_file": record.source_file,
                }
            )

    roles = list(role_map.values())
    roles.sort(key=lambda item: (-item["shot_count"], item["name"]))
    for index, item in enumerate(roles, start=1):
        item["role_id"] = f"ROLE-{index:03d}"
        item["role_level"] = infer_role_level(item["name"], len(item["group_ids"]), total_groups)
        costume_counter = Counter(item["costume_mentions"])
        costume_state, variation_rules = infer_costume_state(item["costume_mentions"])
        item["costume_profile"] = {
            "primary_costumes": [text for text, _ in costume_counter.most_common(2)] or ["unknown"],
            "variant_costumes": [text for text, _ in costume_counter.most_common()[2:8]],
        }
        item["costume_state"] = costume_state
        item["variation_rules"] = variation_rules
        first = item["first_appearance"]
        item["display_card"] = {
            "title": item["name"],
            "subtitle": f"{item['role_level']} · {item['shot_count']} 镜 / {len(item['group_ids'])} 组",
            "first_appearance_label": f"{first['episode']} / {first['group_id']} / {first['shot_id']}",
        }
    return roles


def build_payload(
    project_name: str,
    episode_label: str,
    input_file: Path,
    records: List[ShotRoleRecord],
    roles: List[dict],
    generated_at: str,
) -> dict:
    unknown_count = sum(1 for record in records if record.role_names == ["unknown"])
    return {
        "meta": {
            "schema_version": "aigc/design-role-list/v1",
            "skill_id": "aigc-design-role-list",
            "project_name": project_name,
            "episode_id": episode_label,
            "primary_input": input_file.as_posix(),
            "source_inputs": [input_file.as_posix()],
            "source_schema": DIRECTOR_SCHEMA,
            "source_file": input_file.as_posix(),
            "generated_at": generated_at,
        },
        "statistics": {
            "group_count": len({record.group_id for record in records}),
            "shot_count": len(records),
            "role_count": len(roles),
            "unknown_shot_count": unknown_count,
        },
        "presentation": {
            "default_view": "role_cards",
            "summary": f"共收敛 {len(roles)} 位角色，覆盖 {len(records)} 个分镜。",
        },
        "group_role_map": [
            {
                "group_id": record.group_id,
                "shot_id": record.shot_id,
                "shot_scene": record.shot_scene,
                "role_text": record.role_text,
                "roles": record.role_names,
                "costume_mentions": record.costume_mentions,
                "source_file": record.source_file,
            }
            for record in records
        ],
        "roles": roles,
    }


def build_manifest(
    episode_label: str,
    input_file: Path,
    output_dir: Path,
    json_name: str,
    manifest_name: str,
    payload: dict,
    notes: Optional[List[str]] = None,
) -> dict:
    return {
        "status": "ok",
        "episode_id": episode_label,
        "input_file": to_repo_relative(input_file),
        "output_dir": to_repo_relative(output_dir),
        "output_files": [
            to_repo_relative(output_dir / json_name),
            to_repo_relative(output_dir / manifest_name),
        ],
        "statistics": payload["statistics"],
        "notes": notes or [
            "canonical business truth 是 `角色清单.json`；`_manifest.json` 只承担审计与统计侧车职责。",
        ],
    }


def write_outputs(output_dir: Path, json_name: str, manifest_name: str, payload: dict, manifest: dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / json_name).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / manifest_name).write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    args = parse_args()
    input_path = resolve_input_path(args.input, args.project, args.episode)
    input_files = collect_input_files(input_path)

    for input_file in input_files:
        episode_label, records = extract_records_from_episode(input_file)
        project_name = infer_project_name(input_file)
        roles = build_roles(records)
        if not roles:
            raise RuntimeError(f"{input_file} 未提取到有效角色。")

        generated_at = datetime.now().astimezone().isoformat(timespec="seconds")
        output_dir = infer_output_dir(input_file, args.output_dir, episode_label)
        payload = build_payload(project_name, episode_label, input_file, records, roles, generated_at)
        manifest = build_manifest(
            episode_label,
            input_file,
            output_dir,
            args.json_name,
            args.manifest_name,
            payload,
        )

        if args.dry_run:
            print(f"[DRY-RUN] {episode_label}")
            print(f"- 输入: {input_file}")
            print(f"- 分镜组: {payload['statistics']['group_count']}")
            print(f"- 分镜数: {payload['statistics']['shot_count']}")
            print(f"- 角色数: {payload['statistics']['role_count']}")
            print(f"- unknown 分镜数: {payload['statistics']['unknown_shot_count']}")
            continue

        write_outputs(output_dir, args.json_name, args.manifest_name, payload, manifest)
        print(f"输出目录: {output_dir}")
        print(f"- {args.json_name}")
        print(f"- {args.manifest_name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
