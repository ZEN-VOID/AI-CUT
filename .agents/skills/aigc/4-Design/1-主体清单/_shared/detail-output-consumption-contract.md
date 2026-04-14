# 4-Design / 1-主体清单 Shared Detail Consumption Contract

## Purpose

本文件是 `.agents/skills/aigc/4-Design/1-主体清单/` 全部 sibling leaf 的共享输入消费真源。

它把 `3-Detail` 阶段的 canonical episode JSON 与四类主体清单的抽取边界收成一处，避免 `角色 / 服装 / 道具 / 场景` 各自再演化一套平行的输入口径。

## Canonical Input Root

- 第一真源固定为：
  - `projects/aigc/<项目名>/3-Detail/第N集.json`
- 兼容 fallback 仅允许：
  - `projects/aigc/<项目名>/编导/第N集.json`
- legacy fallback 只用于路径兼容或旧项目修补，不得在 sibling leaf 的主合同里和 canonical 路径并列成双真源。

## Readiness Gate

直接消费 `3-Detail` episode JSON 的 leaf（角色 / 道具 / 场景）默认要求：

1. 输入能被 `.agents/skills/aigc/_shared/director_episode_output.schema.json` 解释。
2. 存在 `final_output.main_content.分镜组列表[]`。
3. 每个命中 group 至少具备：
   - `分镜组ID`
   - `组间设计`
   - `分镜明细[]`
4. `metadata.document_phase` 推荐位于：
   - `detail_in_progress`
   - `ready`

若 phase 更早，但用户显式要求 repair / bootstrap 兼容消费，必须在 leaf 输出中显式记缺口，不得伪装为标准完成态。

## Consumer Matrix

| leaf | primary_input | supplemental_input | canonical_fields | forbidden_assumptions |
| --- | --- | --- | --- | --- |
| `角色` | `3-Detail/第N集.json` | 兼容 `编导/第N集.json` | `分镜明细[].角色站位走位`、`分镜明细[].角色背景面`、`组间设计.出场角色及穿搭` | 不得回到旧 markdown 分镜块猜角色；不得把道具/动作词当人名 |
| `服装` | `4-Design/角色/1-清单/角色清单.json` | `3-Detail/第N集.json` 仅作补证 | `roles[].costume_profile`、`roles[].costume_state`、`roles[].variation_rules`、`group_role_map[].costume_mentions` | 不得绕过角色链重做 identity；不得把导演 JSON 升格为角色真源 |
| `道具` | `3-Detail/第N集.json` | 兼容 `编导/第N集.json` | `分镜明细[].道具及状态`、`分镜明细[].角色背景面`、`分镜明细[].角色站位走位`、`分镜表现` | 不得发明上游未出现的 prop；不得回写 `3-Detail` |
| `场景` | `3-Detail/第N集.json` | 兼容 `编导/第N集.json` | `分镜明细[].角色背景面` | 不得把方位短语误提升为第二主场景；不得补研究型空间设定 |

## Canonical Field Mapping

### Group Level

- `分镜组列表[].分镜组ID`
  - 全体 leaf 的 group 回链主键
- `分镜组列表[].组间设计.出场角色及穿搭`
  - `角色` 的服装补读摘要
  - `服装` 的 transitive evidence 来源之一

### Shot Level

- `分镜明细[].分镜ID`
  - 全体 leaf 的 shot 回链主键
- `分镜明细[].角色背景面`
  - `场景` 的主抽取字段
  - `角色 / 道具` 的 scene anchor
- `分镜明细[].角色站位走位`
  - `角色` 的主抽取字段
  - `道具` 的 role anchor
- `分镜明细[].道具及状态`
  - `道具` 的主抽取字段
- `分镜明细[].分镜表现`
  - `道具` 的 research / bridge 补证字段

## Legacy Compatibility Rule

允许 fallback 的旧字段只有：

- `场景及方位`
- `角色及站位和穿搭`

规则：

1. 旧字段只允许作为读取 fallback，不得在 leaf 主合同里继续写成 canonical 名。
2. 任何 leaf 一旦成功命中当前 canonical 字段，就不得再回头覆盖成 legacy 字段口径。
3. 经验层与脚本注释若仍使用 legacy 名称，必须同时标注“仅兼容 fallback”。

## Traceability Contract

所有 leaf 的抽取结果都必须能回链：

- `group_id`
- `shot_id`（若该 leaf 产物是 shot 级）
- `source_file`

不允许只留下抽象结论、不留上游锚点。

## Non-Ownership Contract

`1-主体清单` sibling leaf 统一不拥有：

- 改写 `3-Detail/第N集.json`
- 重判 `分镜切换`
- 重写 `组间设计`
- 重新生成 shot factual/cinematic patch

它们只消费 `3-Detail` 已稳定落位的结构化对象，并在各自运行根下写出 design-source artifacts。

## Conflict Policy

- 用户显式请求 > 根 `AGENTS.md` > `.agents/skills/aigc/3-Detail/SKILL.md` / shared schema > 本合同 > sibling leaf `SKILL.md` > sibling leaf `CONTEXT.md`
