#!/usr/bin/env python3
"""Scan copy files and generate missing MiniMax TTS audio.

This script is mechanical workflow glue for the text-to-speech skill. It does
not edit source copy. It only strips a first-line bracket title from the
temporary TTS input.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path


DEFAULT_VOICES = {
    "贝因男声2": "moss_audio_ba1bbbae-6f8d-11f1-ba6a-025474e1e406",
    "贝因女声2": "moss_audio_9e8695bb-6f8d-11f1-938c-a6f6fa6b2a0c",
    "贝因女声1": "moss_audio_644a5ef6-6f8d-11f1-83ef-8afcbb8b5b5c",
}


TITLE_RE = re.compile(r"^\s*【[^】]+】\s*$")
COPY_NAME_RE = re.compile(r"^文案(\d+)\.txt$")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(
        description="Generate missing MiniMax TTS MP3 files for matching copy files.",
    )
    parser.add_argument("--text-dir", default=str(root / "projects/内容/文案"))
    parser.add_argument("--audio-dir", default=str(root / "projects/内容/音频"))
    parser.add_argument("--mmx-dir", default=str(root / ".agents/skills/cli/mmx-cli"))
    parser.add_argument("--start", type=int, help="First 文案 number to scan.")
    parser.add_argument("--end", type=int, help="Last 文案 number to scan.")
    parser.add_argument(
        "--files",
        nargs="*",
        help="Explicit text files to process. Overrides --start/--end scan filtering.",
    )
    parser.add_argument("--speed", default="1.26")
    parser.add_argument("--model", default="speech-2.8-hd")
    parser.add_argument("--region", default="global")
    parser.add_argument("--seed", type=int, help="Optional deterministic shuffle seed.")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--sleep", type=float, default=1.0, help="Seconds between calls.")
    parser.add_argument("--output-json", action="store_true")
    return parser.parse_args()


def copy_sort_key(path: Path) -> tuple[int, str]:
    match = COPY_NAME_RE.match(path.name)
    if match:
        return (int(match.group(1)), path.name)
    return (10**9, path.name)


def collect_text_files(args: argparse.Namespace) -> list[Path]:
    text_dir = Path(args.text_dir)
    if not text_dir.is_dir():
        raise SystemExit(f"Text directory not found: {text_dir}")
    if args.files:
        files = [Path(p) if Path(p).is_absolute() else repo_root() / p for p in args.files]
    else:
        files = sorted(text_dir.glob("文案*.txt"), key=copy_sort_key)
        if args.start is not None or args.end is not None:
            start = args.start if args.start is not None else -1
            end = args.end if args.end is not None else 10**12
            filtered = []
            for path in files:
                match = COPY_NAME_RE.match(path.name)
                if match and start <= int(match.group(1)) <= end:
                    filtered.append(path)
            files = filtered
    missing_sources = [str(path) for path in files if not path.is_file()]
    if missing_sources:
        raise SystemExit(f"Missing text files: {missing_sources}")
    if not files:
        raise SystemExit("No text files matched the requested scope.")
    return files


def strip_first_bracket_title(text: str) -> tuple[str, bool]:
    lines = text.splitlines()
    first_nonempty = None
    for index, line in enumerate(lines):
        if line.strip():
            first_nonempty = index
            break
    if first_nonempty is None:
        return "", False
    if not TITLE_RE.match(lines[first_nonempty]):
        return text.strip() + "\n", False
    kept = lines[:first_nonempty] + lines[first_nonempty + 1 :]
    while kept and not kept[0].strip():
        kept.pop(0)
    return "\n".join(kept).strip() + "\n", True


def build_targets(files: list[Path], audio_dir: Path, overwrite: bool) -> tuple[list[dict], list[dict]]:
    audio_dir.mkdir(parents=True, exist_ok=True)
    targets = []
    skipped = []
    for text_path in files:
        out_path = audio_dir / f"{text_path.stem}.mp3"
        exists = out_path.exists() and out_path.stat().st_size > 0
        item = {
            "text_path": str(text_path),
            "output_path": str(out_path),
            "stem": text_path.stem,
        }
        if exists and not overwrite:
            item["bytes"] = out_path.stat().st_size
            skipped.append(item)
        else:
            targets.append(item)
    return targets, skipped


def voice_plan(count: int, seed: int | None) -> list[tuple[str, str]]:
    voices = list(DEFAULT_VOICES.items())
    base = count // len(voices)
    remainder = count % len(voices)
    pool = []
    for voice in voices:
        pool.extend([voice] * base)
    extras = voices[:]
    rng = random.Random(seed) if seed is not None else random.SystemRandom()
    rng.shuffle(extras)
    pool.extend(extras[:remainder])
    rng.shuffle(pool)
    return pool


def mmx_binary(mmx_dir: Path) -> Path:
    binary = mmx_dir / "node_modules/.bin/mmx"
    if not binary.exists():
        raise SystemExit(f"Local mmx binary not found: {binary}")
    return binary


def load_env_file(env_path: Path) -> None:
    if not env_path.is_file():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key or key in os.environ:
            continue
        value = value.strip().strip('"').strip("'")
        os.environ[key] = value


def synthesize(
    *,
    mmx: Path,
    mmx_dir: Path,
    text: str,
    out_path: Path,
    voice_id: str,
    args: argparse.Namespace,
) -> tuple[bool, str]:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as handle:
        handle.write(text)
        temp_path = Path(handle.name)
    try:
        cmd = [
            str(mmx),
            "speech",
            "synthesize",
            "--text-file",
            str(temp_path),
            "--voice",
            voice_id,
            "--model",
            args.model,
            "--speed",
            str(args.speed),
            "--out",
            str(out_path),
            f"--region={args.region}",
            "--non-interactive",
            "--quiet",
        ]
        last_output = ""
        for attempt in range(1, args.retries + 1):
            proc = subprocess.run(
                cmd,
                cwd=mmx_dir,
                text=True,
                capture_output=True,
                timeout=240,
            )
            last_output = (proc.stdout + proc.stderr).strip()
            if proc.returncode == 0 and out_path.exists() and out_path.stat().st_size > 0:
                return True, last_output
            lowered = last_output.lower()
            if "auth" in lowered or "quota" in lowered or "subscription" in lowered:
                return False, last_output
            if attempt < args.retries:
                time.sleep(10 * attempt)
        return False, last_output
    finally:
        try:
            temp_path.unlink()
        except OSError:
            pass


def main() -> int:
    args = parse_args()
    text_files = collect_text_files(args)
    audio_dir = Path(args.audio_dir)
    targets, skipped = build_targets(text_files, audio_dir, args.overwrite)
    assignments = voice_plan(len(targets), args.seed)

    plan = []
    for target, (voice_name, voice_id) in zip(targets, assignments):
        source = Path(target["text_path"])
        raw_text = source.read_text(encoding="utf-8-sig")
        tts_text, stripped = strip_first_bracket_title(raw_text)
        if not tts_text.strip():
            raise SystemExit(f"No speakable text after title filtering: {source}")
        target.update(
            {
                "voice_name": voice_name,
                "voice_id": voice_id,
                "speed": str(args.speed),
                "model": args.model,
                "region": args.region,
                "title_stripped": stripped,
                "tts_characters": len(tts_text.strip()),
            }
        )
        plan.append((target, tts_text))

    manifest = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "dry-run" if args.dry_run else "generate",
        "text_dir": str(Path(args.text_dir)),
        "audio_dir": str(audio_dir),
        "speed": str(args.speed),
        "model": args.model,
        "region": args.region,
        "total_text_files": len(text_files),
        "skipped_existing": len(skipped),
        "planned": len(plan),
        "generated": 0,
        "failed": 0,
        "voices": {name: voice_id for name, voice_id in DEFAULT_VOICES.items()},
        "skipped": skipped,
        "items": [],
    }

    if args.dry_run:
        for target, _ in plan:
            manifest["items"].append({**target, "status": "planned"})
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0

    mmx_dir = Path(args.mmx_dir)
    binary = mmx_binary(mmx_dir)
    load_env_file(repo_root() / ".env")
    for index, (target, tts_text) in enumerate(plan, 1):
        out_path = Path(target["output_path"])
        print(f"[{index}/{len(plan)}] {out_path.name} voice={target['voice_name']}", flush=True)
        ok, cli_output = synthesize(
            mmx=binary,
            mmx_dir=mmx_dir,
            text=tts_text,
            out_path=out_path,
            voice_id=target["voice_id"],
            args=args,
        )
        item = {**target, "status": "generated" if ok else "failed"}
        item["bytes"] = out_path.stat().st_size if out_path.exists() else 0
        if not ok:
            item["error"] = cli_output[-1000:]
            manifest["failed"] += 1
            manifest["items"].append(item)
            break
        manifest["generated"] += 1
        manifest["items"].append(item)
        time.sleep(args.sleep)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    manifest_path = audio_dir / f"text-to-speech_manifest_{timestamp}.json"
    manifest["manifest_path"] = str(manifest_path)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.output_json:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
    else:
        print(f"manifest: {manifest_path}")
        print(f"generated={manifest['generated']} failed={manifest['failed']} skipped={manifest['skipped_existing']}")
    return 0 if manifest["failed"] == 0 else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
