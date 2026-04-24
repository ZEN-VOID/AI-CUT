# Output Persistence

This reference owns save-path and final asset persistence rules for built-in and CLI imagegen execution.

## Built-In Save-Path Policy

- Built-in `image_gen` saves generated images under `$CODEX_HOME/*` by default.
- Do not describe or rely on OS temp as the built-in default destination.
- Do not describe or rely on a destination-path argument on the built-in `image_gen` tool.
- If a specific location is needed, generate first and then move or copy the selected output from `$CODEX_HOME/generated_images/...`.

Save-path precedence in built-in mode:

1. If the user names a destination, move or copy the selected output there.
2. If the image is meant for the current project, move or copy the final selected image into the workspace before finishing.
3. If the image is only for preview or brainstorming, render it inline; the underlying file can remain at the default `$CODEX_HOME/*` path.

Never leave a project-referenced asset only at the default `$CODEX_HOME/*` path.

## Workspace Naming

- Do not overwrite an existing asset unless the user explicitly asked for replacement.
- Create descriptive sibling filenames when replacing is not explicit, such as `hero-v2.png`, `item-icon-edited.png`, or `cutout-alpha.png`.
- For batches, persist every requested final deliverable unless the user explicitly asked for preview-only outputs.
- Discarded variants do not need to be kept unless requested.

## CLI Fallback Output

These conventions apply only to the explicit CLI fallback:

- Use `tmp/imagegen/` for intermediate JSONL batches or scratch files.
- Use `output/imagegen/` for final CLI outputs unless the user names another destination.
- Use `--out` or `--out-dir` for CLI output paths.
- Keep filenames stable and descriptive.
- Reruns should not overwrite existing output unless the user requested replacement or CLI `--force` is intentionally used.

## Final Report Requirements

Every completed imagegen task should report:

- execution mode: built-in `image_gen`, transparent chroma-key post-process, or CLI fallback;
- saved path(s) for any workspace-bound asset(s);
- final prompt or prompt set;
- whether transparent output was validated when requested;
- any residual risk, such as imperfect text rendering or user-confirmed fallback constraints.
