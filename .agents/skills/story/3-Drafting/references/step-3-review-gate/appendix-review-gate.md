# Step 3 Review Gate

> Canonical module route: `references/step-3-review-gate/module-spec.md`
> 当前角色：Step 3 appendix。根 `SKILL.md` 不再直接路由到本文件。

## 调用约束（硬规则）

- Step 3 的 canonical 入口是 [`4-Validation`](../../../4-Validation/SKILL.md)，而不是主流程直接起 checker。
- 必须通过 `4-Validation` 创建新的后台多智能体团队，再由该团队并行调度 checker。
- 禁止主流程直接内联“自审结论”。
- `overall_score` 必须来自隔离评估团队的聚合结果，不可主观估分。
- 单章写作场景下，统一传入：`{chapter, chapter_file, project_root}`。

## 审查路由模式

- 标准/`--fast`：`auto` 路由（核心 3 个 + 条件命中）。
- `--minimal`：固定核心 3 个（不启用条件审查器）。

核心审查器（始终执行）：
- `consistency-checker`
- `continuity-checker`
- `ooc-checker`
- `immersion-voice-checker`

条件审查器（仅 `auto` 命中时执行）：
- `reader-pull-checker`
- `high-point-checker`
- `pacing-checker`
- `spoiler-checker`

## Auto 路由判定信号

输入信号来源：
1. Step 1 创作执行包 / Context Contract（是否过渡章、追读力设计、核心冲突）。
2. 本章正文（战斗/反转/高光/章末未闭合问题等信号）。
3. 章节规划标签（关键章/高潮章/卷末章/转场章）。
4. 最近章节节奏（连续主线、情感线断档、世界观线断档）。

路由规则：
- `reader-pull-checker`：当满足任一条件时启用
  - 非过渡章；
  - 有明确未闭合问题/期待锚点；
  - 用户显式要求“追读力审查”。
- `high-point-checker`：当满足任一条件时启用
  - 关键章/高潮章/卷末章；
  - 正文出现战斗、反杀、打脸、身份揭露、大反转等高光信号。
- `pacing-checker`：当满足任一条件时启用
  - 章号 >= 10；
  - 最近章节存在明显节奏失衡风险；
  - 用户显式要求“节奏审查”。
- `spoiler-checker`：当满足任一条件时启用
  - 当前章存在活跃伏笔或计划中的 `payoff_window`；
  - 题材命中悬疑/规则/推理/身份反转类；
  - 用户显式要求“反剧透审查”。

## 团队调度模板（示意）

```text
selected = ["consistency-checker", "continuity-checker", "ooc-checker", "immersion-voice-checker"]

if mode != "minimal":
  if trigger_reader_pull: selected.append("reader-pull-checker")
  if trigger_high_point: selected.append("high-point-checker")
  if trigger_pacing: selected.append("pacing-checker")
  if trigger_spoiler: selected.append("spoiler-checker")

enter 4-Validation
create new background isolated team
parallel dispatch selected agents inside the new team
aggregate results
handoff aggregate packet to review/
```

## 输出契约（统一）

每个 checker 返回值必须遵循 `.agents/skills/story/references/checker-output-schema.md`：
- 必含：`agent`、`chapter`、`overall_score`、`pass`、`issues`、`metrics`、`summary`
- 允许扩展字段（如 `hard_violations`、`soft_suggestions`），但不得替代必填字段

`4-Validation` 聚合输出最小字段：
- `validation_mode`
- `chapter`（单章）
- `start_chapter`、`end_chapter`（单章时二者都等于 `chapter`）
- `selected_agents`
- `overall_score`
- `severity_counts`
- `critical_issues`
- `issues`（扁平化聚合）
- `dimension_scores`（按已启用 checker 计算）
- `anti_ai_force_check`
- `spoiler_risk`
- `contrivance_risk`
- `cold_commentary_risk`
- `routing_decision`
- `handoff_targets`

## 汇总输出模板

```text
审查汇总 - 第 {chapter_num} 章
- 验证模式: {validation_mode}
- 已启用审查器: {list}
- 严重问题: {N} 个
- 高优先级问题: {N} 个
- 综合评分: {score}
- 可进入润色: {是/否}
```

## 审查指标落库（必做）

> 由 `review/` 承接生成 `review_metrics.json` 并完成落库；Step 3 必须确保可落库字段齐全。

```bash
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" index save-review-metrics --data "@${PROJECT_ROOT}/.webnovel/tmp/review_metrics.json"
```

review_metrics 文件字段约束（当前工作流约定只传以下字段）：
- `start_chapter`（int）、`end_chapter`（int）：单章时二者相等
- `overall_score`（float）：必填
- `dimension_scores`（Dict[str, float]）：按已启用 checker 计算
- `anti_ai_force_check`（str）：`pending|pass|fail`
- `spoiler_risk`（str）：`low|medium|high|critical`
- `contrivance_risk`（str）：`low|medium|high|critical`
- `cold_commentary_risk`（str）：`low|medium|high|critical`
- `severity_counts`（Dict[str, int]）：键为 critical / high / medium / low
- `critical_issues`（List[str]）
- `report_file`（str）
- `notes`（str）：在当前执行契约中必须是单个字符串；`selected_agents`、`validation_mode`、`routing_decision`、`timeline_gate` 等扩展信息统一压成单行文本写入此字段，不得作为独立顶层键传入

## 进入 Step 4 前闸门

- `overall_score` 已由隔离评估团队生成。
- `review/` 已完成 `save-review-metrics`。
- 审查报告中的 `issues`、`severity_counts` 可被 Step 4 直接消费。
- `spoiler_risk / contrivance_risk / cold_commentary_risk` 已进入正式指标，而非 `notes`。
- **时间线闸门**：若存在 `TIMELINE_ISSUE` 且 `severity >= high`，禁止进入 Step 4/5，必须先修复。

### 时间线闸门规则

**Hard Block（必须修复才能继续）**：
- `TIMELINE_ISSUE` + `severity = critical`
- `TIMELINE_ISSUE` + `severity = high`

**Soft Warning（建议修复但可继续）**：
- `TIMELINE_ISSUE` + `severity = medium`
- `TIMELINE_ISSUE` + `severity = low`

**闸门判定逻辑**：
```text
timeline_issues = filter(issues, type="TIMELINE_ISSUE")
critical_timeline = filter(timeline_issues, severity in ["critical", "high"])

if len(critical_timeline) > 0:
    BLOCK: "存在 {len(critical_timeline)} 个严重时间线问题，必须修复后才能进入润色步骤"
    return BLOCKED
else:
    通过: "时间线检查通过"
```
