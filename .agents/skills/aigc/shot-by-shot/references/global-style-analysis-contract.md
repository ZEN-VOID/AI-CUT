# Global Style Analysis Contract

`全局风格解析.md` 是 `shot-by-shot` 输出给项目风格底座的 legacy 解析细则。它参照旧 `global-style-director` 的字段逻辑，但在本技能中只作为 side context，不直接生成或改写 `style_contract.json`、`2-美学` canonical 输出、`MEMORY.md` 或其他初始化 canonical 文件。

## Scope

- 目标：从参考素材中提炼全片可继承的叙事承诺、世界构建语法、视觉母题、年代质感、媒介属性、渲染管线、美学范式、叙事节奏锚点和无污染风格提示词候选。
- 落点：`projects/aigc/<项目名>/shot-by-shot/<reference_slug>/全局风格解析.md`。
- 非目标：不得复制参考片具体角色、场景、道具、构图、镜头顺序、颜色组合、材质组合或受版权保护的画面表达。
- 下游：供旧项目初始化回读、`2-美学`、`7-摄影`、`8-分组`、`3-主体` 和项目风格复核加载；显式 legacy 光影任务可回读 archived `backup/9-光影`。若需要进入正式美学协议或阶段正文，必须由 owning stage 另行执行。

## Field Map

| field_id | Markdown 区块 | 内容要求 | 失败码 |
| --- | --- | --- | --- |
| `GLOBAL-NARRATIVE-RESEARCH` | `## 叙事与世界约束` | TL;DR、主题三联、世界三联、时代/地域/叙事类型/节奏倾向，信息不足时标记推导补位 | `FAIL-GLOBAL-NARRATIVE-WEAK` |
| `GLOBAL-GENRE-PROMISE` | `## 类型叙事承诺` | 类型核心契约、高光时刻类型、观众期待兑现节奏、类型承诺如何驱动全片节奏 | `FAIL-GLOBAL-GENRE-PROMISE` |
| `GLOBAL-VISUAL-MOTIF` | `## 视觉母题系统` | 贯穿全片的视觉符号、色调节点、标志性视觉承诺，识别可迁移的视觉母题语法 | `FAIL-GLOBAL-VISUAL-MOTIF` |
| `GLOBAL-TEMPORAL-TEXTURE` | `## 年代质感语法` | 年代质感来源、服装/道具/光色的时代信号密度、时间感如何被视觉材质构建 | `FAIL-GLOBAL-TEMPORAL-TEXTURE` |
| `GLOBAL-EMOTION-CURVE` | `## 情绪曲线轮廓` | 全片情绪升温/高点/释放/余波结构，识别可迁移的情绪叙事节奏模式 | `FAIL-GLOBAL-EMOTION-CURVE` |
| `GLOBAL-STYLE-ROUTE` | `## 路由决议` | 明确 `R1-STANDARD-INHERIT`、`R2-DECONTAMINATE`、`R3-TYPE-BACKFILL` 或 `R4-EXACT-LOCK` 之一及原因 | `FAIL-GLOBAL-ROUTE` |
| `GLOBAL-MEDIUM-STACK` | `## 媒介与技术栈` | 真人/2D/3D 或混合媒介选择，2-3 个核心渲染技术栈，说明如何服务叙事 | `FAIL-GLOBAL-MEDIUM` |
| `GLOBAL-AESTHETIC-PARADIGM` | `## 美学范式` | 明确美学流派、气质和叙事服务理由，不使用空泛词 | `FAIL-GLOBAL-PARADIGM` |
| `GLOBAL-PACING-ANCHOR` | `## 叙事节奏锚定` | 慢/中/快节奏、判断依据、拍摄段落执行字窗、无明确逻辑根源时默认中节奏 | `FAIL-GLOBAL-PACING` |
| `GLOBAL-POLLUTION-AUDIT` | `## 去污染审计` | 默认审计颜色/材质/构图/摄影越权项；`R4` 时审计原文保真 | `FAIL-GLOBAL-POLLUTION` |
| `GLOBAL-STYLE-PROMPT` | `## 全局风格提示词候选` | 默认 200 字以内纯中文无污染提示词；`R4` 可保留用户锁定原文但必须标明 exact | `FAIL-GLOBAL-PROMPT` |

