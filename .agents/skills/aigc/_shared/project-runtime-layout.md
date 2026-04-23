# AIGC Project Runtime Layout

本文件是 `aigc` 项目运行时目录的单一真源。

## Canonical Project Root

- 项目根目录：`projects/aigc/<项目名>/`
- 项目级核心真源：
  - `projects/aigc/<项目名>/team.yaml`
  - `projects/aigc/<项目名>/STATE.json`
- 项目级创作记忆载体：
  - `projects/aigc/<项目名>/MEMORY.md`
- 项目级共享附加上下文根：
  - `projects/aigc/<项目名>/CONTEXT/`
- 项目级补充时间序载体：
  - `projects/aigc/<项目名>/CHANGELOG.md`
- 项目级辅助资产库：
  - `projects/aigc/<项目名>/Assets/`
  - `projects/aigc/<项目名>/Assets/角色/`
  - `projects/aigc/<项目名>/Assets/道具/`
  - `projects/aigc/<项目名>/Assets/场景/`
  - `projects/aigc/<项目名>/Assets/服装/`
  - `projects/aigc/<项目名>/Assets/分镜画板/分镜帧/`
  - `projects/aigc/<项目名>/Assets/分镜画板/分镜故事板/`
  - `projects/aigc/<项目名>/Assets/分镜画板/漫画/`
- 项目级惰性治理工件（按需生成）：
  - `projects/aigc/<项目名>/governance-state.yaml`
  - `projects/aigc/<项目名>/mandate.yaml`
  - `projects/aigc/<项目名>/mission-brief.yaml`
  - `projects/aigc/<项目名>/route-plan.yaml`
  - `projects/aigc/<项目名>/preflight-verdict.yaml`
  - `projects/aigc/<项目名>/validation-report.md`
  - `projects/aigc/<项目名>/learning-record.md`
- 项目级卫星审计根（按需生成）：
  - `projects/aigc/<项目名>/review/`

## Governance Snapshot Contract

- `projects/aigc/<项目名>/STATE.json`
  - 面向人和主路由的简明项目摘要。
  - 负责给出当前阶段、推荐下一入口和用户可读状态。
  - 是轻量初始化态的最低治理入口，`0-Init` 默认必须生成。
- `projects/aigc/<项目名>/governance-state.yaml`
  - 面向 `query / resume` 与根 `aigc` 高风险治理 gate 的结构化治理快照与断点真源。
  - 负责记录 `last_stable_checkpoint`、`resume_contract`、`artifact_status`、`review_bridge` 与按需存在的 `reset_bridge`。
  - 不是所有创作起盘都要首轮前置；当项目进入 `query / resume` 深治理、复杂多步执行或需要结构化断点时再生成即可。
- 模板真源：`.agents/skills/aigc/_shared/governance-state.template.yaml`

硬规则：

