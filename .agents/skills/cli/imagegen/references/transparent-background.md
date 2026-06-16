# Transparent Background Workflow

This reference owns transparent and cutout image handling.

## Default Position

Transparent-image requests still use built-in `image_gen` first. The built-in tool does not expose a true transparent-background parameter, so the default path is:

1. Generate the subject on a perfectly flat chroma-key background.
2. Copy the selected source image into the workspace or `tmp/imagegen/`.
3. Remove the key color locally with the installed helper.
4. Validate alpha before using the result.

Do not use CLI `gpt-image-1.5 --background transparent --output-format png` from this skill. If built-in chroma-key cannot satisfy the request, report the limitation as `blocked_non_builtin_route`.

## Chroma-Key Prompt

Use `#00ff00` by default. Use `#ff00ff` for green subjects. Avoid key colors that may appear in the subject.

```text
Create the requested subject on a perfectly flat solid #00ff00 chroma-key background for background removal.
The background must be one uniform color with no shadows, gradients, texture, reflections, floor plane, or lighting variation.
Keep the subject fully separated from the background with crisp edges and generous padding.
Do not use #00ff00 anywhere in the subject.
No cast shadow, no contact shadow, no reflection, no watermark, and no text unless explicitly requested.
```

## Local Alpha Removal

Use the installed helper path, which is valid after the skill is installed into Codex:

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/scripts/remove_chroma_key.py" \
  --input <source> \
  --out <final.png> \
  --auto-key border \
  --soft-matte \
  --transparent-threshold 12 \
  --opaque-threshold 220 \
  --despill
```

If a thin key-color fringe remains, retry once with `--edge-contract 1`. Use `--edge-feather 0.25` only when the edge is visibly stair-stepped and the subject is not shiny or reflective.

## Validation Gate

Before delivery, verify:

- output has an alpha channel;
- corners/background are transparent;
- subject coverage is plausible;
- no obvious key-color fringe remains;
- no required subject detail or exact text was removed;
- final alpha PNG/WebP is persisted into the workspace when project-bound.

## Native Transparency Limitation

Report a blocker instead of switching tools when:

- the user asks for true/native transparency;
- chroma-key removal fails validation;
- the subject is complex: hair, fur, feathers, smoke, glass, liquids, translucent materials, reflective objects, soft shadows, or realistic product grounding;
- all practical key colors conflict with the subject.

Use this blocker wording:

```text
This likely needs true native transparency. `.agents/skills/cli/imagegen` is defined as the built-in `image_gen` route only, so I cannot switch to CLI/API transparency from this skill. I can attempt the built-in chroma-key workflow or stop here.
```

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Did transparent output use built-in chroma-key and validate alpha without hidden native transparency fallback? | Missing alpha, opaque corners, key fringe, or CLI/API transparency fallback fails | `FAIL-IMG-ROUTE-TRANSPARENT` | `SKILL.md#thinking-action-node-map` / `N6-INSPECT` | alpha validation notes, final path, and limitation report if blocked |
