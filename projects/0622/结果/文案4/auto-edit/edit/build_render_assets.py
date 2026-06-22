#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path("/Volumes/AIGC/AI-CUT")
RESULT = ROOT / "projects/0622/结果/文案4"
WORK = RESULT / "auto-edit/edit"
SEGMENTS = WORK / "segments"
SOURCE = ROOT / "projects/0622/素材/视频"
AUDIO = ROOT / "projects/0622/素材/音频/文案4-音频.mp3"
FINAL = RESULT / "文案4_final.mp4"


def run(cmd: list[str], log_name: str) -> None:
    log_path = WORK / "logs" / log_name
    with log_path.open("w", encoding="utf-8") as log:
        log.write(" ".join(cmd) + "\n\n")
        proc = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"command failed: {log_path}")


def ass_time(seconds: float) -> str:
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
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def break_text(text: str, limit: int = 14) -> str:
    compact = text.strip()
    if len(compact) <= limit:
        return compact
    split_at = len(compact) // 2
    for i in range(split_at, 0, -1):
        if compact[i] in "，、 和":
            split_at = i + 1
            break
    return compact[:split_at].strip() + r"\N" + compact[split_at:].strip()


def span_for(cues: list[dict], indices: list[int], start_override: float | None = None, end_override: float | None = None) -> dict:
    selected = [cue for cue in cues if cue["index"] in indices]
    start = selected[0]["audio_span"]["start"] if start_override is None else start_override
    end = selected[-1]["audio_span"]["end"] if end_override is None else end_override
    return {"start": round(start, 3), "end": round(end, 3)}


