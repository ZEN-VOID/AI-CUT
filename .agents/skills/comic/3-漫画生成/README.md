# 漫画生成

Skill 2.0 package for generating one comic `page-group` from `nine_blade_comic_prompts.v1` JSON through `.agents/skills/cli/imagegen` built-in `image_gen` mode.

## Layout

```text
3-漫画生成/
├── references/
├── scripts/
├── templates/
├── review/
├── steps/
├── knowledge-base/
├── types/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## Quick Commands

```bash
python3 .agents/skills/comic/3-漫画生成/scripts/prepare_builtin_imagegen_comic_generation.py --self-test
```

```bash
python3 .agents/skills/comic/3-漫画生成/scripts/prepare_builtin_imagegen_comic_generation.py \
  projects/comic/<项目名>/2-九刀流漫画提示词/page-group-01-nine_blade_comic_prompts.json
```

The planner writes `imagegen_handoff_plan.json`, `imagegen_prompt_set.json`, per-page prompt files, and `comic_generation_report.json`. It does not call built-in `image_gen`; actual generation is done by the agent/tool path and then copied into the project output directory.

Legacy external CLI usage is intentionally separate:

```bash
python3 .agents/skills/comic/3-漫画生成/scripts/run_legacy_imagegen_cli_comic_generation.py \
  projects/comic/<项目名>/2-九刀流漫画提示词/page-group-01-nine_blade_comic_prompts.json \
  --execute \
  --ack-legacy-cli
```

Legacy CLI execution requires `OPENAI_API_KEY` and is not the default `comic-generation` route.
