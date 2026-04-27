# Runtime And Handoff Contract

本文件拥有 `story-init` 的项目运行时骨架、状态同步和初始化交接工件边界。

## Canonical Runtime Root

所有初始化输出只写入：

```text
projects/story/<项目名>/
```

不得写入 `projects/aigc/`、旧 `.webnovel/tasks/`、旧 `Init/*` 平行真源或项目内 `.git/`。

## Required Project Skeleton

初始化或重初始化后，至少存在：

```text
projects/story/<项目名>/
├── 源/
├── CONTEXT/
├── 0-初始化/
├── 1-设定/
├── 2-卷章规划/
├── 3-初稿/
├── 4-润色/
├── review/
├── context-return/
├── CHANGELOG.md
├── MEMORY.md
├── STATE.json
└── team.yaml
```

初始化只预建阶段根目录，不在 `1-设定/` 下预建卡片子目录；卡片子目录由 `1-设定` 阶段按实际调度创建。

## Canonical Landing

| artifact | owner | purpose |
| --- | --- | --- |
| `team.yaml` | team governance | 角色阵容、init contract、subagent runtime policy |
| `STATE.json` | workflow runtime | stage progress、paths、task log、latest command |
| `MEMORY.md` | project memory | 跨阶段持续生效的偏好、口味、禁区、长期要求 |
| `CONTEXT/` | project context root | 项目共享附加上下文与非偏好参考 |
| `CHANGELOG.md` | project change history | 初始化与重初始化事件摘要 |
| `0-初始化/north_star.yaml` | long-term contract | 读者承诺、题材走廊、长期创作约束 |
| `0-初始化/story-source-manifest.yaml` | source registry | 故事主源根、来源层级、可追溯材料 |
| `0-初始化/init_handoff.yaml` | stage handoff | `1-设定 / 2-卷章规划` seed、unknowns、下一入口 |

## STATE.json Synchronization

`STATE.json.paths` 至少包含：

- `source_root`
- `context_root`
- `project_memory`
- `init_root`
- `setting_root`
- `planning_root`
- `drafting_root`
- `polish_root`
- `review_root`
- `context_return_root`

`STATE.json.workflow_runtime.execution_state.stage_progress["0-init"]` 必须：

- 标记为 `completed`
- `latest_command` 为 `story-init`
- 首次初始化记录 `project_initialized`
- 重初始化追加 `project_reinitialized`
- 重初始化刷新 `last_completed_at`

## Handoff Boundary

- 初始化只产出 `0-初始化` 三件套和 runtime 骨架。
- 初始化不得生成 `2-卷章规划/整体规划.md`、`2-卷章规划/全息地图.json` 或正文主稿。
- 长期偏好写入项目 `MEMORY.md`；运行期共享事实写入项目 `CONTEXT/`；技能经验写回技能 `CONTEXT.md` 或 `knowledge-base/`。
- 更适合 cards/planning 收敛的问题写入 `init_handoff.yaml.unknowns`，不得在初始化阶段强行补完。
