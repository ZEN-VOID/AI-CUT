# aigc-review

`aigc-review` 是 `.agents/skills/aigc` 的包级 review 卫星技能包，用于 checkpoint、stage acceptance 与 package release 的结构化审计聚合。

## Directory Tree

```text
review/
├── agents/
│   └── openai.yaml
├── references/
├── scripts/
├── templates/
├── review/
├── steps/
├── knowledge-base/
├── types/
├── _shared/
├── 规划与种子兑现/
├── 分镜执行连续性/
├── 设计对位/
├── 图像交付就绪/
├── 视频交付就绪/
├── 治理闭环/
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## Quick Entry

- 技能入口：`SKILL.md`
- 经验层：`CONTEXT.md`
- 规范分区：`references/`
- 运行拓扑：`steps/review-workflow.md`
- 审计门禁：`review/review-gate.md`
- runner 兼容配置：`_shared/`

六个中文维度目录是父包内 governed dimension modules，不是独立对外受理的 Skill 2.0 包。父包负责完整 2.0 结构、aggregate gate 和最终 route；维度目录只提供局部判据与经验层。

常用执行入口：

```bash
python3 scripts/aigc_review_runner.py --help
```
