# Video Learning Contract

本文件定义 `$aigc-learn` 面对视频、课程视频、拉片素材、访谈录像、屏幕录制和视频链接时的复杂对象学习细则。它扩展 `source-ingestion-contract.md`，只拥有视频证据分解、跨轨融合和可迁移知识抽取规则，不直接决定技能写回 owner。

## Scope

适用对象：

- 本地视频文件、在线视频、课程片段、访谈、电影/剧集参考片段、屏幕录制、带字幕或无字幕视频。
- 用户要求“学习这个视频”“学习这个课程”“拉片吸收方法”“分析镜头/节奏/表演/剪辑/声音方法”的任务。

不适用对象：

- 只有音频无画面时，优先使用 `types/audio-source/audio-source.md`，本文件只补充可见元数据。
- 只有字幕或转写文本时，优先使用 `types/text-source/text-source.md`，并在缺口中标记 `visual_track: missing`、`audio_track: missing`。

## Evidence Stack

视频学习必须按四层建立证据栈：

| layer | required anchors | learning value |
| --- | --- | --- |
| `visual_track` | 时间码、镜头/画面事件、构图、动作、屏幕文字、场面调度 | 镜头语言、空间组织、视觉叙事、设计线索 |
| `subtitle_track` | 字幕行、旁白字幕、屏幕文字转录、缺失说明 | 语义结构、教学步骤、叙事信息、术语 |
| `audio_track` | 语音转写、说话人、音乐、环境声、节奏、静默、缺失说明 | 情绪、节拍、表演、声音叙事、教学语气 |
| `sequence_track` | 段落边界、动作连续、剪辑点、示范顺序 | 结构、节奏、因果链、步骤依赖 |

缺少任一层时不得补写想象内容；必须在 `media_evidence_status` 中标记 `missing`、`unavailable` 或 `user_not_provided`。

## Workflow

1. 先建立 `source_digest`：视频来源、时长、作者/发布方、访问时间、许可边界、可用轨道和缺口。
2. 按段落切分视频：优先使用章节、字幕时间码、场景切换、主题转折或用户指定片段。
3. 对每个高价值片段建立 `evidence_unit`：`time_range + visual_note + subtitle_or_transcript + audio_note + sequence_role`。
4. 抽取 `learning_units`：只抽象可迁移的方法、判断标准、流程节点、审查项、失败模式和适用边界。
5. 建立 `fusion_note`：说明结论来自画面、字幕、音频、顺序，还是多轨互证。
6. 若视频内容与仓库合同、事实判断或高风险建议冲突，转入 `conflict-verification-contract.md`。
7. 进入 `global-improvement-contract.md`，把学习结论映射到最窄 owning skill。

## Segmentation Policy

- 短视频或单段参考：可以整体作为一个学习对象，但仍需列出时间码锚点。
- 长视频或课程：必须先做目录级 / 章节级 digest，再选择与学习目标相关的片段深入。
- 影视拉片：不得把参考片的完整镜头序列、台词、角色造型或具体剧情复制为模板；只能沉淀为镜头功能、节奏策略、调度原则和审查门槛。
- 教程类视频：优先抽取流程、决策条件、常见错误和验证方法；不要复制课程讲稿长段表达。

## Output Additions

视频学习对象的学习证据必须补充：

| field | requirement |
| --- | --- |
| `video_segmentation` | 章节、场景、主题段或时间码范围 |
| `media_evidence_status` | `visual_track`、`subtitle_track`、`audio_track`、`sequence_track` 四栏状态 |
| `evidence_units` | 可回指的时间码证据单元 |
| `fusion_notes` | 每条关键结论的跨轨依据 |
| `missing_tracks` | 缺失轨道、原因和残余风险 |

> **注意**：以上是执行型改进的学习证据，不是报告。完成任务的标准是：`audit_result: pass` + `changed_files` 已验证。

## Review Gate

不得通过视频学习审计，若出现以下情况：

- 没有时间码或片段锚点。
- 视频学习结论未说明来自画面、字幕、音频或顺序中的哪一层。
- 影视/课程内容被复制成长段正文或被当作 canonical 创作模板。
- 缺失轨道被隐性补全，没有进入 residual risks。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 视频学习是否先建立来源、时长、作者/发布方、访问时间、许可边界、可用轨道和缺口？ | `GATE-LEARN-SOURCE-01` | `FAIL-AIGC-LEARN-SOURCE` | `N2-MEDIA` / `Workflow` | `source_digest`、duration、source owner、license boundary、track availability |
| 是否按章节、字幕时间码、场景切换、主题转折或用户片段完成 `video_segmentation`？ | `GATE-LEARN-VIDEO-02` | `FAIL-AIGC-LEARN-VIDEO` | `N2-MEDIA` / `Segmentation Policy` | `video_segmentation`、time ranges、segment rationale |
| 每个高价值片段是否有 `time_range + visual_note + subtitle_or_transcript + audio_note + sequence_role`？ | `GATE-LEARN-VIDEO-02` | `FAIL-AIGC-LEARN-VIDEO` | `N2-MEDIA` / `Evidence Stack` | `evidence_units` with timecode and four-track notes |
| `media_evidence_status` 是否逐项声明 visual/subtitle/audio/sequence 四轨状态？ | `GATE-LEARN-VIDEO-01` | `FAIL-AIGC-LEARN-VIDEO` | `N2-MEDIA` / `Evidence Stack` | four-track status table with available/missing/unavailable/user_not_provided |
| 缺失轨道是否进入 `missing_tracks` 和 residual risks，而不是被隐性补全？ | `GATE-LEARN-VIDEO-03` | `FAIL-AIGC-LEARN-VIDEO` | `N3-DISTILL` / `Output Additions` | `missing_tracks`、缺失原因、对学习结论的影响 |
| 每条关键视频学习结论是否说明来自画面、字幕、音频、顺序或多轨互证？ | `GATE-LEARN-VIDEO-03` | `FAIL-AIGC-LEARN-VIDEO` | `N3-DISTILL` / `Workflow` | `fusion_notes` mapped to each learning unit |
| 影视拉片是否只沉淀镜头功能、节奏策略、调度原则和审查门槛，没有复制完整镜头序列、台词、造型或剧情？ | `GATE-LEARN-SOURCE-03` | `FAIL-AIGC-LEARN-SOURCE` | `N3-DISTILL` / `Segmentation Policy` | abstraction note、copyright check、no canonical template copying |
| 教程类视频是否抽取流程、决策条件、常见错误和验证方法，而非复制课程讲稿长段表达？ | `GATE-LEARN-SOURCE-03` | `FAIL-AIGC-LEARN-SOURCE` | `N3-DISTILL` / `Segmentation Policy` | learning_units、quote-length check、summary-only evidence |
| 视频内容与仓库合同、事实判断或高风险建议冲突时，是否转入 conflict verification？ | `GATE-LEARN-VERIFY-01` | `FAIL-AIGC-LEARN-VERIFY` | `N4-VERIFY` / `Workflow` | conflict note、verification trigger、adopt/adapt/reject/hold decision |
