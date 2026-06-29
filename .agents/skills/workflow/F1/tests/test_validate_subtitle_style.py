from __future__ import annotations

import importlib.util
import json
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_subtitle_style.py"
SPEC = importlib.util.spec_from_file_location("validate_subtitle_style", SCRIPT_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def write_style(tmp_path: Path, style: dict) -> Path:
    path = tmp_path / "subtitle_style.json"
    path.write_text(json.dumps(style, ensure_ascii=False), encoding="utf-8")
    return path


def base_style() -> dict:
    return {
        "font_name": "PingFang SC",
        "font_size": 20,
        "font_size_lock": True,
        "font_size_scope": "global",
        "auto_shrink": False,
        "primary_color": "&H00FFFFFF",
        "outline_color": "&H00000000",
        "back_color": "&H80000000",
        "outline": 2,
        "shadow": 1,
        "margin_l": 40,
        "margin_r": 40,
        "margin_v": 46,
        "max_chars_per_line": 16,
        "max_lines": 1,
        "line_break_policy": "single-line",
        "alignment": 2,
        "border_style": 1,
        "preview_required": True,
    }


def test_locked_single_line_subtitle_style_passes(tmp_path: Path) -> None:
    path = write_style(tmp_path, base_style())

    report = validator.validate(path)

    assert report["ok"], report["errors"]


def test_expected_font_size_and_render_command_projection_passes(tmp_path: Path) -> None:
    style = base_style()
    style["font_size"] = 30
    path = write_style(tmp_path, style)
    render_command = tmp_path / "render_command.txt"
    render_command.write_text(
        "ffmpeg -vf subtitles=subtitles.srt:force_style='Fontname=STHeiti,Fontsize=30'",
        encoding="utf-8",
    )

    report = validator.validate(
        path,
        expected_font_size=30,
        render_command=render_command,
        require_render_font_size=True,
    )

    assert report["ok"], report["errors"]


def test_render_font_size_mismatch_fails(tmp_path: Path) -> None:
    style = base_style()
    style["font_size"] = 30
    path = write_style(tmp_path, style)
    render_command = tmp_path / "render_command.txt"
    render_command.write_text(
        "ffmpeg -vf subtitles=subtitles.srt:force_style='Fontname=STHeiti,Fontsize=44'",
        encoding="utf-8",
    )

    report = validator.validate(
        path,
        expected_font_size=30,
        render_command=render_command,
        require_render_font_size=True,
    )

    assert not report["ok"]
    assert "subtitle Fontsize mismatch" in "\n".join(report["errors"])


def test_missing_font_size_lock_fails(tmp_path: Path) -> None:
    style = base_style()
    del style["font_size_lock"]
    path = write_style(tmp_path, style)

    report = validator.validate(path)

    assert not report["ok"]
    assert "font_size_lock" in "\n".join(report["errors"])


def test_auto_shrink_and_per_cue_font_size_fails(tmp_path: Path) -> None:
    style = base_style()
    style["auto_shrink"] = True
    style["font_size_overrides"] = {"cue-12": 16}
    path = write_style(tmp_path, style)

    report = validator.validate(path)

    assert not report["ok"]
    errors = "\n".join(report["errors"])
    assert "auto_shrink" in errors
    assert "font_size_overrides" in errors
