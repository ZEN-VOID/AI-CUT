# Type Map

每次调用 `$aigc-learn` 时，先根据学习对象选择一个或多个类型包，并加载其 `context_files` 作为固定上下文。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `text-source` | `types/text-source/` | 用户粘贴文字、笔记、文章摘录、提示词片段 | stackable | `types/text-source/text-source.md` | none | none |
| `web-source` | `types/web-source/` | URL、网页、在线文档、最新信息 | stackable | `types/web-source/web-source.md` | none | none |
| `document-source` | `types/document-source/` | PDF、docx、书籍、长文档、本地资料 | stackable | `types/document-source/document-source.md` | none | none |
| `video-source` | `types/video-source/` | 视频链接、本地 mp4/mov、拉片素材、课程视频 | stackable | `types/video-source/video-source.md` | none | none |
| `audio-source` | `types/audio-source/` | 音频文件、播客、访谈录音、视频音轨 | stackable | `types/audio-source/audio-source.md` | none | none |
| `skill-package-source` | `types/skill-package-source/` | 目标是现有 skill、外部技能包、AGENTS/SKILL/CONTEXT 文档 | stackable | `types/skill-package-source/skill-package-source.md` | none | none |

## Default Package Rule

默认按学习对象选择一个或多个类型包；若无法判定格式，先加载 `text-source`，并在 source digest 中记录 `source_kind: unknown`。

## Loading Flow

1. 识别学习对象的媒介、目标 skill 和写回权限。
2. 从 `Package Index` 选择可叠加类型包。
3. 加载所有选中类型包的 `context_files`。
4. 将类型画像交给 `SKILL.md#Thinking-Action Node Map`，再按需要加载视频、书籍、冲突核查或全局改进 references。

## Selection Rule

- 多媒介材料必须多选叠加，例如视频链接同时加载 `web-source`、`video-source` 和 `audio-source`。
- 命中复杂视频、课程视频、访谈录像、屏幕录制或影视拉片素材时，除类型包外必须加载 `references/video-learning-contract.md`。
- 命中书籍、超长 PDF、长文档、课程讲义合集或长网页合集时，除类型包外必须加载 `references/book-long-context-learning-contract.md`。
- 用户指定某个技能包为学习对象或改进对象时，加载 `skill-package-source`。
- 未知格式先按 `text-source` 处理，并在 source digest 中记录 `source_kind: unknown`。
