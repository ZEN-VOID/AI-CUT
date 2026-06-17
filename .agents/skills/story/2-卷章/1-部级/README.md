# story-plan-book-level

`story-plan-book-level` 是 `2-卷章` 的部级规划子技能，负责生成或修订 `projects/story/<项目名>/2-卷章/整体规划.md`，并锁定整书级悬念总设计。

## Directory Tree

```text
1-部级/
├── guardrails/
│   └── guardrails-contract.md
├── references/
│   ├── book-level-output-contract.md
│   ├── legacy-upgrade-migration-matrix.md
│   └── book-rhythm-save-the-cat.md
├── scripts/
│   └── README.md
├── templates/
│   ├── output-template.md
│   └── overall-planning.template.md
├── review/
│   └── review-contract.md
├── knowledge-base/
│   └── book-level-planning-heuristics.md
├── types/
│   ├── type-map.md
│   └── book-level-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

1. 读取 `SKILL.md + CONTEXT.md`。
2. 回读父层 `../SKILL.md + ../CONTEXT.md` 和共享 planning 合同。
3. 按 `Module Loading Matrix` 与 `Module Trigger Matrix` 加载 `references/`、`types/`、`review/` 与模板；执行节点以 `SKILL.md` 的 `Thinking-Action Node Map` 为唯一真源。
4. 生成或修订 `projects/story/<项目名>/2-卷章/整体规划.md`，其中必须包含 `整部悬念总设计` 与 `整书悬念池`。
5. 使用 `review/review-contract.md` 确认可交给 `2-卷级`。
6. 使用 `guardrails/guardrails-contract.md` 校验运行时边界。

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/story/2-卷章/1-部级 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/story/2-卷章/1-部级 --mode delivery
python3 .agents/skills/story/2-卷章/scripts/validate_planning_outputs.py --help
python3 scripts/skill_context_audit.py --root .agents/skills/story/2-卷章/1-部级 --strict
```
