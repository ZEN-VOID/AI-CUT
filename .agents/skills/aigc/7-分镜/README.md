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
├── knowledge-base/
│   └── shot-composition-taxonomy.md
└── references/
    ├── visual-point-and-beat-contract.md
    ├── shot-composition-contract.md
    ├── start-frame-spatial-continuity-contract.md
    ├── shot-duration-and-planning-contract.md
    └── shot-continuity-and-transition-contract.md
```

## Default Inputs

- `projects/aigc/<项目名>/6-氛围/第N集.md`
- `projects/aigc/<项目名>/3-美学/画面基调/全局风格协议.md`
- `projects/aigc/<项目名>/3-美学/第N集/分镜风格/分镜风格协议.md`，缺失时回退 `projects/aigc/<项目名>/3-美学/分镜风格/分镜风格协议.md`

用户指定文稿时优先指定文稿，并在执行报告记录 `source_override=true`。

## Output

- 分镜稿：`projects/aigc/<项目名>/7-分镜/第N集.md`
- 执行报告：`projects/aigc/<项目名>/7-分镜/执行报告.md`

格式固定为：

```text
节拍量化：beat=N（beat1: BT-xx 触发依据；beat2: BT-xx 触发依据）
分镜1（0-1.5秒）：景别，景深，构图形式，前景，中景，后景，主体站位。
分镜2（1.5-3秒）：景别，景深，构图形式，前景，中景，后景，主体站位。
```

时码以 0.5 秒为最小颗粒，可用整数或 `.5` 小数，不要求整数秒。

本技能不生成图像、视频、storyboard sheet、prompt 或设备参数。

## Composition Control

`7-分镜` 负责定静态画面结构：起始状态帧里的主体位置、前中后景、左右方位、遮挡关系、空间纵深和构图层次。`8-摄影` 只引用这些既有空间关系来设计摄影机运动，不反向重写空间布局。

多人、对峙、追逐、进出门或转场承接时，内部证据必须记录 screen left/right、主体朝向、入口/出口方向、视线轴线和上一镜交出点。前中后景、框架、遮挡或纵深不是装饰词，应拆成可供 `8-摄影` 使用的空间条件。

同一画面点有多条分镜时，必须先解析 `spatial_field_map`，再用 `within_point_spatial_continuity_map` 约束前景、中景、后景和主体站位的连续变化；不得把每条分镜当作重新取景的独立画面。

构图形式使用 `knowledge-base/shot-composition-taxonomy.md` 的受控词表。正式执行时，每条分镜的构图方式应命中常见摄影/电影构图方法，例如三分法构图、黄金比例构图、对角线构图、框架式构图、引导线构图、中心构图、留白构图等；表外术语需要记录例外理由。
