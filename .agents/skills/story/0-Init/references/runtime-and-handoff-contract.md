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
├── Story/
├── CONTEXT/
├── 0-Init/
├── 1-Cards/
├── 2-Planning/
├── 3-Drafting/
├── 4-Review/
├── 5-Loopback/
├── CHANGELOG.md
├── MEMORY.md
├── STATE.json
└── team.yaml
```

当前 `1-Cards` 最小骨架必须包含：

- `1-Cards/0-全局卡/总设定`
- `1-Cards/1-风格卡/总风格`
- `1-Cards/2-角色卡/`
- `1-Cards/3-场景卡/`
- `1-Cards/4-物品卡/`
- `1-Cards/5-类型卡/总题材`

## Canonical Landing

| artifact | owner | purpose |
| --- | --- | --- |
| `team.yaml` | team governance | 角色阵容、init contract、subagent runtime policy |
| `STATE.json` | workflow runtime | stage progress、paths、task log、latest command |
| `MEMORY.md` | project memory | 跨阶段持续生效的偏好、口味、禁区、长期要求 |
| `CONTEXT/` | project context root | 项目共享附加上下文与非偏好参考 |
| `CHANGELOG.md` | project change history | 初始化与重初始化事件摘要 |
| `0-Init/north_star.yaml` | long-term contract | 读者承诺、题材走廊、长期创作约束 |
| `0-Init/story-source-manifest.yaml` | source registry | 故事主源根、来源层级、可追溯材料 |
| `0-Init/init_handoff.yaml` | stage handoff | `1-Cards / 2-Planning` seed、unknowns、下一入口 |

## STATE.json Synchronization

`STATE.json.paths` 至少包含：

- `story_root`
- `context_root`
- `project_memory`
- `init_root`
- `cards_root`
- `planning_root`
- `drafting_root`
- `validation_root`
- `loopback_root`

`STATE.json.workflow_runtime.execution_state.stage_progress["0-init"]` 必须：

- 标记为 `completed`
- `latest_command` 为 `story-init`
- 首次初始化记录 `project_initialized`
- 重初始化追加 `project_reinitialized`
- 重初始化刷新 `last_completed_at`

## Handoff Boundary

- 初始化只产出 `0-Init` 三件套和 runtime 骨架。
- 初始化不得生成 `2-Planning/整体规划.md`、`2-Planning/全息地图.json` 或正文主稿。
- 长期偏好写入项目 `MEMORY.md`；运行期共享事实写入项目 `CONTEXT/`；技能经验写回技能 `CONTEXT.md` 或 `knowledge-base/`。
- 更适合 cards/planning 收敛的问题写入 `init_handoff.yaml.unknowns`，不得在初始化阶段强行补完。
