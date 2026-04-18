---
name: workflow-resume
purpose: 中断恢复时加载，约束如何检测、归一化和执行安全恢复
---

<context>
本文件只定义 `resume/` 的恢复原则与安全边界，不替代 `3-Drafting`、`review/`、`5-Loopback` 自身的 stage 合同。
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
- `story-loopback`
- `story-query`

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
6. 恢复后继续 `story-write` / `story-plan` / 规划类 `query` 时，默认重新接回 `Planning/8-全息地图.json`。
7. 优先读取 `execution_state.json + task_log.jsonl` 辅助判断全阶段 run 与 resume marker，不把 `workflow_state.json` 当唯一线索。

## Step 语义与默认策略

### `story-write`

| tracked step | 当前含义 | 默认策略 |
|---|---|---|
| `Step 1` | Context Agent | 重新做 Step 1 |
| `Step 2A` | 正文起草 | 清理半成品后从 Step 1 重跑 |
| `Step 2B` | 风格适配 | 视情况继续适配，或退回 Step 2A |
| `Step 3` | 审查 | 重新执行审查，或用户确认跳过 |
| `Step 4` | 润色 | 优先继续润色 |
| `Step 5` | Data Agent | 直接重跑（幂等） |
| `Step 6` | Git/备份收尾 | 保留工作区，继续提交或人工处理 |
| `Step 1.5` | legacy 旧断点 | 兼容视为 Step 1 |

### `story-review`

| tracked step | 当前含义 | 默认策略 |
|---|---|---|
| `Step 1-2` | 读取 validation 结果与项目状态 | 重新加载 |
| `Step 3-6` | 汇总、报告、落库、写回 | 核对输入未变后继续 |
| `Step 7` | 关键问题人工决策 | 必须重新确认 |
| `Step 8` | 收尾 | 完成任务 |

## 推荐恢复选项模板

### 模板 A：删除半成品并重跑（推荐）

- 风险：`low`
- 适用：`story-write` 的 `Step 2A / Step 2B`
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
- 适用：`Step 4 / Step 5 / Step 6`，或 `story-review` 中后段
- 动作：
  - 核对输入文件仍存在且未被外部改坏
  - 从当前 stage 继续，而不是回滚全部流程

## 禁止事项

- ❌ 直接按 `detect` 输出里的文本动作无脑执行
- ❌ 自动替用户选择恢复策略
- ❌ 未备份即删除正文
- ❌ 把 `resume/` 冒充 `5-Loopback` actualization 主流程
- ❌ 恢复后继续默认退回旧 `Planning/legacy/`

</instructions>

<examples>

<example>
<input>`story-write` 在 `Step 2A` 中断</input>
<output>
当前中断：`story-write` / `Step 2A`

推荐：
A) 预览并清理半成品，然后从 Step 1 重跑（推荐，low）
B) 保留半成品做人工检查，再手动决定是否重跑（medium）

下一跳：
- 若选 A：回到 `3-Drafting`
- 继续写作时默认重新读取 `Planning/8-全息地图.json`
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
- 当前没有 `story-query` 的正式 workflow 断点记录
- 本次只能做安全重跑建议，不做假断点续跑

建议：
A) 重新定位 `PROJECT_ROOT` 后直接重跑查询
B) 若担心上下文漂移，先确认当前规划真源仍是 `全息地图.json`
</output>
</example>

</examples>
