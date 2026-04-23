---
name: aigc-detail
description: Use when the `3-Detail` stage must fill `projects/aigc/<项目名>/3-Detail/第N集.json` in one root skill, with `1-分镜构图` fixed as the first pass to decide shot count, script split, and shot skeleton before all other creative fields are written.
governance_tier: full
---

# aigc 3-Detail

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 本技能默认采用 `单技能知行合一 + references 细则下沉` 模式；根 `SKILL.md` 负责主骨架、顺序门、字段真源与验收门，`references/` 负责字段细则、示例和模块配置。
- 冲突优先级固定为：用户显式请求 > 根 `AGENTS.md` > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本目录 `references/*` > 本 `CONTEXT.md`。

## 概述

`3-Detail` 当前回到更直接的编导 detail root 结构：

1. 在根技能内直接读取 `projects/aigc/<项目名>/2-Global/episode_root.json`。
2. 以 `.agents/skills/aigc/3-Detail/_shared/episode_detail.json` 为 detail 模板真源。
3. 以 `.agents/skills/aigc/3-Detail/references/*` 作为阶段内字段细则，再按需接入 `knowledge-base/电影学院派/*` 作为导演 / 分镜 / 摄影判断的学院派知识包。
4. 固定先执行 `1-分镜构图`，先决定：
   - 每个分镜组的 `分镜数`
   - 组内 `剧本正文` 的切分点
   - 每镜 `时间 / 剧本正文 / 主体锚定 / 分镜构图`
5. 再按固定顺序补齐其余字段：
   - `角色表现`
   - `氛围表现`
   - `摄影表现`
   - `运镜手法`
   - `转场特效`
6. 学院派知识库只作为“判断增强器”，不直接替代字段写作；所有知识都必须被翻译回当前 JSON 槽位，而不是把教材术语原样堆入字段。
7. 最后只向一个主文件写回：
   - `projects/aigc/<项目名>/3-Detail/第N集.json`

换句话说：`3-Detail` 当前主问题不是多子技能接力，而是在一套固定思行顺序里，把 `meta + groups[].global/detail.分镜列表` 里的每个字段写得艺术、逻辑、连续且一致。

这里的阶段边界必须固定：

- `2-Global/episode_root.json` 是围绕 `.agents/skills/aigc/2-Global/_shared/episode_root.json` 直接填好的组级 seed root。
- 上游当前不提供 shot-level 字段。
- `1-分镜构图` 负责先锁 `分镜数`、正文切分点，以及每镜 `时间 / 剧本正文 / 主体锚定 / 分镜构图` 的骨架。

## Single-Skill Positioning

### 本技能拥有

- detail root 的唯一写回权
- `1-分镜构图` 先行的硬顺序门
- `groups[].detail.分镜列表` 的镜级骨架裁决
- `角色表现 / 氛围表现 / 摄影表现 / 运镜手法 / 转场特效` 的内部 pass 顺序
- 阶段级验证与 `validation-report.md` 写回

### 本技能不拥有

- 再拆出 `1-水月 / 2-镜花` 作为当前主链真源
- 把字段判断外包给 package-local 子技能再回收
- 在多个中间 bundle 之间往返压缩、转写、拼装
- 用已移除的旧桥接字段作为当前 canonical 字段
- 用抽象评语替代具体字段填写

## Internal Capability Fusion Contract (Mandatory)

`3-Detail` 当前内部能力按根技能内的固定 pass 治理：

| pass_id | 固定顺序 | 写入重点 | 作用 |
| --- | --- | --- | --- |
| `P1` | `1-分镜构图` | `detail.分镜数`、`分镜列表.<分镜ID>.时间 / 剧本正文 / 主体锚定 / 分镜构图` | 先锁镜数、正文切分点和镜级骨架 |
| `P2` | `2-角色表现` | `角色表现` | 把人物目的、表演动作和内里压力写成可演信号 |
| `P3` | `3-氛围表现` | `氛围表现` | 把环境压强、空间层次和诗性来源写实化 |
| `P4` | `4-摄影表现` | `摄影表现` | 把光影、色彩、质感控制线落到当前镜头 |
| `P5` | `5-运镜手法` | `运镜手法` | 让镜头运动服务已锁定的构图和剧情骨架 |
| `P6` | `6-转场特效` | `转场特效` | 只在确有必要时补组内/组间衔接与特效策略 |
| `P7` | `7-验收` | `validation-report.md` | 形成阶段闭环 |

