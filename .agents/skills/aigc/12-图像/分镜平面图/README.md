# aigc-image-storyboard-floor-plan

`分镜平面图` 是 `12-图像` 阶段的组级空间调度图入口。它从 `projects/aigc/<项目名>/10-分组` 直接引用分镜组内容，调用 `.agents/skills/cli/imagegen` 生成一张多 panel 顶视图平面图 sheet，用黑白建筑平面图底图表达场景边界、角色站位、动线、摄影机位置、运镜方向和上下组空间连续性。

它不生成分镜故事板画面。角色用彩色圆形、三角形、方形、菱形等图标表示，动线和机位沿用图像阶段标注色：红色为身体运动，蓝色为摄影机运动，绿色为取景/构图，橙色为灯光方向，紫色为情绪/声音/叙事强调，黑色文本为角色名、锚点和 panel 标签。

## Directory Tree

```text
分镜平面图/
├── agents/
│   └── openai.yaml
├── references/
│   └── floor-plan-sheet-contract.md
├── scripts/
│   └── README.md
├── templates/
│   └── output-template.md
├── review/
│   └── review-contract.md
├── types/
│   ├── type-map.md
│   └── default/default.md
├── guardrails/
│   └── guardrails-contract.md
├── knowledge-base/
│   └── workshop-heuristics.md
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
├── test-prompts.json
└── README.md
```

## Usage

```text
使用 $分镜平面图，为 projects/aigc/诡校-测试版/10-分组/第1集.md 生成第1集全部分镜平面图，并保持同一集上下分镜组空间连续。
```

## Runtime Output

```text
projects/aigc/<项目名>/12-图像/分镜平面图/第N集/
├── 第N集-分镜平面图-prompts.md
├── 第N集-floor-plan-index.json
├── 第N集-reference-manifest.json
├── 第N集-spatial-continuity-manifest.json
├── 第N集-imagegen-plan.json
├── 第N集-imagegen-results.json
├── floor-plan-sheets/
│   └── <分镜组ID>.png
└── 执行报告.md
```

## Runtime Spine

- `SKILL.md` 是唯一主合同，直接承载业务画像、类型路由、节点、量化口径、注意力协议、checkpoint、模块授权、review gate 和输出合同。
- `references/floor-plan-sheet-contract.md` 只展开图面 payload 和审查映射，不新增入口或完成态。
- `CONTEXT.md` 只存经验，不重定义规则。
- `scripts/` 只能做路径、manifest、尺寸和校验辅助，不生成空间裁决或 prompt 正文。
- `第N集-imagegen-plan.json` 只是调用载体，不是完成态；最终必须有 `floor-plan-sheets/<分镜组ID>.png`。
