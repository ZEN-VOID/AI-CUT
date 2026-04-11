# 主创会诊模式模块规范

## Module Identity

- `module_type`: `mode-playbook`
- `activation_signal`: `init_mode == 主创会诊模式`
- `entrypoint`: `0-Init/SKILL.md` 的 `Initialization Mode Contract`、`Advisor Council Contract`
- `primary_consumers`: 初始化协调助手、顾问读取流程、综合确认流程

## Scope

本模块只负责：

- 校验顾问路径
- 校验 `team.yaml` 布阵字段是否完整
- 组织共享 brief
- 将顾问会诊写回 `策划 / 监制 / 评审` 三角色团队
- 汇总多位顾问建议
- 将会诊结果收束成一份可落盘初始化合稿

本模块不负责：

- 重新定义初始化元选项
- 把顾问团模式改回问卷模式
- 直接改写下游阶段真源

## Load Contract

- 加载条件：`init_mode == 主创会诊模式`
- 互斥规则：本模块成为主路径后，不得再加载其他模式模块
- 交互闸门：不进入长问卷；只允许确认卡或 1 张裁决卡

## Mode Goal

让多位顾问围绕同一份影视项目 brief 给出结构化建议，并由协调层收束为 `north_star` 与 `init_handoff`。

## Team Routing Contract

`advisor-council-mode` 不再把顾问视为一个平铺列表，而是必须按项目根 `team.yaml` 的三角色路由。

| 角色 | 默认作用阶段 | 介入方式 | 阶段真源引用 |
| --- | --- | --- | --- |
| `策划` | `1-规划`、`4-主体` | 前置 seed 与结构方向建议 | `.agents/skills/aigc/1-规划/SKILL.md`、`.agents/skills/aigc/4-主体/SKILL.md` |
| `监制` | `2-组间`、`3-明细` | 执行一致性、资源感与可拍性约束 | `.agents/skills/aigc/2-组间/SKILL.md`、`.agents/skills/aigc/3-明细/SKILL.md` |
| `评审` | `1-规划`、`2-组间`、`3-明细`、`4-主体` | 仅在阶段最终验收闸门给 PASS / 返工意见 | `.agents/skills/aigc/1-规划/SKILL.md`、`.agents/skills/aigc/2-组间/SKILL.md`、`.agents/skills/aigc/3-明细/SKILL.md`、`.agents/skills/aigc/4-主体/SKILL.md` |

硬规则：

1. `same_lineup` 只表示成员复用，不表示职责折叠；写回时仍必须展开为三角色。
2. `评审` 默认不参与前置发散讨论，其职责是对阶段终稿或阶段级 `validation-report.md` 给最终闸门意见。
3. 如果用户临时只提供一组顾问名单，协调层也必须在写回 `team.yaml` 时完成角色化映射。

## Required Inputs

- 用户原始 brief
- 顾问路径
- `team_ref`
- `team_setup`
- `team_enabled`
- `research_policy`
- `decision_owner`
- 当前已知字段与禁区

## Shared Dependency Contract

- 必读：
  - `.agents/skills/aigc/0-Init/templates/north-star.template.yaml`
  - `.agents/skills/aigc/0-Init/templates/init-handoff.template.yaml`
  - `.agents/skills/aigc/_shared/council-runtime/team.template.yaml`
- 按需读取：
  - 根 `.agents/skills/aigc/SKILL.md`

## Execution Procedure

1. 校验顾问路径真实存在且可读。
2. 依据 `team_setup.team_mode` 规范化团队布阵，确保三角色都能展开到项目根 `team.yaml`。
3. 构造统一 `initialization_brief`，其中必须写清：
   - 当前已确认字段
   - 不得越权提前拍死的下游 canonical
   - 三角色默认作用阶段
   - `评审` 只在最终闸门介入
4. 若可并行，则一顾问一线程；若不可并行，则顺序读取并模拟纪要。
5. 汇总所有顾问结果。
6. 输出：
   - `共识`
   - `关键分歧`
   - `建议采用方案`
   - `少数派高价值提醒`
7. 将综合结果写回项目根 `team.yaml`、`north_star` 与 `init_handoff`。
8. 如分歧会改变长期项目约束，只发 1 张裁决卡。
9. 确认后落盘。

## Output Contract

- 必须产出：
  - `projects/<项目名>/team.yaml`
  - `north_star`
  - `init_handoff`
  - `sources_breakdown`
- `team.yaml` 必须显式记录：
  - `enabled`
  - `team_setup.team_mode`
  - `roles.planning.members`
  - `roles.supervision.members`
  - `roles.review.members`
  - `roles.review.operates_on_final_stage_of`
- `sources_breakdown` 必须区分：
  - `user_confirmed`
  - `council_advised`
  - `assistant_inferred`

## Output Landing Contract

- `projects/<项目名>/team.yaml`
- `projects/<项目名>/Init/north_star.yaml`
- `projects/<项目名>/Init/init_handoff.yaml`
- `projects/<项目名>/Init/confirmation_card.md`
- `projects/<项目名>/project_state.yaml`

额外硬规则：

1. `init_handoff.yaml` 只能回写 `team_ref` 指向 `team.yaml`，不得复制完整团队 schema。
2. `project_state.yaml` 至少要能追溯 `init_mode + team_ref + decision_owner + research_policy`。

## Fallback

- 顾问路径失效：停止本模式并要求用户修正或切换模式。
- 无法并发：顺序会诊，但必须标记为降级执行。

## Verification Checklist

1. 顾问建议有统一 brief，不是各自漫游。
2. 输出保留共识、分歧和来源分层。
3. 没有回退成长问卷。
4. 项目根 `team.yaml` 已明确 `策划 / 监制 / 评审` 三角色，而不是只有平铺顾问列表。
5. `评审` 的作用位点只出现在 `1-规划 / 2-组间 / 3-明细 / 4-主体` 的最终验收闸门。
6. 会诊结果能稳定映射到标准落盘位点。
