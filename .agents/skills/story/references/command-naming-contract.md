# story2026 命名合同

## Purpose

本文件是 `story2026` 命令命名的单一真源。

它统一回答三件事：

1. 用户侧 canonical 命令名是什么。
2. workflow / state / task log 应写入什么 canonical command id。
3. 旧 `webnovel-*` 与历史 `story2026-*` 标识如何兼容。

除兼容说明外，其他文档、技能、模板、脚本都不得各自重新发明一套命名表。

## Canonical Rules

- 用户侧命令 canonical 一律使用 `/story-*`。
- workflow / state / task log 中的 canonical `command` 一律写入 `story-*`。
- 技能 frontmatter 中，直接对应用户命令的 skill id 也一律使用 `story-*`。
- 根级总技能保留 `story2026`，因为它表示的是整条系统而不是单个用户命令。
- 旧命令名只允许存在于兼容映射层、迁移说明或历史 case evidence 中。

## Canonical Mapping

| 用户侧命令 | canonical skill / workflow id | legacy aliases |
|---|---|---|
| `/story-init` | `story-init` | `webnovel-init` |
| `/story-cards` | `story-cards` | `story2026-cards` |
| `/story-plan` | `story-plan` | `webnovel-plan` |
| `/story-write` | `story-write` | `webnovel-write` |
| `/story-validate` | `story-validate` | `webnovel-validate`, `story2026-validation` |
| `/story-review` | `story-review` | `webnovel-review` |
| `/story-loopback` | `story-loopback` | `webnovel-loopback`, `story2026-loopback` |
| `/story-query` | `story-query` | `webnovel-query` |
| `/story-resume` | `story-resume` | `webnovel-resume` |

## Auxiliary Command

- `/story-learn`
  - 当前只保留为用户命令层的辅助入口，用于把经验沉淀进项目记忆。
  - 它当前没有 tracked workflow id，也不对应正式 stage skill。
  - 若未来恢复为正式技能或 tracked workflow，必须先在本文件补登记，再同步命令文档、workflow registry 与测试。

## CLI Contract

- 文档、技能示例和人工执行说明默认使用 `.agents/skills/story/scripts/story.py`。
- `.agents/skills/story/scripts/webnovel.py` 只作为 legacy alias 保留。
- `data_modules/webnovel.py` 可继续保留旧文件名，但不得再作为用户侧 canonical 名暴露。

## State Contract

- `STATE.json.workflow_runtime.workflow_state`
  - `current_task.command` 必须写入 canonical `story-*`。
- `STATE.json.workflow_runtime.execution_state`
  - `runs[].command`、`latest_resume_point.command`、`stage_progress[*].latest_command` 必须写入 canonical `story-*`。
- 读取旧状态时，允许在脚本入口自动把 legacy alias 归一化为 canonical 名。

## Compatibility Guardrail

- 可以兼容读取旧名。
- 不允许继续把旧名写回新状态。
- 新文档若再次把 `webnovel-*` 写成用户侧命令，视为命名真源漂移。

## Maintenance Rule

- 若新增阶段命令，必须先更新本文件，再更新命令文档、技能 frontmatter、workflow registry、模板 metadata 与测试。
- 若只改了某一层而没同步本文件，视为 canonical source governance 未完成。
