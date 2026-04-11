# 快速成案模式模块规范

## Module Identity

- `module_type`: `mode-playbook`
- `activation_signal`: `init_mode == 快速成案模式`
- `entrypoint`: `0-Init/SKILL.md` 的 `Initialization Mode Contract`、`Fast Mode Contract`
- `primary_consumers`: 初始化协调助手、一次性成案流程、确认卡生成流程

## Scope

本模块只负责：

- 从最小 brief 抽取硬信号
- 一次性补完 `north_star` 草案与 `init_handoff` 草案
- 把推断项与用户确认项分层

本模块不负责：

- 重新展开完整问卷
- 用炫技脑补替代保守补全
- 越权替后续阶段做终局裁决

## Load Contract

- 加载条件：`init_mode == 快速成案模式`
- 互斥规则：本模块成为主路径后，不得再加载其他模式模块
- 交互闸门：不得进入长问卷；最多允许 1 张阻塞卡

## Mode Goal

用最少追问，为当前影视项目生成一份可落盘、可继续推进的 `north_star` 起盘包。

## Required Inputs

- 用户最小 brief
- `research_policy`
- `decision_owner`
- 当前已知禁区与显式偏好

## Shared Dependency Contract

- 必读：
  - `.agents/skills/aigc/0-Init/templates/north-star.template.yaml`
  - `.agents/skills/aigc/0-Init/templates/init-handoff.template.yaml`
- 按需读取：
  - 根 `.agents/skills/aigc/SKILL.md`

## Execution Procedure

1. 读取最小 brief，抽出不可违背的硬约束。
2. 一次性补完 `north_star` 草案。
3. 按当前阶段链补完 `stage_entry_seeds`。
4. 证据不足或分叉过大的部分写入 `unknowns`。
5. 若无高后果分歧，直接输出确认卡；否则补 1 张阻塞卡。
6. 用户确认后落盘。

## Output Contract

- 必须产出：
  - `north_star`
  - `init_handoff`
  - `sources_breakdown`
  - `risk_notes`
- `sources_breakdown` 至少包含：
  - `user_confirmed`
  - `assistant_inferred`

## Output Landing Contract

- `projects/<项目名>/Init/north_star.yaml`
- `projects/<项目名>/Init/init_handoff.yaml`
- `projects/<项目名>/project_state.yaml`
- `projects/<项目名>/mission-brief.yaml`
- `projects/<项目名>/route-plan.yaml`

## Fallback

- 若用户输入过少且分叉过大：发 1 张阻塞卡，不回退成长问卷。
- 若外部核验失败：采用保守本地方案，并在 `risk_notes` 标不确定性。

## Verification Checklist

1. 快速模式执行中没有回流成长问卷。
2. `assistant_inferred` 与 `user_confirmed` 可以区分。
3. `unknowns` 没有被强行填满。
4. 输出可以直接映射到标准落盘位点。
