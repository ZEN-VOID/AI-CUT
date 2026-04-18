# story2026 Root References

## Purpose

根级 `references/` 只承载跨阶段共享的参考合同，不再堆放单一阶段私有技巧。

保留原则：

- 会被两个及以上阶段共享消费。
- 会被脚本、checker、context builder 或模板同步依赖。
- 属于“系统合同 / schema / 统一分类法”，而不是局部写法技巧。

下沉原则：

- 只服务单一阶段的文档，应留在该阶段自己的 `references/`。
- 只服务某个 checker、某个写作专项或某个恢复动作的文档，不应提升到根级。

## Current Coverage

| 文件 | 当前定位 | 覆盖阶段 |
|---|---|---|
| `checker-output-schema.md` | 统一 checker 输出、validation 聚合、review sink 字段合同 | `4-Validation` / `review` / `3-Drafting` |
| `command-naming-contract.md` | 用户命令、skill id、workflow command 与兼容 alias 的单一真源 | `0-Init` ~ `5-Loopback` + satellites + scripts |
| `claude-code-call-matrix.md` | 统一命令归属与脚本触发矩阵；文件名保留兼容性 | `0-Init` ~ `5-Loopback` + satellites |
| `context-contract-v2.md` | 章节级上下文合同与 `validation_fact_pack` 投影约定 | `3-Drafting` / `4-Validation` / `review` |
| `entity-management-spec.md` | `Cards / story_map / index.db` 三层实体真源分工 | `1-Cards` / `3-Drafting` / `5-Loopback` |
| `genre-profiles.md` | 题材 profile 参考 | `3-Drafting` / context builder |
| `reading-power-taxonomy.md` | 追读力 taxonomy | `3-Drafting` / checkers / context builder |
| `preferences-schema.md` | `.webnovel/preferences.json` 可选偏好覆盖层 schema | runtime context |
| `project-memory-schema.md` | `.webnovel/project_memory.json` 成功经验沉淀 schema | runtime context / 手工经验沉淀 |
| `validation-team-contract.md` | validation checker 白名单、职责边界与调度规则 | `4-Validation` / `review` / `3-Drafting` |
| `validation-fact-pack-spec.md` | validation 五类强制 slice 合同 | `3-Drafting` / `4-Validation` / checkers |
| `loopback-actualization-spec.md` | validated actualization 与 truth writeback 合同 | `5-Loopback` / `2-Planning` / `1-Cards` |
| `shared/core-constraints.md` | 写作硬约束单一事实源 | `3-Drafting` / `review` |
| `shared/cool-points-guide.md` | 爽点工程共享参考 | planning / drafting / review |
| `shared/strand-weave-pattern.md` | Strand 节奏共享参考 | query / planning / drafting / review |

## Compatibility Notes

- `claude-code-call-matrix.md` 仍保留旧文件名，是为了兼容既有引用；其内容已按跨工具工作流维护，不再只服务 Claude Code。
- `command-naming-contract.md` 是命令命名的唯一真源；若 call matrix、技能 frontmatter、workflow registry 与它冲突，以本文件为准。
- `context-contract-v2.md` 继续保留 `v2` 标识，是因为脚本与测试都以此版本号作为兼容锚点。
- 若需要新增根级参考，优先先问一句：它是否真的跨阶段共享；如果答案是否定的，应回到对应阶段目录。
