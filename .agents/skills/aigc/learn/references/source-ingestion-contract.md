# Source Ingestion Contract

本文件定义 `aigc-learn` 如何接收和归一不同媒介的学习对象。它只负责证据摄取和可信度标注，不直接决定技能改写。

## Source Digest

每个学习对象必须先归一为 `source_digest`：

| field | requirement |
| --- | --- |
| `source_kind` | text / web / document / book / video / audio / image_sequence / skill_package |
| `source_locator` | URL、绝对路径、项目路径、用户粘贴内容或材料描述 |
| `source_owner` | 作者、发布方、文件来源或 unknown |
| `captured_at` | 本轮读取或用户提供日期 |
| `evidence_units` | 摘要、段落锚点、页码、时间码、截图号、字幕行或转写片段 |
| `license_boundary` | 可引用、只可摘要、不可复制、unknown |
| `credibility` | high / medium / low / unknown，并说明原因 |
| `gaps` | 不可访问、缺页、缺字幕、缺音频、画面不可见等 |

## Media Handling

| source_kind | required handling |
| --- | --- |
| text | 保留用户原意，抽取核心主张、方法步骤、适用条件和限制 |
| web | 读取页面内容；若信息可能变化或涉及事实冲突，必须联网查可靠来源 |
| document / book | 按章节、页码或标题建立摘录锚点；书籍、超长 PDF 和长文档必须进一步加载 `book-long-context-learning-contract.md`；禁止整段复制受版权保护内容 |
| video | 同时解析画面、字幕、音频和顺序轨；复杂视频、课程视频和拉片素材必须进一步加载 `video-learning-contract.md`；至少记录时间码、可见事件、字幕/转写、声音线索和缺口 |
| audio | 转写为文字，标注说话人、时间码、语气、环境声和不可听清片段 |
| image_sequence | 按帧序号或截图号记录画面元素、构图、动作和连续性 |
| skill_package | 读取 `SKILL.md + CONTEXT.md`，再按 Reference Loading Guide 读取必要分区 |

## Complex Object Delegation

- 视频、课程视频、访谈录像、屏幕录制和影视拉片素材的细则真源为 `references/video-learning-contract.md`。
- 书籍、超长 PDF、长文档、课程讲义合集和长网页合集的细则真源为 `references/book-long-context-learning-contract.md`。
- 本文件只负责统一 source digest 和媒介缺口标注；复杂对象的分段、覆盖、跨轨融合和深读策略不得塞回本文件。

## Video Minimum Gate

视频学习对象必须输出：

- `visual_track`: 可见画面、镜头、动作、构图、屏幕文字和时间码。
- `subtitle_track`: 内嵌字幕、旁白字幕、外置字幕或缺失说明。
- `audio_track`: 语音转写、环境声、音乐、节奏、静默和缺失说明。
- `sequence_track`: 段落边界、动作连续、剪辑点、示范顺序或缺失说明。
- `fusion_note`: 四类证据如何共同支持学习结论。

如果工具环境无法解析其中任一 track，不得伪造；必须在 `media_evidence_status` 中标记 `missing` 或 `unavailable`。

## Copyright Boundary

- 可以吸收原则、结构、方法、检查项和可迁移模式。
- 不得复制书籍、课程、文章或影视作品的长段受保护表达。
- 不得把参考视频的具体镜头序列、台词、角色造型、构图和剧情事件作为 AIGC canonical 模板。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每个学习对象是否先被归一为完整 `source_digest`，而不是直接进入总结或写回？ | `GATE-LEARN-SOURCE-01` | `FAIL-AIGC-LEARN-SOURCE` | `N2-MEDIA` / `Source Digest` | `source_kind`、`source_locator`、`source_owner`、`captured_at`、`evidence_units`、`license_boundary`、`credibility`、`gaps` |
| `evidence_units` 是否能回指到段落、页码、时间码、截图号、字幕行或转写片段？ | `GATE-LEARN-SOURCE-01` | `FAIL-AIGC-LEARN-SOURCE` | `N2-MEDIA` / `Source Digest` | 每条关键 learning claim 对应的 evidence unit id 与 locator |
| 视频、课程视频、访谈录像、屏幕录制或拉片素材是否交给 `video-learning-contract.md` 处理？ | `GATE-LEARN-SOURCE-02` | `FAIL-AIGC-LEARN-SOURCE` | `N2-MEDIA` / `Complex Object Delegation` | `source_kind: video`、delegated reference、四轨证据计划或缺口说明 |
| 书籍、超长 PDF、长文档、课程讲义合集或长网页合集是否交给 `book-long-context-learning-contract.md` 处理？ | `GATE-LEARN-SOURCE-02` | `FAIL-AIGC-LEARN-SOURCE` | `N2-MEDIA` / `Complex Object Delegation` | `source_kind: book/document/web_collection`、delegated reference、coverage plan 摘要 |
| 视频对象是否至少声明 `visual_track`、`subtitle_track`、`audio_track`、`sequence_track` 和 `fusion_note` 的状态？ | `GATE-LEARN-VIDEO-01` | `FAIL-AIGC-LEARN-VIDEO` | `N2-MEDIA` / `Video Minimum Gate` | `media_evidence_status` 四栏、`fusion_note`、缺失轨道标记 |
| 工具环境无法解析某个媒介轨道时，是否显式标记 `missing` / `unavailable`，而不是补写想象内容？ | `GATE-LEARN-VIDEO-03` | `FAIL-AIGC-LEARN-VIDEO` | `N3-DISTILL` / `Video Minimum Gate` | `missing_tracks`、不可用原因、residual risks |
| 版权材料是否只吸收原则、结构、方法和检查项，没有复制长段表达或具体镜头/台词/造型作为模板？ | `GATE-LEARN-SOURCE-03` | `FAIL-AIGC-LEARN-SOURCE` | `N2-MEDIA` / `Copyright Boundary` | `license_boundary`、summary-only note、copyright risk check |
