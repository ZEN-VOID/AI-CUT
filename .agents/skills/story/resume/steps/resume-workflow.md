# Resume Workflow

本文件定义 `$story-resume` 的思行一体化节点。节点必须同时表达判断、动作、证据、路由和 gate。

## Business Requirement Analysis

| slot | conclusion |
| --- | --- |
| `business_goal` | 将中断或疑似中断的 story2026 任务恢复到可证明、安全、唯一的下一入口。 |
| `business_object` | `projects/story/<项目名>/` runtime、`STATE.json.workflow_runtime`、draft/review/context-return 工件、统一 CLI 输出与用户确认。 |
| `constraint_profile` | 不能猜断点，不能绕过 `story.py`，不能默认执行 destructive Git 或未确认 cleanup，不能把恢复卫星技能冒充主阶段。 |
| `success_criteria` | 输出恢复裁决包，包含证据链、风险等级、用户确认状态、已执行命令和唯一 next handoff。 |
| `non_goals` | 不写正文，不改规划，不做 PASS actualization，不替 review 做人工裁决。 |
| `complexity_source` | 复杂度来自 tracked run、artifact fallback、query 轻量恢复、write/review/context-return 多 stage 回接和 cleanup 安全门。 |
| `topology_fit` | 串行预检 + 树形类型分流 + 用户确认 + closure 汇流。 |

## Node Network

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 锁定恢复诉求与候选项目根 | 用户请求、cwd、项目名/路径、stage hint | 判定是否是 resume、query、context return、drafting 或 review 请求 | intent label、候选路径、reroute reason | `N2-PREFLIGHT` 或 reroute/block | 恢复意图明确，或已给最小追问/路由 |
| `N2-PREFLIGHT` | 解析真实 `PROJECT_ROOT` | `WORKSPACE_ROOT`、`story.py preflight` | 执行 preflight 和 `where`，确认 `STATE.json` | preflight JSON、project_root | `N3-DETECT` | 项目根唯一且包含 `STATE.json` |
| `N3-DETECT` | 读取中断或 fallback 证据 | `workflow detect`、runtime files | 执行或消费 `workflow detect`；无 tracked 中断时检查 artifact fallback | detect payload、fallback evidence | `N4-TYPE` | 不凭聊天记忆判断断点 |
| `N4-TYPE` | 判定恢复模式与风险 | detect/fallback payload、用户意图、types 矩阵 | 形成 `resume_type_profile` | mode、risk、command、current_step、candidate_entry | `N5-NORMALIZE` | 模式命中且风险已标注 |
| `N5-NORMALIZE` | 归一化恢复方案 | type profile、reference protocol | 过滤危险动作，生成 A/B/C 选项或唯一 next stage | normalized options、recommended option | `N6-CONFIRM` | 选项可执行，且没有无序多入口 |
| `N6-CONFIRM` | 获取用户恢复策略 | normalized options、用户回复 | 等待用户选择继续、cleanup、保留现场、仅清理或人工诊断 | user_confirmed_option | `N7-ACT` 或 stop | 不替用户自动执行风险动作 |
| `N7-ACT` | 执行安全动作或退出 | confirmed option、scripts boundary | 只通过 `story.py` 执行 preview/cleanup/clear/fail-task；或不执行只报告 | commands_executed、command output summary | `N8-CLOSURE` | destructive cleanup 已 preview 且确认 |
| `N8-CLOSURE` | 验证 closure 并回接 stage | post-action detect、stage handoff | 核对旧断点状态、备份/清理证据、下一入口 | closure summary、next_stage_handoff | done | 输出恢复裁决包或 blocker |

## Branch Rules

### `tracked_workflow_resume`

- 条件：`workflow detect` 返回 tracked JSON。
- 动作：读取 `command`、`current_step.id`、`completed_steps`、`artifacts`、`elapsed_seconds`。
- gate：不得直接照搬 detect 的动作文本，必须由 `resume/` 二次归一化。

### `artifact_fallback_resume`

- 条件：没有 tracked interruption，但命中 `return`、`review`、`3-初稿` 写作日志等可证明业务证据链。
- 动作：列出证据链，并收敛到唯一下一入口。
- gate：不得把 fallback 伪装成 tracked interruption。

### `query_light_resume`

- 条件：tracked command 是 `story-query`。
- 动作：说明最近查询 run 的阶段，只给 generic continue / rerun / manual diagnosis。
- gate：不得进入章节 cleanup。

### `write_cleanup_resume`

- 条件：`story-write` 在 Step 2-8 中断，且正文可能失真或用户要重跑。
- 动作：先执行 `workflow cleanup --chapter {N}` 预览；用户确认后才 `--confirm` 和 `workflow clear`。
- gate：删除前必须由脚本自动备份正文根文件。

### `review_decision_resume`

- 条件：`story-review` 在 Step 7 或后段中断。
- 动作：重新确认关键问题处理策略或核对输入未变后继续。
- gate：不得替用户自动完成 Step 7 裁决。

## Failure Loops

| failure | loop target | repair |
| --- | --- | --- |
| 项目根无法解析 | `N2-PREFLIGHT` | 修 project pointer 或询问项目路径 |
| `workflow detect` 缺失且无 fallback 证据 | `N3-DETECT` | 输出 no tracked interruption + 安全重跑建议 |
| fallback 证据冲突 | `N4-TYPE` | 降级人工诊断，列冲突文件 |
| 恢复选项含危险动作 | `N5-NORMALIZE` | 移除 Git hard reset / 未确认删除 |
| 用户未确认 cleanup | `N6-CONFIRM` | 停止在 preview 后，不执行 confirm |
| cleanup 后未验证 | `N8-CLOSURE` | 重新运行 detect 或说明保留现场 |

## Evidence Packet Shape

```yaml
resume_evidence:
  project_root: ""
  preflight_status: ""
  detect_payload:
    tracked_command: ""
    current_step: ""
    completed_steps: []
    artifacts: []
  artifact_fallback:
    reason: ""
    evidence_files: []
    next_entry: ""
  risk_profile:
    risk_level: "low|medium|high|blocked"
    destructive_action_requested: false
    cleanup_requires_confirmation: false
  user_confirmation:
    selected_option: ""
    confirmed_at: ""
  closure:
    commands_executed: []
    next_stage_handoff: ""
```