def script_span_for(cues: list[dict], indices: list[int]) -> dict:
    selected = [cue for cue in cues if cue["index"] in indices]
    start = selected[0]["script_span"]["start_char_compact"]
    end = selected[-1]["script_span"]["end_char_compact"]
    return {
        "start": start,
        "end": end,
        "start_char_compact": start,
        "end_char_compact": end,
        "source_text": "".join(cue["text"] for cue in selected),
    }


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "logs").mkdir(exist_ok=True)
    SEGMENTS.mkdir(exist_ok=True)

    timing = json.loads((WORK / "subtitle_timing.json").read_text(encoding="utf-8"))
    dialogue = json.loads((WORK / "dialogue_alignment.json").read_text(encoding="utf-8"))
    cues = dialogue["cues"]

    style = {
        "font_name": "PingFang SC",
        "font_size": 24,
        "primary_color": "&H00FFFFFF",
        "outline_color": "&H00000000",
        "outline": 2.2,
        "shadow": 0.8,
        "border_style": 3,
        "back_color": "&H80000000",
        "alignment": 2,
        "margin_l": 48,
        "margin_r": 48,
        "margin_v": 42,
        "max_chars_per_line": 14,
        "max_lines": 2,
        "line_break_policy": "auto-safe-in-ass-render",
        "preview_required": True,
        "style_reason": "工具和操作素材文字密集，采用底部半透明底盒、白字黑描边提高可读性。",
    }
    (WORK / "subtitle_style.json").write_text(json.dumps(style, ensure_ascii=False, indent=2), encoding="utf-8")

    ass_lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1280",
        "PlayResY: 720",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Default,{style['font_name']},{style['font_size']},{style['primary_color']},&H000000FF,{style['outline_color']},{style['back_color']},0,0,0,0,100,100,0,0,{style['border_style']},{style['outline']},{style['shadow']},{style['alignment']},{style['margin_l']},{style['margin_r']},{style['margin_v']},1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for cue in timing["cues"]:
        ass_lines.append(
            f"Dialogue: 0,{ass_time(cue['start'])},{ass_time(cue['end'])},Default,,0,0,0,,{break_text(cue['text'])}"
        )
    (WORK / "master.ass").write_text("\n".join(ass_lines) + "\n", encoding="utf-8")

    groups = [
        {"id": "mc-01", "cue_indices": [1, 2], "primary_category": "aigc_content", "visual_role": "hook", "source_file": "影像内容/微信视频2026-06-21_220234_765.mp4", "segment_id": "content-01-s03", "source_start": 6.9, "selection_reason": "开头提醒和行业变革先给成片效果与玄幻冲击，建立 AI 漫剧结果感。", "category_evidence": {"semantic_match": "成片结果展示、玄幻爽点", "visual_rhythm_reason": "高动作强度适合开头钩子。"}, "subtitle_risk": "medium; bottom box"},
        {"id": "mc-02", "cue_indices": [3, 4, 5, 6], "primary_category": "tool_display", "visual_role": "tool_proof", "source_file": "工具使用/1.mp4", "segment_id": "tool-01-s01", "source_start": 0.0, "selection_reason": "Gemini/GPT 和赛道变化属于工具能力说明，使用节点式工具总览。", "category_evidence": {"screen_state": "节点式创作工具工作流总览，可见节点和连线。"}, "subtitle_risk": "high; bottom box"},
        {"id": "mc-03", "cue_indices": [7, 8], "primary_category": "operation_demo", "visual_role": "process_proof", "source_file": "操作展示/微信视频2026-06-21_220316_527.mp4", "segment_id": "operation-01-s01", "source_start": 0.0, "selection_reason": "讲工具简单和上传小说，使用素材库/网页操作开场作实操证明。", "category_evidence": {"operation_state": "browse_gallery", "step_label": "浏览素材库网格"}, "subtitle_risk": "high; bottom box"},
        {"id": "mc-04", "cue_indices": [9, 10, 11], "primary_category": "tool_display", "visual_role": "workflow_reasoning", "source_file": "工具使用/1.mp4", "segment_id": "tool-01-s03", "source_start": 24.0, "selection_reason": "AI 梳理故事逻辑和生成脚本需要展示资源列表与节点联动。", "category_evidence": {"screen_state": "资源列表与节点流程并列显示。"}, "subtitle_risk": "high; bottom box"},
        {"id": "mc-05", "cue_indices": [12, 13], "primary_category": "tool_display", "visual_role": "storyboard_proof", "source_file": "工具使用/1.mp4", "segment_id": "tool-01-s04", "source_start": 38.0, "selection_reason": "复杂分镜指令和电影分镜剧本对应节点生成/参数状态。", "category_evidence": {"screen_state": "节点参数/生成状态收束。"}, "subtitle_risk": "high; bottom box"},
        {"id": "mc-06", "cue_indices": [14, 15, 16], "primary_category": "tool_display", "visual_role": "asset_proof", "source_file": "工具使用/1.mp4", "segment_id": "tool-01-s02", "source_start": 12.0, "selection_reason": "人物画风、三视图属于角色资产证明，使用人物素材卡片与预览。", "category_evidence": {"screen_state": "人物素材/角色卡片区域。"}, "subtitle_risk": "high; bottom box"},
        {"id": "mc-07", "cue_indices": [17, 18], "primary_category": "operation_demo", "visual_role": "asset_review", "source_file": "操作展示/微信视频2026-06-21_220316_527.mp4", "segment_id": "operation-01-s03", "source_start": 5.2, "selection_reason": "场景、道具、角色不跑偏需要资产详情和相关素材作为操作证据。", "category_evidence": {"operation_state": "inspect_asset_info", "step_label": "查看素材详情信息"}, "subtitle_risk": "high; bottom box"},
        {"id": "mc-08", "cue_indices": [19, 20, 21, 22], "primary_category": "aigc_content", "visual_role": "style_showcase", "source_file": "影像内容/微信视频2026-06-21_220234_765.mp4", "segment_id": "content-01-s01", "source_start": 0.0, "selection_reason": "风格切换段用成片影像作视觉承托；当前素材仅能证明古风/玄幻视觉，其他风格为素材缺口风险。", "category_evidence": {"semantic_match": "古风主角、冷蓝战场；赛璐璐/国风3D/日系动漫无专门素材。"}, "subtitle_risk": "medium; bottom box", "residual_risk": "素材池没有赛璐璐、国风 3D、日系动漫三种独立画面。"},
        {"id": "mc-09", "cue_indices": [23, 24], "primary_category": "tool_display", "visual_role": "cloud_tool_close", "source_file": "工具使用/1.mp4", "segment_id": "tool-01-s04", "source_start": 44.0, "selection_reason": "云端运行和低配电脑使用回到工具界面作收束证明。", "category_evidence": {"screen_state": "节点工具界面尾段，可见工作流状态。"}, "subtitle_risk": "high; bottom box"},
    ]

    composition = []
    last_end = 0.0
    for group in groups:
        indices = group["cue_indices"]
        start = last_end
        end = span_for(cues, indices)["end"]
        if group["id"] == "mc-09":
            end = timing["voice_duration"]
        visual_span = {"start": round(start, 3), "end": round(end, 3)}
        audio_span = visual_span
        duration = end - start
        item = {
            **group,
            "audio_span": audio_span,
            "visual_span": visual_span,
            "script_span": script_span_for(cues, indices),
            "source_end": round(group["source_start"] + duration, 3),
            "transition_policy": "hard_cut_on_cue_group_boundary",
            "verdict": "pass",
        }
        composition.append(item)
        last_end = end

    tool_alignment = []
    for item in composition:
        if item["primary_category"] == "tool_display":
            ev = item["category_evidence"]
            tool_alignment.append({
                "id": "ts-" + item["id"].split("-")[1],
                "cue_indices": item["cue_indices"],
                "script_span": item["script_span"],
                "audio_span": item["audio_span"],
                "visual_span": item["visual_span"],
                "source_file": item["source_file"],
                "segment_id": item["segment_id"],
                "screen_state": ev.get("screen_state", ""),
                "spoken_topic": item["script_span"]["source_text"],
                "match_evidence": item["selection_reason"],
                "verdict": "pass",
            })

    visual_plan = {
        "schema_version": 1,
        "target": {"width": 1280, "height": 720, "fps": 30, "duration_sec": timing["voice_duration"]},
        "video_manifest_path": "projects/0622/素材/视频/视频说明.yaml",
        "manifest_status": "loaded_with_segments",
        "material_composition": composition,
        "tool_screen_alignment": tool_alignment,
        "title_cards": [],
        "title_card_decision": "not_enabled; no user-specified title cards, automatic emphasis suppressed to avoid covering dense tool/operation UI and bottom subtitles",
        "verdict": "pass_with_residual_style_material_risk",
    }
    (WORK / "visual_alignment_plan.json").write_text(json.dumps(visual_plan, ensure_ascii=False, indent=2), encoding="utf-8")
    (WORK / "material_composition_plan.json").write_text(json.dumps({"material_composition": composition}, ensure_ascii=False, indent=2), encoding="utf-8")
    (WORK / "title_card_plan.json").write_text(json.dumps({"title_cards": [], "decision": visual_plan["title_card_decision"], "verdict": "not_enabled"}, ensure_ascii=False, indent=2), encoding="utf-8")
    (WORK / "edl.json").write_text(json.dumps({"render_order": composition, "audio": str(AUDIO), "subtitle_ass": str(WORK / "master.ass"), "subtitle_srt": str(WORK / "master.srt")}, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# F1 Reference Notes: 文案4",
        "",
        "- 参考目录: projects/0622/示例",
        "- 参考样片: 5 个短视频，时长约 17.32-60.60 秒。",
        "- 画幅: 主要为 1280x720，另有 1280x592；本片输出 1280x720。",
        "- 节奏应用: 短 cue、硬切、旁白主时钟；参考片只用于节奏/字幕风格，不作为成片素材。",
        "- 字幕应用: 底部硬字幕，工具/操作画面文字密集，采用半透明底盒。",
    ]
    (WORK / "reference_notes.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    prp = f"""# F1 PRP: 文案4

## Goal

按 F1 full_auto_edit 生成文案4硬字幕成片。

## Inputs

- Reference directory: projects/0622/示例
- Source video/material directory: projects/0622/素材/视频
- Script text: projects/0622/素材/文案/文案4.md
- Voiceover audio: projects/0622/素材/音频/文案4-音频.mp3
- Result directory: projects/0622/结果/文案4

## Outputs

- Final MP4: projects/0622/结果/文案4/文案4_final.mp4
- Work directory: projects/0622/结果/文案4/auto-edit/edit
- Master SRT: projects/0622/结果/文案4/auto-edit/edit/master.srt
- Dialogue alignment plan: projects/0622/结果/文案4/auto-edit/edit/dialogue_alignment.json
- Material composition plan: projects/0622/结果/文案4/auto-edit/edit/material_composition_plan.json
- Visual alignment plan: projects/0622/结果/文案4/auto-edit/edit/visual_alignment_plan.json
- Title-card plan: projects/0622/结果/文案4/auto-edit/edit/title_card_plan.json
- Subtitle style: projects/0622/结果/文案4/auto-edit/edit/subtitle_style.json
- EDL/render plan: projects/0622/结果/文案4/auto-edit/edit/edl.json
- Execution report: projects/0622/结果/文案4/auto-edit/edit/execution_report.md

## Routing

- Main workflow: $F1 full_auto_edit
- ASR route: unavailable/not invoked; silencedetect fallback with LLM semantic chunks.
- Manifest route: read existing projects/0622/素材/视频/视频说明.yaml; no modification.

## Acceptance

- final MP4 decodes and has video/audio streams.
- SRT and dialogue alignment validate.
- Visual plan validates with material composition and tool-screen alignment.
- Subtitle style validates and preview/final frames are extracted.
"""
    (WORK / "PRP-文案4-20260622.md").write_text(prp, encoding="utf-8")

    if FINAL.exists():
        backup = RESULT / f"文案4_final.backup.mp4"
        shutil.copy2(FINAL, backup)

    for old in SEGMENTS.glob("segment_*.mp4"):
        old.unlink()

    segment_paths: list[Path] = []
    for idx, item in enumerate(composition, 1):
        source = SOURCE / item["source_file"]
        duration = item["visual_span"]["end"] - item["visual_span"]["start"]
        out = SEGMENTS / f"segment_{idx:02d}.mp4"
        segment_paths.append(out)
        vf = "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps=30,format=yuv420p"
        run([
            "ffmpeg", "-hide_banner", "-y",
            "-ss", f"{item['source_start']:.3f}",
            "-i", str(source),
            "-t", f"{duration:.3f}",
            "-an",
            "-vf", vf,
            "-r", "30",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "18",
            str(out),
        ], f"render_segment_{idx:02d}.log")

    concat_file = WORK / "concat_segments.txt"
    concat_file.write_text("".join(f"file '{path.as_posix()}'\n" for path in segment_paths), encoding="utf-8")
    visual_no_subs = WORK / "visual_no_subtitles.mp4"
    run([
        "ffmpeg", "-hide_banner", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(visual_no_subs),
    ], "concat_visual.log")

    ass_path = WORK / "master.ass"
    run([
        "ffmpeg", "-hide_banner", "-y",
        "-i", str(visual_no_subs),
        "-i", str(AUDIO),
        "-vf", f"ass={ass_path.as_posix()}",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(FINAL),
    ], "render_final.log")


if __name__ == "__main__":
    main()
