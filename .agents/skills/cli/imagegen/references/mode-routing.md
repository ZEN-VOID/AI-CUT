# Mode Routing

This reference owns imagegen mode boundaries, intent detection, and fallback policy.

## Top-Level Modes

Imagegen has exactly two top-level execution paths:

- Default built-in tool mode: use built-in `image_gen` for normal generation, editing, variants, and simple transparent/cutout requests. This path does not require `OPENAI_API_KEY`.
- Explicit CLI fallback mode: use `scripts/image_gen.py` only when the user explicitly asks for CLI/API/model controls, or after the user explicitly confirms true model-native transparency through `gpt-image-1.5`.

Within CLI fallback, the script exposes:

- `generate`
- `edit`
- `generate-batch`

`generate-batch` is a CLI subcommand, not a top-level skill mode. The word `batch` alone is not CLI opt-in.

## Default Rules

- Use built-in `image_gen` by default for ordinary generation and editing.
- If the user does not specify resolution, target 2K output. In built-in mode, this is a prompt/delivery target rather than a hard tool parameter.
- Do not switch to CLI fallback merely for quality, size, output path, or batch wording.
- If the built-in tool fails or is unavailable, tell the user the CLI fallback exists and requires `OPENAI_API_KEY`; proceed only if the user explicitly asks for it.
- If the user explicitly asks for CLI mode, use the bundled `scripts/image_gen.py` workflow. Do not create one-off SDK runners.
- Never modify `scripts/image_gen.py`. If it lacks a capability, ask the user before doing anything else.
- Never silently switch from built-in `image_gen` or CLI `gpt-image-2` to CLI `gpt-image-1.5`.

## When To Use Imagegen

- Generate a new image, including concept art, product shots, covers, website hero images, textures, sprites, UI mockups, or infographics.
- Generate a new image using one or more reference images for style, composition, mood, subject identity, or scene guidance.
- Edit an existing image: inpainting, background replacement, object removal, compositing, lighting/weather transformation, style transfer, or transparent cutout.
- Produce many bitmap assets or variants for one task.

## When Not To Use Imagegen

- Extending or matching existing SVG/vector icon sets, logos, or illustration libraries inside the repo.
- Creating deterministic diagrams, wireframes, or small UI graphics better produced directly in SVG, HTML/CSS, canvas, or code.
- Making a small local asset edit when the source is already in an editable native format.
- Any task where the user clearly wants code-native output instead of generated bitmap output.

## Intent Decision Tree

Ask two separate questions:

1. Is this a new image or an edit of an existing image?
2. Is this one asset, many distinct assets, or variants of one prompt?

Intent rules:

- If the user wants to modify an existing image while preserving parts of it, treat the request as `edit`.
- If images are supplied only as style, composition, mood, or subject references, treat the request as `generate_with_references`.
- If no image is supplied, treat the request as `generate`.
- For edits, preserve invariants aggressively and save non-destructively by default.

Built-in edit semantics:

- Built-in edit mode is for images visible in the conversation context, such as attached images, generated images, or local images first inspected with `view_image`.
- If the user wants to edit a local file with the built-in tool, inspect it first so it is available in context.
- Do not promise arbitrary filesystem-path editing through the built-in tool.
- If direct file-path control, masks, or explicit CLI parameters are required, use CLI fallback only after explicit user opt-in.

Execution strategy:

- In built-in mode, make one `image_gen` call per distinct asset or variant.
- In CLI fallback mode, omitted `--size` resolves to `2048x1152` for the default `gpt-image-2` model; use `generate-batch` only after explicit CLI/API/model opt-in.
- Do not use `n` as a substitute for distinct prompts. `n` is for variants of one prompt.
