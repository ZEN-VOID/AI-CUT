# 北冥神功

`北冥神功` 用于把外部升级点吸收到现有 skill。它先研究目标 skill 当前配置与技能组上下文，再裁决升级点应落在哪些载体，并完成同步、验证和学习沉淀。

## 快速入口

```text
使用 $beiming-skill-learning 升级 <target_skill>，吸收 <upgrade_points>
```

## 目录树

```text
北冥神功/
├── references/
│   ├── skill-2.0-upgrade-migration-matrix.md
│   └── upgrade-point-absorption-map.md
├── scripts/
│   └── README.md
├── templates/
│   ├── absorption-summary.template.md
│   └── output-template.md
├── review/
│   └── review-contract.md
├── steps/
│   └── skills-update-absorption-workflow.md
├── knowledge-base/
│   └── skills-update-heuristics.md
├── types/
│   └── upgrade-point-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── SKILL.md
└── CONTEXT.md
```

## Owner 摘要

- `SKILL.md`: 入口、输入、路由、门禁和输出合同。
- `CONTEXT.md`: 吸收升级的经验层。
- `references/`: 升级点吸收矩阵与本次 Skill 2.0 迁移矩阵。
- `steps/`: 思行一体的执行拓扑。
- `review/`: reviewer gate、降级规则和验收 verdict。
- `types/`: 升级点类型画像。
- `templates/`: absorption summary 和输出报告模板。
- `scripts/`: 机械辅助脚本边界说明。
- `agents/openai.yaml`: 产品侧入口元数据。