## Routing Rules

| route_id | trigger | action |
| --- | --- | --- |
| `R1-STANDARD-INHERIT` | 输入丰满且无显式锁定 | 推导媒介、技术栈、流派并蒸馏无污染提示词 |
| `R2-DECONTAMINATE` | 草稿或参考表达含污染项 | 清洗颜色、材质、构图、摄影越权项，只保留底层渲染与美学范式 |
| `R3-TYPE-BACKFILL` | 输入稀疏 | 用叙事类型、情感目标、时代和世界约束反推稳妥底座 |
| `R4-EXACT-LOCK` | 用户明确要求原文直通、逐字继承、不要净化 | 保真记录原文为项目级锁定候选，不做净化或删改 |

## Default Pollution Boundary

默认模式下，`全局风格提示词候选` 禁止出现：

- 具体颜色词。
- 具体材质词。
- 构图术语。
- 焦段、光圈、光源位置、推拉摇移等摄影/运镜词。
- 下游对象细节，例如角色外貌、场景物件、道具形状、剧情动作。

`R4-EXACT-LOCK` 命中时允许保留用户原文，但必须在 `## 用户锁定风格原文` 中逐字落盘，并在审计中声明未净化原因。

## Required Markdown Shape

`全局风格解析.md` 至少包含：

1. `## 使用边界`
2. `## 叙事与世界约束`
3. `## 类型叙事承诺`
4. `## 视觉母题系统`
5. `## 年代质感语法`
6. `## 情绪曲线轮廓`
7. `## 路由决议`
8. `## 媒介与技术栈`
9. `## 美学范式`
10. `## 叙事节奏锚定`
11. `## 去污染审计`
12. `## 全局风格提示词候选`
13. `## Do Not Import`

## New Field Definitions

### GLOBAL-GENRE-PROMISE: 类型叙事承诺

| subfield | requirement |
| --- | --- |
| `genre_core_contract` | 该类型对观众的核心承诺是什么（如"正义必胜"、"真相揭示"、"命运抗争"） |
| `highlight_type_moments` | 类型标志性高光时刻的视觉/叙事节奏模式 |
| `promise_delivery_rhythm` | 承诺兑现的节奏：持续累积 / 集中爆发 / 延迟反转 |
| `sub_genre_or_hybrid` | 是否混合多个类型，各类型如何分配权重 |

### GLOBAL-VISUAL-MOTIF: 视觉母题系统

| subfield | requirement |
| --- | --- |
| `recurring_visual_symbols` | 贯穿全片重复出现的视觉符号，及其在叙事中的语义演变 |
| `color_tonal_nodes` | 全片色调节点变化，哪些颜色承担叙事功能 |
| `iconic_visual_commitment` | 参考片最具辨识度的视觉承诺，可抽象迁移的视觉语法 |
| `motif_grammar` | 母题的语法规则：如何开始、如何重复、如何在叙事高潮处被打破或终极兑现 |

### GLOBAL-TEMPORAL-TEXTURE: 年代质感语法

| subfield | requirement |
| --- | --- |
| `era_signal_source` | 年代质感从哪里来：服装、道具、建筑、语言密度、光色、声音材质 |
| `signal_density` | 年代信号的出现频率：高密度（时刻提醒）/ 低密度（偶尔暗示） |
| `modern_interference` | 是否有意识地混入当代视觉/听觉元素，如何处理时代感冲突 |
| `time_sense_construction` | 时间感如何被材质、构图和节奏共同构建 |

### GLOBAL-EMOTION-CURVE: 情绪曲线轮廓

