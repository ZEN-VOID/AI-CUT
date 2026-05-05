# 好好坏坏

`好好坏坏` 用于根据目标技能包某个任务环节输出中的好示例与坏示例，回看目标 skill 当前配置、任务要求和资料来源，分析好坏差异并回到源层调优。

## 快速入口

```text
使用 $haohao-huaihuai 调优 <target_skill>，对比 <good_examples> 和 <bad_examples>
```

## 目录树

```text
好好坏坏/
├── references/
│   └── good-bad-source-diagnosis.md
├── scripts/
│   └── README.md
├── templates/
│   └── output-template.md
├── review/
│   └── review-contract.md
├── steps/
│   └── good-bad-learning-workflow.md
├── knowledge-base/
│   └── good-bad-heuristics.md
├── types/
│   ├── type-map.md
│   ├── output-quality-contrast/
│   ├── source-fidelity-contrast/
│   ├── workflow-routing-contrast/
│   ├── template-schema-contrast/
│   └── review-gate-contrast/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── SKILL.md
└── CONTEXT.md
```

## Owner 摘要

- `SKILL.md`: 入口、输入、连续调度、源层路由、门禁和输出合同。
- `CONTEXT.md`: 好/坏对照学习的经验层。
- `references/`: 好/坏诊断维度、源层 owner 裁决和防过拟合规则。
- `steps/`: 思行一体的诊断、调优、验证闭环。
- `review/`: 质量门禁、过拟合检查和 reviewer 降级口径。
- `types/`: 不同好/坏差异类型的固定上下文包。
- `templates/`: good/bad contrast summary 输出模板。
- `scripts/`: 机械辅助边界说明。
- `agents/openai.yaml`: 产品侧入口元数据。
