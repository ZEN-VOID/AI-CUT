# A.分镜画面

`A.分镜画面` 是 `5-Image` 阶段的单帧画面融合技能包，把原 `分镜帧`、`2-参照引用`、`3-图像生成` 三段能力收束为一个可路由入口。

## Directory Tree

```text
A.分镜画面/
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
├── TODO.md
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## Quick Entry

- 入口合同：`SKILL.md`
- 经验层：`CONTEXT.md`
- 执行拓扑：`steps/frame-image-workflow.md`
- 单帧蒸馏完整方法：`references/request-distillation.md`
- 旧包迁移追踪：`references/legacy-upgrade-migration-matrix.md`
- 输出模板：`templates/output-template.md`

## Compatibility

原三个技能包暂不移除。本包默认写入既有 runtime 槽位，不创建新的项目输出根。