| subfield | requirement |
| --- | --- |
| `curve_structure` | 全片情绪曲线类型：线性升温 / 波浪起伏 / 三幕两高 / U 型 / 螺旋上升 |
| `act_emotion_anchor` | 每幕的情绪档位和核心情绪任务 |
| `climax_emotion_type` | 高潮的情绪类型：压抑释放 / 震惊反转 / 感动余震 / 智识快感 |
| `emotion_residual_design` | 终场情绪余震设计：开放式 / 释然落幕 / 悬念留存 / 情绪蒸发 |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| `全局风格解析.md` 是否只作为 side context，不直接生成或改写 `2-美学` canonical 输出、`style_contract.json` 或当前项目 `MEMORY.md` / `CONTEXT/`？ | `GATE-SBS-ADAPT-01` | `FAIL-SBS-ADAPT-SIDE-CONTEXT` | `N5-BRIDGE` | 使用边界与未写 canonical 文件证据 |
| `## 叙事与世界约束` 是否包含 TL;DR、主题三联、世界三联、时代/地域/类型/节奏倾向，并标注推导补位？ | `GATE-SBS-GLOBAL-01` | `FAIL-GLOBAL-NARRATIVE-WEAK` | `N5-BRIDGE` | narrative_research 字段与 evidence grade |
| 类型叙事承诺是否说明核心契约、高光类型、观众期待兑现节奏和子类型权重？ | `GATE-SBS-GLOBAL-02` | `FAIL-GLOBAL-GENRE-PROMISE` | `N5-BRIDGE` | genre_promise 字段表 |
| 视觉母题是否提炼为可迁移母题语法，而不是复制参考片具体符号、构图或对象细节？ | `GATE-SBS-GLOBAL-03` | `FAIL-GLOBAL-VISUAL-MOTIF` | `N5-BRIDGE` | visual_motif_seed 与 do_not_import 对照 |
| 年代质感是否说明信号来源、密度、现代干扰和时间感构建？ | `GATE-SBS-GLOBAL-04` | `FAIL-GLOBAL-TEMPORAL-TEXTURE` | `N5-BRIDGE` | temporal_texture 字段覆盖 |
| 情绪曲线是否给出结构、幕情绪锚点、高点情绪类型和余震设计？ | `GATE-SBS-GLOBAL-05` | `FAIL-GLOBAL-EMOTION-CURVE` | `N5-BRIDGE` | emotion_curve_profile |
| 路由决议是否在 `R1/R2/R3/R4` 中单选，并给出证据和污染处理策略？ | `GATE-SBS-GLOBAL-06` | `FAIL-GLOBAL-ROUTE` | `N5-BRIDGE` | route_decision 与 pollution audit |
| 媒介与技术栈是否说明真人/2D/3D/混合媒介和 2-3 个技术栈如何服务叙事？ | `GATE-SBS-GLOBAL-07` | `FAIL-GLOBAL-MEDIUM` | `N5-BRIDGE` | style_foundation.medium_stack |
| 美学范式是否明确流派、气质和叙事服务理由，避免空泛审美词？ | `GATE-SBS-GLOBAL-07A` | `FAIL-GLOBAL-PARADIGM` | `N5-BRIDGE` | style_foundation.aesthetic_paradigm |
| 叙事节奏锚定是否给慢/中/快判断依据和拍摄段落执行字窗？ | `GATE-SBS-GLOBAL-08` | `FAIL-GLOBAL-PACING` | `N5-BRIDGE` | pacing_anchor |
| 去污染审计是否清除颜色、材质、构图、摄影越权和下游对象细节；`R4` 是否标明 exact？ | `GATE-SBS-GLOBAL-09` | `FAIL-GLOBAL-POLLUTION` | `N5-BRIDGE` | pollution_audit 与用户锁定原文说明 |
| 全局风格提示词候选是否 200 字以内、纯中文、无污染，且不得包含下游对象细节？ | `GATE-SBS-GLOBAL-10` | `FAIL-GLOBAL-PROMPT` | `N5-BRIDGE` | style_prompt_candidate 与 Do Not Import 检查 |
