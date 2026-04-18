# story2026 调用矩阵（兼容旧文件名 `claude-code-call-matrix`）

> 目的：明确“谁调用、什么时候调用、调用什么脚本”，避免把阶段调度、技能入口、agent 内部动作和人工命令混成一层。

说明：

- 文件名保留旧命名，是为了兼容既有引用。
- 内容已按 `story2026` 的最新六阶段系统维护，不再只服务 Claude Code。
- 命令名以 `command-naming-contract.md` 为唯一真源；本文件只负责“谁在何时调用什么”。

## 规则

- 本项目中的脚本默认由 **story2026 Skill / Agent / CLI workflow** 在流程节点触发。
- 除非文档显式说明，否则不把脚本视为“用户手动日常命令”。
- 新增脚本或新增命令触发点时，必须同步更新本文件。

## 命令级矩阵（入口 -> 调用方 -> 触发时机）

| 入口命令 | 调用方 | 触发时机 | 关键脚本/动作 |
|---|---|---|---|
| `/story-init` | `0-Init` Skill | 新建项目、模式选择后的初始化阶段（顾问团 / 快速 / 自主） | `scripts/init_project.py` + 生成 `idea_bank.json` + 初始化 `workflow_state/execution_state/task_log` |
| `1-Cards` | `story-cards` 父技能 | 初始化完成后的整书建卡 / 增量回写 | 路由四张子卡，正式写入 `Cards/**` |
| `/story-plan` | `2-Planning` Skill | 1-7 号 planning passes 收敛并产出 `Planning/8-全息地图.json` 时 | `scripts/update_state.py --volume-planned ...` + 落盘 `全息地图.json` |
| `/story-write` | `3-Drafting` Skill | Step 1 先读 `Planning/8-全息地图.json` 组装上下文，Step 5 再更新数据链 | Task 调 `data-agent`（内部再写 state/index） |
| `4-Validation` | `story-validate` Skill | 章节或历史章节进入隔离上下文质检时 | 新建 checker 团队 + 聚合结构化结果 |
| `/story-review` | `review` Skill | `4-Validation` 聚合结果需要生成正式报告、持久化评分并桥接修复 / `5-Loopback` 闭环时 | `scripts/workflow_manager.py` + `index save-review-metrics` + `update_state --add-review` |
| `5-Loopback` | `story-loopback` Skill | `4-Validation = PASS` 后做 validated actualization 时 | 读取 `templates/loopback.json`，写回 Cards / story_map / projection |
| `/story-query` | `query` Skill | 查询 Cards / MAP / runtime state / validated actualization / 伏笔紧急度 / 质量趋势等运行时信息时 | `scripts/story.py` 统一入口，按需转发 `status` / `index` 并补读 truth layers |
| `/story-resume` | `resume` Skill | 中断恢复检测、清理、断点恢复时 | `scripts/workflow_manager.py detect/cleanup/clear` |

## 脚本级矩阵（脚本 -> 谁触发 -> 什么时候）

| 脚本 | 主要触发方 | 触发节点 | 备注 |
|---|---|---|---|
| `.agents/skills/story/scripts/story.py` | 所有 Skills / Agents | 任何需要调用 CLI 的节点 | **统一入口**：负责解析真实 book project_root，并转发到 `data_modules/*` 或 `scripts/*.py`，避免 `PYTHONPATH/cd/参数顺序` 导致的隐性失败 |
| `.agents/skills/story/scripts/update_state.py` | `2-Planning` Skill | 全息地图落盘后同步更新 `state.json` 的卷规划信息 | 也可被自动化脚本调用；默认不是人工常规入口 |
| `.agents/skills/story/scripts/extract_chapter_context.py` | `3-Drafting` Skill / `context-agent` | 章节级执行包与 validation fact pack 投影生成 | 默认从 `Planning/8-全息地图.json` 收束输入 |
| `.agents/skills/story/scripts/status_reporter.py` | `query` Skill / `pacing-checker` Agent(可选) | 查询分析或节奏审查时 | 产出健康报告与紧急度分析 |
| `.agents/skills/story/scripts/workflow_manager.py` | `resume` Skill / 各 stage 调度点 | 全阶段 run 跟踪、恢复检测、心跳、状态汇总与 task log | 不再只服务 write/review；负责 `workflow_state + execution_state + task_log` |
| `.agents/skills/story/scripts/init_project.py` | `0-Init` Skill | 项目初始化阶段 | 负责项目脚手架、基础状态文件以及状态管理期初文件 |

## 内部库调用（非独立命令）

| 内部模块 | 调用方 | 触发时机 |
|---|---|---|
| `.agents/skills/story/scripts/data_modules/state_validator.py` | `update_state.py`、`status_reporter.py` | 读写 `state.json` 时自动规范化与校验 |

## 阶段级职责提醒

- `4-Validation` 是调度层，不是 checker 本体。
- `review/` 是聚合落盘层，不是隔离评估入口。
- `5-Loopback` 是 `PASS` 后的 validated actualization 层，不是泛化收尾说明页。

## 变更约束（后续开发必须遵守）

1. 若新增“可由 Skill/Agent 触发”的脚本，必须补充到本矩阵。
2. 若脚本触发时机变化，必须同步更新本矩阵。
3. PR/提交说明中需写清“调用方 + 触发节点 + 是否允许人工调用”。
