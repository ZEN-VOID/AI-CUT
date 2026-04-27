# 九刀流漫画提示词

`comic-nine-blade-prompts` 将上游 `第N组.md` 或 raw source 转换为组级 `nine_blade_comic_prompts.v1` JSON。每个 group 可被 3 号 `.agents/skills/cli/imagegen` 执行层投影为 9 个单页生图 job。

## Directory Tree

```text
2-九刀流漫画提示词/
├── agents/
│   └── openai.yaml
├── knowledge-base/
│   └── comic-prompt-heuristics.md
├── references/
│   └── nine-blade-prompt-contract.md
├── review/
│   └── review-contract.md
├── scripts/
│   └── validate_nine_blade_prompt_json.py
├── steps/
│   ├── nine-blade-workflow.md
│   └── source-routing-and-handoff.md
├── templates/
│   ├── nine-blade-comic-prompts.schema.json
│   ├── nine-blade-template.json
│   └── output-template.md
├── types/
│   ├── 漫画/
│   │   ├── 少年战斗冒险/
│   │   ├── 推理悬疑/
│   │   └── ...
│   └── type-map.md
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## Quick Entry

1. 读取 `SKILL.md + CONTEXT.md`。
2. 读取 `steps/source-routing-and-handoff.md`，锁定 grouped/raw/multi-episode/poster-aware mode。
3. 读取 `types/type-map.md` 并加载命中的 `types/漫画/<题材>/` 题材包。
4. 按需加载 `steps/nine-blade-workflow.md`、`references/nine-blade-prompt-contract.md`、`knowledge-base/comic-prompt-heuristics.md`。
5. 复制 `templates/nine-blade-template.json` 的结构，由 LLM 填入具体创作内容。
6. 运行校验：

```bash
python3 .agents/skills/comic/2-九刀流漫画提示词/scripts/validate_nine_blade_prompt_json.py path/to/page-group-01-nine_blade_comic_prompts.json
```

## Skill 2.0 Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/comic/2-九刀流漫画提示词
```
