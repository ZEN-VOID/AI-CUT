# aigc 8-摄影

`8-摄影` 将 `projects/aigc/<项目名>/7-分镜/第N集.md` 或用户指定分镜稿升级为逐分镜摄影·运镜稿。

## Directory Tree

```text
8-摄影/
├── SKILL.md
├── CONTEXT.md
├── CHANGELOG.md
├── README.md
├── test-prompts.json
├── agents/
│   └── openai.yaml
├── references/
│   ├── ai-video-prompt-execution-contract.md
│   ├── camera-movement-emotion-contract.md
│   ├── dynamic-lens-language-contract.md
│   ├── intra-shot-transition-contract.md
│   ├── peak-shot-language-contract.md
│   ├── shot-continuity-contract.md
│   ├── shot-planning-integration-contract.md
│   ├── source-detail-incremental-fusion-contract.md
│   └── transition-design-contract.md
└── scripts/
    └── README.md
```

## Default Inputs

- `projects/aigc/<项目名>/7-分镜/第N集.md`
- `projects/aigc/<项目名>/3-美学/画面基调/全局风格协议.md`
- `projects/aigc/<项目名>/3-美学/摄影风格/摄影风格协议.md`

用户指定文稿时优先指定文稿，并在执行报告记录 `source_override=true`。

## Output

- 摄影稿：`projects/aigc/<项目名>/8-摄影/第N集.md`
- 执行报告：`projects/aigc/<项目名>/8-摄影/执行报告.md`

普通格式固定为：

```text
分镜1（0-2秒）：原有内容。镜头从具体机位和角度进入，说明景别/镜头类型、运动方式、运动路径、速度曲线、如何沿既有构图轴线或空间层次运动，以及景深与对焦行为。
```

`8-摄影` 负责定摄影机如何使用 `7-分镜` 的既有空间：机位从哪里进入、沿哪条轴线运动、是否穿过前景/绕开遮挡/压向后景、速度怎么变，以及景深和对焦如何处理。它可以引用空间层次，但不重新发明空间布局。

一镜到底时以画面点为单位输出连续组合运镜：

```text
一镜到底运镜（覆盖分镜A-B，N-N秒）：从分镜A的既有起始状态帧和具体机位/角度进入，连续串联分镜A-B，说明景别/镜头类型、运动方式、如何沿既有构图轴线或空间层次推进、如何使用既有前中后景或遮挡关系、速度曲线与停点、景深策略与对焦/拉焦/转焦接力，以及跨分镜交出点。
```

内部计划必须区分摄影机运动、焦距变化和透视效果；必须用 `spatial_movement_action_map` 回指 7 的既有空间，并用 `focus_transition_map` 说明起止焦点、对焦模式、景深策略和必须保持可读的信息。本技能不生成图像 prompt、视频 prompt、设备参数或剪辑方案。
