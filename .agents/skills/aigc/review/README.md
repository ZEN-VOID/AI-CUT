# aigc-review

`aigc-review` 是 `.agents/skills/aigc` 的包级 review 卫星技能包，用于 checkpoint、stage acceptance 与 package release 的结构化审计聚合。

## Directory Tree

```text
review/
├── agents/
│   └── openai.yaml
├── references/
│   └── dimensions/
├── scripts/
├── templates/
├── review/
├── steps/
├── knowledge-base/
├── types/
├── _shared/
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## Quick Entry

- 技能入口：`SKILL.md`
- 经验层：`CONTEXT.md`
- 规范分区：`references/`
- 六维审计细则：`references/dimensions/`
- 运行拓扑：`steps/review-workflow.md`
- 审计门禁：`review/review-gate.md`
- runner 兼容配置：`_shared/`

六个审计维度是父包内 governed dimension specs，不是独立对外受理的 Skill 2.0 包。父包负责完整 2.0 结构、aggregate gate 和最终 route；维度细则落在 `references/dimensions/`，维度经验回收到父级 `CONTEXT.md`。

常用执行入口：

```bash
python3 scripts/aigc_review_runner.py --help
```
