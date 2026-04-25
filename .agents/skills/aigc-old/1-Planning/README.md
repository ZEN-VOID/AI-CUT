# aigc 1-Planning

`aigc-planning` 是 AIGC 规划阶段的单一 Skill 2.0 包。原 `1-分集`、历史 `2-格式`、`3-分组` 三个子 skill 已融合为父包内的 `episode_split`、`script_format`、`grouping` 三种 mode；其中 `script_format` 的业务显示名调整为 `2-剧本`，runtime 路径仍保留 `2-格式/`。

## Directory Tree

```text
1-Planning/
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
├── README.md
└── skill_manifest.json
```

## Quick Entry

- 入口 skill：`$aigc-planning`
- 分集细则：`references/episode-splitter-contract.md`
- 格式细则：`references/script-format-contract.md`
- 分组细则：`references/grouping-contract.md`
- 共享 I/O：`references/planning-io-contract.md`

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/aigc/1-规划
python3 scripts/skill_context_audit.py --root .agents/skills/aigc/1-规划 --strict
python3 scripts/aigc_skill_audit.py --strict
```
