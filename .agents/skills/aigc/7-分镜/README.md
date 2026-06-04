# aigc 7-分镜

`7-分镜` 将 `projects/aigc/<项目名>/6-氛围/第N集.md` 或用户指定文稿拆成逐画面点内联分镜稿。

## Directory Tree

```text
7-分镜/
├── SKILL.md
├── CONTEXT.md
├── CHANGELOG.md
├── README.md
├── test-prompts.json
├── agents/
│   └── openai.yaml
└── references/
    ├── visual-point-and-beat-contract.md
    ├── shot-composition-contract.md
    ├── shot-duration-and-planning-contract.md
    └── shot-continuity-and-transition-contract.md
```

## Default Inputs

- `projects/aigc/<项目名>/6-氛围/第N集.md`
- `projects/aigc/<项目名>/3-美学/画面基调/全局风格协议.md`
- `projects/aigc/<项目名>/3-美学/分镜风格/分镜风格协议.md`

用户指定文稿时优先指定文稿，并在执行报告记录 `source_override=true`。

## Output

- 分镜稿：`projects/aigc/<项目名>/7-分镜/第N集.md`
- 执行报告：`projects/aigc/<项目名>/7-分镜/执行报告.md`

格式固定为：

```text
分镜1（0-2秒）：景别，景深，构图形式，主体陪体背景描述
```

本技能不生成图像、视频、storyboard sheet、prompt 或设备参数。
