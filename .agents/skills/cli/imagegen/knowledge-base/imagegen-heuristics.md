# Imagegen Heuristics

This file stores stable reusable practices for imagegen. It does not override `SKILL.md`.

## Prompt Heuristics

- If the user prompt is detailed, preserve it and normalize structure only.
- If the user prompt is generic, add only details that materially improve output quality.
- For people and identity-sensitive edits, repeat invariants in every follow-up prompt.
- For in-image text, quote exact text and forbid extra words.
- For layouts, name the intended asset use so the model can choose the right polish and whitespace.

## Execution Heuristics

- Built-in `image_gen` is the only execution route for `.agents/skills/cli/imagegen`.
- If a request requires CLI/API/model controls, treat it as outside `.agents/skills/cli/imagegen` instead of using a hidden fallback.
- When no user or upstream size is specified, keep the skill-level output target at 2K. Built-in mode expresses this through prompt wording.
- When an upstream skill explicitly passes `resolution_target`, preserve it exactly as the current task target. A 4K parent handoff should not be treated as absent size.
- For many assets, one clean prompt per asset is more reliable than one overloaded prompt; run those per-asset specs through subagents parallel fan-out by default, capped at 10 active workers.
- Keep discarded variants out of project asset directories unless the user asks to keep them.
- When the target is a repo or project asset, copy the final file into the associated project directory before updating code, manifest, documentation, or canvas references.

## Transparent Output Heuristics

- Chroma-key removal works best for opaque objects with clear edges and no shadows.
- Avoid green key backgrounds for green subjects; magenta is the usual alternative.
- Hair, glass, smoke, liquids, glossy reflections, and soft shadows are likely true-transparency cases.
- The source keyed image and final alpha image are different artifacts; keep the final path unambiguous.

## External CLI/API Legacy Notes

- These notes are legacy/external material and do not define `.agents/skills/cli/imagegen` execution.
- Use `gpt-image-2` by default for a separate CLI/API workflow unless true transparency requires user-confirmed `gpt-image-1.5`.
- Omitted CLI `--size` should produce `2048x1152` for `gpt-image-2`; do not force this size onto legacy external models.
- Explicit 4K in a separate CLI/API workflow should map to `3840x2160` landscape or `2160x3840` portrait unless the handoff supplies another valid size.
- Do not set `input_fidelity` with `gpt-image-2`.
- Use dry-run for command validation only in that separate workflow when the user asks for a plan or when API/network readiness is uncertain.
