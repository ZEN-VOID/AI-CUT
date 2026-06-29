from __future__ import annotations

import importlib.util
import json
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_bgm_mix_plan.py"
SPEC = importlib.util.spec_from_file_location("validate_bgm_mix_plan", SCRIPT_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def write_plan(tmp_path: Path, plan: dict) -> Path:
    path = tmp_path / "bgm_mix_plan.json"
    path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    return path


def base_bgm_plan() -> dict:
    return {
        "background_music": {
            "enabled": True,
            "source_file": "projects/0624/素材/音频/BGM.mp4",
            "source_has_audio": True,
            "source_probe": {"duration_sec": 64.0, "audio_streams": 1},
            "final_duration_sec": 27.0,
            "voiceover_priority": True,
            "coverage_policy": "continuous_bed",
            "mix_policy": {
                "bed_volume_db": "-18 dB",
                "ducking": {"enabled": True, "sidechain": "voiceover", "amount_db": -9},
                "target_lufs": -24,
                "peak_limit_db": -1.0,
            },
            "segments": [
                {
                    "id": "bgm-001",
                    "source_start": 8.0,
                    "source_end": 35.0,
                    "target_start": 0.0,
                    "target_end": 27.0,
                    "selection_reason": "the BGM rise and drop match the hook, tool proof, and result reveal structure",
                    "visual_sync_points": [
                        {"target_time": 0.0, "visual_event": "hook"},
                        {"target_time": 14.0, "visual_event": "result reveal"},
                    ],
                    "rhythm_match": {
                        "visual_cut_sync": "beats land near the hook and result-reveal cuts",
                        "max_sync_delta_sec": "0.18s",
                    },
                    "fade_in_sec": 0.35,
                    "fade_out_sec": 1.0,
                    "loop_policy": "single selected excerpt, no loop",
                    "ducking": {"enabled": True, "sidechain": "voiceover"},
                    "volume_db": "-18dB",
                    "verdict": "pass",
                }
            ],
        }
    }


def test_bgm_mix_plan_passes(tmp_path: Path) -> None:
    path = write_plan(tmp_path, base_bgm_plan())

    report = validator.validate(path, require_bgm=True)

    assert report["ok"], report["errors"]
    assert report["segment_count"] == 1


def test_bgm_mix_plan_rejects_loud_unmatched_or_uncovered_bgm(tmp_path: Path) -> None:
    plan = base_bgm_plan()
    bgm = plan["background_music"]
    bgm["voiceover_priority"] = False
    bgm["mix_policy"]["bed_volume_db"] = -3
    bgm["segments"][0]["target_end"] = 6.0
    bgm["segments"][0]["rhythm_match"]["max_sync_delta_sec"] = 0.8
    bgm["segments"][0]["verdict"] = "needs_review"
    path = write_plan(tmp_path, plan)

    report = validator.validate(path, require_bgm=True)

    assert not report["ok"]
    errors = "\n".join(report["errors"])
    assert "voiceover_priority" in errors
    assert "louder than -6" in errors
    assert "max_sync_delta_sec" in errors
    assert "coverage" in errors
    assert "verdict" in errors
