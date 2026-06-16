# Imagegen Type Map

This file owns request classification, use-case slugs, and prompt schema. It does not own execution steps.

## Package Index

| package | purpose | load_when | owner_gate |
| --- | --- | --- | --- |
| `types/request-profile.md` | Canonical type-profile fields, routing examples, and classification checklist | Any imagegen invocation that needs request classification | `N2-TYPE` in `SKILL.md` |

## Default Package Rule

Load `types/request-profile.md` whenever `types/type-map.md` is loaded for execution. `types/` may define classification vocabulary and reusable examples, but it must return a `type_profile` to `SKILL.md` and must not own execution nodes, provider choice, completion gates, or output paths.

## Loading Flow

1. `SKILL.md` selects `N2-TYPE`.
2. `types/type-map.md` loads this package index and `types/request-profile.md`.
3. The agent builds one `type_profile` with intent, asset count, batch execution, background need, execution mode, persistence, resolution target, and risk profile.
4. `type_profile` returns to `N3-MODE`; no type package calls tools or writes final outputs.

## Type Profile

| variable | allowed values | meaning |
| --- | --- | --- |
| `intent` | `generate`, `edit`, `generate_with_references` | Whether the user wants a new image or a modification of an existing image |
| `asset_count` | `single`, `variants`, `multiple_distinct` | Determines call strategy |
| `batch_execution` | `subagents_parallel_default`, `main_thread_serial_user_requested`, `not_applicable` | Determines whether batch work fans out to subagents or remains serial |
| `background_need` | `opaque`, `transparent_chroma_key`, `true_transparency_confirmed` | Determines transparency route |
| `execution_mode` | `built_in`, `unsupported_non_builtin` | Whether the request can run through built-in `image_gen`; CLI/API fallback is not part of this skill |
| `persistence` | `preview_only`, `project_bound`, `user_named_destination` | Determines save-path handling |
| `resolution_target` | `2k_default`, `explicit_user_or_upstream`, `model_limited_default` | Determines built-in prompt/delivery resolution wording |
| `risk_profile` | `text_heavy`, `identity_sensitive`, `mask_sensitive`, `style_sensitive`, `low_risk` | Determines review intensity |

## Use-Case Taxonomy

Generate:

- `photorealistic-natural`: candid/editorial lifestyle scenes with real texture and natural lighting.
- `product-mockup`: product/packaging shots, catalog imagery, merch concepts.
- `ui-mockup`: app/web interface mockups and wireframes; specify fidelity.
- `infographic-diagram`: diagrams and infographics with structured layout and text.
- `scientific-educational`: classroom explainers, scientific diagrams, and learning visuals.
- `ads-marketing`: campaign concepts and ad creatives with audience, brand position, scene, and exact tagline/copy.
- `productivity-visual`: slides, charts, workflows, and data-heavy business visuals.
- `logo-brand`: logo/mark exploration, vector-friendly.
- `illustration-story`: comics, children's book art, and narrative scenes.
- `stylized-concept`: style-driven concept art, 3D/stylized renders.
- `historical-scene`: period-accurate scenes.

Edit:

- `text-localization`: translate or replace in-image text while preserving layout.
- `identity-preserve`: try-on or person-in-scene work that locks face, body, pose, hair, and expression.
- `precise-object-edit`: remove or replace a specific element.
- `lighting-weather`: change time of day, season, weather, or atmosphere only.
- `background-extraction`: transparent background or clean cutout.
- `style-transfer`: apply reference style while changing subject or scene.
- `compositing`: merge or insert subjects across images with matched lighting and perspective.
- `sketch-to-render`: convert drawing or line art to a rendered result while preserving layout.

## Shared Prompt Schema

Use only the lines that help. This schema is prompt scaffolding, not CLI flags.

```text
Use case: <taxonomy slug>
Asset type: <where the asset will be used>
Primary request: <user's main prompt>
Input images: <Image 1: role; Image 2: role>
Scene/backdrop: <environment>
Subject: <main subject>
Style/medium: <photo/illustration/3D/etc>
Composition/framing: <wide/close/top-down; placement>
Lighting/mood: <lighting + mood>
Color palette: <palette notes>
Materials/textures: <surface details>
Text (verbatim): "<exact text>"
Constraints: <must keep/must avoid>
Avoid: <negative constraints>
```

## Mapping Matrix

| type signal | step impact | reference impact | review impact |
| --- | --- | --- | --- |
| `intent=edit` | load visible edit target and repeat invariants | `references/mode-routing.md`, `references/prompting.md` | preserve unchanged regions |
| `asset_count=multiple_distinct` | one prompt/call per asset; default to subagents parallel fan-out capped at 10 | `SKILL.md#thinking-action-node-map` | each requested deliverable exists and batch execution shape is recorded |
| `asset_count=variants` | one prompt/call per explicit variant; default to subagents parallel fan-out capped at 10 when more than one output is requested | `SKILL.md#thinking-action-node-map` | each requested variant exists or blocker is reported |
| `batch_execution=subagents_parallel_default` | create per-asset task specs and dispatch subagents, maximum concurrency 10 | `SKILL.md#thinking-action-node-map` | no more than 10 concurrent workers; parent gathers results |
| `batch_execution=main_thread_serial_user_requested` | run the same per-asset task specs one by one in the main thread | `SKILL.md#thinking-action-node-map` | explicit user request for serial execution is recorded |
| `background_need=transparent_chroma_key` | generate keyed source then remove key | `references/transparent-background.md` | alpha channel and transparent corners |
| `background_need=true_transparency_confirmed` | unsupported by this skill's single built-in route; use chroma-key path or report blocker | `references/transparent-background.md`, `references/mode-routing.md` | no hidden CLI/API fallback |
| `persistence=project_bound` | copy final to workspace | `references/output-persistence.md` | no project reference to `$CODEX_HOME/*` only |
| `resolution_target=2k_default` | add 2K target to built-in prompt/delivery wording | `references/prompting.md` | prompt/report records 2K intent |
| `resolution_target=explicit_user_or_upstream` | preserve the explicit target, including 4K handoffs from parent skills, in built-in prompt/delivery wording | `references/prompting.md` | prompt/report records the explicit target |
| `risk_profile=text_heavy` | quote exact text and inspect output | `references/prompting.md` | verbatim text review |

## Type Gate

Before execution, state or infer:

- request use-case slug;
- intent;
- execution mode;
- output persistence;
- batch execution mode when `asset_count` is not `single`;
- resolution target;
- risk profile.

Resolution source rules:

- User wording such as `4K`, `3840x2160`, `2160x3840`, or an upstream handoff field such as `resolution_target: 4K` sets `resolution_target=explicit_user_or_upstream`.
- `explicit_user_or_upstream` has priority over the skill-level 2K default and must be carried into built-in prompts, reports, and review notes.
- If no user or upstream resolution is present, use `resolution_target=2k_default`.

If any of these cannot be reasonably inferred and affects correctness, ask a concise question before generating.
