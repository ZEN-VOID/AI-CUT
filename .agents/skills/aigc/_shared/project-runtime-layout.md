# AIGC Project Runtime Layout

本文件是 `aigc` 项目运行时目录的单一真源。

## Canonical Project Root

- 项目根目录：`projects/aigc/<项目名>/`
- 项目级核心真源：
  - `projects/aigc/<项目名>/team.yaml`
  - `projects/aigc/<项目名>/project_state.yaml`
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

## Governance Snapshot Contract

- `projects/aigc/<项目名>/project_state.yaml`
  - 面向人和主路由的简明项目摘要。
  - 负责给出当前阶段、推荐下一入口和用户可读状态。
  - 是轻量初始化态的最低治理入口，`0-Init` 默认必须生成。
- `projects/aigc/<项目名>/governance-state.yaml`
  - 面向 `query / resume / review` 的结构化治理快照与断点真源。
  - 负责记录 `last_stable_checkpoint`、`resume_contract`、`artifact_status`、`review_bridge` 与按需存在的 `reset_bridge`。
  - 不是所有创作起盘都要首轮前置；当项目进入 `query / resume / review` 深治理、复杂多步执行或需要结构化断点时再生成即可。
- 模板真源：`.agents/skills/aigc/_shared/governance-state.template.yaml`

硬规则：

1. 对创作起盘来说，`team.yaml + project_state.yaml` 是项目根最低治理配置；不应为了首次初始化强绑整套 HARNESS 载体。
2. `project_state.yaml` 与 `governance-state.yaml` 不是二选一；前者是默认入口，后者是按需补上的结构化控制面。
3. 若 `query / resume / review` 需要判断断点、治理缺口或唯一回接入口，优先读取 `governance-state.yaml`；若其缺失，则退回 `project_state.yaml` 并显式说明当前处于轻量初始化态。
4. `Assets/` 是项目级辅助资产库，不是阶段业务真源；它用于沉淀可复用参考图、选角图、道具图、场景图和分镜画板资产，不替代 `4-Design/`、`5-Image/`、`6-Video/` 的 canonical 输出。
5. 不新增 `CHANGELOGS.md` 作为一级项目治理真源；如需时间序列说明，应由 `validation-report.md`、`learning-record.md` 与 `governance-state.yaml` 派生，而不是再造并行状态本。
6. 若项目经历“回到初始化态重来”的 `rebootstrap`，应把保留/归档/失效边界记录到 `governance-state.yaml.reset_bridge`，而不是让 `query / resume` 靠目录猜当前是否仍在旧周期。

## Canonical Runtime Roots

初始化阶段默认按“两层骨架”预建项目目录：

### Stage Roots

- `projects/aigc/<项目名>/0-Init/`
- `projects/aigc/<项目名>/Story/`
- `projects/aigc/<项目名>/Assets/`
- `projects/aigc/<项目名>/1-Planning/`
- `projects/aigc/<项目名>/2-Global/`
- `projects/aigc/<项目名>/3-Detail/`
- `projects/aigc/<项目名>/4-Design/`
- `projects/aigc/<项目名>/5-Image/`
- `projects/aigc/<项目名>/6-Video/`
- `projects/aigc/<项目名>/7-Cut/`

### Active Child Skeleton

这里列的是 **项目 runtime 预建骨架**，不是 `.agents/skills/aigc/` 的技能目录镜像。

尤其对 `3-Detail`、`4-Design`、`5-Image` 与 `6-Video`，当前仓存在“技能树执行层”和“项目 runtime 落盘层”不完全同构的情况：

1. 技能树执行入口层
   例如 `水月 / 镜花`、`1-清单 / 2-设计 / 3-面板`、`1-提示词蒸馏/分镜故事板`、`2-参照引用`、`3-图像生成`、`1-提示词蒸馏/首帧参照`、`2-视频生成`
2. 项目 runtime 落盘层
   例如 `projects/aigc/<项目名>/2-Global/`、`projects/aigc/<项目名>/3-Detail/水月/`、`projects/aigc/<项目名>/4-Design/角色/1-清单/`、`projects/aigc/<项目名>/5-Image/分镜故事板/`、`projects/aigc/<项目名>/5-Image/2-参照引用/`、`projects/aigc/<项目名>/5-Image/3-图像生成/`、`projects/aigc/<项目名>/6-Video/生成任务/`

初始化预建目录时，必须服从 **runtime 落盘层**，而不是机械复制技能树中间 tranche 名称。

