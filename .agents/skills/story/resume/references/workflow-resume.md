---
name: workflow-resume
purpose: 中断恢复时加载，约束如何检测、归一化和执行安全恢复
---

<context>
本文件只定义 `resume/` 的恢复原则与安全边界，不替代 `3-初稿`、`review/`、`context-return` 自身的 stage 合同。
</context>

<instructions>

## 支持范围

正式 workflow 断点恢复支持：

- `story-init`
- `story-cards`
- `story-plan`
- `story-write`
- `story-validate`
- `story-review`
- `story-context-return`
- `story-query`（轻量 tracked run，仅 generic recovery）

其余场景：

- 手工 Bash / 临时调试任务只做安全重跑建议，不做假断点续跑
- 未注册命令要先补 workflow registry，再谈正式断点恢复

## 检测命令

```bash
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow detect
```

恢复类操作统一走：

```bash
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow cleanup --chapter {N}
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow cleanup --chapter {N} --confirm
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow fail-task --reason "{reason}"
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow clear
```

## 安全恢复原则

1. 先 `detect`，后恢复。
2. 任何 destructive cleanup 先预览，再确认。
3. 删除正文前必须由脚本自动备份。
4. 不默认执行 `git reset --hard`。
5. 不假定存在 `ch0007` 之类 tag/commit。
6. 恢复后继续 `story-write` / `story-plan` / 规划类 `query` 时，默认重新接回 `2-卷章/整体规划.md + 第N卷/卷规划.md + 第N卷/第N章.md`。
7. 优先读取 `STATE.json.workflow_runtime.execution_state + task_log` 辅助判断全阶段 run 与 resume marker，不把 `workflow_state` 当唯一线索。
8. `story-query` 若存在 tracked run，可读其 run 信息；但默认只给 generic continue / rerun / diagnosis，不提供章节 cleanup。
9. 若 `workflow detect` 没有 tracked 中断，必须继续执行 artifact fallback 检测，而不是立刻返回“无中断任务”。

## No-Interrupt Artifact Fallback

当 `workflow detect` 没命中 `current_task` 时，继续按以下顺序寻找可证明的下一入口：

1. `context-return/第V卷.context-return.json`
2. `review/第V卷.validation.json`
3. `review/第V卷审查报告.md` + `STATE.json.review_checkpoints`
4. `3-初稿/第V卷.写作日志.yaml`

默认解释：

- 命中最新 `上下文回流`：
  - 视为上一卷已完成 validated actualization
  - 下一稳定入口：`story-write` 下一卷首章 worker
- 命中 `validation PASS`，但无 review 持久化：
  - 下一稳定入口：`story-review`
- 命中 `validation PASS + review 持久化`，但无 上下文回流：
  - 下一稳定入口：`story-context-return`
- 命中 `candidate_volume_draft` 写作日志，但无 validation 包：
  - 下一稳定入口：`story-review`
- 命中 `validation FAIL`：
  - 按 `routing_decision` 回 `story-write` 或 source contract owner

禁止：

- 把 artifact fallback 当成 tracked interruption 伪装输出
- 在已存在 `validation / review / 上下文回流` 业务证据时仍简单打印“无中断任务”
- 只看 `STATE.current_stage` 就给结论；它只能作为弱摘要，不是 fallback 真源

## Step 语义与默认策略

### `story-write`

| tracked step | 当前含义 | 默认策略 |
|---|---|---|
| `Step 1` | 单章叙事起盘 | 重新做 Step 1 |
| `Step 2` | 节奏优化（父层工序） | 优先继续当前工序，必要时清理当前章正文后回到 Step 1 |
| `Step 3` | 场景和氛围渲染 | 优先继续当前工序，必要时清理当前章正文后回到 Step 1 |
| `Step 4` | 角色形象刻画 | 优先继续当前工序，必要时清理当前章正文后回到 Step 1 |
| `Step 5` | 对白优化 | 优先继续当前工序，必要时清理当前章正文后回到 Step 1 |
| `Step 6` | 心理活动描写 | 优先继续当前工序，必要时清理当前章正文后回到 Step 1 |
| `Step 7` | 追读力强化 | 优先继续当前工序，必要时清理当前章正文后回到 Step 1 |
| `Step 8` | 润色 | 优先继续终修，必要时清理当前章正文后回到 Step 1 |
| `Step 1.5` | legacy 旧断点 | 兼容视为 Step 1 |

