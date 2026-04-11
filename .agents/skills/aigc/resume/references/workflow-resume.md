# AIGC Resume Workflow Reference

## Purpose

定义 `aigc/resume` 的安全恢复协议。

## Recovery Evidence Chain

恢复判定优先级：

1. `project_state.yaml`
2. `governance-state.yaml`
3. `mission-brief.yaml`
4. `route-plan.yaml`
5. `preflight-verdict.yaml`
6. `validation-report.md`
7. 阶段 runtime 真实产物
8. 工作区最近修改痕迹

## Recovery Modes

| mode | symptom | safe action |
| --- | --- | --- |
| `governance_rebuild` | 治理工件缺失、`governance-state.yaml` 缺失或 `project_state` 不完整 | 回根 `aigc` 或 `review/` 补治理链 |
| `stage_continue` | 阶段产物已存在、scope 清楚、尚未完成验收 | 回目标阶段继续执行 |
| `review_reentry` | 内容产物存在，但缺预审/验收桥接 | 进入 `review/` |
| `root_reroute` | 目标阶段不清、阶段已搁浅、技能合同缺失 | 回根 `aigc` 重判 |

## Hard Guards

- 不得伪造不存在的 workflow state
- 不得默认建议 destructive Git 动作
- 不得在缺 `preflight-verdict` 的高风险任务上直接建议继续执行
- 不得把 stage 已搁浅的目录说成“可直接恢复”
