# AIGC Project Runtime Layout

本文件是 `aigc` 项目运行时目录的单一真源。

## Canonical Project Root

- 项目根目录：`projects/<项目名>/`
- 项目级治理工件：
  - `projects/<项目名>/team.yaml`
  - `projects/<项目名>/project_state.yaml`
  - `projects/<项目名>/mandate.yaml`
  - `projects/<项目名>/mission-brief.yaml`
  - `projects/<项目名>/route-plan.yaml`
  - `projects/<项目名>/preflight-verdict.yaml`
  - `projects/<项目名>/validation-report.md`
  - `projects/<项目名>/learning-record.md`

## Canonical Runtime Roots

初始化阶段可以一次性预建以下目录：

- `projects/<项目名>/Init/`
- `projects/<项目名>/1-规划/`
- `projects/<项目名>/编导/`
- `projects/<项目名>/4-主体/`
- `projects/<项目名>/5-画面/`
- `projects/<项目名>/视频/`
- `projects/<项目名>/后期/`

## Phase To Runtime Mapping

| 技能阶段 | runtime 根目录 | 说明 |
| --- | --- | --- |
| `0-Init` | `projects/<项目名>/Init/` | 初始化合同、项目种子与根布局预建 |
| `1-规划` | `projects/<项目名>/1-规划/` | 规划阶段父级合同、阶段验收与多数规划子路径落点；仅 `1-分集` 继续在 `Init/` 写 bootstrap 产物 |
| `2-组间` | `projects/<项目名>/编导/` | 与 `3-明细` 共享同一份 `第N集.json` 主文件 |
| `3-明细` | `projects/<项目名>/编导/` | 围绕同一份 `第N集.json` 做字段分属 patch-in-place |
| `4-主体` | `projects/<项目名>/4-主体/` | 主体阶段产物 |
| `5-画面` | `projects/<项目名>/5-画面/` | 画面阶段，可含子目录 |
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
