# AIGC Project Runtime Layout

本文件是 `aigc` 项目运行时目录的单一真源。

## Canonical Project Root

- 项目根目录：`projects/<项目名>/`
- 项目级治理工件：
  - `projects/<项目名>/team.yaml`
  - `projects/<项目名>/project_state.yaml`
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
- `projects/<项目名>/governance-state.yaml`
  - 面向 `query / resume / review` 的结构化治理快照与断点真源。
  - 负责记录 `last_stable_checkpoint`、`resume_contract`、`artifact_status` 与 `review_bridge`。
  - 首次生成责任在 `0-Init`，后续由根 `aigc`、`resume/`、`review/` 与相关阶段按需同步更新。
- 模板真源：`.agents/skills/aigc/_shared/governance-state.template.yaml`

硬规则：

1. `project_state.yaml` 与 `governance-state.yaml` 不是二选一，而是“人类摘要 + 结构化控制面”的分工组合。
2. 若 `query / resume / review` 需要判断断点、治理缺口或唯一回接入口，默认优先读取 `governance-state.yaml`，再回看 `project_state.yaml`。
3. 不新增 `CHANGELOGS.md` 作为一级项目治理真源；如需时间序列说明，应由 `validation-report.md`、`learning-record.md` 与 `governance-state.yaml` 派生，而不是再造并行状态本。

## Canonical Runtime Roots

初始化阶段可以一次性预建以下目录：

- `projects/<项目名>/Init/`
- `projects/<项目名>/故事/`
- `projects/<项目名>/规划/`
- `projects/<项目名>/编导/`
- `projects/<项目名>/主体/`
- `projects/<项目名>/画面/`
- `projects/<项目名>/视频/`
- `projects/<项目名>/后期/`

硬规则：

1. 技能阶段名可以保留序号，如 `1-规划`、`4-主体`、`5-画面`。
2. 项目运行时目录默认去掉阶段序号，统一使用业务语义目录：`规划 / 主体 / 画面`。
3. 任何阶段合同、模板、脚本或项目文件若引用运行时路径，都必须以本文件为唯一真源，不得各自保留旧的带序号目录名。

## Phase To Runtime Mapping

| 技能阶段 | runtime 根目录 | 说明 |
| --- | --- | --- |
| `0-Init` | `projects/<项目名>/Init/` | 初始化合同、项目种子与根布局预建 |
| `故事` | `projects/<项目名>/故事/` | 项目级故事主源与辅助源材料落点，由 `Init/story-source-manifest.yaml` 统一登记 |
| `1-规划` | `projects/<项目名>/规划/` | 规划阶段父级合同、阶段验收与多数规划子路径落点；仅 `1-分集` 继续在 `Init/` 写 bootstrap 产物 |
| `2-组间` | `projects/<项目名>/编导/` | 与 `3-明细` 共享同一份 `第N集.json` 主文件 |
| `3-明细` | `projects/<项目名>/编导/` | 围绕同一份 `第N集.json` 做字段分属 patch-in-place |
| `4-主体` | `projects/<项目名>/主体/` | 主体阶段产物 |
| `5-画面` | `projects/<项目名>/画面/` | 画面阶段，可含子目录 |
| `6-视频` | `projects/<项目名>/视频/` | 视频阶段，可含子目录 |
| `7-后期` | `projects/<项目名>/后期/` | 后期阶段 |

## Canonical Director Root File

- 唯一主文件：`projects/<项目名>/编导/第N集.json`
- shared schema：`.agents/skills/aigc/_shared/director_episode_output.schema.json`
- bootstrap template：`.agents/skills/aigc/_shared/director_episode_bootstrap.template.json`

## Ownership Contract

1. `1-规划/subtypes/1-分集` 在集数与集标识确定后，负责首次创建 `projects/<项目名>/编导/第N集.json` 空壳文件。
2. `2-组间` 与 `3-明细` 后续都只允许围绕同一份 `第N集.json` 做字段分属 patch-in-place。
3. `2-组间` 负责优先补齐 `分镜组列表[].组间设计` 等组级字段。
4. `3-明细` 负责继续补齐 `分镜组列表[].分镜明细[]` 等镜级字段。
5. 下游阶段若消费编导数据，默认读取 `projects/<项目名>/编导/第N集.json`，不得私造第二份 episode/group/shot 根文件。
