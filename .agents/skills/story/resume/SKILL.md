---
name: story-resume
description: Use when a story2026 task was interrupted and the operator needs to inspect `.webnovel/workflow_state.json`, present safe recovery choices, or restart a tracked `story-write` or `story-review` run without guessing the breakpoint.
governance_tier: lite
---

# Task Resume

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- `CONTEXT.md` 只沉淀恢复策略、断点兼容与安全清理经验，不得覆盖本 `SKILL.md` 的 tracked workflow 恢复合同。
- 若恢复经验与 `workflow_manager.py` 当前行为冲突，以本 `SKILL.md` 与实际脚本为准。

## Purpose

- `resume/` 是 `story2026` 在 `5-Loopback` 侧的卫星恢复技能，不负责写入 truth，也不冒充 drafting / review / loopback actualization 主流程。
- 它的职责是：定位真实中断点、给出安全恢复选项、清理或保留现场、把后续执行重新接回当前 canonical truth。
- 当前 canonical truth 约定保持一致：
  - 规划真源：`Planning/8-全息地图.json`
  - 运行态真源：`.webnovel/state.json`
  - 实体/关系/状态变化主存储：`.webnovel/index.db`
  - 工作流断点：`.webnovel/workflow_state.json`
  - 全阶段执行状态：`.webnovel/execution_state.json`
  - 追加式任务日志：`.webnovel/task_log.jsonl`

## Stage Position

- `resume/` 不等于 `5-Loopback` actualization。
- `5-Loopback` 主流程只处理 `4-Validation = PASS` 后的 validated actualization。
- `resume/` 只处理“任务被打断了，如何安全恢复或安全退出恢复流程”。
- 若诉求其实是：
  - 查询运行时信息：转 `query/`
  - 对 PASS 集做正式回写：转 `5-Loopback/`
  - 修正文稿质量问题：转 `3-Drafting` Step 4 或 `review/`

## Supported Scope

正式支持的 tracked workflow 对象：

| command | 恢复能力 | 依据 |
|---|---|---|
| `story-init` | 读取初始化 run、查看当前步骤、继续/清理/重跑建议 | `workflow_manager.py` + `0-Init` 合同 |
| `story-cards` | 读取 cards run、查看子卡步骤、继续/清理/重跑建议 | `workflow_manager.py` + `1-Cards` 合同 |
| `story-plan` | 读取 1-8 planning pass 进度、继续/清理/重跑建议 | `workflow_manager.py` + `2-Planning` 合同 |
| `story-write` | 完整 workflow 断点检测、清理、重启建议 | `workflow_manager.py` + `3-Drafting` 当前 Step 合同 |
| `story-validate` | 读取 validation run、继续/清理/重跑建议 | `workflow_manager.py` + `4-Validation` 合同 |
| `story-review` | 完整 workflow 断点检测、清理、重启建议 | `workflow_manager.py` + `review/` Step 合同 |
| `story-loopback` | 读取 actualization run、继续/清理/重跑建议 | `workflow_manager.py` + `5-Loopback` 合同 |
| `story-query` | 读取 query run、继续/清理/重跑建议 | `workflow_manager.py` + `query/` 合同 |

降级支持：

| 场景 | 支持方式 | 限制 |
|---|---|---|
| 手工 Bash / 临时调试任务被打断 | 只做诊断与安全建议 | 不伪造 `workflow_state.json` |
| 未注册的自定义命令被打断 | 只做诊断与安全建议 | 不伪造 `workflow_state.json / execution_state.json` |

## Project Root Guard

- 工作区根目录不一定等于真实书项目根目录。
- 必须先解析 `PROJECT_ROOT`，它必须包含 `.webnovel/state.json`。
- 所有恢复命令都必须走统一入口 `scripts/story.py`，不要直接绕过统一 CLI 拼脚本路径。

环境设置（bash 命令执行前）：

```bash
export WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
export REPO_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
export SCRIPTS_DIR="${REPO_ROOT}/.agents/skills/story/scripts"
export SKILL_ROOT="${REPO_ROOT}/.agents/skills/story/resume"

python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${WORKSPACE_ROOT}" preflight --format json
export PROJECT_ROOT="$(python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${WORKSPACE_ROOT}" where)"
```

硬门槛：

- `PROJECT_ROOT` 无法解析时立即阻断。
- 若目标任务是 `story-write` 或 `story-review`，`preflight` 必须成功。
- 若 `planning_source=legacy_fallback`，必须明确告知用户当前是 degraded mode。
- 若 `planning_source=missing` 且目标任务是 `story-write`，禁止假装可以安全续跑，必须先修复规划真源。

## Input Contract

最小输入：

- `project_root`
- 用户当前恢复诉求
- `workflow detect` 输出，或能证明“没有 tracked interruption”的诊断结果

可选输入：