硬规则：

1. `P1-分镜构图` 必须最先执行，不得跳过。
2. 若 `P1` 还没锁定 `分镜数 + 分镜列表` 骨架，后续所有 pass 都不得先写字段。
3. 后续任何 pass 都不得反向改写 `P1` 已锁定的分镜数、分镜 ID、时间或分镜正文，除非本轮显式回退到 `P1` 重建。
4. 根技能是唯一真源；`references/` 只提供细则、模块配置、示例和审读标尺。

## Shared Canonical Sources (Mandatory)

- `.agents/skills/aigc/SKILL.md`
- `.agents/skills/aigc/2-Global/SKILL.md`
- `.agents/skills/aigc/2-Global/_shared/episode_root.json`
- `.agents/skills/aigc/2-Global/_shared/IO_CONTRACT.md`
- `.agents/skills/aigc/_shared/project-runtime-layout.md`
- `.agents/skills/aigc/_shared/group_design_seed_contract.md`
- `.agents/skills/aigc/3-Detail/_shared/episode_detail.json`
- `.agents/skills/aigc/3-Detail/_shared/branch-output-contract.md`
- `.agents/skills/aigc/3-Detail/_shared/node-pack-contract.md`
- `.agents/skills/aigc/3-Detail/_shared/creative-guidance-contract.md`
- `.agents/skills/aigc/3-Detail/references/思行网络.md`
- `.agents/skills/aigc/3-Detail/references/能力通道图谱.yaml`
- `.agents/skills/aigc/3-Detail/references/模板字段填写指南.md`
- `.agents/skills/aigc/3-Detail/references/编剧手册.md`
- `.agents/skills/aigc/3-Detail/references/镜头语言.md`
- `.agents/skills/aigc/3-Detail/references/路由画像.yaml`
- `.agents/skills/aigc/3-Detail/references/正反例.md`
- `.agents/skills/aigc/3-Detail/references/创作评审标尺.md`
- `.agents/skills/aigc/3-Detail/references/电影学院派知识接线.md`
- `knowledge-base/电影学院派/README.md`
- `knowledge-base/电影学院派/导演手册/电影导演方法.md`
- `knowledge-base/电影学院派/导演手册/电影导演技术.md`
- `knowledge-base/电影学院派/导演手册/一流对话场景.md`
- `knowledge-base/电影学院派/分镜脚本/电影镜头设计.md`
- `knowledge-base/电影学院派/分镜脚本/电影镜头调度.md`
- `knowledge-base/电影学院派/分镜脚本/电影镜头语法.md`
- `knowledge-base/电影学院派/分镜脚本/电影镜头技术.md`
- `knowledge-base/电影学院派/电影摄影/影像的创造.md`
- `knowledge-base/电影学院派/电影摄影/摄影创作技法.md`

## Academy Knowledge Utilization Contract (Mandatory)

`3-Detail` 必须把 `knowledge-base/电影学院派/*` 视为“按需加载的学院派判断库”，而不是背景摆设。使用规则固定如下：

