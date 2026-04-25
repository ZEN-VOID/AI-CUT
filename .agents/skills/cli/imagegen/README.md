# imagegen

Skill 2.0 package for generating and editing raster images through the built-in `image_gen` tool by default, with an explicit CLI/API fallback.

## Directory Tree

```text
imagegen/
├── assets/
├── agents/
│   └── openai.yaml
├── knowledge-base/
│   └── imagegen-heuristics.md
├── references/
│   ├── cli.md
│   ├── codex-network.md
│   ├── image-api.md
│   ├── mode-routing.md
│   ├── output-persistence.md
│   ├── prompting.md
│   ├── sample-prompts.md
│   └── transparent-background.md
├── review/
│   └── review-contract.md
├── scripts/
│   ├── image_gen.py
│   └── remove_chroma_key.py
├── steps/
│   └── execution-workflow.md
├── templates/
│   └── output-template.md
├── types/
│   └── type-map.md
├── CHANGELOG.md
├── CONTEXT.md
├── LICENSE.txt
├── README.md
└── SKILL.md
```

## Quick Entry

- Load `SKILL.md` and `CONTEXT.md` together.
- Use built-in `image_gen` for normal image generation and editing.
- Use `references/transparent-background.md` for simple transparent/cutout requests.
- Use `scripts/image_gen.py` only after explicit CLI/API/model opt-in.
- Run the Skill 2.0 validator after structural changes.

## CLI Fallback

The CLI is an opt-in fallback:

```bash
python scripts/image_gen.py generate --prompt "A clean product photo" --out output/imagegen/product.png --dry-run
```

Live CLI calls require `OPENAI_API_KEY` and network access.