- 章节号
- 当前章节正文文件路径
- 最近一次 `git status`
- 来自 `3-Drafting` / `review/` 的失败症状
- 用户是否要“立即继续”还是“只做安全清理”

## Reference Loading Levels

- L0：先判断是否真的是中断恢复诉求。
- L1：加载恢复协议主文件。
- L2：仅在需要确认当前数据真源或恢复后续上下文时，加载数据流规范与上下文契约。

L1（必读）：

- [workflow-resume.md](references/workflow-resume.md)

L2（按需）：

- [system-data-flow.md](references/system-data-flow.md)
- [context-contract-v2.md](../references/context-contract-v2.md)

## Workflow Checklist

复制使用：

```text
恢复进度：
- [ ] Step 0: 预检并解析 PROJECT_ROOT
- [ ] Step 1: 加载恢复协议
- [ ] Step 2: 检测中断状态
- [ ] Step 3: 归一化恢复选项
- [ ] Step 4: 与用户确认恢复策略
- [ ] Step 5: 执行恢复或安全退出
- [ ] Step 6: 重新接回对应 stage
- [ ] Step 7: 验证 closure
```

## Step 0：预检并解析 `PROJECT_ROOT`

必须执行：

```bash
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${WORKSPACE_ROOT}" preflight --format json
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${WORKSPACE_ROOT}" where
```

目标：

- 确认当前目录能解析到真实书项目根。
- 提前暴露 `planning_source`、脚本缺失、project pointer 失效等问题。
- 避免把恢复命令执行到 skill 仓库目录或工作区父目录。

## Step 1：加载恢复协议

```bash
cat "${SKILL_ROOT}/references/workflow-resume.md"
```

必要时再加载：

```bash
cat "${SKILL_ROOT}/references/system-data-flow.md"
cat "${REPO_ROOT}/.agents/skills/story/references/context-contract-v2.md"
```

核心原则：

- 禁止猜断点。
- 禁止把 `workflow detect` 输出中的动作文本原样当执行脚本。
- 禁止为了“省事”直接做 destructive Git 操作。
- 恢复后必须重新接回当前 canonical truth，而不是退回旧 `Planning/legacy/` 默认路径。

## Step 2：检测中断状态

必须执行：

```bash
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow detect
```

解释规则：

- 输出 `✅ 无中断任务`：
  - 说明当前没有 workflow-tracked 断点。
  - 对 `story-query` / 手工任务，只能提供“安全重跑建议”，不能伪造断点续跑。
- 输出 JSON 中断信息：
  - 读取 `command`
  - 读取 `current_step.id`
  - 读取 `completed_steps`
  - 读取 `artifacts`
  - 读取 `elapsed_seconds`

## Step 3：归一化恢复选项

恢复选项必须由 `resume/` 再归一化一次，不直接照搬 `workflow detect` 的原始文本。

### `story-write` 的当前 Step 解释

| tracked step | 语义 | 默认恢复策略 |
|---|---|---|
| `Step 1` | Context Agent | 直接从 Step 1 重建上下文 |
| `Step 2A` | 正文起草 | 优先“带备份地清理半成品 + 从 Step 1 重跑” |
| `Step 2B` | 风格适配 | 与 `Step 2A` 同级处理；必要时保留半成品供人工比对 |
| `Step 3` | 审查 | 重新执行审查，或经用户确认后跳过并转 Step 4 |
| `Step 4` | 润色 | 优先继续润色；若文稿失真，再回 Step 2A |
| `Step 5` | Data Agent | 直接重跑，按幂等步骤处理 |
| `Step 6` | Git/备份收尾 | 默认保留工作区并检查 `git status`，不自动删除正文 |
| `Step 1.5` | legacy 旧断点 | 视为 Step 1 兼容处理，不再单独追踪 |

### `story-review` 的当前 Step 解释

- `Step 1-2`：重新加载 validation 输出与项目状态。
- `Step 3-6`：可从当前聚合/报告/落库位置继续，但必须先确认输入未变。
- `Step 7`：关键问题处理未完成，必须重新向用户确认，不自动替用户裁决。
- `Step 8`：只做收尾，可重新完成任务。

### 统一安全策略

- 优先选项：
  - `cleanup --chapter N` 先预览
  - 用户确认后再 `cleanup --chapter N --confirm`
  - 执行 `workflow clear`
- 保留现场时：
  - 可以先 `workflow fail-task --reason "..."`
  - 再决定是否 `workflow clear`
- 禁止默认执行：
  - `git reset --hard`
  - 假定存在 `ch0007` 之类 tag/commit 再硬回滚
  - 未备份即删除正文文件

## Step 4：与用户确认恢复策略

必须输出四类信息：

1. 当前任务与中断位置
2. 已完成步骤 / 未完成步骤
3. 推荐恢复策略与风险等级
4. 若立即继续，下一跳会进入哪个 stage

确认方式：

