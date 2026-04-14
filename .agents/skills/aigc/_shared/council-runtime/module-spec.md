# Council Runtime 共享运行时规范

## Module Identity

- `module_type`: `shared-runtime`
- `activation_signal`: 项目根存在 `projects/aigc/<项目名>/team.yaml` 且 `enabled == true`
- `primary_consumers`: `1-Planning`、`2-Global`、`3-Detail`、`4-Design` 及其可直达子技能

## Scope

本模块只负责跨阶段共享的顾问团运行时：

- 读取并解释项目根 `team.yaml`
- 判断当前阶段是否启用智能顾问团模式
- 决定当前阶段先调用 `策划` 还是 `监制`
- 规定 `评审` 在阶段级 `validation-report.md` 前后介入
- 约束 subagents 只是参谋，不夺取 canonical 写回权

本模块不负责：

- 重新定义 `1-Planning / 2-Global / 3-Detail / 4-Design` 的阶段内容合同
- 直接产出阶段 canonical
- 取代 `0-Init` 生成 `team.yaml`

## Canonical Sources

- 项目级团队真源：`projects/aigc/<项目名>/team.yaml`
- 共享模板真源：`.agents/skills/aigc/_shared/council-runtime/team.template.yaml`

## Stage Role Routing

| 当前阶段 | 默认前置顾问角色 | 评审时机 | canonical 写回权 |
| --- | --- | --- | --- |
| `1-Planning` | `策划` | `projects/aigc/<项目名>/1-Planning/validation-report.md` 前后 | 主代理 |
| `2-Global` | `监制` | `projects/aigc/<项目名>/3-Detail/validation-report.md` 前后 | 主代理 |
| `3-Detail` | `监制` | `projects/aigc/<项目名>/3-Detail/validation-report.md` 前后 | 主代理 |
| `4-Design` | `策划` | `projects/aigc/<项目名>/4-Design/validation-report.md` 前后 | 主代理 |

## Runtime Decision Contract

1. 进入阶段根技能或其可直达子技能时，先读取 `projects/aigc/<项目名>/team.yaml`。
2. 若文件不存在、`enabled != true`、或所有角色成员都为空，走普通路径。
3. 若 `enabled == true` 但当前阶段默认角色成员为空，则跳过前置顾问，仅保留已配置的 `评审` 闸门。
4. 若启用且当前阶段默认角色成员非空：
   - `1-Planning / 4-Design` 先调用 `roles.planning.members`
   - `2-Global / 3-Detail` 先调用 `roles.supervision.members`
5. 主代理先整合前置顾问意见，再产出本轮阶段草案。
6. 在阶段级 `validation-report.md` 写作前后，若 `roles.review.members` 非空，则调用 `评审` 给出 PASS/返工意见。
7. 无论顾问是否启用，主代理都保留最终 canonical 写回权。
8. 若当前环境不能真实使用 subagents，允许降级为顺序读取 agent 文档并模拟顾问纪要，但必须显式说明降级。

## Subagent Contract

### 前置顾问

- `策划 / 监制` 的职责是提出结构、执行、资源与风险建议。
- 他们不能直接落盘 canonical。
- 主代理必须把其建议整理为：
  - `共识`
  - `关键分歧`
  - `建议采用方案`
  - `少数派高价值提醒`

### 评审顾问

- `评审` 只对阶段终稿与阶段级 `validation-report.md` 负责。
- `评审` 默认不参与前置发散创作。
- `评审` 产出应收敛为：
  - `PASS / FAIL`
  - `返工关注点`
  - `高风险遗漏`

## Verification Checklist

1. 当前阶段进入前，已读取项目根 `team.yaml`。
2. `enabled == false` 或无成员时，没有误触发顾问团。
3. `1-Planning / 4-Design` 命中的是 `策划`，`2-Global / 3-Detail` 命中的是 `监制`。
4. `评审` 只在阶段级 `validation-report.md` 前后介入。
5. 主代理保留最终 canonical 写回权。