1. 对创作起盘来说，`team.yaml + STATE.json` 是项目根最低治理配置；不应为了首次初始化强绑整套 HARNESS 载体。
2. `STATE.json` 与 `governance-state.yaml` 不是二选一；前者是默认入口，后者是按需补上的结构化控制面。
3. 若 `query / resume` 或根 `aigc` 的高风险治理 gate 需要判断断点、治理缺口或唯一回接入口，优先读取 `governance-state.yaml`；若其缺失，则退回 `STATE.json` 并显式说明当前处于轻量初始化态。
4. `Assets/` 是项目级辅助资产库，不是阶段业务真源；它用于沉淀可复用参考图、选角图、道具图、场景图和分镜画板资产，不替代 `4-Design/`、`5-Image/`、`6-Video/` 的 canonical 输出。
5. `projects/aigc/<项目名>/CHANGELOG.md` 是项目级时间序记录入口，`0-Init` 默认应创建它；它可记录结构调整、重要阶段切换与长期可追踪变更，但不是治理真源或状态本。
6. `projects/aigc/<项目名>/MEMORY.md` 是项目级创作记忆载体；`.agents/skills/aigc` 体系内的阶段任务一旦锁定项目根，应优先读取它来获取当前项目已确认的偏好、口味、特殊元素与长期要求。
7. `projects/aigc/<项目名>/CONTEXT/` 是项目级共享附加上下文根；`.agents/skills/aigc` 体系内的阶段任务一旦锁定项目根，应按需读取其中相关文件。
8. `MEMORY.md` 不承载治理断点、路线状态、审计结论或 skill 经验；这些内容仍分别属于 `STATE.json` / `governance-state.yaml` / `validation-report.md` / 对应 skill `CONTEXT.md`。
9. 不新增 `CHANGELOGS.md` 作为一级项目治理真源；如需时间序列说明，应优先追加到项目根 `CHANGELOG.md` 或由 `validation-report.md`、`learning-record.md` 与 `governance-state.yaml` 派生，而不是再造并行状态本。
10. 若项目经历“回到初始化态重来”的 `rebootstrap`，应把保留/归档/失效边界记录到 `governance-state.yaml.reset_bridge`，而不是让 `query / resume` 靠目录猜当前是否仍在旧周期。
11. `projects/aigc/<项目名>/review/` 是 package-level 审计运行时根；它承载 `checkpoint / stage / release` aggregate review packets，不替代阶段 `validation-report.md`。
12. `projects/aigc/<项目名>/review/` 同级还可派生 `*.review.fact-pack.json`、`*.review.repair.json`、`*.review.review.md` 与 `.code-reviewer/` provider sidecars；这些都服务 `review` 聚合与返工闭环，不是新的阶段业务真源。
13. 当 `governance-state.yaml` 已存在时，`review` runner 应同步更新 `review_bridge.latest_review_*` 与 `resume_contract.required_repairs`，让 `query / resume` 与后续治理入口读取同一份 repair bridge。

## Canonical Runtime Roots

初始化阶段默认按“两层骨架”预建项目目录：

### Stage Roots

- `projects/aigc/<项目名>/0-Init/`
- `projects/aigc/<项目名>/Story/`
- `projects/aigc/<项目名>/CONTEXT/`
- `projects/aigc/<项目名>/Assets/`
- `projects/aigc/<项目名>/1-Planning/`
- `projects/aigc/<项目名>/2-Global/`
- `projects/aigc/<项目名>/3-Detail/`
- `projects/aigc/<项目名>/4-Design/`
- `projects/aigc/<项目名>/5-Image/`
- `projects/aigc/<项目名>/6-Video/`
- `projects/aigc/<项目名>/7-Cut/`

### Satellite Runtime Roots

- `projects/aigc/<项目名>/review/`

### Active Child Skeleton

这里列的是 **项目 runtime 预建骨架**，不是 `.agents/skills/aigc/` 的技能目录镜像。

尤其对 `3-Detail`、`4-Design`、`5-Image` 与 `6-Video`，当前仓存在“技能树执行层”和“项目 runtime 落盘层”不完全同构的情况：

1. 技能树执行入口层
   例如 `3-Detail` 根技能内的固定 pass、`1-清单 / 2-设计 / 3-面板`、`1-提示词蒸馏/分镜故事板`、`2-参照引用`、`3-图像生成`、`1-提示词蒸馏/首帧参照`、`2-参照引用`、`3-视频生成`
2. 项目 runtime 落盘层
   例如 `projects/aigc/<项目名>/2-Global/`、`projects/aigc/<项目名>/3-Detail/`、`projects/aigc/<项目名>/4-Design/角色/1-清单/`、`projects/aigc/<项目名>/5-Image/分镜故事板/`、`projects/aigc/<项目名>/5-Image/2-参照引用/`、`projects/aigc/<项目名>/5-Image/3-图像生成/`、`projects/aigc/<项目名>/6-Video/生成任务/`

初始化预建目录时，必须服从 **runtime 落盘层**，而不是机械复制技能树中间 tranche 名称。

