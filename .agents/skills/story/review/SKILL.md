---
name: story-review
description: Use when `4-Validation` 已产出聚合结果，或需要把正式章节审查结论落盘、回写状态并衔接 `5-Loopback` / 修复闭环。
governance_tier: lite
allowed-tools: Read Grep Write Edit Bash Task
---

# Quality Review Skill

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- `CONTEXT.md` 只承载报告层、持久化层与趋势层的经验，不得覆盖本 `SKILL.md` 的上游 intake gate 与下游 handoff 边界。
- 若 `CONTEXT.md` 与 `4-Validation` 聚合字段合同冲突，以本 `SKILL.md` 与 shared references 为准。

## Scope

- `review/` 是**评估结果承接层**，负责报告生成、评分落库、状态回写、关键问题升级，以及向后续闭环提供稳定的审查持久化结果。
- 它不是 canonical checker 调度入口；canonical 调度入口始终是 [`4-Validation`](../4-Validation/SKILL.md)。
- 当用户直接调用 `/story-review` 且未显式提供当前轮聚合结果时，必须先进入 `4-Validation` 创建新的后台隔离评估团队；若当前轮聚合结果已存在且仍有效，可直接由 `review/` 消费。

## Stage Alignment（必须遵守）

- `4-Validation`
  - 拥有评估判断权、`validation_status` 判定权、`routing_decision` 判定权。
- `review/`
  - 只拥有报告、持久化、升级与闭环编排权。
- `5-Loopback`
  - 只拥有 validated truth writeback / actualization 权。

硬规则：

- `review/` 不得重写 `validation_status`、`routing_decision`、`handoff_targets`。
- `review/` 可以补充 `review_handoff_summary`，但不能替代 `4-Validation` 的 handoff packet。
- 若用户在 `PASS` 结果上要求先修问题，则该 `PASS` 只可视为“已过一轮评估”，不能继续直接进入 `5-Loopback`；修复后必须重新跑 `4-Validation`。

## Project Root Guard（必须先确认）

- Codex / Claude Code 的“工作区根目录”不一定等于“书项目根目录”。
- 必须先解析真实书项目根（必须包含 `STATE.json`），后续所有读写路径都以该目录为准。

环境设置（bash 命令执行前）：
```bash
export WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
export REPO_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"

if [ ! -d "${REPO_ROOT}/.agents/skills/story/review" ]; then
  echo "ERROR: 缺少目录: ${REPO_ROOT}/.agents/skills/story/review" >&2
  exit 1
fi
export SKILL_ROOT="${REPO_ROOT}/.agents/skills/story/review"

if [ ! -d "${REPO_ROOT}/.agents/skills/story/scripts" ]; then
  echo "ERROR: 缺少目录: ${REPO_ROOT}/.agents/skills/story/scripts" >&2
  exit 1
fi
export SCRIPTS_DIR="${REPO_ROOT}/.agents/skills/story/scripts"

export PROJECT_ROOT="$(python "${SCRIPTS_DIR}/story.py" --project-root "${WORKSPACE_ROOT}" where)"
```

## 输入合同

最小输入：

- `project_root`
- `chapter` 或 `{start_chapter, end_chapter}`
- 来自 `4-Validation` 的聚合评估结果

聚合评估结果至少必须包含：

- `validation_mode`
- `validation_status`
- `selected_agents`
- `issues`
- `severity_counts`
- `critical_issues`
- `overall_score`
- `dimension_scores`
- `anti_ai_force_check`
- `spoiler_risk`
- `contrivance_risk`
- `cold_commentary_risk`
- `routing_decision`
- `handoff_targets`

推荐附带：

- `chapter`、`start_chapter`、`end_chapter`
- `validation_ref`
- 各 checker 原始输出
- 章节文件路径
- 用户额外关注项

## 数据源现实（与最新系统对齐）

- `4-Validation` 聚合结果
  - 是本 skill 的唯一审查判断真源。
- `STATE.json`
  - 只承担轻量运行态与 checkpoint 摘要，不承载大体量实体/关系数据。
- `Planning/全息地图.json`
  - 是规划真源；若需要定位问题落点、说明后续影响、或给 `5-Loopback`/`3-Drafting` 回流说明，应优先读 holomap，而不是回退到旧 `Planning/legacy/`。