| 阶段 | 默认预建子路径 |
| --- | --- |
| `Assets` | `projects/aigc/<项目名>/Assets/角色/`、`projects/aigc/<项目名>/Assets/道具/`、`projects/aigc/<项目名>/Assets/场景/`、`projects/aigc/<项目名>/Assets/服装/`、`projects/aigc/<项目名>/Assets/分镜画板/分镜帧/`、`projects/aigc/<项目名>/Assets/分镜画板/分镜故事板/`、`projects/aigc/<项目名>/Assets/分镜画板/漫画/` |
| `1-Planning` | `projects/aigc/<项目名>/1-Planning/1-分集/`、`projects/aigc/<项目名>/1-Planning/2-格式/`、`projects/aigc/<项目名>/1-Planning/3-分组/` |
| `2-Global` | `projects/aigc/<项目名>/2-Global/`；阶段执行后根层写入 `全局风格.md`、`导演意图.md`、`全集类型元素.md`、`分组类型元素.md` |
| `3-Detail` | `projects/aigc/<项目名>/3-Detail/水月/`、`projects/aigc/<项目名>/3-Detail/镜花/` |
| `4-Design` | 当前初始化只预建 active leaf：`projects/aigc/<项目名>/4-Design/场景/1-清单/`、`2-设计/`、`3-面板/`；`projects/aigc/<项目名>/4-Design/角色/1-清单/`、`2-设计/`、`3-面板/`；`projects/aigc/<项目名>/4-Design/道具/1-清单/`、`2-设计/`、`3-面板/`。`服装` 仍是类目宇宙的一部分，但 source leaf 尚未迁回 active，初始化不得预建 `4-Design/服装/*` 伪 active 目录。 |
| `5-Image` | `projects/aigc/<项目名>/5-Image/分镜故事板/`、`projects/aigc/<项目名>/5-Image/分镜帧/`、`projects/aigc/<项目名>/5-Image/漫画/`、`projects/aigc/<项目名>/5-Image/2-参照引用/`、`projects/aigc/<项目名>/5-Image/3-图像生成/` |
| `6-Video` | `projects/aigc/<项目名>/6-Video/全能参照/`、`projects/aigc/<项目名>/6-Video/首帧参照/`、`projects/aigc/<项目名>/6-Video/生成任务/` |

### Skill Tree To Runtime Mapping

| 技能树 active 路径 | 项目 runtime 预建路径 | 说明 |
| --- | --- | --- |
| `.agents/skills/aigc/3-Detail/水月` | `projects/aigc/<项目名>/3-Detail/水月/` | 子技能名与 runtime sidecar 目录同名，可直接预建 |
| `.agents/skills/aigc/3-Detail/镜花` | `projects/aigc/<项目名>/3-Detail/镜花/` | 同上 |
| `.agents/skills/aigc/4-Design/1-清单/{场景,角色,道具}` | `projects/aigc/<项目名>/4-Design/{场景,角色,道具}/1-清单/` | `1-清单` 是父级执行 tranche，runtime 按 active domain-first 业务目录落盘 |
| `.agents/skills/aigc/4-Design/2-设计/{场景,角色,道具}` | `projects/aigc/<项目名>/4-Design/{场景,角色,道具}/2-设计/` | `2-设计` 是父级执行 tranche，runtime 按 active domain-first 业务目录落盘 |
| `.agents/skills/aigc/4-Design/3-面板/{场景,角色,道具}` | `projects/aigc/<项目名>/4-Design/{场景,角色,道具}/3-面板/` | `3-面板` 是父级执行 tranche，runtime 按 active domain-first 业务目录落盘 |
| `.agents/skills/aigc/4-Design/*/服装` | 暂不预建 `projects/aigc/<项目名>/4-Design/服装/*` | `服装` 当前仍是 4-Design 类目宇宙和 Assets 资产库类目，但 source leaf 未迁回 active；初始化不得把 pending sibling 投影成 runtime active 目录 |
| `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板` | `projects/aigc/<项目名>/5-Image/分镜故事板/` | `1-提示词蒸馏` 是父级执行 tranche，不是 runtime 目录名 |
| `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜帧` | `projects/aigc/<项目名>/5-Image/分镜帧/` | 叶子技能名直接投影为业务落盘名 |
| `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画` | `projects/aigc/<项目名>/5-Image/漫画/` | 同上 |
| `.agents/skills/aigc/5-Image/2-参照引用` | `projects/aigc/<项目名>/5-Image/2-参照引用/` | provider/mode/source/episode 目录在执行时下钻创建；初始化只预建稳定根目录 |
| `.agents/skills/aigc/5-Image/3-图像生成` | `projects/aigc/<项目名>/5-Image/3-图像生成/` | provider/source/episode 目录在执行时下钻创建；`submit-plan`、`submit-brief` 与真实输出图像同目录落盘 |
| `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照` | `projects/aigc/<项目名>/6-Video/全能参照/` | `1-提示词蒸馏` 只属于技能树执行层 |
| `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照` | `projects/aigc/<项目名>/6-Video/首帧参照/` | 同上 |
| `.agents/skills/aigc/6-Video/2-视频生成` | `projects/aigc/<项目名>/6-Video/生成任务/` | runtime 采用业务语义落点，不沿用技能树编号名 |