| 阶段 | 默认预建子路径 |
| --- | --- |
| `Assets` | `projects/aigc/<项目名>/Assets/角色/`、`projects/aigc/<项目名>/Assets/道具/`、`projects/aigc/<项目名>/Assets/场景/`、`projects/aigc/<项目名>/Assets/服装/`、`projects/aigc/<项目名>/Assets/分镜画板/分镜帧/`、`projects/aigc/<项目名>/Assets/分镜画板/分镜故事板/`、`projects/aigc/<项目名>/Assets/分镜画板/漫画/` |
| `1-Planning` | `projects/aigc/<项目名>/1-Planning/1-分集/`、`projects/aigc/<项目名>/1-Planning/2-格式/`、`projects/aigc/<项目名>/1-Planning/3-分组/` |
| `2-Global` | `projects/aigc/<项目名>/2-Global/`；阶段执行后根层写入 `episode_root.json` 与 `validation-report.md`，旧 Markdown 仅作兼容投影 |
| `3-Detail` | `projects/aigc/<项目名>/3-Detail/` |
| `4-Design` | 当前初始化只预建 active leaf：`projects/aigc/<项目名>/4-Design/场景/1-清单/`、`2-设计/`、`3-面板/`；`projects/aigc/<项目名>/4-Design/角色/1-清单/`、`2-设计/`、`3-面板/`；`projects/aigc/<项目名>/4-Design/道具/1-清单/`、`2-设计/`、`3-面板/`。`服装` 仍是类目宇宙的一部分，但 source leaf 尚未迁回 active，初始化不得预建 `4-Design/服装/*` 伪 active 目录。 |
| `5-Image` | `projects/aigc/<项目名>/5-Image/分镜故事板/`、`projects/aigc/<项目名>/5-Image/分镜帧/`、`projects/aigc/<项目名>/5-Image/2-参照引用/`、`projects/aigc/<项目名>/5-Image/3-图像生成/` |
| `6-Video` | `projects/aigc/<项目名>/6-Video/全能参照/`、`projects/aigc/<项目名>/6-Video/首帧参照/`、`projects/aigc/<项目名>/6-Video/2-参照引用/`、`projects/aigc/<项目名>/6-Video/生成任务/` |
| `review` | 懒生成目录；正式路径为 `projects/aigc/<项目名>/review/checkpoints/`、`projects/aigc/<项目名>/review/stages/`、`projects/aigc/<项目名>/review/releases/` |

### Skill Tree To Runtime Mapping

