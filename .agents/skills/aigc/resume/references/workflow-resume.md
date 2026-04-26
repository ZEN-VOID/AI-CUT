# AIGC Resume Workflow Reference

本文件定义 `$aigc-resume` 的恢复证据链、恢复模式细则和 hard guards。它展开 `SKILL.md` 的恢复协议，但不拥有入口路由权。

## Recovery Evidence Chain

恢复判定优先级：

1. `projects/aigc/<项目名>/governance-state.yaml`，若存在，优先读取 `last_stable_checkpoint`、`resume_contract`、`review_bridge`、`artifact_status`。
2. `projects/aigc/<项目名>/STATE.json`，读取 `current_stage`、`current_stage_path`、`recommended_next_stage`、`recommended_entry_path`、`recommended_next_step`。
3. 初始化核心工件：`0-初始化/north_star.yaml`、`0-初始化/init_handoff.yaml`、`0-初始化/story-source-manifest.yaml`、`team.yaml`。
4. 根治理工件：`mission-brief.yaml`、`route-plan.yaml`、`preflight-verdict.yaml`、`validation-report.md`、`learning-record.md`。
5. 阶段 runtime 真实产物：例如 `1-分集/第N集.md`、`2-编导/第N集.md`、`3-摄影/第N集.md`、`4-分组/第N集.md`、`5-设计/**`、`6-图像/**`、`7-视频/**`。
6. Git 工作区状态与最近修改文件，只能作为辅助证据，不能单独决定断点。

## Recovery Modes

| mode | symptom | safe action |
| --- | --- | --- |
| `lightweight_init_continue` | 初始化五件套和 `STATE.json` 足够，但 `governance-state.yaml` 尚未生成 | 允许低风险回根或下一阶段；复杂恢复前再补治理快照 |
| `governance_rebuild` | `STATE.json` 缺失、初始化核心工件缺失，或高风险 gate 所需治理工件缺失 | 回根 `aigc` 或 `0-初始化` 补治理链 |
| `stage_continue` | 目标阶段真实产物存在，任务 scope 清楚，验收闭环未完成 | 回目标阶段继续，并声明必读输入和 validation gate |
| `gate_reentry` | 内容产物已存在，但缺 preflight、validation 或 package gate | 回根 `aigc` 或 `review/` 做 gate |
| `review_repair_reentry` | `review_bridge` 或 `resume_contract.required_repairs` 指向 repair route | 优先进入 repair route 指向的唯一阶段或根 gate |
| `root_reroute` | 当前阶段不清、路径口径漂移、阶段冻结或缺少技能合同 | 回根 `aigc` 重判 |
| `init_rebootstrap_reroute` | 用户明确要回到初始化态重来 | 交给 `0-初始化`，不按续跑处理 |

## Read Commands

常用只读检查命令：

```bash
test -f "$PROJECT_ROOT/STATE.json" && sed -n '1,220p' "$PROJECT_ROOT/STATE.json"
test -f "$PROJECT_ROOT/governance-state.yaml" && sed -n '1,260p' "$PROJECT_ROOT/governance-state.yaml"
test -f "$PROJECT_ROOT/0-初始化/init_handoff.yaml" && sed -n '1,220p' "$PROJECT_ROOT/0-初始化/init_handoff.yaml"
test -f "$PROJECT_ROOT/0-初始化/story-source-manifest.yaml" && sed -n '1,220p' "$PROJECT_ROOT/0-初始化/story-source-manifest.yaml"
test -f "$PROJECT_ROOT/team.yaml" && sed -n '1,220p' "$PROJECT_ROOT/team.yaml"
find "$PROJECT_ROOT" -maxdepth 3 -type f | sort
git status --short
```

这些命令只用于取证，不自动改写业务真源。

## Governance Gate Rules

- `governance-state.yaml` 存在时，`resume_contract.recommended_entry_*` 是结构化恢复优先证据，但仍需与 `STATE.json` 和产物存在性核对。
- 高风险执行缺 `mission-brief.yaml` 或 `route-plan.yaml` 时，默认先回根 `aigc` 补计划，不直接进入阶段生产。
- 高风险执行缺 `preflight-verdict.yaml` 时，默认输出 `gate_reentry`。
- 已有 `validation-report.md` 且最近 gate 未通过时，应进入 repair route 或 review，而不是继续下游。
- review runner 产生的 `required_repairs` 不得被 resume 擅自合并成内容真稿；resume 只决定回接入口。

## Hard Guards

- 不得伪造不存在的 workflow state。
- 不得只凭目录名、空目录或最近修改时间判断阶段完成。
- 不得把旧英文 runtime 当作新项目默认落点。
- 不得在缺高风险 gate 时直接建议继续生产。
- 不得默认建议 destructive Git 动作。
- 不得把主动 rebootstrap 伪装为 `stage_continue` 或 `governance_rebuild`。
- 不得输出多个并列下一入口；无法唯一时输出 blocker。

## Safe Reentry Shape

一次安全回接必须说明：

- `project_root`
- `evidence_used`
- `resume_mode`
- `risk_level`
- `blockers`
- `required_repairs`
- `unique_next_entry`
- `why_this_entry`

如果恢复需要写入治理工件，必须说明写入 owner 和验证命令；默认情况下只输出建议，不改写项目业务真源。
