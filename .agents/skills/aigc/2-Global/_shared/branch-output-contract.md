# 2-Global Field Fill Contract

## Purpose

本文件定义当前 `2-Global` 单技能模式下的字段填写真源。

- `2-Global` 在根技能内完成字段填写
- canonical 输出只有一个：
  - `projects/aigc/<项目名>/2-Global/episode_root.json`

## Canonical Carriers

### 1. canonical episode root

- 路径：
  - `projects/aigc/<项目名>/2-Global/episode_root.json`
- 作用：
  - 唯一业务真源
  - 承载 `meta + project_global + groups[].global`

### 2. stage validation report

- 路径：
  - `projects/aigc/<项目名>/2-Global/validation-report.md`
- 作用：
  - 记录本轮验收、阻塞、根因上溯和 closure

### 3. compatibility projections

- 典型路径：
  - `projects/aigc/<项目名>/2-Global/全局风格.md`
  - `projects/aigc/<项目名>/2-Global/全集类型元素.md`
  - `projects/aigc/<项目名>/2-Global/分组类型元素.md`
  - `projects/aigc/<项目名>/2-Global/导演意图.md`
- 作用：
  - 仅服务旧下游兼容
  - 不再作为当前主链必需输出

## Hard Rules

1. 所有 pass 都直接写向同一颗 `episode_root.json`，不再先写 Markdown 真源再回收。
2. 项目级字段统一进入 `project_global`，组级字段统一进入 `groups[].global`。
3. `groups[].global.剧本正文` 必须完整保留命中组正文。
4. 兼容 Markdown 若被生成，只能由已确认 JSON 派生，不得反向夺取写回权。

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
  - `.agents/skills/aigc/2-Global/_shared/branch-output-contract.md`
- shared handoff 合同：
  - `.agents/skills/aigc/_shared/group_design_seed_contract.md`