- `index.db.review_metrics`
  - 是趋势统计与横向比较数据源；不替代本轮聚合结果。

## Shadow Governance Artifact Chain

若本轮 `review/` 跑在 tracked workflow 中，必须把当前 `<run_id>` 的 task artifact 目录视为正式承接层之一：

- 读取并保留 `mission_brief_ref / preflight_verdict_ref / validation_report_ref`
- 生成正式审查报告后，允许把报告路径、状态与 next action 写回同一 `<run_id>` 的工件索引
- 不得因为 task dir 已有 `validation_report.md` 就跳过正式 `Validation/第X章审查报告.md` 的业务报告输出

边界：

- task dir 是治理闭环证据层。
- `Validation/第X章审查报告.md` 是书项目业务报告层。
- 两者必须互相回指，但不能互相替代。

## 0.5 工作流断点（best-effort，不得阻断主流程）

> 目标：让 `/story-resume` 能基于真实断点恢复。即使 workflow_manager 出错，也只记录警告。

推荐（bash）：
```bash
python "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow start-task --command story-review --chapter {end_chapter} || true
```

Step 映射（必须与 `workflow_manager.py get_pending_steps("story-review")` 对齐）：

- Step 1：确认 `4-Validation` 输出
- Step 2：加载参考与项目状态
- Step 3：汇总评估结果并组装审查工件
- Step 4：生成审查报告
- Step 5：保存审查指标到 index.db
- Step 6：写回审查记录到 `STATE.json`
- Step 7：处理关键问题升级 / 修复分流
- Step 8：收尾（完成任务）

## Step 1：确认 `4-Validation` 输出

硬要求：

- 若当前没有 `4-Validation` 的聚合输出，必须先回到 `4-Validation` 创建新的后台多智能体团队。
- 不得在 `review/` 内直接复用旧 checker 线程或直接产出“自审”结论。
- 若用户是直接调用 `/story-review` 且未给出当前轮聚合结果，本 skill 的第一动作仍然是触发 `4-Validation`，而不是跳过隔离评估。
- 若用户已显式提供当前轮聚合 JSON / `validation_ref`，可直接进入 `review/`，但必须先校验字段完整性与当前轮有效性。
- 若 `validation_status=PASS`：
  - 必须保留上游的 `routing_decision=handoff_to_review_and_loopback`
  - 必须保留 `handoff_targets` 中的 `review/` 与 `5-Loopback`
- 若 `validation_status!=PASS`：
  - 本 skill 可以生成报告与落盘，但不得伪造 loopback-ready 结论。

## Step 2：加载参考与项目状态（按需）

必读：
```bash
cat "${REPO_ROOT}/.agents/skills/story/_shared/core-constraints.md"
cat "${REPO_ROOT}/.agents/skills/story/_shared/context-loading-contract.md"
cat "$PROJECT_ROOT/STATE.json"
```

按需：
```bash
cat "$PROJECT_ROOT/Planning/全息地图.json"
cat "${SKILL_ROOT}/references/common-mistakes.md"
cat "${SKILL_ROOT}/references/pacing-control.md"
python "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" index get-recent-review-metrics --limit 5
```

读取原则：

- 定位本轮问题本体：先读 `4-Validation` 聚合结果。
- 解释规划影响与下游回流：优先读 `全息地图.json`。
- 查看运行态和历史 checkpoint：读 `STATE.json`。
- 做趋势叙述或横向比较：读 `index.db.review_metrics`。

## Step 3：汇总评估结果并组装审查工件

职责：

- 消费 `4-Validation` 的聚合输出，不改写 checker 原始判断。
- 只做报告级归并、问题分桶、优先级排序、工件整理与持久化前格式化。

硬要求：

- `overall_score` 必须来自聚合结果，不可在 `review/` 层主观重估。
- `issues / severity_counts / critical_issues` 必须原样可追溯到上游聚合结果。
- `anti_ai_force_check / spoiler_risk / contrivance_risk / cold_commentary_risk` 必须原样进入 `review_metrics` 正式字段。
- `validation_status / routing_decision / handoff_targets` 只可复制进辅助工件，不可在 `review/` 层改写。
- 若发现聚合结果缺字段或相互矛盾，应阻断并回溯 `4-Validation` / checker 合同，而不是在 `review/` 层自行补猜。

