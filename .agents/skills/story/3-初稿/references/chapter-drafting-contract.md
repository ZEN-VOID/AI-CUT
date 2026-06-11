# Chapter Drafting Contract

本文件展开 `story-drafting` 的章节正文细则。入口、路由、gate 和输出真源仍归根 `SKILL.md`。

## Stage Position

- 当前技能是 `story2026` 主链 `3-初稿` 阶段的根执行包。
- 当前章正文业务真源固定为 `projects/story/<项目名>/3-初稿/第N卷/第N章.md`。
- `3-初稿` 根目录是唯一阶段技能入口，不形成 A/B/C 子技能、返工归属或 frontmatter 真源。

## Total Input Contract

### Required

- `projects/story/<项目名>/0-初始化/north_star.yaml`
- `projects/story/<项目名>/2-卷章/整体规划.md`
- `projects/story/<项目名>/2-卷章/第N卷/卷规划.md`
- `projects/story/<项目名>/2-卷章/第N卷/第N章.md`
- 角色、场景、物品、技能卡；存在关系图谱时必须加载
- `volume_num / chapter_num`
- 当前项目根与目标输出路径

### Conditional

- `MEMORY.md` 与项目 `CONTEXT/`
- 当前卷内早于目标章的所有已存在初稿
- 目标章既有正文
- `team.yaml` 与 `supervision_packet` 或降级报告
- 内置验收 finding / 用户局部问题描述

## Hard Rules

1. 最小业务单元是“章”，不是“集”或“卷批次”。
2. 必须先锁定当前章 planning，再读取全局/风格/题材真源；不得凭风格反推当前章义务。
3. 新产物 frontmatter 只保留 `创作阶段: 初稿` 与 `字数: XXX字`。
4. 旧稿已有 `写作模型` 时只作 legacy metadata；不得据此路由到旧子目录。
5. 上下文引用、摘要、监制包、执行环境和 sidecar 路径不得写入正文 YAML。
6. 正文必须是小说 prose，不得复制 planning 标题、任务线、规避条目或执行说明。
7. 每章至少一个“现场发现”，并由场景自身的物件、声音、气味、动作、空间阻隔、误触、沉默或环境反作用推动剧情。
8. 正文不得出现章节流程标签或执行证据层标签。
9. 角色对白必须能体现身份、关系、利益、情绪和当前意图差异。
10. `不是……是……` 及其变体只允许偶尔用于关键反转，不得成为默认解释句式。
11. 不得用脸色颜色变化作为情绪表达捷径。
12. 输出路径固定为 canonical path，不得写到旧分支子目录或临时 sibling 文件。
13. 目标章已存在时，必须明确 `chapter_continue / chapter_rewrite / local_repair` 和覆盖授权。
14. 脚本、模板、正则和映射表不得生成正文；正文必须来自 LLM-first 主创。

## Frontmatter Contract

```yaml
创作阶段: 初稿
字数: XXX字
```

`字数` 记录正文估算结果，不作为固定长度区间硬门槛。

## Continuity Bridge Contract

- 同卷前文存在时，必须加载当前卷所有早于目标章的正文。
- 连续性桥至少覆盖：既成事实、人物所在位置、线索状态、关系推进、道具流向、卷目标完成度、任务连续性、悬疑节奏、情绪余波、未完成动作和章末压力。
- 本章 planning 负责“要推进到哪里”，同卷前文负责“从哪里入场”和“哪些事实已经成立”。
- planning 与前文冲突时，先保留前文已成立事实，再让本章完成推进；若冲突无法调和，阻断并路由 `repair`。

## Built-in Acceptance Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否先锁定当前章 planning、north_star、对象真源、项目记忆和监制包？ | `source_context` | `FAIL-DRAFT-CONTEXT` | `N2-SOURCE-LOCK` / `N4-SUPERVISION` | loaded source manifest |
| 本章 planning 义务是否被写成戏剧事件而非摘要式提到？ | `structure_realization` | `FAIL-DRAFT-STRUCTURE` | `N5-CREATIVE-DRAFT` | obligation evidence |
| 同卷前文是否完整加载并形成连续性桥？ | `continuity` | `FAIL-DRAFT-CONTINUITY` | `N3-CONTINUITY` | previous chapter refs |
| 因果、人物、时间线和章级/卷级任务汇聚是否成立？ | `logic_character_timeline_task` | `FAIL-DRAFT-LOGIC` / `FAIL-DRAFT-CHARACTER` / `FAIL-DRAFT-TIMELINE` / `FAIL-DRAFT-TASK` | `N2-SOURCE-LOCK` / `N5-CREATIVE-DRAFT` | issue map |
| 正文是否完成 prose 转换，有现场感、读者牵引和章末钩子，没有 planning 标题或执行标签？ | `prose_reader_pull` | `FAIL-DRAFT-PROSE-PULL` | `N5-CREATIVE-DRAFT` | offending excerpt |
| 是否遵守 LLM-first 作者性，脚本没有生成正文？ | `creative_authorship` | `FAIL-DRAFT-AUTHORSHIP` | `N5-CREATIVE-DRAFT` | script audit |
| 输出是否只写入 canonical path，并同步生成 `第N章.acceptance.json`？ | `output_state` | `FAIL-DRAFT-WRITEBACK` | `N7-WRITEBACK-STATE` | expected vs actual path |

## Acceptance Output

每次正式写回正文时必须同步写入：

```text
projects/story/<项目名>/3-初稿/第N卷/第N章.acceptance.json
```

初稿验收通过只授权 `4-润色`，不得直接授权 `return`。
