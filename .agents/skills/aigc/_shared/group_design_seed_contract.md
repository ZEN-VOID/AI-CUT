# Group Design Seed Contract

本文件是 `aigc/2-Global -> 3-Detail` 之间 `episode_root.json` handoff 的单一真源。

## Purpose

- 让 `2-Global` 围绕 `.agents/skills/aigc/2-Global/_shared/episode_root.json` 模板直接生成 `projects/aigc/<项目名>/2-Global/episode_root.json`
- 让 `3-Detail` 直接继承已收束的组级 `global` 字段，而不是再次从 Markdown 长文中抽取
- 将旧 `2-Global/*.md` 明确降级为兼容投影，而不是 handoff 真源

## Canonical Carrier

- template:
  - `.agents/skills/aigc/2-Global/_shared/episode_root.json`
- downstream detail template:
  - `.agents/skills/aigc/3-Detail/_shared/episode_detail.json`
- seed root file:
  - `projects/aigc/<项目名>/2-Global/episode_root.json`
- target slot:
  - `meta`
  - `project_global`
  - `groups[]`

## Ownership

| phase | owner | responsibility |
| --- | --- | --- |
| `2-Global` | `aigc-global` | 直接填写 `episode_root.json` 的 `meta / project_global / groups[].global` |
| `3-Detail` | `aigc-detail` | 读取 `2-Global/episode_root.json` 作为组级前置 seed，并基于 `.agents/skills/aigc/3-Detail/_shared/episode_detail.json` 在自己的 runtime 下生成更细分的 detail root |

硬规则：

1. `2-Global` 只拥有 `meta`、`project_global` 与 `groups[]` 的写入权，不得在本阶段发明 shot-level 字段。
2. `3-Detail` 默认继承 `groups[].global.剧本正文` 与 `groups[].global.*`，不得在无明确返工理由时重写其含义。
3. 跨阶段第一结构化 handoff 以 `2-Global/episode_root.json` 为准。
4. 旧 `2-Global/*.md` 若被生成，只是兼容投影；不得再被描述为跨阶段第一真源。

## Mapping

| episode root field | upstream source | scope | max_chars | mapping rule |
| --- | --- | --- | --- | --- |
| `meta.剧名` | 项目根目录名或项目级显式标题 | 当前项目 | exact | 使用项目 canonical 名称写回 |
| `meta.集数` | 当前集 episode id | 当前集 | exact | 默认使用 `第N集` 形式 |
| `meta.组数` | 当前集命中分镜组数量 | 当前集 | exact | 直接写组总数，不写 shot count |
| `meta.总时长` | 当前集所有命中组总时长汇总 | 当前集 | exact | 直接写当前集总时长，不拆分 shot-level 秒位 |
| `project_global.全局风格` | `2-Global` 内部风格能力链定稿结果 | 项目级稳定项 | 220 | 写入项目级统一风格前缀 |
| `project_global.全集类型元素` | `2-Global` 内部类型总则能力链定稿结果 | 项目级稳定项 | 400 | 写入项目级类型总则 |
| `groups[].分镜组ID` | `1-Planning/3-分组/第N集.md` 的 `【x-x-x】` 标题 | 当前组 | exact | 保持三段式 `分镜组ID` 原样写回 |
| `groups[].global.剧本正文` | `1-Planning/3-分组/第N集.md` 中命中组正文 | 当前组 | full_text | 完整整理该组正文入壳，只去掉重复组号标题，不得摘要、净化或改写语义 |
| `groups[].global.全局风格` | `project_global.全局风格` | 项目级稳定项 | 220 | 默认与项目级字段保持同值，便于下游直接读取 |
| `groups[].global.类型元素` | `2-Global` 内部组级类型能力链定稿结果 | 当前组 | 100 | 直接写当前组类型信号，不再经 Markdown 中转 |
| `groups[].global.导演意图` | `2-Global` 内部导演意图能力链定稿结果 | 当前组 | 240 | 直接写当前组导演执行导向，不再经 Markdown 中转；必须能拆出观看策略、执行抓手与禁用方向 |

## Distillation Rules

1. 字数窗必须在 JSON 定稿阶段满足；写回阶段只允许 patch 已确认字段内容。
2. `global.剧本正文` 必须完整整理命中组全文；如果写入结果更像摘要而不是原组正文，视为失败。
3. `全局风格` 必须保持项目级稳定，不得被单组临时情绪污染；默认也不得混入景别偏置、具体颜色/材质/构图或镜头操作词。
4. `类型元素` 与 `导演意图` 都必须严格对齐当前 `分镜组ID`，不得跨组混写。
5. `导演意图` 不得写成剧情复述、剧本正文摘句、情绪评语或一句漂亮比喻；定稿句至少要同时覆盖：
   - `观看策略`：这一组要求观众先看见什么、后意识到什么。
   - `执行抓手`：可转入 `3-Detail` 的调度、表演、节奏、空间或镜头处理方向。
   - `禁用方向`：本组不能被拍成的误读、爽点或泛化套路。
6. 三个 `global` 字段都必须能被 `3-Detail` 后续 detail 模板直接消费；如果一句话不能转译成镜头、表演、调度、氛围或摄影方向，应回到 `2-Global` 能力链继续压实，而不是写成模糊摘要。
7. 当前合同不负责 shot-level 的 `时间`、逐镜 `剧本正文`、`主体锚定`、`分镜构图`、`运镜手法`、`角色表现`、`氛围表现`、`摄影表现` 与 `转场特效`；这些 finer-grained 字段应在 `3-Detail` 的独立模板 `.agents/skills/aigc/3-Detail/_shared/episode_detail.json` 中定义。

## Writeback Policy

1. `2-Global` 首次进入时，如 `episode_root.json` 不存在，可基于 `.agents/skills/aigc/2-Global/_shared/episode_root.json` 创建同模板文件。
2. `2-Global` 写回时，必须同时形成完整 `meta`、`project_global` 与 `groups[]` 壳。
3. `3-Detail` 后续读取时，应把 `2-Global/episode_root.json` 当成组级 seed root，而不是 detail root。
4. `3-Detail` 自己的 detail root 可以在 `projects/aigc/<项目名>/3-Detail/` 下独立落盘，并由 `.agents/skills/aigc/3-Detail/_shared/episode_detail.json`、其本地 schema 与 validator 负责约束。
