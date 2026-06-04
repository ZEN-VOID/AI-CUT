# aigc-learn

`aigc-learn` 是 AIGC 技能树的学习型卫星入口，用于把外部学习对象吸收为可审计、可同步、可落盘的技能改进。

## Directory Tree

```text
learn/
├── agents/
├── guardrails/
├── knowledge-base/
├── references/
├── review/
├── scripts/
├── templates/
├── types/
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

1. 加载 `SKILL.md + CONTEXT.md`。
2. 读取 `types/type-map.md` 并加载命中的学习对象类型包。
3. 视频类复杂对象加载 `references/video-learning-contract.md`；书籍和超长上下文加载 `references/book-long-context-learning-contract.md`。
4. 执行型改进按 `SKILL.md#Thinking-Action Node Map`：source digest → target_skill_map → gap_matrix → landing_set → writeback → audit。
5. **完成标志**：`audit_result: pass` 或 `pass_with_followups` + `changed_files` 已验证 = **任务完成**。
6. **报告只是副产物**：只有用户明确要求或需要审计追溯时才生成报告；默认不需要报告。
