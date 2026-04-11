# 自主问答模式模块规范

## Module Identity

- `module_type`: `mode-playbook`
- `activation_signal`: `init_mode == 自主问答模式`
- `entrypoint`: `0-Init/SKILL.md` 的 `Initialization Mode Contract`、`Autonomous Mode Contract`
- `primary_consumers`: 初始化协调助手、问答回填流程、确认卡生成流程

## Scope

本模块只负责 `自主问答模式`：

- 规划下一轮该问什么
- 把自由叙述回填为 `north_star` 与 `init_handoff` 字段
- 区分哪些问题应继续问，哪些应进入 `unknowns`

本模块不负责：

- 重新定义模式元选项
- 替用户做关键长期约束拍板
- 越权替下游阶段形成 canonical

## Load Contract

- 加载条件：`init_mode == 自主问答模式`
- 互斥规则：本模块成为主路径后，不得再加载 `advisor-council-mode` 或 `fast-mode` 作为主执行细则
- 交互闸门：允许进入问答卡流程

## Mode Goal

通过多轮但收敛的结构化问答，让用户亲自锁定项目 north star，同时只为后续阶段提供足够开工的 seed。

## Shared Dependency Contract

- 必读：
  - `templates/north-star.template.yaml`
  - `templates/init-handoff.template.yaml`
- 按需读取：
  - 根 `.agents/skills/aigc/SKILL.md`

## Execution Procedure

1. 先问核心合同卡。
2. 判断缺口是 `north_star` 缺口，还是 `stage_entry_seeds` 缺口。
3. 每轮 4-8 题，优先减少当前最阻塞 unknowns。
4. 每轮结束后更新：
   - `user_confirmed`
   - `assistant_inferred`
   - `unknowns`
   - `recommended_next_stage`
5. 达到充分性闸门后，发送确认卡并落盘。

## Output Contract

- 每轮都要保留：
  - `user_confirmed`
  - `assistant_inferred`
  - `unknowns`
- 最终必须产出：
  - `north_star`
  - `init_handoff`
  - `sources_breakdown`

## Output Landing Contract

- `projects/<项目名>/Init/north_star.yaml`
- `projects/<项目名>/Init/init_handoff.yaml`
- `projects/<项目名>/Init/interview_summary.md`
- `projects/<项目名>/Init/confirmation_card.md`
- `projects/<项目名>/project_state.yaml`

## Escalation

- 用户中途要求“你直接来一版”，切换到 `快速成案模式`，并记录 `mode_source = switched_midway`。
- 用户中途指定顾问路径，切换到 `主创会诊模式`。

## Verification Checklist

1. 没有退化成一题一题碎片追问。
2. 没有把下游 canonical 问题强行在初始化拍死。
3. `north_star` 与 `init_handoff` 的字段更新可追溯。
4. 最终能直接落到 `0-Init/` 与项目根标准路径。