硬规则：

1. 技能阶段名必须跟随当前技能树真实目录，如 `1-Planning`、`3-Detail`、`5-Image`、`6-Video`、`7-Cut`；不得再混用 `1-规划 / 3-明细 / 5-画面 / 6-视频 / 7-后期` 作为阶段标识。
2. 项目运行时目录必须以本文件为准；当前 `1-Planning / 2-Global / 4-Design` 保留阶段名，`Assets` 作为项目级辅助资产层，`编导 / 画面 / 视频 / 后期` 采用业务语义目录。
3. 初始化预建的 child skeleton 必须跟随“当前已建 active 子技能的 canonical landing”，而不是机械照抄技能文件系统中间层名称；因此项目 runtime 预建 `3-Detail/水月/`、`5-Image/分镜故事板/`、`5-Image/2-参照引用/`、`5-Image/3-图像生成/`，而不是误造新的执行层投影目录。
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
| `2-Global` | `projects/aigc/<项目名>/2-Global/` | 负责全局风格、类型元素、设计元素与导演意图等项目级设计真源，并在阶段末段把 `组间设计 + 分镜切换` 写入 shared episode root |
| `3-Detail` | `projects/aigc/<项目名>/3-Detail/` | 优先继承 `2-Global` 已 seed 的 episode root，再围绕同一份 `第N集.json` 完成 shot-level patch-in-place |
| `4-Design` | `projects/aigc/<项目名>/4-Design/` | design-source 阶段产物 |
| `5-Image` | `projects/aigc/<项目名>/5-Image/` | 画面阶段；当前 active 链路是 `分镜故事板 / 分镜帧 / 漫画 -> 2-参照引用 -> 3-图像生成` |
| `6-Video` | `projects/aigc/<项目名>/6-Video/` | 视频阶段；当前 active 子路径是 `全能参照 / 首帧参照 / 生成任务` |
| `7-Cut` | `projects/aigc/<项目名>/7-Cut/` | 后期阶段 |

## Canonical Director Root File

- 唯一主文件：`projects/aigc/<项目名>/3-Detail/第N集.json`
- shared schema：`.agents/skills/aigc/_shared/director_episode_output.schema.json`
- bootstrap template：`.agents/skills/aigc/_shared/director_episode_bootstrap.template.json`
- group seed contract：`.agents/skills/aigc/_shared/group_design_seed_contract.md`
- phase transition reading rule：以同一 `第N集.json` 的 `metadata.document_phase` 读取 `directing_in_progress -> detail_in_progress -> ready` 的推进，不再依赖共享静态样例。

## Ownership Contract

1. `1-Planning` 只负责在 `projects/aigc/<项目名>/1-Planning/2-格式/第N集.md` 中登记每集 `bootstrap_output` 目标路径与 `source_profile` handoff，不在规划阶段默认创建 `projects/aigc/<项目名>/2-Global/*.md` 或 shared episode root。
2. `2-Global` 负责写入项目级设计真源；当前已稳定的 canonical 落点包括 `projects/aigc/<项目名>/2-Global/全局风格.md`、`projects/aigc/<项目名>/2-Global/全集类型元素.md`、`projects/aigc/<项目名>/2-Global/分组类型元素.md`、`projects/aigc/<项目名>/2-Global/导演意图.md`，并由组级导演链路在阶段末段把 `组间设计 + 分镜切换` 写入 `projects/aigc/<项目名>/3-Detail/第N集.json`。
3. `2-Global` 在 shared root 不存在时，可基于 `.agents/skills/aigc/_shared/director_episode_bootstrap.template.json` 创建同模版 episode root，但只拥有 `组间设计`、`分镜切换` 与相关 metadata 的写入权。
4. `3-Detail` 后续只允许围绕同一份 `第N集.json` 做 shot-level 与 detail-level patch-in-place，并默认继承已有 `组间设计 + 分镜切换`。
5. 下游阶段若消费编导数据，默认读取 `projects/aigc/<项目名>/3-Detail/第N集.json`，不得私造第二份 episode/group/shot 根文件。
