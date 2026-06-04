# aigc-image-storyboard-sheet

`B-分镜故事板` 是 `12-图像` 阶段的组级多格 storyboard 入口。它从 `projects/aigc/<项目名>/10-分组` 直接引用对应分镜组完整内容，按视觉节拍识别 storyboard frame units，按组底 YAML 绑定主体参照，并以分镜组为单位调用 imagegen。原始 `分镜N` 只作为追溯标签，不默认等同于 storyboard panel；默认输出为标准分镜手稿风格黑白线稿基底，每个 panel 图片区默认 16:9，图片下方包含由分组稿原文保真精简的 `rich_brief` 分镜描述文字，每个可见角色头顶包含与分组稿一致的黑色角色名，参照图用于还原角色、场景、道具既有形象而不是继承全局风格。彩色仅用于标注系统：红色箭头=身体运动，蓝色箭头=摄影机运动，绿色标记=取景/构图笔记，橙色标记=灯光方向，紫色标记=情绪/声音/叙事强调，黑色文本=角色头顶名称、简短镜头笔记和面板标签。

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
使用 $aigc-image-storyboard-sheet，为 projects/aigc/诡校-测试版/10-分组/第1集.md 生成第1集全部分镜故事板，并绑定已有角色、场景、道具参照图。
```

## Runtime Output

```text
projects/aigc/<项目名>/12-图像/B-分镜故事板/第N集/
├── 第N集-分镜故事板-prompts.md
├── 第N集-group-index.json
├── 第N集-reference-manifest.json
├── 第N集-imagegen-plan.json
├── 第N集-imagegen-results.json
├── images/
│   └── <分镜组ID>.png
└── 执行报告.md
```
