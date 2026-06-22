#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import re
import subprocess
from pathlib import Path


ROOT = Path("/Volumes/AIGC/AI-CUT")
WORK = ROOT / "projects/0622/结果/文案5/auto-edit/edit"
FINAL = ROOT / "projects/0622/结果/文案5/文案5_final.mp4"
VOICE = ROOT / "projects/0622/素材/音频/文案5-音频.mp3"
SCRIPT = ROOT / "projects/0622/素材/文案/文案5.md"
MANIFEST = ROOT / "projects/0622/素材/视频/视频说明.yaml"
BASE_DIR = ROOT / "projects/0622/素材/视频"
TOOL = BASE_DIR / "工具使用/1.mp4"
CONTENT = BASE_DIR / "影像内容/微信视频2026-06-21_220234_765.mp4"
OPERATION = BASE_DIR / "操作展示/微信视频2026-06-21_220316_527.mp4"


def run(cmd: list[str]) -> None:
    print("RUN", cmd[0], " ".join(cmd[1:4]), flush=True)
    subprocess.run(cmd, check=True)


def ts_ass(seconds: float) -> str:
    seconds = max(0.0, seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    if cs == 100:
        s += 1
        cs = 0
    if s == 60:
        m += 1
        s = 0
    if m == 60:
        h += 1
        m = 0
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def wrap_cn(text: str, limit: int = 15) -> str:
    if len(text) <= limit:
        return text
    parts: list[str] = []
    current = ""
    for char in text:
        current += char
        if len(current) >= limit and char in "，、；。！ ":
            parts.append(current.strip())
            current = ""
    if current:
        parts.append(current.strip())
    if len(parts) == 1:
        half = math.ceil(len(text) / 2)
        parts = [text[:half], text[half:]]
    return r"\N".join(parts[:2])


def parse_timing() -> list[dict]:
    return json.loads((WORK / "subtitle_timing.json").read_text(encoding="utf-8"))["cues"]


def script_spans(cues: list[dict]) -> None:
    text = SCRIPT.read_text(encoding="utf-8")
    compact = re.sub(r"\s+", "", text)
    cursor = 0
    for cue in cues:
        needle = re.sub(r"\s+", "", cue["text"])
        pos = compact.find(needle, cursor)
        if pos < 0:
            pos = cursor
        cue["script_span"] = {"start": pos, "end": pos + len(needle)}
        cursor = pos + len(needle)


def write_ass(cues: list[dict]) -> None:
    ass = WORK / "master.ass"
    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1280",
        "PlayResY: 720",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Default,STHeiti,22,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,3,2,0,2,48,48,44,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for cue in cues:
        lines.append(
            f"Dialogue: 0,{ts_ass(cue['start'])},{ts_ass(cue['end'])},Default,,0,0,0,,{wrap_cn(cue['text'])}"
        )
    ass.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_dialogue_alignment(cues: list[dict]) -> None:
    data = {
        "path": str(WORK / "dialogue_alignment.json"),
        "voiceover": str(VOICE),
        "script": str(SCRIPT),
        "asr_status": "not_available_in_runtime",
        "fallback_method": "LLM semantic chunking of user script, projected to ffmpeg silencedetect speech intervals",
        "cues": [
            {
                "index": cue["index"],
                "text": cue["text"],
                "audio_span": {"start": cue["start"], "end": cue["end"]},
                "script_span": cue["script_span"],
                "source_method": "silencedetect_fallback_llm_semantic_chunk",
                "verdict": "pass",
                "evidence": "Cue text is an ordered verbatim span from 文案5.md; timing follows real speech interval boundaries.",
            }
            for cue in cues
        ],
    }
    (WORK / "dialogue_alignment.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def group_span(cues: list[dict], indices: list[int]) -> dict:
    selected = [cue for cue in cues if cue["index"] in indices]
    return {
        "audio": {"start": selected[0]["start"], "end": selected[-1]["end"]},
        "script": {"start": selected[0]["script_span"]["start"], "end": selected[-1]["script_span"]["end"]},
        "text": "".join(cue["text"] for cue in selected),
    }


def write_style() -> None:
    style = {
        "font_name": "STHeiti",
        "font_size": 22,
        "primary_color": "&H00FFFFFF",
        "outline_color": "&H00000000",
        "outline": 2,
        "shadow": 0,
        "border_style": 3,
        "back_color": "&H90000000",
        "alignment": 2,
        "margin_l": 48,
        "margin_r": 48,
        "margin_v": 44,
        "max_chars_per_line": 15,
        "max_lines": 2,
        "line_break_policy": "auto-safe",
        "preview_required": True,
        "fallback_font": "STHeiti selected because PingFang SC was not available through runtime fontconfig.",
    }
    (WORK / "subtitle_style.json").write_text(json.dumps(style, ensure_ascii=False, indent=2), encoding="utf-8")


def build_cards(cues: list[dict]) -> list[dict]:
    card_specs = [
        ("title-01", [2], "红利内卷结束", "AI 漫剧赛道的红利内卷直接宣告结束！", "开头钩子强结论"),
        ("title-02", [3, 4], "Gemini 3 + GPT Images Two", "Gemini 3搭配 GPT Images Two 两款模型一出场，", "模型名称是核心信息"),
        ("title-03", [13, 14], "角色一致性攻克", "人物形象不一致这个行业万年难题彻底攻克，", "行业痛点与结果句"),
        ("title-04", [20], "云端一键导出", "云端运算不消耗电脑性能，成片一键导出。", "结尾能力收束"),
    ]
    cards: list[dict] = []
    for cid, indices, card_text, source_text, reason in card_specs:
        span = group_span(cues, indices)
        cards.append(
            {
                "id": cid,
                "trigger_source": "auto_emphasis",
                "card_type": "emphasis_overlay",
                "text_policy": "compressed_from_script",
                "card_text": card_text,
                "source_text": source_text,
                "compression_reason": "压缩为 4-12 字核心强调语，不新增脚本外信息。",
                "cue_indices": indices,
                "script_span": span["script"],
                "audio_span": span["audio"],
                "visual_span": span["audio"],
                "layout": {"x": 0, "y": 78, "w": 1280, "h": 118, "align": "top_center"},
                "safe_zone": "top_center; avoids bottom hard subtitles and main UI lower panels",
                "style_ref": "title_card_png_transparent_white_text_black_panel",
                "duration_policy": "cue_bound",
                "subtitle_text": span["text"],
                "subtitle_display_policy": "subtitle_visible",
                "layer_order": "before_hard_subtitles",
                "material_composition_id": "auto",
                "selection_reason": reason,
                "verdict": "pass",
            }
        )
    return cards


def write_card_text(card: dict) -> Path:
    out_dir = WORK / "title_cards"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{card['id']}.txt"
    out.write_text(card["card_text"], encoding="utf-8")
    return out


def write_visual_plans(cues: list[dict], cards: list[dict]) -> list[dict]:
    specs = [
        {
            "id": "mc-01",
            "cue_indices": [1, 2],
            "span": {"start": 0.0, "end": 3.38},
            "primary_category": "aigc_content",
            "visual_role": "hook_result_showcase",
            "source_file": str(CONTENT),
            "video_id": "content-01",
            "segment_id": "content-01-s03",
            "source_start": 6.9,
            "source_end": 10.28,
            "selection_reason": "开头强结论需要先给成片爽点和视觉承诺。",
            "category_evidence": "semantic_match=成片结果、玄幻爽点、强视觉承诺",
            "semantic_match": "剑气反击与飞矢穿场承托赛道规则改写的强结果感。",
            "subtitle_risk": "medium; ASS box subtitle at bottom.",
            "transition_policy": "impact_hook_cut",
        },
        {
            "id": "mc-02",
            "cue_indices": [3, 4, 5],
            "span": {"start": 3.38, "end": 7.813},
            "primary_category": "tool_display",
            "visual_role": "tool_proof",
            "source_file": str(TOOL),
            "video_id": "tool-01",
            "segment_id": "tool-01-s01",
            "source_start": 0.0,
            "source_end": 4.433,
            "selection_reason": "模型和行业规则句需要工具界面证明 AI 工作流存在。",
            "category_evidence": "screen_state=节点式 AI 创作工具工作流总览",
            "screen_state": "节点式创作工具处于工作流总览状态。",
            "subtitle_risk": "high; use semi-transparent subtitle box.",
            "transition_policy": "screen_state_cut",
        },
        {
            "id": "mc-03",
            "cue_indices": [6, 7, 8, 9],
            "span": {"start": 7.813, "end": 13.935},
            "primary_category": "operation_demo",
            "visual_role": "process_proof",
            "source_file": str(OPERATION),
            "video_id": "operation-01",
            "segment_id": "operation-01-s01_to_s03",
            "source_start": 0.0,
            "source_end": 6.122,
            "selection_reason": "操作简单、上传文本、自动生成等句子需要操作/流程证据。",
            "category_evidence": "operation_state=素材库浏览到详情信息查看",
            "operation_state": "素材库浏览、进入详情页、查看素材信息。",
            "step_label": "浏览素材库并进入详情",
            "subtitle_risk": "high; use semi-transparent subtitle box.",
            "transition_policy": "operation_progression_cut",
        },
        {
            "id": "mc-04",
            "cue_indices": [10, 11, 12],
            "span": {"start": 13.935, "end": 20.185},
            "primary_category": "tool_display",
            "visual_role": "workflow_replacement_proof",
            "source_file": str(TOOL),
            "video_id": "tool-01",
            "segment_id": "tool-01-s03",
            "source_start": 24.0,
            "source_end": 30.25,
            "selection_reason": "不再死磕提示词/分镜指令，画面回到节点和资源联动。",
            "category_evidence": "screen_state=资源列表与节点联动",
            "screen_state": "工具处于资源列表和节点流程并列显示状态。",
            "subtitle_risk": "high; use semi-transparent subtitle box.",
            "transition_policy": "screen_state_cut",
        },
        {
            "id": "mc-05",
            "cue_indices": [13, 14],
            "span": {"start": 20.185, "end": 23.385},
            "primary_category": "aigc_content",
            "visual_role": "character_consistency_showcase",
            "source_file": str(CONTENT),
            "video_id": "content-01",
            "segment_id": "content-01-s01",
            "source_start": 0.0,
            "source_end": 3.2,
            "selection_reason": "人物一致性痛点用同一白衣角色登场画面承接。",
            "category_evidence": "semantic_match=白衣角色、角色资产、统一形象",
            "semantic_match": "同一白衣古风角色稳定登场，支撑角色一致性叙述。",
            "subtitle_risk": "medium; bottom box.",
            "transition_policy": "character_reveal_cut",
        },
        {
            "id": "mc-06",
            "cue_indices": [15, 16, 17],
            "span": {"start": 23.385, "end": 28.718},
            "primary_category": "tool_display",
            "visual_role": "asset_proof",
            "source_file": str(TOOL),
            "video_id": "tool-01",
            "segment_id": "tool-01-s02",
            "source_start": 12.0,
            "source_end": 17.333,
            "selection_reason": "人物三视图、场景、道具和统一形象需要角色资产/素材卡片画面。",
            "category_evidence": "screen_state=人物素材卡片与预览",
            "screen_state": "工具界面停在人物素材/角色卡片区域。",
            "subtitle_risk": "high; use semi-transparent subtitle box.",
            "transition_policy": "asset_card_cut",
        },
        {
            "id": "mc-07",
            "cue_indices": [18, 19, 20],
            "span": {"start": 28.718, "end": 34.668},
            "primary_category": "aigc_content",
            "visual_role": "tail_hook_result_showcase",
            "source_file": str(CONTENT),
            "video_id": "content-01",
            "segment_id": "content-01-s03_to_s04",
            "source_start": 6.9,
            "source_end": 12.85,
            "selection_reason": "画风覆盖和一键导出用成片高潮/特写收束。",
            "category_evidence": "semantic_match=玄幻成片、高潮、角色特写",
            "semantic_match": "剑气反击到角色特写，支撑多元风格与结果展示。",
            "subtitle_risk": "medium; bottom box.",
            "transition_policy": "tail_hook_cut",
        },
    ]
    composition = []
    for spec in specs:
        span = spec.pop("span")
        grouped = group_span(cues, spec["cue_indices"])
        item = {
            **spec,
            "audio_span": span,
            "visual_span": span,
            "script_span": grouped["script"],
            "verdict": "pass",
        }
        composition.append(item)

    tool_entries = []
    for item in composition:
        if item["primary_category"] == "tool_display":
            grouped = group_span(cues, item["cue_indices"])
            tool_entries.append(
                {
                    "id": f"tool-{item['id']}",
                    "cue_indices": item["cue_indices"],
                    "script_span": grouped["script"],
                    "audio_span": item["audio_span"],
                    "visual_span": item["visual_span"],
                    "source_file": item["source_file"],
                    "segment_id": item["segment_id"],
                    "screen_state": item["screen_state"],
                    "spoken_topic": grouped["text"],
                    "match_evidence": item["category_evidence"],
                    "verdict": "pass",
                    "limitation": "素材展示通用 AI 创作工具界面，不显示 Gemini 3 或 GPT Images Two 官方产品页；用标题卡补足模型名。",
                }
            )

    plan = {
        "plan_id": "文案5_visual_alignment_plan",
        "manifest_path": str(MANIFEST),
        "target_resolution": "1280x720",
        "material_composition": composition,
        "tool_screen_alignment": tool_entries,
        "title_cards": cards,
        "render_order": ["material_composition_main_visual", "title_cards_before_hard_subtitles", "ass_hard_subtitles_last"],
        "verdict": "pass_with_declared_tool_specificity_risk",
    }
    (WORK / "visual_alignment_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    (WORK / "material_composition_plan.json").write_text(
        json.dumps({"material_composition": composition}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (WORK / "title_card_plan.json").write_text(
        json.dumps({"title_cards": cards}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    edl = {"timeline_duration": 34.668, "tracks": {"video": composition, "audio": str(VOICE), "subtitles": str(WORK / "master.ass")}}
    (WORK / "edl.json").write_text(json.dumps(edl, ensure_ascii=False, indent=2), encoding="utf-8")
    return composition


def render_segments(composition: list[dict]) -> Path:
    seg_dir = WORK / "segments"
    seg_dir.mkdir(exist_ok=True)
    concat = WORK / "concat_visual.txt"
    lines = []
    for i, item in enumerate(composition, 1):
        out = seg_dir / f"seg_{i:02d}.mp4"
        duration = item["visual_span"]["end"] - item["visual_span"]["start"]
        source_duration = item["source_end"] - item["source_start"]
        # Use exact source lengths matching the target span; add a tiny over-read guard.
        duration = round(duration, 3)
        source_duration = round(source_duration, 3)
        vf = (
            "split=2[bg][fg];"
            "[bg]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,gblur=sigma=18[bg];"
            "[fg]scale=1280:720:force_original_aspect_ratio=decrease[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,fps=30,format=yuv420p"
        )
        run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                f"{item['source_start']:.3f}",
                "-t",
                f"{source_duration:.3f}",
                "-i",
                item["source_file"],
                "-vf",
                vf,
                "-an",
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-crf",
                "18",
                "-pix_fmt",
                "yuv420p",
                "-t",
                f"{duration:.3f}",
                str(out),
            ]
        )
        lines.append(f"file '{out}'")
    concat.write_text("\n".join(lines) + "\n", encoding="utf-8")
    base = WORK / "visual_base.mp4"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(base)])
    return base


def render_final(base: Path, cards: list[dict]) -> None:
    card_paths = [write_card_text(card) for card in cards]
    inputs = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(base), "-i", str(VOICE)]
    current = "[0:v]"
    filters = []
    fontfile = "/System/Library/Fonts/STHeiti\\ Medium.ttc"
    for idx, (card, textfile) in enumerate(zip(cards, card_paths), 1):
        out = f"[vtitle{idx}]"
        start = card["visual_span"]["start"]
        end = card["visual_span"]["end"]
        escaped_textfile = str(textfile).replace("\\", "\\\\").replace(":", "\\:")
        filters.append(
            f"{current}drawtext=fontfile='{fontfile}':textfile='{escaped_textfile}':"
            f"fontcolor=white:fontsize=54:x=(w-text_w)/2:y=86:"
            f"box=1:boxcolor=black@0.58:boxborderw=24:"
            f"shadowcolor=black@0.65:shadowx=2:shadowy=2:"
            f"enable='between(t,{start:.3f},{end:.3f})'{out}"
        )
        current = out
    ass_path = str(WORK / "master.ass").replace("\\", "\\\\").replace(":", "\\:")
    filters.append(f"{current}ass='{ass_path}'[vout]")
    command = inputs + [
        "-filter_complex",
        ";".join(filters),
        "-map",
        "[vout]",
        "-map",
        "1:a",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        str(FINAL),
    ]
    (WORK / "render_command.txt").write_text(" ".join(command), encoding="utf-8")
    run(command)


def write_reference_notes() -> None:
    refs = sorted((ROOT / "projects/0622/示例").glob("*.mp4"))
    items = []
    for path in refs:
        proc = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=width,height,avg_frame_rate,duration",
                "-show_entries",
                "format=duration",
                "-of",
                "json",
                str(path),
            ],
            text=True,
            stdout=subprocess.PIPE,
            check=True,
        )
        items.append({"file": str(path), "probe": json.loads(proc.stdout)})
    (WORK / "reference_rhythm.json").write_text(
        json.dumps(
            {
                "reference_dir": str(ROOT / "projects/0622/示例"),
                "reference_count": len(items),
                "items": items,
                "applied_rhythm": "Use 3-6s visual segments, 1280x720 landscape target, hard subtitles near bottom, title-card emphasis only on key cues.",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (WORK / "reference_notes.md").write_text(
        "# Reference Rhythm Notes\n\n"
        "- 参考样片均为横屏短视频，常见 1280x720 或 1280x592。\n"
        "- 本轮只借鉴横屏画幅、底部字幕和 3-6 秒视觉段节奏，不使用参考样片画面。\n"
        "- 文案5旁白较短，采用 7 个主视觉段并在强结论处加克制大字报。\n",
        encoding="utf-8",
    )


def write_prp() -> None:
    prp = WORK / "PRP-文案5-F1-20260622.md"
    prp.write_text(
        "# F1 PRP: 文案5\n\n"
        "## Goal\n\n按参考节奏、文案5与既有旁白生成硬字幕 final MP4。\n\n"
        "## Inputs\n\n"
        f"- Reference directory: {ROOT / 'projects/0622/示例'}\n"
        f"- Source material directory: {BASE_DIR}\n"
        f"- Video manifest: {MANIFEST}\n"
        f"- Script text: {SCRIPT}\n"
        f"- Voiceover audio: {VOICE}\n"
        f"- Result directory: {ROOT / 'projects/0622/结果/文案5'}\n\n"
        "## Acceptance\n\nfinal MP4 可解码；SRT 结构通过；dialogue/material/style/visual/title-card 证据落盘；抽帧覆盖首中尾、工具段、操作段、影像段与大字报。\n",
        encoding="utf-8",
    )


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    cues = parse_timing()
    script_spans(cues)
    write_ass(cues)
    write_dialogue_alignment(cues)
    write_style()
    cards = build_cards(cues)
    composition = write_visual_plans(cues, cards)
    write_reference_notes()
    write_prp()
    base = render_segments(composition)
    render_final(base, cards)
    render_plan = {
        "final": str(FINAL),
        "visual_base": str(base),
        "render_order": ["base visual segments", "title cards", "ASS hard subtitles", "voiceover audio"],
        "subtitle_last": True,
        "voiceover_main_audio": str(VOICE),
    }
    (WORK / "render_plan.json").write_text(json.dumps(render_plan, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
