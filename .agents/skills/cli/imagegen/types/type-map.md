# Imagegen Type Map

This file owns request classification, use-case slugs, and prompt schema. It does not own execution steps.

## Type Profile

| variable | allowed values | meaning |
| --- | --- | --- |
| `intent` | `generate`, `edit`, `generate_with_references` | Whether the user wants a new image or a modification of an existing image |
| `asset_count` | `single`, `variants`, `multiple_distinct` | Determines call strategy |
| `background_need` | `opaque`, `transparent_chroma_key`, `true_transparency_confirmed` | Determines transparency route |
| `execution_mode` | `built_in`, `cli_confirmed` | Whether built-in `image_gen` or CLI fallback is allowed |
| `persistence` | `preview_only`, `project_bound`, `user_named_destination` | Determines save-path handling |
| `resolution_target` | `2k_default`, `user_specified`, `model_limited_default` | Determines prompt/payload resolution handling |
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
| `asset_count=multiple_distinct` | one prompt/call per asset | `steps/execution-workflow.md` | each requested deliverable exists |
| `background_need=transparent_chroma_key` | generate keyed source then remove key | `references/transparent-background.md` | alpha channel and transparent corners |
| `background_need=true_transparency_confirmed` | CLI fallback allowed | `references/cli.md`, `references/image-api.md` | confirmation and API-key readiness |
| `persistence=project_bound` | copy final to workspace | `references/output-persistence.md` | no project reference to `$CODEX_HOME/*` only |
| `resolution_target=2k_default` | add 2K target to prompt or CLI payload | `references/prompting.md`, `references/cli.md` | output/payload records 2K intent |
| `risk_profile=text_heavy` | quote exact text and inspect output | `references/prompting.md` | verbatim text review |

## Type Gate

Before execution, state or infer:

- request use-case slug;
- intent;
- execution mode;
- output persistence;
- resolution target;
- risk profile.

If any of these cannot be reasonably inferred and affects correctness, ask a concise question before generating.
