# aigc-image-storyboard-sheet

`B-分镜故事板` 是 `7-图像` 阶段的组级多格 storyboard 入口。它从 `projects/aigc/<项目名>/5-分组` 读取分镜组原文，按视觉节拍识别 storyboard frame units，按组底 YAML 绑定主体参照，并以分镜组为单位调用 imagegen。原始 `分镜N` 只作为追溯标签，不默认等同于 storyboard panel；场景参照图同时约束空间、风格、光影和氛围。

## Directory Tree

```text
B-分镜故事板/
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
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## Quick Entry

```text
使用 $aigc-image-storyboard-sheet，为 projects/aigc/诡校-测试版/5-分组/第1集.md 生成第1集全部分镜故事板，并绑定已有角色、场景、道具参照图。
```

## Runtime Output

```text
projects/aigc/<项目名>/7-图像/B-分镜故事板/第N集/
├── 第N集-分镜故事板-prompts.md
├── 第N集-group-index.json
├── 第N集-reference-manifest.json
├── 第N集-imagegen-plan.json
├── 第N集-imagegen-results.json
├── images/
│   └── <分镜组ID>.png
└── 执行报告.md
```