| pass_id | 首要问题 | 必读知识包 | 允许带来的增益 | 禁止误用 |
| --- | --- | --- | --- | --- |
| `P1-分镜构图` | 这组戏该切几镜、如何保证空间与戏剧节拍清晰 | `导演手册/电影导演方法.md`、`导演手册/电影导演技术.md`、`分镜脚本/电影镜头设计.md`、`分镜脚本/电影镜头语法.md` | 戏剧单元切分、轴线/视线/揭示关系、镜头语句、空间方向 | 把 180°/30° 规则写成生硬教材句，或直接写器材参数 |
| `P2-角色表现` | 人物为什么这样演、对白攻守如何外显 | `导演手册/电影导演方法.md`、`导演手册/一流对话场景.md` | 目标、障碍、气口、抢话/吞话、反应动作 | 用导演术语替代人物行为，或把对话戏写成台词复述 |
| `P3-氛围表现` | 空间如何施压、气息如何由可见条件生成 | `导演手册/电影导演方法.md`、`电影摄影/影像的创造.md`、`电影摄影/摄影创作技法.md` | 空间层级、负空间、框式构图、影调/质感/景物承情 | 只搬运“冷/空/美/压抑”之类抽象审美词 |
| `P4-摄影表现` | 光色质如何服务当前戏而不是泛泛“有电影感” | `电影摄影/影像的创造.md`、`电影摄影/摄影创作技法.md`、`分镜脚本/电影镜头技术.md` | 光位、影调、色彩关系、质感显影、透视和视觉重力 | 堆摄影器材、焦段数值、曝光参数，或抢写构图骨架 |
| `P5-运镜手法` | 镜头如何带着观众看，而不破坏前面锁定的结构 | `导演手册/电影导演技术.md`、`分镜脚本/电影镜头调度.md`、`分镜脚本/电影镜头语法.md` | 机位路径、揭示、伴行、重取景、空间导览 | 后序反改镜数、正文切分或主体锚定 |
| `P6-转场特效` | 哪里需要桥梁、重复、释放镜头或最小转场收益 | `导演手册/电影导演方法.md`、`分镜脚本/电影镜头语法.md` | 时间压缩、桥梁镜头、重复画面、组内组间顺滑挂接 | 为了炫技硬加特效，掩盖本来不稳的镜级结构 |
| `P7-验收` | 当前字段是否真正吃到了知识包，而不是只挂名 | `references/创作评审标尺.md`、`references/电影学院派知识接线.md` | 抽检字段是否具备学院派可解释性与下游可消费性 | 只检查结构，不检查知识是否有效转译 |

硬规则：

1. 学院派知识库默认按需读取，不是每次全量通读；必须先看当前组的戏剧问题，再决定读哪个包。
2. `knowledge-base/电影学院派/*` 只提供判断与术语来源，最终输出必须回写为当前字段对象语言，而不是教材摘要。
3. 若当前问题属于“镜头如何落”和“空间如何不乱”，优先读 `分镜脚本/`；若属于“为什么这样组织”，优先读 `导演手册/`；若属于“光色质如何支撑”，优先读 `电影摄影/`。
4. 内部 `references/*` 仍是本阶段的第一落地细则；电影学院派知识包负责给这些细则补“为什么这样写”的判断深度。
5. 若读完知识包仍不能改善当前字段，则回到本阶段字段边界，不允许为了“用了知识库”而硬塞术语。
6. `validation-report.md` 必须显式记录本轮学院派知识证据，至少包括：
   - `knowledge_mode: applied | unused_with_reason`
   - `knowledge_domain`
   - `selected_bundles`
   - `applied_passes`
   - `translation_targets`
7. `selected_bundles` 不能只列文件名；必须让 `translation_targets` 回链到本轮实际写入的字段或 shot/group scope。

