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
分镜1（0-2秒）：原有内容。镜头角度（如何变化），镜头类型，镜头速度，焦点（静止或变化）的综合运镜手法。
```

一镜到底时以画面点为单位输出连续组合运镜。本技能不生成图像 prompt、视频 prompt、设备参数或剪辑方案。
