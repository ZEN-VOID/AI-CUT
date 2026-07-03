# Scripts

## `generate_missing_audio.py`

Mechanical runner for `$text-to-speech`.

It scans copy files, matches audio by identical stem, filters only the first standalone `【标题】` line from temporary TTS input, assigns MiniMax voices, calls the local mmx binary, and writes a manifest.

Default paths:

```bash
python3 .agents/skills/workflow/text-to-speech/scripts/generate_missing_audio.py --dry-run
```

Generate a range:

```bash
python3 .agents/skills/workflow/text-to-speech/scripts/generate_missing_audio.py --start 81 --end 140
```

Important boundaries:

- The script does not edit source `.txt` copy.
- Existing nonempty `.mp3` files are skipped unless `--overwrite` is provided.
- The script calls `.agents/skills/cli/mmx-cli/node_modules/.bin/mmx`; it must not require global `mmx`.
- Real API keys must come from MiniMax CLI config, process environment, or repo-root `.env`; keys are never passed as command arguments or written to the manifest.