## Business Requirement Analysis Contract (Mandatory)

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 将 `2-Global/episode_root.json` 这颗由 `2-Global` 围绕模板直接填好的组级 seed root 继续细化为可被 `4-Design / 5-Image / 6-Video` 消费的 `projects/aigc/<项目名>/3-Detail/第N集.json`，并通过固定顺序把每个 group 的分镜数、镜级正文和镜级字段一次性收成单一 detail 真源。 |
| `business_object` | `projects/aigc/<项目名>/3-Detail/第N集.json` 与 `projects/aigc/<项目名>/3-Detail/validation-report.md`。 |
| `constraint_profile` | `2-Global` 以 `episode_root.json` 直接提供 `project_global + groups[].global.剧本正文 / 全局风格 / 类型元素 / 导演意图` 这一层组级 seed；`3-Detail` 必须自己决定镜头切分与镜级骨架；第一步固定先做 `分镜构图`；输出结构固定为 `meta + groups[].global/detail`；运行时 detail root 必须继续保留继承来的 `groups[].global.剧本正文`，不能在 detail 阶段丢失；字段必须可见、可拍、可连续。 |
| `success_criteria` | 每个命中 group 都具备稳定的 `detail.分镜数`、完整的 `分镜列表`、以及每镜稳定的 `时间 / 剧本正文 / 主体锚定 / 分镜构图 / 运镜手法 / 角色表现 / 氛围表现 / 摄影表现 / 转场特效`，并通过验证写回 `validation-report.md`。 |
| `non_goals` | 不再维护 `1-水月 / 2-镜花` 作为当前主执行入口；不再把多条中间结果汇成 bundle 再回写；不重新改写 `2-Global` 的组级剧情事实。 |
| `complexity_source` | 复杂度主要来自镜头切分、字段边界、跨字段一致性，以及艺术性与逻辑性的同时成立。 |
| `topology_fit` | 最优拓扑固定为“输入锁定 -> 分镜构图先行 -> 表演/氛围 -> 摄影/运镜/转场 -> 验收”。 |
| `step_strategy` | 先搭 detail skeleton，再逐字段充实；先锁结构，再做审美。 |

## Context Preload (Mandatory)

加载顺序固定为：

1. 根 `AGENTS.md`
2. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
3. 本 `SKILL.md + CONTEXT.md`
4. `.agents/skills/aigc/_shared/project-runtime-layout.md`
5. `.agents/skills/aigc/_shared/group_design_seed_contract.md`
6. `.agents/skills/aigc/2-Global/_shared/episode_root.json`
7. `.agents/skills/aigc/2-Global/_shared/IO_CONTRACT.md`
8. `.agents/skills/aigc/3-Detail/_shared/episode_detail.json`
9. `.agents/skills/aigc/3-Detail/_shared/branch-output-contract.md`
10. `.agents/skills/aigc/3-Detail/_shared/node-pack-contract.md`
11. `.agents/skills/aigc/3-Detail/_shared/creative-guidance-contract.md`
12. `.agents/skills/aigc/3-Detail/references/思行网络.md`
13. `.agents/skills/aigc/3-Detail/references/能力通道图谱.yaml`
14. `.agents/skills/aigc/3-Detail/references/模板字段填写指南.md`
15. `.agents/skills/aigc/3-Detail/references/编剧手册.md`
16. `.agents/skills/aigc/3-Detail/references/镜头语言.md`
17. `.agents/skills/aigc/3-Detail/references/路由画像.yaml`
18. `.agents/skills/aigc/3-Detail/references/正反例.md`
19. `.agents/skills/aigc/3-Detail/references/创作评审标尺.md`
20. `.agents/skills/aigc/3-Detail/references/电影学院派知识接线.md`
21. `knowledge-base/电影学院派/README.md`
22. 按 `references/路由画像.yaml` 与当前 pass 选择性加载：
   - `knowledge-base/电影学院派/导演手册/*`
   - `knowledge-base/电影学院派/分镜脚本/*`
   - `knowledge-base/电影学院派/电影摄影/*`
23. `projects/aigc/<项目名>/MEMORY.md`（若项目已绑定）
24. `projects/aigc/<项目名>/CONTEXT/` 相关文件（若存在）
25. `projects/aigc/<项目名>/2-Global/episode_root.json`
26. `projects/aigc/<项目名>/3-Detail/第N集.json`（若存在）
27. `projects/aigc/<项目名>/team.yaml`（若存在）

## Total Input Contract (Mandatory)

### 必需输入

- `projects/aigc/<项目名>/2-Global/episode_root.json`

### 推荐输入

- `projects/aigc/<项目名>/3-Detail/第N集.json`
- `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md`
- `projects/aigc/<项目名>/team.yaml`

### 硬规则

1. `2-Global/episode_root.json` 是 detail 阶段唯一上游 seed。
2. `2-Global/episode_root.json` 当前提供 `meta + project_global + groups[].global`；`3-Detail` 的直接消费重点仍是 `groups[].global.*`。
3. `3-Detail` 不得要求上游先给任何 shot-level 字段；这些字段必须由本阶段自己落出来。
4. 组级 seed 只负责 `global.*`，镜级正文和主体锚定都在 `3-Detail` 内部生成；但运行时输出必须继续保留继承来的 `global.剧本正文` 作为组级全文锚点。
5. 若只命中局部 group 或局部字段，只 patch 命中 scope，不默认全量重跑。

