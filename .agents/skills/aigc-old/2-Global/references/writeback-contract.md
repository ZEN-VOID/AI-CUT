# 2-Global Writeback Contract

## Purpose

本文件定义当前 `2-Global` 单技能模式下的字段填写真源。

- `2-Global` 在根技能内完成字段填写
- creative 输出只有一个：
  - `projects/aigc/<项目名>/2-Global/第N集.json`

## Canonical Carriers

### 1. canonical episode root

- 路径：
  - `projects/aigc/<项目名>/2-Global/第N集.json`
- 作用：
  - 唯一创作业务真源
  - 承载 `meta + project_global + groups[].global`

### 2. stage validation report

- 路径：
  - `projects/aigc/<项目名>/2-Global/validation-report.md`
- 作用：
  - 记录本轮验收、阻塞、根因上溯和 closure
  - 治理侧车，不是创作业务输出物

### 3. removed legacy projections

- 典型路径：
  - `projects/aigc/<项目名>/2-Global/全局风格.md`
  - `projects/aigc/<项目名>/2-Global/全集类型元素.md`
  - `projects/aigc/<项目名>/2-Global/分组类型元素.md`
  - `projects/aigc/<项目名>/2-Global/导演意图.md`
- 作用：
  - 新执行不得生成或更新
  - 历史项目中仅作为 legacy artifact
  - 组级类型信号直接读取 `groups[].global.类型元素`

## Hard Rules

1. 所有 pass 都直接写向当前集 `第N集.json`，不再先写 Markdown 真源再回收；`templates/episode-root.template.json` 只作为模板。
2. 项目级字段统一进入 `project_global`，组级字段统一进入 `groups[].global`。
3. `groups[].global.剧本正文` 必须完整保留命中组正文。
4. 新执行不得生成 Markdown 输出；历史迁移若派生 Markdown，只能由已确认 JSON 派生，不得反向夺取写回权。

## Default Pass Ownership

| pass | 直接写入字段 |
| --- | --- |
| `1-项目级风格` | `project_global.全局风格`、`groups[].global.全局风格` |
| `2-项目级类型` | `project_global.全集类型元素` |
| `3-组级类型` | `groups[].global.类型元素` |
| `4-导演意图` | `groups[].global.导演意图` |
| `5-组正文入壳` | `groups[].global.剧本正文`、`meta.组数`、`meta.总时长` |

## Validation Hooks

- stage 主校验入口：
  - `.agents/skills/aigc/2-Global/references/writeback-contract.md`
- shared handoff 合同：
  - `.agents/skills/aigc/_shared/group_design_seed_contract.md`
