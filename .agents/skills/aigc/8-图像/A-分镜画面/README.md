# aigc 8-图像 / A-分镜画面

从 `projects/aigc/<项目名>/6-分组/` 提取镜级分镜，生成四段式 `分镜ID` 的英文生图 prompt，绑定 `7-设计/*/3-生成` 中的主体图片，并按需调用 `.agents/skills/cli/imagegen` 批量生成分镜画面。

组织新画面 prompt 时，若当前场景有本地场景参照图，必须先用 `view_image` 检视场景图，并把画面风格、光影、色调和氛围与场景参照图保持一致作为固定提示词。同一场景下继续组织新画面 prompt 时，若上一分镜已有本地生成图，必须先用 `view_image` 回看上一画面并把站位、走位、朝向、遮挡和关键道具相对位置纳入当前 prompt 的连续性约束。

空间一致性不是平面背景复用；同场景分镜必须建立 3D 空间模型，定位角色起点、终点、移动轨迹、视线、遮挡、固定锚点和镜头轴线。正反打对话戏可出现相对的南北面、东西面或房间两端背景，但必须保持同一对话轴线和视线闭合。

批量生成采用两阶段：先为指定范围完整生成并落盘 `第N集-分镜画面-prompts.md`、`reference-manifest.json` 与 `imagegen-plan.json`；再按该 prompt 文档逐镜串行生图。第二阶段不是并发队列；整集或多分镜生成必须按 `shot_id` 严格串行逐镜完成，前一镜生成、持久化和结果记录完成后，才允许进入下一镜。

## Directory Tree

```text
A-分镜画面/
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
使用 $aigc-image-storyboard-frame，为 projects/aigc/诡校-测试版/6-分组/第1集.md 生成第1集全部分镜画面 prompt，并绑定已有角色、场景、道具参照图。
```

输出根路径固定为：

```text
projects/aigc/<项目名>/8-图像/A-分镜画面
```

逐集产物可在该根路径下使用 `第N集/` 子目录组织。
