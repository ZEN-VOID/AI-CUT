# Mode And Team Contract

本文件拥有 `story-init` 的初始化模式、team 编组、`team.yaml` 唯一真源和 planning subagent kickoff 合同。入口路由仍由上级 `SKILL.md` 裁决。

## Single Mode Rule

- `init_mode` 固定为 `team代入模式`。
- 内部存储可使用 `team_roleplay`，但用户可见显示必须为 `team代入模式`。
- 合法编组子路径只有 `auto` 与 `custom`。
- 不得恢复 `顾问团模式 / 快速模式 / 自主问卷` 为平行 mode-playbook。
- 初始化元选项卡只能展示一次；其他文档只能引用，不得复制第二套入口。

## Team Lineup Routes

| route | trigger | required action | evidence |
| --- | --- | --- | --- |
| `auto` | 用户明确要求自动组队，或没有给 roster | 读取 `.agents/skills/team/SKILL.md + CONTEXT.md`，按项目类型 shortlist 规划/监制/评审阵容 | `init_contract.auto_selection_notes` |
| `custom` | 用户给出成员、角色或路径 | 校验所有成员位于 `.agents/skills/team/`，再落位到角色 | `init_contract.custom_selection_notes` |

## Team Manifest Contract

`projects/story/<项目名>/team.yaml` 是唯一项目级 team 真源，至少包含：

```yaml
init_contract:
  init_mode: team_roleplay
  init_mode_display: team代入模式
  team_lineup_mode: auto
  selector_scope_root: .agents/skills/team/
runtime_policy:
  require_subagents_for_init_execution: true
  init_execution_owner_role: planning
roles:
  planning:
    members: []
    init_execution:
      kickoff_owner: true
```

硬规则：

1. 不允许再生成并行 `advisor_manifest`、`team_manifest` 或其他 team 真源。
2. `roles.*.members` 只允许引用 `.agents/skills/team/` 下的技能。
3. `planning / production / review` 可以同人复用，也可以分人治理；默认允许重叠。
4. `team.yaml` 必须先于 `0-初始化/north_star.yaml` 锁定。
5. `team.yaml` 重初始化时必须覆盖刷新，不得停留在旧 skeleton。

## Subagent Execution Rule

- `roles.planning.members` 是初始化固定题包直答的 kickoff owner。
- 仓库治理要求真实 subagents 执行 planning 直答，再由主流程聚合。
- 若当前环境、更高优先级 system/developer/tool/user 策略阻断真实 subagent dispatch，不得伪装成已真实执行；必须报告：
  - 阻断来源层级
  - 原计划路径：`roles.planning.members -> fixed direct-answer packet`
  - 实际降级路径或阻塞状态
  - 未真实启动的成员列表

## Prohibited Drift

- 不得把 `team.yaml` 的内容镜像到项目根其他 team 真源。
- 不得让 `creative-seed-routing` 抢占 team 路由。
- 不得因为用户 brief 很少而退回长问卷或快速补全模式。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| `init_mode` 是否固定为 `team代入模式`，且合法编组子路径只有 `auto/custom`？ | `mode` | `FAIL-INIT-MODE` | `SKILL.md` Mode Selection、`SKILL.md` N2-MODE | init_mode、team_lineup_mode、mode_source |
| `team.yaml` 是否是唯一 team 真源，且未生成并行 advisor/team manifest？ | `team` | `FAIL-INIT-TEAM` | 本文件 Team Manifest Contract、`SKILL.md` N5-TEAM-LOCK | team.yaml 路径、唯一性扫描结果 |
| 自定义成员是否均位于 `.agents/skills/team/`，自动组队是否读取 team 根 `SKILL.md + CONTEXT.md`？ | `team` | `FAIL-INIT-TEAM` | 本文件 Team Lineup Routes、`.agents/skills/team/SKILL.md` | roster 路径清单、auto selection notes |
| planning 固定题包直答是否由 `roles.planning.members` 真实执行，或已明确报告阻断/降级？ | `subagents` | `FAIL-INIT-SUBAGENT` | 本文件 Subagent Execution Rule、`references/prompt-packet-contract.md` | dispatch evidence、未启动成员列表、降级来源 |
