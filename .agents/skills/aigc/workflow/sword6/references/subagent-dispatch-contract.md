# Subagent Dispatch Contract

本文件定义 `sword6` 的 subagent 派发、隔离、降级和主窗口边界。

## Core Rules

1. 一个目标分集在一个阶段只能对应一个后台隔离 subagent。
2. 同一阶段可并发启动多个 episode subagents；阶段之间必须等待汇流门。
3. 每个 subagent 的 task packet 必须写清项目根、集数、阶段技能路径、输入路径、输出路径、加载上下文和完成 gate。
4. 主窗口只保留 `subagent_id / episode_id / stage / status / output_path / verdict / fail_code`，不得把分集正文复制回主上下文。
5. 真实 subagent runtime 不可用时，必须报告 `degraded-subagent-unavailable`，不得用主窗口顺序扮演多个 subagents。
6. subagent 只能按阶段技能合同写该阶段产物，不得改写其他分集、其他阶段或 workflow 合同文件。

## Runtime Packet Fields

| field | requirement |
| --- | --- |
| `project_root` | `projects/aigc/<项目名>/` |
| `episode_id` | `第N集` 或等价稳定集号 |
| `stage_slug` | `2-编剧`、`3-导演`、`4-表演`、`5-摄影`、`6-分组` |
| `stage_skill` | `.agents/skills/aigc/<stage>/SKILL.md` |
| `input_path` | 上一阶段 canonical 文件；`2-编剧` 读取 `1-分集/第N集.md` |
| `output_path` | 当前阶段 canonical `第N集.md` |
| `context_bundle` | 阶段 `SKILL.md + CONTEXT.md`、项目 `MEMORY.md`、相关项目 `CONTEXT/` |
| `completion_gate` | 阶段 review contract 中对该集的通过条件 |

## Degradation Protocol

允许降级的唯一场景：

- 更高优先级系统、工具或运行环境不提供真实 subagent runtime。
- 用户明确要求不要启用 subagents。
- 当前环境只允许生成调度计划，不允许后台执行。

降级输出必须包含：

- `runtime_mode: degraded-subagent-unavailable`
- `used_subagent_runtime: false`
- `blocking_layer`
- `expected_path`
- `actual_path`
- `missing_runtime`

降级后不得继续生成阶段主创正文。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否做到一集一个后台隔离 subagent，且主窗口只追踪状态？ | `GATE-SWORD6-02` | `FAIL-SWORD6-SUBAGENT` | `steps/sword6-workflow.md#N3-DISPATCH-STAGE` | dispatch packet 清单、subagent status table |
| subagent runtime 不可用时是否停止或显式降级，而不是本地伪装执行？ | `GATE-SWORD6-02` | `FAIL-SWORD6-SUBAGENT` | 本文件 `Degradation Protocol`、`SKILL.md#Runtime Guardrails` | completion report 中的 runtime_mode 与 blocking_layer |
| 每个 subagent 是否只获得本集、本阶段和必要上下文？ | `GATE-SWORD6-03` | `FAIL-SWORD6-CONTEXT` | `templates/stage-dispatch-packet-template.md` | packet 中的 context_bundle 与 input/output path |