| 技能树 active 路径 | 项目 runtime 预建路径 | 说明 |
| --- | --- | --- |
| `.agents/skills/aigc/3-Detail` | `projects/aigc/<项目名>/3-Detail/` | 当前 `3-Detail` 已收束为单根技能；`1-分镜构图 -> 其余字段 pass` 在根技能内部完成，不再把 `1-水月 / 2-镜花` 当作 runtime 预建子目录 |
| `.agents/skills/aigc/4-Design/1-清单/{场景,角色,道具}` | `projects/aigc/<项目名>/4-Design/{场景,角色,道具}/1-清单/` | `1-清单` 是父级执行 tranche，runtime 按 active domain-first 业务目录落盘 |
| `.agents/skills/aigc/4-Design/2-设计/{场景,角色,道具}` | `projects/aigc/<项目名>/4-Design/{场景,角色,道具}/2-设计/` | `2-设计` 是父级执行 tranche，runtime 按 active domain-first 业务目录落盘 |
| `.agents/skills/aigc/4-Design/3-面板/{场景,角色,道具}` | `projects/aigc/<项目名>/4-Design/{场景,角色,道具}/3-面板/` | `3-面板` 是父级执行 tranche，runtime 按 active domain-first 业务目录落盘 |
| `.agents/skills/aigc/4-Design/*/服装` | 暂不预建 `projects/aigc/<项目名>/4-Design/服装/*` | `服装` 当前仍是 4-Design 类目宇宙和 Assets 资产库类目，但 source leaf 未迁回 active；初始化不得把 pending sibling 投影成 runtime active 目录 |
| `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板` | `projects/aigc/<项目名>/5-Image/分镜故事板/` | `1-提示词蒸馏` 是父级执行 tranche，不是 runtime 目录名 |
| `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜帧` | `projects/aigc/<项目名>/5-Image/分镜帧/` | 叶子技能名直接投影为业务落盘名 |
| `.agents/skills/aigc/5-Image/2-参照引用` | `projects/aigc/<项目名>/5-Image/2-参照引用/` | provider/mode/source/episode 目录在执行时下钻创建；初始化只预建稳定根目录 |
| `.agents/skills/aigc/5-Image/3-图像生成` | `projects/aigc/<项目名>/5-Image/3-图像生成/` | provider/source/episode 目录在执行时下钻创建；`submit-plan`、`submit-brief` 与真实输出图像同目录落盘 |
| `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照` | `projects/aigc/<项目名>/6-Video/全能参照/` | `1-提示词蒸馏` 只属于技能树执行层 |
| `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照` | `projects/aigc/<项目名>/6-Video/首帧参照/` | 同上 |
| `.agents/skills/aigc/6-Video/2-参照引用` | `projects/aigc/<项目名>/6-Video/2-参照引用/` | mode/episode 目录在执行时下钻创建；初始化只预建稳定根目录 |
| `.agents/skills/aigc/6-Video/3-视频生成` | `projects/aigc/<项目名>/6-Video/生成任务/` | runtime 采用业务语义落点，不沿用技能树编号名 |
| `.agents/skills/aigc/review` | `projects/aigc/<项目名>/review/` | review 是卫星技能，不并入主阶段链；其 aggregate packet 分为 `checkpoints / stages / releases` 三层落点 |

硬规则：

1. 技能阶段名必须跟随当前技能树真实目录，如 `1-Planning`、`3-Detail`、`5-Image`、`6-Video`、`7-Cut`；不得再混用 `1-规划 / 3-明细 / 5-画面 / 6-视频 / 7-后期` 作为阶段标识。
2. 项目运行时目录必须以本文件为准；当前 `1-Planning / 2-Global / 4-Design` 保留阶段名，`Assets` 作为项目级辅助资产层，`编导 / 画面 / 视频 / 后期` 采用业务语义目录。
3. 初始化预建的 child skeleton 必须跟随“当前已建 active 子技能的 canonical landing”，而不是机械照抄技能文件系统中间层名称；因此项目 runtime 对 `3-Detail` 只预建阶段根目录 `3-Detail/`，而不是误造旧的执行层投影目录。
4. `Assets/分镜画板/*` 与 `5-Image/*` 名称相近但职责不同：前者是可复用资产库，后者是阶段业务输出根；不得把两者混为同一真源。
5. 预建目录骨架不等于提前生成阶段产物；它只负责锁定路径与防漂移。
6. `0-Init`、根 `aigc/SKILL.md`、各阶段 `SKILL.md` 与审计脚本若同时提到“当前 active 子路径”，必须明确标注自己说的是“技能树执行层”还是“项目 runtime 落盘层”。
7. 任何阶段合同、模板、脚本或项目文件若引用运行时路径，都必须以本文件为唯一真源，不得各自保留旧的 `主体/` 旧口径或其他平行目录名。

## Phase To Runtime Mapping

