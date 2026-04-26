# Resume Workflow

本文件定义 `$aigc-resume` 的思行一体化节点。节点必须同时表达判断、动作、证据、路由和 gate。

## Business Requirement Analysis

| slot | conclusion |
| --- | --- |
| `business_goal` | 将中断的 AIGC 项目恢复到一个可证明、安全、唯一的下一入口。 |
| `business_object` | `projects/aigc/<项目名>/` runtime、`STATE.json`、可选 `governance-state.yaml`、初始化工件、阶段产物与 gate 工件。 |
| `constraint_profile` | 不能猜断点，不能跳过高风险治理 gate，不能执行 destructive 默认动作，不能把 rebootstrap 混成续跑。 |
| `success_criteria` | 输出一个唯一下一入口，附带证据链、风险等级、blocker 和必要修复。 |
| `non_goals` | 不生成阶段业务真稿，不做 Git 回滚，不替代 query/review/0-初始化。 |
| `complexity_source` | 复杂度来自项目根定位、轻量状态与结构化治理状态并存、legacy runtime 兼容、review repair bridge 和高风险 gate。 |
| `topology_fit` | 串行 intake + 树形模式分流 + 安全 gate 汇流。 |

## Node Network

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 锁定项目与恢复意图 | 用户请求、cwd、项目名候选 | 解析 `PROJECT_ROOT`，判断是否是 rebootstrap/query/review/stage 任务 | 项目路径、候选列表、意图标签 | `N2-TRUTH-LOCK` 或 reroute/block | 项目根唯一，或已输出最小追问 |
| `N2-TRUTH-LOCK` | 建立恢复证据包 | `STATE.json`、初始化工件、governance sidecars、阶段文件 | 读取状态、工件、gate 与工作区状态；标注证据等级 | `state_truth`、`artifact_truth`、`gate_truth` | `N3-TYPE` | 至少有一类状态证据和一类工件证据，或已说明缺口 |
| `N3-TYPE` | 判定恢复模式与风险 | 证据包、用户意图、类型矩阵 | 形成 `resume_type_profile` | mode、risk、blockers、candidate_entry | `N4-PLAN` | 模式命中且不与用户意图冲突 |
| `N4-PLAN` | 归一化安全恢复方案 | `resume_type_profile` | 将候选入口收敛为唯一入口；列 required repairs | 唯一入口、repair list、禁止动作过滤结果 | `N5-GATE` | 没有无序多入口 |
| `N5-GATE` | 执行交付前安全 gate | 恢复方案、review gate | 检查项目根、证据链、风险、治理 gate、输出模板字段 | verdict | `N6-CLOSE` 或回 `N2/N3/N4` | pass 或 blocked_with_minimal_question |
| `N6-CLOSE` | 输出恢复裁决 | gate verdict、输出模板 | 给出用户-facing 恢复报告；如被要求写报告，则按模板落盘 | final report | done | 报告含唯一下一入口或 blocker |

## Branch Rules

### `lightweight_init_continue`

- 条件：`STATE.json`、`team.yaml`、`0-初始化/north_star.yaml`、`0-初始化/init_handoff.yaml`、`0-初始化/story-source-manifest.yaml` 足以证明项目已初始化。
- 动作：允许回根或低风险下一阶段；若用户要求复杂恢复、review bridge 或高风险执行，再补治理快照。
- gate：不得把缺少 `governance-state.yaml` 单独视为阻断。

### `governance_rebuild`

- 条件：live route truth 缺失、初始化核心工件缺失、高风险 gate 所需 sidecar 缺失。
- 动作：回根 `aigc` 或 `0-初始化` 补治理工件。
- gate：不得直接进入高风险阶段生产。

### `stage_continue`

- 条件：目标阶段 scope 与产物证据清楚，且 gate 没有阻断。
- 动作：回目标阶段技能继续。
- gate：阶段目录必须包含真实产物；空目录不算。

### `gate_reentry`

- 条件：内容产物存在，但缺 preflight、validation 或 release gate。
- 动作：回根 `aigc` 或 `review/`。
- gate：输出只给一个 gate owner。

### `review_repair_reentry`

- 条件：`review_bridge` 或 `resume_contract.required_repairs` 指向 repair route。
- 动作：进入 repair route 指定阶段；若 repair route 不唯一，回 review 聚合层修 route。
- gate：不得自己发明 repair 内容。

### `init_rebootstrap_reroute`

- 条件：用户明确要求回到初始化态重来、推翻方向、重新起盘。
- 动作：回 `0-初始化`。
- gate：不得读取旧阶段产物作为继续当前方向的依据，除非用于 rebootstrap preserve/archive 判断。

## Failure Loops

| failure | loop target | repair |
| --- | --- | --- |
| 项目根不唯一 | `N1-INTAKE` | 询问项目名或路径 |
| 状态证据不足 | `N2-TRUTH-LOCK` | 读取初始化核心工件或报告缺口 |
| 模式与用户意图冲突 | `N3-TYPE` | 先判 rebootstrap/query/review |
| 多个下一入口并列 | `N4-PLAN` | 选择 gate owner 或输出 blocker |
| 高风险 gate 缺失 | `N5-GATE` | reroute 到根 gate |

## Evidence Packet Shape

```yaml
resume_evidence:
  project_root: ""
  state_truth:
    state_json_present: false
    current_stage: ""
    recommended_entry_path: ""
  governance_truth:
    governance_state_present: false
    resume_contract_present: false
    review_bridge_state: "absent"
  artifact_truth:
    init_core_present: false
    stage_outputs: []
  gate_truth:
    mission_brief_present: false
    route_plan_present: false
    preflight_verdict_present: false
    validation_report_present: false
  workspace_truth:
    git_dirty_summary: ""
```