本阶段至少组装两类工件：

1. `review_metrics.json`
   - 只包含允许落库的指标字段。
2. `review_handoff_summary`
   - 记录：
     - `validation_status`
     - `routing_decision`
     - `handoff_targets`
     - `report_file`
     - `review_metrics_saved`
     - `review_checkpoint_written`
     - `critical_blockers`
     - `next_action`

## Step 4：生成审查报告

保存到：`Validation/第{start_chapter}-{end_chapter}章审查报告.md`

报告结构（精简版）：
```markdown
# 第 {start_chapter}-{end_chapter} 章质量审查报告

## 评估团队
- 验证模式
- 验证状态
- 已启用审查器
- 是否来自新后台隔离团队

## 综合评分
- 爽点密度 / 设定一致性 / 节奏控制 / 人物塑造 / 连贯性 / 追读力
- 总评与等级

## 修改优先级
- 高优先级（必须修改）
- 中优先级（建议修改）
- 低优先级（可选优化）

## 风险雷达
- anti_ai_force_check
- spoiler_risk
- contrivance_risk
- cold_commentary_risk

## 下游影响
- 是否允许进入 `5-Loopback`
- 是否必须先回到 `3-Drafting` / 其他源层

## 改进建议
- 可执行的修复建议
```

审查指标 JSON（用于趋势统计）：
```json
{
  "start_chapter": 100,
  "end_chapter": 100,
  "overall_score": 85.0,
  "dimension_scores": {
    "爽点密度": 8.5,
    "设定一致性": 8.0,
    "节奏控制": 7.8,
    "人物塑造": 8.2,
    "连贯性": 9.0,
    "追读力": 8.7
  },
  "anti_ai_force_check": "pass",
  "spoiler_risk": "low",
  "contrivance_risk": "medium",
  "cold_commentary_risk": "low",
  "severity_counts": {"critical": 0, "high": 1, "medium": 2, "low": 0},
  "critical_issues": ["问题描述"],
  "report_file": "Validation/第100-100章审查报告.md",
  "notes": "单个字符串；selected_agents / validation_mode / routing_decision / handoff_targets 等扩展信息压成单行文本写入此字段"
}
```

## Step 5：保存审查指标到 index.db（必做）

```bash
python "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" index save-review-metrics --data '@review_metrics.json'
```

硬要求：

- `anti_ai_force_check / spoiler_risk / contrivance_risk / cold_commentary_risk` 必须真实写入 SQLite 正式列，而不是只存在于 JSON 示例或 `notes`。
- 若落库失败的根因是 schema 缺列或 CLI 丢字段，先修持久化源层，再重试本轮落库。

## Step 6：写回审查记录到 `STATE.json`（必做）

```bash
python "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" update-state -- \
  --add-review "{start_chapter}-{end_chapter}" "Validation/第{start_chapter}-{end_chapter}章审查报告.md" \
  --review-anti-ai-force-check "{anti_ai_force_check}" \
  --review-spoiler-risk "{spoiler_risk}" \
  --review-contrivance-risk "{contrivance_risk}" \
  --review-cold-commentary-risk "{cold_commentary_risk}"
```

写回原则：

- `STATE.json.review_checkpoints` 只保存摘要指针：
  - 章节范围
  - 报告路径
  - 时间戳
  - `anti_ai_force_check / spoiler_risk / contrivance_risk / cold_commentary_risk`
- 不把完整 issues / 分数明细重新塞回 `STATE.json`，但上述四个一等风险字段必须作为轻量摘要同步回写，供 resume / status / trend 快速读取。

## Step 7：处理关键问题升级 / 修复分流

若发现 critical 问题（`severity_counts.critical > 0` 或 `critical_issues` 非空），必须做用户升级分流。

Codex / 普通对话环境中，使用纯文本分流卡，不依赖 `AskUserQuestion`：

```markdown
发现 critical 问题，建议选择：

A. 立即修复（推荐）
B. 先保存报告，稍后处理
```

若用户选择 A：

- 输出返工清单：逐条 critical 问题 -> 定位 -> 最小修复动作 -> 注意事项。
- 若用户明确授权可直接修改正文文件，则做最小修复。
- 一旦进入修复，本轮原始 `PASS` 不得继续直接进入 `5-Loopback`；必须在修后重新进入 `4-Validation` 开一轮新隔离团队复核。

