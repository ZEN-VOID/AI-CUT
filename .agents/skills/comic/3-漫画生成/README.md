# 漫画生成

Skill 2.0 package for generating one comic `page-group` from `nine_blade_comic_prompts.v1` JSON through `.agents/skills/cli/imagegen`.

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
python3 .agents/skills/comic/3-漫画生成/scripts/run_imagegen_cli_comic_generation.py --self-test
```

```bash
python3 .agents/skills/comic/3-漫画生成/scripts/run_imagegen_cli_comic_generation.py \
  projects/comic/<项目名>/2-九刀流漫画提示词/page-group-01-nine_blade_comic_prompts.json \
  --dry-run
```

```bash
python3 .agents/skills/comic/3-漫画生成/scripts/run_imagegen_cli_comic_generation.py \
  projects/comic/<项目名>/2-九刀流漫画提示词/page-group-01-nine_blade_comic_prompts.json \
  --execute
```

`--execute` requires `OPENAI_API_KEY`. Dry-run does not.
