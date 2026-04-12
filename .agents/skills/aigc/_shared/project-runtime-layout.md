# AIGC Project Runtime Layout

本文件是 `aigc` 项目运行时目录的单一真源。

## Canonical Project Root

- 项目根目录：`projects/<项目名>/`
- 项目级核心真源：
  - `projects/<项目名>/team.yaml`
  - `projects/<项目名>/project_state.yaml`
- 项目级惰性治理工件（按需生成）：
  - `projects/<项目名>/governance-state.yaml`
  - `projects/<项目名>/mandate.yaml`
  - `projects/<项目名>/mission-brief.yaml`
  - `projects/<项目名>/route-plan.yaml`
  - `projects/<项目名>/preflight-verdict.yaml`
  - `projects/<项目名>/validation-report.md`
  - `projects/<项目名>/learning-record.md`

## Governance Snapshot Contract

- `projects/<项目名>/project_state.yaml`
  - 面向人和主路由的简明项目摘要。
  - 负责给出当前阶段、推荐下一入口和用户可读状态。
  - 是轻量初始化态的最低治理入口，`0-Init` 默认必须生成。
- `projects/<项目名>/governance-state.yaml`
  - 面向 `query / resume / review` 的结构化治理快照与断点真源。
  - 负责记录 `last_stable_checkpoint`、`resume_contract`、`artifact_status` 与 `review_bridge`。
  - 不是所有创作起盘都要首轮前置；当项目进入 `query / resume / review` 深治理、复杂多步执行或需要结构化断点时再生成即可。
- 模板真源：`.agents/skills/aigc/_shared/governance-state.template.yaml`

硬规则：

1. 对创作起盘来说，`team.yaml + project_state.yaml` 是项目根最低治理配置；不应为了首次初始化强绑整套 HARNESS 载体。
2. `project_state.yaml` 与 `governance-state.yaml` 不是二选一；前者是默认入口，后者是按需补上的结构化控制面。
3. 若 `query / resume / review` 需要判断断点、治理缺口或唯一回接入口，优先读取 `governance-state.yaml`；若其缺失，则退回 `project_state.yaml` 并显式说明当前处于轻量初始化态。
4. 不新增 `CHANGELOGS.md` 作为一级项目治理真源；如需时间序列说明，应由 `validation-report.md`、`learning-record.md` 与 `governance-state.yaml` 派生，而不是再造并行状态本。

## Canonical Runtime Roots

初始化阶段默认按“两层骨架”预建项目目录：

### Stage Roots

- `projects/<项目名>/0-Init/`
- `projects/<项目名>/Story/`
- `projects/<项目名>/1-Planning/`
- `projects/<项目名>/2-Global/`
- `projects/<项目名>/3-Detail/`
- `projects/<项目名>/4-Design/`
- `projects/<项目名>/5-Image/`
- `projects/<项目名>/6-Video/`
- `projects/<项目名>/7-Cut/`

### Active Child Skeleton

这里列的是 **项目 runtime 预建骨架**，不是 `.agents/skills/aigc/` 的技能目录镜像。

尤其对 `5-Image` 与 `6-Video`，当前仓存在两套并行但不等价的命名层：

1. 技能树执行入口层
   例如 `1-提示词蒸馏/分镜故事板`、`1-提示词蒸馏/首帧参照`、`2-视频生成`
2. 项目 runtime 落盘层
   例如 `projects/<项目名>/5-Image/分镜故事板/`、`projects/<项目名>/6-Video/全能参照/`、`projects/<项目名>/6-Video/生成任务/`

初始化预建目录时，必须服从 **runtime 落盘层**，而不是机械复制技能树中间 tranche 名称。

| 阶段 | 默认预建子路径 |
| --- | --- |
| `1-Planning` | `projects/<项目名>/1-Planning/1-分集/`、`projects/<项目名>/1-Planning/2-剧本/`、`projects/<项目名>/1-Planning/3-分组/` |
| `4-Design` | `projects/<项目名>/4-Design/1-场景/1-清单/`、`2-设计/`、`3-面板/`；`projects/<项目名>/4-Design/2-角色/1-清单/`、`2-设计/`、`3-面板/`；`projects/<项目名>/4-Design/3-服装/1-清单/`、`2-设计/`、`3-面板/`；`projects/<项目名>/4-Design/4-道具/1-清单/`、`2-设计/`、`3-面板/` |
| `5-Image` | `projects/<项目名>/5-Image/分镜故事板/`、`projects/<项目名>/5-Image/分镜帧/`、`projects/<项目名>/5-Image/漫画/` |
| `6-Video` | `projects/<项目名>/6-Video/全能参照/`、`projects/<项目名>/6-Video/首帧参照/`、`projects/<项目名>/6-Video/生成任务/` |

### Skill Tree To Runtime Mapping

