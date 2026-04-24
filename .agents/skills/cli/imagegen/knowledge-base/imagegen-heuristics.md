# Imagegen Heuristics

This file stores stable reusable practices for imagegen. It does not override `SKILL.md`.

## Prompt Heuristics

- If the user prompt is detailed, preserve it and normalize structure only.
- If the user prompt is generic, add only details that materially improve output quality.
- For people and identity-sensitive edits, repeat invariants in every follow-up prompt.
- For in-image text, quote exact text and forbid extra words.
- For layouts, name the intended asset use so the model can choose the right polish and whitespace.

## Execution Heuristics

- Built-in `image_gen` should feel frictionless. Avoid CLI unless the user clearly wants the extra controls.
- When no size is specified, keep the skill-level output target at 2K. Built-in mode expresses this through prompt wording; CLI `gpt-image-2` resolves the omitted size to `2048x1152`.
- For many assets, one clean prompt per asset is more reliable than one overloaded prompt.
- Keep discarded variants out of project asset directories unless the user asks to keep them.
- When the target is a repo asset, copy the final file into the repo before updating code or documentation references.

## Transparent Output Heuristics

- Chroma-key removal works best for opaque objects with clear edges and no shadows.
- Avoid green key backgrounds for green subjects; magenta is the usual fallback.
- Hair, glass, smoke, liquids, glossy reflections, and soft shadows are likely true-transparency cases.
- The source keyed image and final alpha image are different artifacts; keep the final path unambiguous.

## CLI Fallback Heuristics

- Treat CLI fallback as a user-confirmed provider path.
- Use `gpt-image-2` by default for CLI generation/editing unless true transparency requires user-confirmed `gpt-image-1.5`.
- Omitted CLI `--size` should produce `2048x1152` for `gpt-image-2`; do not force this size onto legacy fallback models.
- Do not set `input_fidelity` with `gpt-image-2`.
- Use dry-run for command validation when the user asks for a plan or when API/network readiness is uncertain.
