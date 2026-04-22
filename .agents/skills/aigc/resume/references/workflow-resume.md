# AIGC Resume Workflow Reference

## Purpose

定义 `aigc/resume` 的安全恢复协议。

## Recovery Evidence Chain

恢复判定优先级：

1. `STATE.json`
2. `0-Init/north_star.yaml`、`0-Init/init_handoff.yaml`、`0-Init/story-source-manifest.yaml`
3. `governance-state.yaml`（若存在）
4. `mission-brief.yaml`、`route-plan.yaml`（若存在）
5. `preflight-verdict.yaml`、`validation-report.md`（若存在）
6. 阶段 runtime 真实产物
7. 工作区最近修改痕迹

## Recovery Modes

| mode | symptom | safe action |
| --- | --- | --- |
| `lightweight_init_continue` | 核心初始化工件已齐，但仍处于轻量起盘态 | 允许回根 `aigc` 或低风险下一阶段继续 |
| `governance_rebuild` | `project_state` 不完整，或高风险恢复所需治理 gate 缺失 | 回根 `aigc` 补治理链 |
| `stage_continue` | 阶段产物已存在、scope 清楚、尚未完成验收 | 回目标阶段继续执行 |
| `gate_reentry` | 内容产物存在，但缺预审/验收桥接 | 回根 `aigc` |
| `root_reroute` | 目标阶段不清、阶段已搁浅、技能合同缺失 | 回根 `aigc` 重判 |

## Hard Guards

- 不得伪造不存在的 workflow state
- 不得默认建议 destructive Git 动作
- 不得在缺 `preflight-verdict` 的高风险任务上直接建议继续执行
- 不得把 stage 已搁浅的目录说成“可直接恢复”
