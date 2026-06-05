# lesson-repair

`lesson-repair` 是 lesson 工作流的 source-first 修复卫星技能。它用于诊断并回接课程定位、知识模型、目标评价、课程架构、课时正文、活动测评、视觉交互、共享内容模型和 DOC/PPT/HTML 三端漂移。

## Directory Tree

```text
repair/
├── SKILL.md
├── CONTEXT.md
├── README.md
├── CHANGELOG.md
├── test-prompts.json
└── agents/
    └── openai.yaml
```

## Runtime Entry

- 主入口：`SKILL.md`
- 经验层：`CONTEXT.md`
- 产品入口元数据：`agents/openai.yaml`
- 评估 prompts：`test-prompts.json`

本包当前只启用 core layout，不创建 optional modules，也不创建 `steps/`。若未来启用外部模块，必须先在 `SKILL.md` 的 Module Loading Matrix 和 Module Trigger Matrix 中授权。

## Boundary

本技能只拥有诊断、影响图、source owner 判定、repair brief、写回顺序和审计汇流权。阶段主稿仍由 `1-课程定位` 到 `8-多端交付生成` 及 DOC/PPT/HTML 叶子 owning skill 写回。
