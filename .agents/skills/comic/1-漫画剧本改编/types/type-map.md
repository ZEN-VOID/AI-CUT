# 漫画剧本改编类型包索引

本文件是执行时固定上下文类型包的选择索引。每次调用 `comic-script-adaptation` 时，先加载本文件，再按命中信号加载一个或多个类型包。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `source-text` | `types/source-types/text.md` | 小说、故事梗概、帖文、长文本、半成品剧本、虚构剧情 | stackable | `types/source-types/text.md` | none | none |
| `source-visual` | `types/source-types/visual.md` | 图片、海报、角色图、视频、镜头序列、直播切片 | stackable | `types/source-types/visual.md` | none | none |
| `source-news-hotsearch` | `types/source-types/news-hotsearch.md` | 新闻事件、热搜、社会议题、纪实事件、真实人物事件 | stackable | `types/source-types/news-hotsearch.md` | none | none |
| `source-mixed` | `types/source-types/mixed.md` | 多图多文、多来源补充材料、用户同时给素材和评论 | stackable | `types/source-types/mixed.md` | none | none |
| `projection-directing-field-bridge` | `types/projection/directing-field-bridge.md` | 对白密集、旁白/音效/系统提示/规则文字密集、用户要求声画字段清楚、需要兼容 2-编导理解 | stackable | `types/projection/directing-field-bridge.md` | none | none |
| `posture-faithful-core` | `types/adaptation-postures/faithful-core.md` | 用户要求保真、现实议题、关键事实不可改、低虚构许可 | exclusive | `types/adaptation-postures/faithful-core.md` | `posture-comic-first, posture-spectacle-first` | none |
| `posture-comic-first` | `types/adaptation-postures/comic-first.md` | 虚构来源、故事梗概、网文、用户要求更精彩、更漫画、更抓人 | exclusive | `types/adaptation-postures/comic-first.md` | `posture-faithful-core, posture-spectacle-first` | none |
| `posture-spectacle-first` | `types/adaptation-postures/spectacle-first.md` | 高概念、奇观驱动、恐怖/战斗/玄幻/灾变、用户要求强冲击 | exclusive | `types/adaptation-postures/spectacle-first.md` | `posture-faithful-core, posture-comic-first` | none |
| `output-reply-only` | `types/output-modes/reply-only.md` | 用户只要当前回复、不允许写文件、快速预览 | exclusive | `types/output-modes/reply-only.md` | `output-grouped-files` | none |
| `output-grouped-files` | `types/output-modes/grouped-files.md` | 用户给项目名、目标目录、要求落盘、进入完整 comic pipeline | exclusive | `types/output-modes/grouped-files.md` | `output-reply-only` | none |

## Default Package Rule

- 未声明 `source_type` 时，先根据素材天然形态选择 `source-*` 包；多源素材叠加 `source-mixed`。
- 虚构故事默认 `posture-comic-first`。
- 现实新闻、热搜和纪实事件默认 `posture-faithful-core`，除非用户明确要求虚构衍生并设定 `truth_boundary=inspired_by | free_reimagining`。
- 视觉驱动素材可以叠加 `posture-spectacle-first`，但现实来源仍受事实边界约束。
- 来源或目标稿含大量对白、旁白、音效、系统提示、规则文字、内心独白或用户要求“声画清楚 / 编导兼容 / 字段对齐”时，叠加 `projection-directing-field-bridge`。
- 用户给出项目名或可写目标目录时默认 `output-grouped-files`；否则默认 `output-reply-only`。

## Loading Flow

1. 读取本索引。
2. 至少选择一个 `source-*` 包。
3. 选择一个互斥 `posture-*` 包。
4. 选择一个互斥 `output-*` 包。
5. 视素材复杂度叠加 `projection-*` 包。
6. 若 comic 根层已经给出 `type_stack_ref / type_pack_context`，作为额外固定上下文输入，不替代本技能本地类型包。