### `story-review`

| tracked step | 当前含义 | 默认策略 |
|---|---|---|
| `Step 1-2` | 读取 validation 结果与项目状态 | 重新加载 |
| `Step 3-6` | 汇总、报告、落库、写回 | 核对输入未变后继续 |
| `Step 7` | 关键问题人工决策 | 必须重新确认 |
| `Step 8` | 收尾 | 完成任务 |

## 推荐恢复选项模板

### 模板 A：删除当前章正文并重跑（推荐）

- 风险：`low`
- 适用：`story-write` 的 `Step 2-8`
- 动作：
  - 先 `workflow cleanup --chapter {N}` 预览
  - 用户确认后 `workflow cleanup --chapter {N} --confirm`
  - `workflow clear`
  - 重新执行原命令

### 模板 B：保留现场供人工检查

- 风险：`medium`
- 适用：需要先比对半成品或保留证据链
- 动作：
  - `workflow fail-task --reason "..."`
  - 必要时保留正文与工作区
  - `workflow clear`
  - 稍后人工决定是否重跑

### 模板 C：继续当前后置步骤

- 风险：`low` 到 `medium`
- 适用：`Step 4 / Step 5 / Step 6 / Step 7`，或 `story-review` 中后段
- 动作：
  - 核对输入文件仍存在且未被外部改坏
  - 从当前 stage 继续，而不是回滚全部流程

## 禁止事项

- ❌ 直接按 `detect` 输出里的文本动作无脑执行
- ❌ 自动替用户选择恢复策略
- ❌ 未备份即删除正文
- ❌ 把 `resume/` 冒充 `context-return` actualization 主流程
- ❌ 恢复后继续默认退回旧 `2-卷章/legacy/`

</instructions>

<examples>

<example>
<input>`story-write` 在 `Step 5` 中断</input>
<output>
当前中断：`story-write` / `Step 5`

推荐：
A) 保留 `3-初稿/第N卷/第N章.md`，继续当前工序（推荐，low）
B) 预览并清理当前章正文，然后从 Step 1 重跑（medium）
C) 保留半成品做人工检查，再手动决定是否重跑（medium）

下一跳：
- 若选 A：继续当前 `Step 5`
- 继续写作时默认重新读取 `2-卷章/整体规划.md + 第N卷/卷规划.md + 第N卷/第N章.md`
</output>
</example>

<example>
<input>`story-review` 在 `Step 7` 中断</input>
<output>
当前中断：`story-review` / `Step 7`

推荐：
A) 重新向用户确认关键问题处理策略
B) 仅清理 workflow 状态，保留当前报告与落库结果供人工复查

禁止：
- 不得替用户自动做 Step 7 的最终裁决
</output>
</example>

<example>
<input>用户说“刚才 query 断了，帮我恢复”</input>
<output>
说明：
- 若 `workflow detect` 已命中 `story-query` run，可说明最近卡在 truth-role / source locate / evidence assemble 哪一步
- 该类恢复仍只提供 generic 继续 / 安全重跑 / 人工诊断，不做章节 cleanup

建议：
A) 若输入未变，按当前 query run 继续或直接重跑查询
B) 若担心上下文漂移，先确认当前规划真源仍是 `整体规划.md + 第N卷/卷规划.md + 第N卷/第N章.md`
C) 若需要保留证据链，先 `workflow fail-task --reason "manual_inspection"` 再人工诊断
</output>
</example>

<example>
<input>workflow detect 显示无中断，但项目里已有 `review/第1章.validation.json` 和 `review/第1-1章审查报告.md`，还没有 `context-return/第1章.context-return.json`</input>
<output>
说明：
- 当前没有 tracked interruption
- 但 artifact fallback 已命中：`validation PASS + review persisted + 上下文回流 pending`

建议：
A) 进入 `story-context-return` 执行第1章 actualization（推荐）
B) 先人工核对 validation packet 与 review checkpoint，再执行 actualization
</output>
</example>

</examples>
