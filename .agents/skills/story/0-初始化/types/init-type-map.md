# Init Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


本文件拥有 `story-init` 的类型变量、分支选择和类型到步骤/审查的映射。

## Type Profile

| variable | allowed values | meaning |
| --- | --- | --- |
| `medium_type` | `story`, `aigc_film`, `ambiguous` | 媒介路由 |
| `init_run_type` | `first_init`, `reinit`, `resume_needed` | 初始化运行类型 |
| `team_lineup_mode` | `auto`, `custom`, `unknown` | 编组子路径 |
| `evidence_type` | `brief_only`, `legacy_init`, `existing_runtime`, `mixed` | 可用证据 |
| `execution_type` | `subagent_required`, `script_assisted`, `blocked` | 执行形态 |
| `handoff_type` | `clean_start`, `partial_runtime`, `legacy_migration` | 写回形态 |

## Routing Matrix

| signal | type_profile | step impact | reference impact | review impact |
| --- | --- | --- | --- | --- |
| 用户说小说/网文/书/novel/book | `medium_type=story` | 进入 `N1-MODE` | 读取本技能 | 媒介 gate pass |
| 用户说影片/电影/视频/film/movie | `medium_type=aigc_film` | 转 `aigc-init` | 读取 AIGC 初始化入口 | story-init blocked |
| 已有项目根且只查状态 | `init_run_type=resume_needed` | 转 `story-resume` | 不进入写回流程 | blocked with route |
| 未给 roster | `team_lineup_mode=auto` | `N3` 走 auto | 读取 team 根索引 | 检查 auto notes |
| 给出 roster | `team_lineup_mode=custom` | `N3` 走 custom | 校验 `.agents/skills/team/` | 检查 custom notes |
| 发现 legacy `Init/*` | `evidence_type=legacy_init` | 只作为 evidence | 写入 source manifest provenance | 禁止覆盖当前真源 |
| 上层策略阻断真实 subagents | `execution_type=blocked` | `N5` 阻塞或显式降级报告 | mode/team contract | verdict 不得伪装 pass |

## Defaults

- `medium_type` 默认不得猜成 story；必须由用户请求或项目路径支撑。
- `team_lineup_mode` 缺省时可以进入 `auto`，但必须记录 `mode_source=defaulted_by_skill` 或等价来源。
- `init_run_type=reinit` 时，写回可覆盖初始化管理工件，但不得无授权删除不可再生故事主源。

## Anti-Patterns

- 把 `auto/custom` 扩展成第三个问卷模式。
- 因 legacy 工件存在而恢复旧 `Init/*` 真源。
- 把 `execution_type=blocked` 当成已经完成 planning 直答。