- 直接在对话中让用户选 `A/B`
- 或让用户明确说“只清理，不继续”
- 或让用户明确说“保留现场，我稍后人工处理”

禁止事项：

- 不得替用户自动选项
- 不得把“推荐”包装成“已经执行”

## Step 5：执行恢复或安全退出

### 推荐路径：清理半成品后重跑

先预览：

```bash
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow cleanup --chapter {N}
```

用户确认后执行：

```bash
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow cleanup --chapter {N} --confirm
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow clear
```

### 保留现场，仅退出恢复流程

```bash
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow fail-task --reason "manual_inspection_required"
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow clear
```

### 仅清除中断状态

```bash
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow clear
```

## Step 6：重新接回对应 stage

### 继续 `story-write`

- 恢复后默认继续走 `3-Drafting` 当前合同。
- 章节级上下文恢复必须重新以 `Planning/8-全息地图.json` 为默认规划真源。
- 若用户要先检查恢复后的上下文包，可执行：

```bash
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" extract-context --chapter {N} --format json
```

- 若用户选择立即继续，则重新执行 `/story-write {N}`。

### 继续 `story-review`

- 必须重新确认 `4-Validation` 聚合结果仍然可用。
- 若用户选择立即继续，则重新执行 `/story-review ...`，并遵守 `review/` 当前 Step 合同。

### 继续 `story-query`

- 只做安全重跑，不宣称“从断点续查”。
- 若查询涉及规划类问题，继续默认先读 `全息地图.json`。

## Step 7：验证 Closure

至少核对：

- `workflow detect` 不再报告旧断点，或旧断点已按用户意图保留为人工现场。
- 若执行了 cleanup：
  - 已有预览
  - 真正删除前已自动备份正文文件
- 若恢复后继续写作：
  - 明确说明下一跳回到 `3-Drafting`
  - 继续以 holomap-first 方式加载上下文
- 若恢复后继续审查：
  - 明确说明下一跳回到 `review/`
- 若只是退出恢复流程：
  - 明确保留了哪些现场
  - 明确哪些步骤尚未恢复

## Output Contract

`resume/` 至少输出：

- `project_root`
- `tracked_command`
- `current_step`
- `interruption_summary`
- `normalized_recovery_options`
- `recommended_option`
- `user_confirmed_option`
- `commands_executed`
- `next_stage_handoff`

## Root-Cause 执行合同

- 若恢复建议与真实脚本行为不一致，必须先上溯脚本和阶段合同，不只改本次说明话术。
- 本 skill 的 `Rule Source` 默认优先检查：
  - `resume/SKILL.md`
  - `resume/references/workflow-resume.md`
  - `scripts/workflow_manager.py`
  - `3-Drafting/SKILL.md`
  - `review/SKILL.md`
  - `5-Loopback/SKILL.md`
- `Meta Rule Source` 默认上溯到仓库 `AGENTS.md` 与相关 meta skill。
- 修复顺序必须是：先修恢复合同与脚本安全策略，再修本次恢复提示文本。

## Lite Tier Field Mapping（Combined）

| field_id | step_id | intent | required_output | fail_code | rework_entry |
|---|---|---|---|---|---|
| FIELD-RESUME-ROOT-01 | Step 0 | 解析真实书项目根并做环境预检 | `project_root`、`preflight_status` | FAIL-RESUME-ROOT-01 | 回到 preflight，修正 project pointer / 工作区路径 |
| FIELD-RESUME-DETECT-02 | Step 2 | 读取真实 workflow 中断状态 | `tracked_command`、`current_step`、`interruption_summary` | FAIL-RESUME-DETECT-02 | 回到 `workflow detect`，禁止猜测断点 |
| FIELD-RESUME-NORMALIZE-03 | Step 3 | 把原始检测结果归一化成安全恢复选项 | `normalized_recovery_options`、`recommended_option` | FAIL-RESUME-NORMALIZE-03 | 回到恢复策略层，移除危险或过时动作 |
| FIELD-RESUME-CONFIRM-04 | Step 4 | 让用户确认恢复还是退出 | `user_confirmed_option` | FAIL-RESUME-CONFIRM-04 | 回到确认层，不得替用户自动决策 |
| FIELD-RESUME-HANDOFF-05 | Step 5-7 | 执行恢复并接回正确 stage | `commands_executed`、`next_stage_handoff` | FAIL-RESUME-HANDOFF-05 | 回到执行/交接层，确认 cleanup / clear / rerun 顺序 |

## Completion Gate

- 已确认真实 `PROJECT_ROOT`，不是误用工作区父目录。
- 已执行 `workflow detect`，而不是主观猜测中断点。
- 恢复选项已去除过时或 destructive 默认动作。
- 已明确“下一跳回哪个 stage”，而不是把 `resume/` 冒充主执行器。
- 若恢复继续写作/查询，已明确使用 holomap-first。
