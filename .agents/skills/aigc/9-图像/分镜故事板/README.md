# aigc-image-storyboard-sheet

`分镜故事板` 是 `9-图像` 阶段的组级多格 storyboard 入口。它从 `projects/aigc/<项目名>/8-分组` 直接引用对应分镜组完整内容，按视觉节拍识别 storyboard frame units，按组底 YAML 绑定主体参照，并以分镜组为单位直接调用 `.agents/skills/cli/imagegen` 生成图片。原始 `分镜N` 只作为追溯标签，不默认等同于 storyboard panel；默认输出为标准分镜手稿风格黑白线稿基底，每个 panel 使用 locked 16:9 image box 和 `panel_geometry_blueprint` 固定几何比例，图片下方包含由分组稿原文保真精简的 `rich_brief` 分镜描述文字，每个可见角色头顶包含与分组稿一致的黑色角色名，参照图用于还原角色、场景、道具既有形象而不是继承全局风格。彩色仅用于标注系统：红色箭头=身体运动，蓝色箭头=摄影机运动，绿色标记=取景/构图笔记，橙色标记=灯光方向，紫色标记=情绪/声音/叙事强调，黑色文本=角色头顶名称、简短镜头笔记和面板标签。

两道硬门禁与一个可选侧车用于稳定成图效果：

- `style_lock_spec`：隔离完整组稿中的上游电影风格、彩色、光影、氛围和胶片质感词，完整组稿只作为证据，不作为画风指令。
- `visual_prompt_atoms`：逐 panel 写出生图可执行原子，避免只把长组稿或摘要交给 imagegen 自行理解。
- `spatial_handoff`：可选读取 `分镜平面图` accepted 侧车作为空间证据；缺失不阻断，且不得替代故事板自身的 frame-unit 和 prompt atoms 裁决。

## Directory Tree

```text
分镜故事板/
├── references/
├── scripts/
├── templates/
├── review/
├── knowledge-base/
├── types/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
├── test-prompts.json
└── README.md
```

## Quick Entry

```text
使用 $aigc-image-storyboard-sheet，为 projects/aigc/诡校-测试版/8-分组/第1集.md 生成第1集全部分镜故事板，并绑定已有角色、场景、道具参照图。
```

## Runtime Output

```text
projects/aigc/<项目名>/9-图像/分镜故事板/第N集/
├── 第N集-分镜故事板-prompts.md
├── 第N集-group-index.json
├── 第N集-reference-manifest.json
├── 第N集-imagegen-plan.json
├── 第N集-imagegen-results.json
├── images/
│   └── <分镜组ID>.png
└── 执行报告.md
```

`第N集-imagegen-plan.json` 只是调用载体，不是完成态；最终必须有 `images/<分镜组ID>.png`。

## Runtime Spine

- `SKILL.md` 是唯一主合同，直接承载业务画像、类型路由、节点、量化口径、注意力协议、checkpoint、模块授权、review gate 和输出合同。
- `steps/` 不再参与执行；旧 workflow 节点已迁入 `SKILL.md` 的 `Thinking-Action Node Map` 与 `Visual Maps`。
- `references/`、`types/`、`review/`、`templates/`、`scripts/`、`guardrails/` 只能展开 `SKILL.md` 已声明的规则，不新增入口或完成态。
- `test-prompts.json` 固定单组生成、整集批量和 repair/review 的回归提示。