| 技能树 active 路径 | 项目 runtime 预建路径 | 说明 |
| --- | --- | --- |
| `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板` | `projects/<项目名>/5-Image/分镜故事板/` | `1-提示词蒸馏` 是父级执行 tranche，不是 runtime 目录名 |
| `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜帧` | `projects/<项目名>/5-Image/分镜帧/` | 叶子技能名直接投影为业务落盘名 |
| `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画` | `projects/<项目名>/5-Image/漫画/` | 同上 |
| `.agents/skills/aigc/5-Image/2-图像生成` | 暂不在 `0-Init` 默认预建列表中 | 当前共享真源尚未声明其稳定 runtime landing，不能先造路径真源 |
| `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照` | `projects/<项目名>/6-Video/全能参照/` | `1-提示词蒸馏` 只属于技能树执行层 |
| `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照` | `projects/<项目名>/6-Video/首帧参照/` | 同上 |
| `.agents/skills/aigc/6-Video/2-视频生成` | `projects/<项目名>/6-Video/生成任务/` | runtime 采用业务语义落点，不沿用技能树编号名 |

硬规则：

1. 技能阶段名必须跟随当前技能树真实目录，如 `1-Planning`、`3-Detail`、`5-Image`、`6-Video`、`7-Cut`；不得再混用 `1-规划 / 3-明细 / 5-画面 / 6-视频 / 7-后期` 作为阶段标识。
2. 项目运行时目录必须以本文件为准；当前 `1-Planning / 2-Global / 4-Design` 保留阶段名，`编导 / 画面 / 视频 / 后期` 采用业务语义目录。
3. 初始化预建的 child skeleton 必须跟随“当前已建 active 子技能的 canonical landing”，而不是机械照抄技能文件系统中间层名称；因此项目 runtime 预建 `5-Image/分镜故事板/`，而不是 `5-Image/1-提示词蒸馏/`。
4. 预建目录骨架不等于提前生成阶段产物；它只负责锁定路径与防漂移。
5. `0-Init`、根 `aigc/SKILL.md`、各阶段 `SKILL.md` 与审计脚本若同时提到“当前 active 子路径”，必须明确标注自己说的是“技能树执行层”还是“项目 runtime 落盘层”。
6. 任何阶段合同、模板、脚本或项目文件若引用运行时路径，都必须以本文件为唯一真源，不得各自保留旧的 `主体/` 旧口径或其他平行目录名。

## Phase To Runtime Mapping

| 技能阶段 | runtime 根目录 | 说明 |
| --- | --- | --- |
| `0-Init` | `projects/<项目名>/0-Init/` | 初始化合同、项目种子与根布局预建 |
| `Story` | `projects/<项目名>/Story/` | 项目级故事主源与辅助源材料落点，由 `0-Init/story-source-manifest.yaml` 统一登记 |
| `1-Planning` | `projects/<项目名>/1-Planning/` | 规划阶段父级合同、阶段验收与多数规划子路径落点；`1-分集` 将故事正文收束到 `2-剧本/第N集.md`，并为后续 `2-Global` 预留 `bootstrap_output` 目标路径 |
| `2-Global` | `projects/<项目名>/2-Global/` | 负责全局风格、类型指导与导演意图三份 Markdown 真源 |
| `3-Detail` | `projects/<项目名>/3-Detail/` | 消费 `2-Global/*.md` 后，围绕 `第N集.json` 做字段分属 patch-in-place |
| `4-Design` | `projects/<项目名>/4-Design/` | design-source 阶段产物 |
| `5-Image` | `projects/<项目名>/5-Image/` | 画面阶段；当前 active 子路径是 `分镜故事板 / 分镜帧 / 漫画` |
| `6-Video` | `projects/<项目名>/6-Video/` | 视频阶段；当前 active 子路径是 `全能参照 / 首帧参照 / 生成任务` |
| `7-Cut` | `projects/<项目名>/7-Cut/` | 后期阶段 |

## Canonical Director Root File

- 唯一主文件：`projects/<项目名>/3-Detail/第N集.json`
- shared schema：`.agents/skills/aigc/_shared/director_episode_output.schema.json`
- bootstrap template：`.agents/skills/aigc/_shared/director_episode_bootstrap.template.json`

## Ownership Contract

1. `1-Planning` 只负责在 `projects/<项目名>/1-Planning/2-剧本/第N集.md` 中登记每集 `bootstrap_output` 目标路径与 `source_profile` handoff，不在规划阶段默认创建 `projects/<项目名>/2-Global/*.md` 或 `projects/<项目名>/3-Detail/第N集.json`。
2. `2-Global` 负责写入 `projects/<项目名>/2-Global/全局风格.md`、`类型指导.md` 与 `导演意图.md`，但不创建 `projects/<项目名>/3-Detail/第N集.json`。
3. `3-Detail` 在首次进入且检测到 `projects/<项目名>/3-Detail/第N集.json` 不存在时，负责基于 `.agents/skills/aigc/_shared/director_episode_bootstrap.template.json` 自动创建根文件。
4. `3-Detail` 后续只允许围绕同一份 `第N集.json` 做字段分属 patch-in-place。
5. 下游阶段若消费编导数据，默认读取 `projects/<项目名>/3-Detail/第N集.json`，不得私造第二份 episode/group/shot 根文件。
