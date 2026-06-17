# aigc 7-摄影

`7-摄影` 将 `projects/aigc/<项目名>/6-分镜/第N集.md` 或用户指定分镜稿升级为逐分镜摄影·运镜稿。

## Directory Tree

```text
7-摄影/
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
│   ├── cinematic-light-in-camera-contract.md
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

- `projects/aigc/<项目名>/6-分镜/第N集.md`
- `projects/aigc/<项目名>/2-美学/画面基调/全局风格协议.md`
- `projects/aigc/<项目名>/2-美学/第N集/摄影风格/摄影风格协议.md`，缺失时回退 `projects/aigc/<项目名>/2-美学/摄影风格/摄影风格协议.md`
- 可选读取 `projects/aigc/<项目名>/2-美学/第N集/场景风格/场景风格协议.md` 中影响摄影的布光偏好、阴影秩序、可用光源边界、材质/空气介质和光影连续性边界；缺失不阻断。

用户指定文稿时优先指定文稿，并在执行报告记录 `source_override=true`。

## Output

- 摄影稿：`projects/aigc/<项目名>/7-摄影/第N集.md`
- 执行报告：`projects/aigc/<项目名>/7-摄影/执行报告.md`

普通格式固定为：

```text
分镜1（0-2秒）：原有内容。镜头从具体机位和角度进入，说明景别/镜头类型、运动方式、运动路径、速度曲线、如何沿既有构图轴线或空间层次运动，以及景深、对焦行为和必要的布光类型、阴影组织、可见光影配合。
```

`7-摄影` 负责定摄影机如何使用 `6-分镜` 的既有空间：机位从哪里进入、沿哪条轴线运动、是否穿过前景/绕开遮挡/压向后景、速度怎么变，以及景深、对焦、布光类型和阴影组织如何配合。它可以引用空间层次、既有光源边界和主体受光/阴影状态，但不重新发明空间布局或新增无源光源，也不把光影写成发光物观察清单或解释性抽象结论。

一镜到底时以画面点为单位输出连续组合运镜：

```text
一镜到底运镜（覆盖分镜A-B，N-N秒）：从分镜A的既有起始状态帧和具体机位/角度进入，连续串联分镜A-B，说明景别/镜头类型、运动方式、如何沿既有构图轴线或空间层次推进、如何使用既有前中后景或遮挡关系、速度曲线与停点、景深策略与对焦/拉焦/转焦接力、布光方案、主光/阴影方向、主体可读性和必要 source motivation boundary 的连续交接，以及跨分镜交出点。
```

内部计划必须区分摄影机运动、焦距变化和透视效果；必须用 `spatial_movement_action_map` 回指 7 的既有空间，并用 `focus_transition_map` 说明起止焦点、对焦模式、景深策略和必须保持可读的信息。旧 `9-光影` 的有效部分只可转化为 `camera_light_plan`：布光类型/光型、阴影组织、内部叙事美学功能、主体可读性控制、连续性交接和必要 source motivation boundary；正式正文只输出可见投影，不输出“阴谋感由...完成”“危险感来自...”等解释句；不得恢复独立光影阶段，不得输出发光物观察清单。本技能不生成图像 prompt、视频 prompt、设备参数、灯位图或剪辑方案。