## One-Shot Output Contract (Mandatory)

### canonical 输出

- `projects/aigc/<项目名>/3-Detail/第N集.json`
- `projects/aigc/<项目名>/3-Detail/validation-report.md`

### `第N集.json` 最低要求

1. 顶层结构必须与 `.agents/skills/aigc/3-Detail/_shared/episode_detail.json` 同构。
2. 顶层必须具备：
   - `meta`
   - `groups`
3. `meta` 必须具备：
   - `剧名`
   - `集数`
   - `组数`
   - `总时长`
4. 每个 group 必须具备：
   - `分镜组ID`
   - `global.剧本正文`
   - `global.全局风格 / 类型元素 / 导演意图`
   - `detail.分镜数`
   - `detail.分镜列表`
5. 每镜至少具备：
   - `时间`
   - `剧本正文`
   - `主体锚定`
   - `分镜构图`
   - `运镜手法`
   - `角色表现`
   - `氛围表现`
   - `摄影表现`
   - `转场特效`

## Template Fill Strategy

- 结构和顺序细则：读取 [references/思行网络.md](references/思行网络.md)
- 字段对象的读写边界：读取 [references/能力通道图谱.yaml](references/能力通道图谱.yaml)
- 模板每个字段怎么写：读取 [references/模板字段填写指南.md](references/模板字段填写指南.md)
- `角色表现 / 氛围表现` 的细粒度写法：读取 [references/编剧手册.md](references/编剧手册.md)
- `分镜构图 / 摄影表现 / 运镜手法 / 转场特效` 的细粒度写法：读取 [references/镜头语言.md](references/镜头语言.md)
- 组型路由与策略偏置：读取 [references/路由画像.yaml](references/路由画像.yaml)
- 学院派知识如何接入当前 pass：读取 [references/电影学院派知识接线.md](references/电影学院派知识接线.md)
- 质量对照与反例：读取 [references/正反例.md](references/正反例.md)
- 验收口径：读取 [references/创作评审标尺.md](references/创作评审标尺.md)

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| `FIELD-DETAIL-01` | `meta` | 项目、集数、组数、总时长正确 | `S1` | 结构稳定性 | `FAIL-DETAIL-01` |
| `FIELD-DETAIL-02` | `groups[].global` | 组级 seed 与上游含义一致 | `S1` | 继承准确性 | `FAIL-DETAIL-02` |
| `FIELD-DETAIL-03` | `detail.分镜数` | 镜数与实际分镜列表一致 | `S2` | 镜级可追溯性 | `FAIL-DETAIL-03` |
| `FIELD-DETAIL-04` | `时间 / 剧本正文 / 主体锚定 / 分镜构图` | 每镜骨架完整且可拍 | `S2` | 构图骨架力 | `FAIL-DETAIL-04` |
| `FIELD-DETAIL-05` | `角色表现` | 人物能演、能看、能被镜头放大 | `S3` | 表演成立度 | `FAIL-DETAIL-05` |
| `FIELD-DETAIL-06` | `氛围表现` | 环境施压真实、有层次、有意境来源 | `S4` | 空间承载力 | `FAIL-DETAIL-06` |
| `FIELD-DETAIL-07` | `摄影表现 / 运镜手法` | 光影与镜头运动服务既有骨架 | `S5-S6` | 视听一致性 | `FAIL-DETAIL-07` |
| `FIELD-DETAIL-08` | `转场特效` | 有收益但不喧宾夺主 | `S7` | 衔接收益 | `FAIL-DETAIL-08` |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `S1` | `FIELD-DETAIL-01~02` | 本轮到底补哪一集、哪几个 group | 锁输入与 scope | 范围混用 |
| `S2` | `FIELD-DETAIL-03~04` | 这组该切成几镜，每镜对应哪段正文 | 先搭 detail skeleton | 先写别的字段、后猜镜数 |
| `S3` | `FIELD-DETAIL-05` | 角色为什么这么演 | 填 `角色表现` | 表演写成机位说明 |
| `S4` | `FIELD-DETAIL-06` | 压力和空气从哪里来 | 填 `氛围表现` | 只剩形容词 |
| `S5-S6` | `FIELD-DETAIL-07` | 光影和镜头运动如何服务这组戏 | 填 `摄影表现 / 运镜手法` | 反向推翻骨架 |
| `S7` | `FIELD-DETAIL-08` | 观众怎么被顺滑带到下一拍 | 填 `转场特效` | 修饰盖过戏剧 |
| `S8` | `FIELD-DETAIL-01~08` | 是否可被下游直接消费 | 跑 validator 并写 report | 无法复验 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| `FIELD-DETAIL-01` | `meta` 完整、数值正确 | `FAIL-DETAIL-01` | `S1` |
| `FIELD-DETAIL-02` | `global` 与上游 seed 含义一致 | `FAIL-DETAIL-02` | `S1` |
| `FIELD-DETAIL-03` | `分镜数` 与 `分镜列表` 对齐 | `FAIL-DETAIL-03` | `S2` |
| `FIELD-DETAIL-04` | 镜级骨架完整且可拍 | `FAIL-DETAIL-04` | `S2` |
| `FIELD-DETAIL-05` | `角色表现` 可演且不越权 | `FAIL-DETAIL-05` | `S3` |
| `FIELD-DETAIL-06` | `氛围表现` 有环境承载与层次 | `FAIL-DETAIL-06` | `S4` |
| `FIELD-DETAIL-07` | `摄影表现 / 运镜手法` 服务既有骨架 | `FAIL-DETAIL-07` | `S5-S6` |
| `FIELD-DETAIL-08` | `转场特效` 有收益且不过量 | `FAIL-DETAIL-08` | `S7` |