| 技能阶段 | runtime 根目录 | 说明 |
| --- | --- | --- |
| `0-Init` | `projects/aigc/<项目名>/0-Init/` | 初始化合同、项目种子与根布局预建 |
| `Story` | `projects/aigc/<项目名>/Story/` | 项目级故事主源与辅助源材料落点，由 `0-Init/story-source-manifest.yaml` 统一登记 |
| `1-Planning` | `projects/aigc/<项目名>/1-Planning/` | 规划阶段父级合同、阶段验收与多数规划子路径落点；`1-分集` 将故事正文收束到 `2-格式/第N集.md`，并为后续 `2-Global` 预留 `bootstrap_output` 目标路径 |
| `2-Global` | `projects/aigc/<项目名>/2-Global/` | 负责围绕 `.agents/skills/aigc/2-Global/_shared/episode_root.json` 直接填好 `episode_root.json`，写出 `meta + project_global + groups[].global` 作为组级 episode seed root |
| `3-Detail` | `projects/aigc/<项目名>/3-Detail/` | 读取 `2-Global/episode_root.json` 作为组级前置 seed，并在本阶段自己的 detail root 上首次生成 `detail.分镜数` 与每镜 `时间 / 剧本正文 / 主体锚定 / 分镜构图` 及其余镜级字段 |
| `4-Design` | `projects/aigc/<项目名>/4-Design/` | design-source 阶段产物 |
| `5-Image` | `projects/aigc/<项目名>/5-Image/` | 画面阶段；当前 active 链路是 `分镜故事板 / 分镜帧 -> 2-参照引用 -> 3-图像生成`；漫画页诉求回接 repo-local `comic` workflow |
| `6-Video` | `projects/aigc/<项目名>/6-Video/` | 视频阶段；当前 active 子路径是 `全能参照 / 首帧参照 / 2-参照引用 / 生成任务` |
| `7-Cut` | `projects/aigc/<项目名>/7-Cut/` | 后期阶段 |

## Canonical Director Root Files

- `2-Global` episode seed root：`projects/aigc/<项目名>/2-Global/episode_root.json`
- `2-Global` seed template：`.agents/skills/aigc/2-Global/_shared/episode_root.json`
- `2-Global -> 3-Detail` handoff contract：`.agents/skills/aigc/_shared/group_design_seed_contract.md`
- `3-Detail` detailed root：`projects/aigc/<项目名>/3-Detail/第N集.json`
- `3-Detail` detail template：`.agents/skills/aigc/3-Detail/_shared/episode_detail.json`（默认组织为 `meta + groups[].global/detail.分镜列表`；运行时建议继续保留继承自 `2-Global` 的 `groups[].global.剧本正文`）
- `3-Detail` shared compatibility schema：`.agents/skills/aigc/_shared/director_episode_output.schema.json`
- phase transition reading rule：`2-Global` 先稳定围绕模板写出 `episode_root.json`，`3-Detail` 再在自己的 detail root 中补齐 finer-grained shot-level 字段；下游默认按结构完整性判定是否 ready，而不再把 `document_phase` 当 canonical 字段真源。

## Ownership Contract

1. `1-Planning` 只负责在 `projects/aigc/<项目名>/1-Planning/2-格式/第N集.md` 中登记每集 `bootstrap_output` 目标路径与 `source_profile` handoff，不在规划阶段默认创建 `2-Global` 兼容 Markdown。
2. `2-Global` 负责以 `.agents/skills/aigc/2-Global/_shared/episode_root.json` 为模板直接写入 `projects/aigc/<项目名>/2-Global/episode_root.json`，并同步写回 `projects/aigc/<项目名>/2-Global/validation-report.md`。
3. `2-Global` 在 episode seed root 不存在时，可基于 `.agents/skills/aigc/2-Global/_shared/episode_root.json` 创建同模板文件，并拥有 `meta`、`project_global` 与 `groups[].分镜组ID / global.剧本正文 / global.*` 的写入权。
4. `3-Detail` 后续只允许围绕自己阶段下的 `projects/aigc/<项目名>/3-Detail/第N集.json` 做 shot-level 与 detail-level patch-in-place，并默认继承 `projects/aigc/<项目名>/2-Global/episode_root.json` 中已有的组级 seed；本地 detail root 的默认壳与字段顺序以 `.agents/skills/aigc/3-Detail/_shared/episode_detail.json` 为准，逐镜实体默认组织在 `groups[].detail.分镜列表.<分镜ID>` 下。
5. 下游阶段若消费 detail 级编导数据，默认读取 `projects/aigc/<项目名>/3-Detail/第N集.json`；若消费 `2-Global` 的组级 seed，则读取 `projects/aigc/<项目名>/2-Global/episode_root.json`，不得混淆两者 truth role。
