# aigc 3-运动

`3-运动` 在 `2-编导` 与 `4-摄影` 之间强化角色动作的空间连续性。默认读取 `projects/aigc/<项目名>/2-编导/第N集.md`，输出 `projects/aigc/<项目名>/3-运动/第N集.md`。同一分镜组或连续动作段会尽量统一最佳参照系，并在报告中留下 `group_reference_profile`。

## Directory Tree

```text
3-运动/
├── guardrails/
│   └── guardrails-contract.md
├── references/
│   ├── motion-five-elements-contract.md
│   ├── source-preservation-contract.md
│   └── temporal-continuity-contract.md
├── scripts/
│   ├── README.md
│   └── validate_motion_enrichment.py
├── templates/
│   ├── episode-motion.template.md
│   └── output-template.md
├── review/
│   └── review-contract.md
├── steps/
│   └── motion-workflow.md
├── knowledge-base/
│   └── motion-heuristics.md
├── types/
│   ├── type-map.md
│   ├── source/
│   │   ├── arbitrary-text.md
│   │   └── upstream-writing-directing.md
│   ├── motion/
│   │   └── character-action.md
│   └── continuity/
│       └── adjacent-frame-state.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
└── SKILL.md
```

## Quick Entry

- 项目逐集：使用 `$aigc-motion-enrichment` 处理 `projects/aigc/<项目名>/2-编导/第N集.md`。
- 任意来源：显式传入 source 文件和目标输出路径。
- 机械检查：`python3 scripts/validate_motion_enrichment.py projects/aigc/<项目名>/3-运动/第N集.md`。
