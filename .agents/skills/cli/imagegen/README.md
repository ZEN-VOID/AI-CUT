# imagegen

Skill 2.0 package for generating and editing raster images through the built-in `image_gen` tool. In this skill, `imagegen` means the built-in `image_gen` tool only.

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
├── templates/
│   └── output-template.md
├── test-prompts.json
├── types/
│   ├── request-profile.md
│   └── type-map.md
├── CHANGELOG.md
├── CONTEXT.md
├── LICENSE.txt
├── README.md
└── SKILL.md
```

## Quick Entry

- Load `SKILL.md` and `CONTEXT.md` together.
- Use built-in `image_gen` for image generation and editing.
- Keep the executable thinking-action node map in `SKILL.md`; this package no longer uses a `steps/` directory.
- For batch/multiple image tasks, default to subagents parallel fan-out with maximum concurrency 10; use main-thread one-by-one execution only when the user explicitly requests it.
- Use `references/transparent-background.md` for simple transparent/cutout requests.
- Transfer project-bound outputs into the associated project directory before completion.
- Do not use `scripts/image_gen.py` as an execution route for this skill.
- Run the Skill 2.0 validator and smoke test after structural changes:

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/cli/imagegen --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/cli/imagegen --mode delivery
```

## Non-Built-In Scripts

`scripts/image_gen.py` remains in the directory for historical compatibility and explicit external workflows, but it is not part of `.agents/skills/cli/imagegen` execution after the single-tool boundary update.

If a task requires API keys, direct filesystem-path editing, masks, hard model parameters, or local CLI execution, route it outside this skill instead of treating it as imagegen fallback.