若用户选择 B：

- 不做正文修改，仅保留审查报告、指标记录、升级说明。
- 若本轮 `validation_status!=PASS`，按上游 `routing_decision` 回流修复路径。
- 若本轮 `validation_status=PASS`，`review/` 只记录“延期处理”说明，不改写上游 gate。

## Step 8：收尾（完成任务）

```bash
python "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow start-step --step-id "Step 8" --step-name "收尾" || true
python "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow complete-step --step-id "Step 8" --artifacts '{"ok":true}' || true
python "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow complete-task --artifacts '{"ok":true}' || true
```

## 输出合同

`review/` 至少应产出：

- `report_file`
- `review_metrics_ref`
- `review_checkpoint_ref`
- `review_handoff_summary`
- `escalation_decision`

说明：

- `review_metrics_ref`
  - 指向已落库指标记录或其对应的章节范围。
- `review_checkpoint_ref`
  - 指向 `STATE.json.review_checkpoints` 的新增摘要项。
- `review_handoff_summary`
  - 只做结果桥接，不改写 `4-Validation` 的 upstream gate packet。

## Root-Cause 执行合同

- 若报告失真、落库数据不一致、引用路径错误、关键问题被错误升级，必须按 `Symptom -> Direct Cause -> Rule Source -> Meta Rule Source` 上溯。
- `Rule Source` 默认优先检查：
  - 当前 `review/SKILL.md`
  - `4-Validation/SKILL.md`
  - `../4-Validation/_shared/validation-team-contract.md`
  - `../3-Drafting/_shared/drafting-instant-validation-contract.md`
  - `scripts/data_modules/index_manager.py`
  - `scripts/data_modules/index_reading_mixin.py`
- `Meta Rule Source` 默认上溯到仓库 `AGENTS.md` 与相关 meta skill。
- 修复顺序必须是：
  1. 先修 intake / 持久化 / handoff 源层合同
  2. 再修报告模板与升级分流
  3. 最后才是本次正文或单次产物

## Lite Tier Field Mapping（Combined）

| field_id | step_id | intent | required_output | fail_code | rework_entry |
|---|---|---|---|---|---|
| FIELD-REV-INTAKE-01 | Step 1 | 确认输入来自 `4-Validation` 新团队，且 gate 信息完整 | 上游聚合结果确认、`validation_status`、`routing_decision`、`handoff_targets` | FAIL-REV-INTAKE-01 | 回到 `4-Validation` 补跑或补齐聚合字段 |
| FIELD-REV-LOAD-02 | Step 2 | 按最新系统读取轻量状态、规划真源与趋势数据 | `STATE.json`、holomap、必要参考加载确认 | FAIL-REV-LOAD-02 | 修正路径或数据流入口，禁止回退旧 `Planning/legacy/` 冒充真源 |
| FIELD-REV-AGG-03 | Step 3 | 保真汇总上游评估结论并生成闭环工件 | `issues`、`severity_counts`、`critical_issues`、`overall_score`、`review_handoff_summary` | FAIL-REV-AGG-03 | 回到聚合接口检查缺字段、矛盾或 gate 被改写 |
| FIELD-REV-PERSIST-04 | Step 4-6 | 生成报告并完成落库回写 | 审查报告、`review_metrics`、`review_checkpoints` | FAIL-REV-PERSIST-04 | 重做报告或修复 SQLite/state 持久化 |
| FIELD-REV-ESCALATE-05 | Step 7 | 对 critical 做人工升级与返工引导 | 返工清单或延期处理决定 | FAIL-REV-ESCALATE-05 | 重新执行关键问题升级流程 |

## Completion Gate

- 本轮报告基于当前轮 `4-Validation` 聚合输出，且该输出已确认仍有效。
- `review_metrics` 已落库，且四个风险字段已写入正式列。
- `STATE.json.review_checkpoints` 已回写摘要记录。
- 已生成 `review_handoff_summary`，且未改写上游 `validation_status / routing_decision / handoff_targets`。
- critical 问题已触发人工升级或记录延期决定。
- 若进入修复闭环，已明确“修复后必须重新走一轮新的隔离评估”，且本轮结果不得直接进入 `5-Loopback`。
