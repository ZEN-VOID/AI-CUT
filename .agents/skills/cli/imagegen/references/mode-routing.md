# Mode Routing

This reference owns imagegen mode boundaries and intent detection for the built-in `image_gen` tool.

## Top-Level Modes

Imagegen has exactly one top-level execution path:

- Built-in tool mode: use built-in `image_gen` for generation, editing, variants, and simple transparent/cutout requests. This path does not require `OPENAI_API_KEY`.

`scripts/image_gen.py`, Image API calls, and `generate-batch` are not execution modes of `.agents/skills/cli/imagegen`. If a user explicitly asks for local/API/CLI execution, treat that as a request for a different route, not as this skill's fallback.

## Default Rules

- Use built-in `image_gen` for generation and editing.
- If neither the user nor an upstream skill handoff specifies resolution, target 2K output. In built-in mode, this is a prompt/delivery target rather than a hard tool parameter.
- If the user or upstream skill handoff explicitly specifies resolution, preserve that target. For example, `resolution_target: 4K` from a parent skill must remain 4K and must not be replaced by the 2K default.
- Do not switch to `scripts/image_gen.py`, Image API calls, libTV, nano-banana, Photoshop, or any other provider from this skill.
- If the built-in tool fails or is unavailable, report that `.agents/skills/cli/imagegen` cannot execute the request under its single-tool contract.
- If the user explicitly asks for CLI/API mode, state that this is outside `.agents/skills/cli/imagegen` as now defined and requires a separately named tool or workflow.
- Never modify or invoke `scripts/image_gen.py` as part of this skill.

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
- If direct file-path control, masks, or hard CLI/API parameters are required, report that built-in `image_gen` cannot guarantee that workflow through this skill.

Execution strategy:

- Make one built-in `image_gen` call per distinct asset or variant.
- Explicit 4K is carried in the prompt/delivery wording because the built-in tool has no hard size parameter.
- Do not use `n` as a substitute for distinct prompts. `n` is for variants of one prompt.

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Did the selected route match the request type and built-in-only boundary? | Wrong mode, hidden fallback, or unsupported direct-path promise fails | `FAIL-IMG-ROUTE-UNSUPPORTED` | `SKILL.md#type-routing-matrix` / `N3-MODE` | `type_profile`, `mode_decision`, and blocker text when applicable |
