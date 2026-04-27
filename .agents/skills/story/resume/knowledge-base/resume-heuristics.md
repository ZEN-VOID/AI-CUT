# Resume Heuristics

本文件保存 `$story-resume` 可复用经验。它不是入口合同；稳定到必须执行的规则应晋升到 `SKILL.md`、`references/`、`steps/`、`types/` 或 `review/`。

## Heuristics

- 恢复的核心不是“上次聊天说到哪”，而是磁盘和 runtime 能证明的最后稳定入口。
- `workflow detect` 是诊断原料，不是用户-facing SOP；恢复选项必须二次归一化。
- 没有 tracked interruption 不等于无事可做；validation、review、context-return 和 writing log 可能已经给出唯一下一入口。
- `story-query` 可以有 tracked run，但不应被抬成章节级恢复对象。
- cleanup 方案必须把“预览”和“确认执行”拆开；预览结果本身不是用户确认。
- `resume/` 不写 canonical truth。它最多执行 workflow runtime 清理，或把任务回接给目标 stage。
- stage 目录改名后，resume 的危险点通常在旧路径泄漏；每次改目录口径都要同时检查 `workflow-resume.md`、`system-data-flow.md`、`types/resume-type-map.md` 和输出模板。

## Reuse Scope

- 适用于 `.agents/skills/story/resume` 内的恢复裁决、文档维护和安全审查。
- 不直接适用于 AIGC 影片项目；AIGC 恢复由 `.agents/skills/aigc/resume` 管理。