## Root-Cause Execution Contract (Mandatory)

出现以下任一症状，必须先修源层，而不是只补单次内容：

- 还没决定镜数就先写 `角色表现 / 摄影表现 / 运镜手法`
- 误把已移除的旧桥接字段当成当前 canonical 字段
- `分镜构图` 不是第一步，导致后续字段反向争夺镜数和正文切分点
- `episode_detail.json` 的字段口径与 validator / consumer 不一致
- 摄影字段又漂回旧命名
- 把 `剧本正文` 只留在组级，却没落到每镜
- 把 `主体锚定` 写成抽象评语，而不是场景/角色/道具锚点

固定上溯链：

`Symptom -> Direct Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

默认排查顺序：

1. `P1-分镜构图` 是否真的先行。
2. `_shared/episode_detail.json` 是否与当前 detail root 同构。
3. `references/能力通道图谱.yaml` 的字段边界是否被遵守。
4. `references/模板字段填写指南.md` 的写作要求是否被跳过。
5. `validation-report.md` 是否真实反映当前 root，而不是空泛自证。
6. `validation-report.md` 是否写出本轮学院派知识证据，而不是只说“已参考知识库”。

## Completion Gate

只有同时满足以下条件，`3-Detail` 才允许宣布完成：

1. `projects/aigc/<项目名>/3-Detail/第N集.json` 已落盘。
2. `1-分镜构图` 已先行锁定：
   - `detail.分镜数`
   - `分镜列表.<分镜ID>.时间`
   - `分镜列表.<分镜ID>.剧本正文`
   - `分镜列表.<分镜ID>.主体锚定`
   - `分镜列表.<分镜ID>.分镜构图`
3. 每镜都具备当前 canonical 字段对象。
4. `projects/aigc/<项目名>/3-Detail/validation-report.md` 已写回。
5. `validation-report.md` 已包含 `## Academy Knowledge Evidence`，并写明：
   - `knowledge_mode`
   - `knowledge_domain`
   - `selected_bundles`
   - `applied_passes`
   - `translation_targets`
6. `python3 .agents/skills/aigc/3-Detail/scripts/validate_stage_output.py projects/aigc/<项目名>/3-Detail/第N集.json` 通过，或显式记录阻塞。
