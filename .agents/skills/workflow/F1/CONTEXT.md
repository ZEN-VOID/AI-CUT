# Context: F1

本文件是 `F1` 的经验层知识库，用于沉淀参考节奏自动剪辑、旁白字幕卡点、ASR 降级和硬字幕合成中的可复用经验。它不重定义 `SKILL.md` 的主合同。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-type-map-and-repair-playbook-focused
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| ASR 不可用后字幕与旁白不贴 | fallback 策略层 | 用音频 `silencedetect` 停顿边界重建 cue，替换全片比例分配 | F1 最低 fallback 固定为“LLM 语义分块 + 停顿边界投影” | cue 最大时长 ≤ 4s，用户听感不再明显抢跑/滞后 |
| 停顿边界 fallback 仍然漂移 | fallback 映射层 | 把字幕语义块先绑定到真实发声区间；只有单个发声区间超过上限时才在区间内部拆分 | ASR 不可用时不要让 cue 数量显著多于 speech interval 后再做全局文本长度摊分 | `subtitle_timing*.json` 中 cue 与 speech interval 有明确对应关系，后段字幕不逐步漂移 |
| SRT 结构通过但台词不对应 | 验收门禁层 | 增加 `dialogue_alignment*.json`，逐条记录 cue 文本、音频区间、文案区间和对齐来源 | 完成门禁必须包含台词对齐证据；SRT validator、final 时长、抽帧可读都不能替代台词对齐验收 | `dialogue_alignment*.json` 覆盖所有 cue，报告记录 pass/fail 和失败返工入口 |
| `视频说明.yaml` 只有视频级摘要导致选段粗糙 | 素材索引粒度层 | 升级为视频级元数据 + `segments[]` 片段级候选；EDL 引用 `segment_id` 而不是只引用文件名 | F1 的 manifest 合同要求 `media/content_profile/selection_profile/splicing_profile/subtitle_safe_zone/segments[]` | EDL/报告记录 `video_id/file/segment_id/source_start/source_end/selection_reason/subtitle_risk` |
| `操作展示/工具使用/影像内容` 被混成普通 B-roll | 素材分类路由层 | 回到 `N5`，按 `operation_demo/tool_display/aigc_content` 分别补 operation state、screen state、semantic match 证据 | 目录分类必须进入 manifest category 和 visual plan；三类素材统一汇入 F1 主链但使用不同解析门 | EDL/visual plan 记录 `category`、类型专属证据和目录-category 校验结果 |
| 三类素材按目录顺序或固定比例拼接 | 素材组合层 | 回到 `N5`，按字幕 cue/audio span 重建 `material_composition[]`，每段只选一个主视觉 category | 三类素材不是三段固定模板；最终必须是一条由旁白主时钟驱动的主视觉时间线 | `material_composition[]` 覆盖 cue，final 抽帧顺序与 composition plan 一致 |
| 缺少 `视频说明.yaml` 但用户希望先整理素材 | 素材说明生成入口层 | 调度 `video-to-manifest/` 卫星先生成或更新 manifest，再回到 F1 `N1/N5` 消费 | F1 父技能只消费 manifest；生成/修复由卫星负责，避免把视频理解生成链塞进 final 渲染主链 | 卫星输出 canonical `视频说明.yaml`、material evidence、validation report 和 handoff verdict |
| 字体/字号/样式只能临时改命令 | 字幕样式治理层 | 把最终样式落盘为 `subtitle_style*.json`，并从该 JSON 投影到 ffmpeg/libass | F1 字幕样式合同固定支持字体、字号、颜色、描边、阴影、位置、边距、盒底和预览验收 | style JSON 校验通过，最长 cue 和高风险背景抽帧可读 |
| 工具类字幕和画面状态不对应 | 视觉语义对齐层 | 回到 `N5`，为工具段建立 `visual_alignment_plan*.json.tool_screen_alignment[]`，绑定 cue、screen state 和素材段 | 文案命中工具、提示词、按钮、参数、导入导出时，不允许只铺泛化工具录屏；必须记录 `screen_state/match_evidence` | visual alignment validator 通过，工具段 final 抽帧能看出对应界面状态 |
| 大字报与字幕/旁白错位 | 强调层时间锚定层 | 建立 `title_card_plan*.json` 或 `visual_alignment_plan*.json.title_cards[]`，把 card_text 绑定 cue/audio/script/visual span | 大字报是视觉层，不是字幕样式；用户圈定或自动强调都必须回指字幕 cue，且硬字幕最后烧录 | title-card validator 通过，大字报段抽帧与对应字幕 cue/旁白区间一致 |
| 大字报过密、遮挡或新增脚本外信息 | 强调层处理细则层 | 回到 `N5`，重建 title-card plan：限制自动触发密度，补 `source_text/text_policy/safe_zone/layer_order`，必要时退回普通字幕或 full-frame card | 大字报必须有文案来源、卡片类型、时长策略、布局安全区和字幕显示策略；不是把好看的标题随意叠上去 | title-card processing validator 通过，final 抽帧不遮挡硬字幕、关键 UI、人物脸部或主体动作 |
| 字幕在亮背景或复杂画面不可读 | 字幕样式层 | 白字黑描边，必要时增加 Outline 或上移 MarginV | 每次全片渲染前抽最长 cue 和亮背景帧 | 抽帧中字幕不溢出、不被底部小字完全遮挡 |
| 参考样片无明显场景切换但被误判为高频剪辑 | 参考节奏解释层 | 以时长、画幅、字幕位置、旁白推进为主要参考，而非硬切数量 | 场景检测为 0 时必须写人工观察说明 | `reference_notes.md` 说明参考节奏来源 |
| 直接覆盖旧 final 导致无法比较 | 输出治理层 | 先备份旧 final，再覆盖 canonical 输出 | `CHK-F1-OVERWRITE` 固定为高影响检查点 | 结果目录存在旧版备份 |
| 只验证命令成功未验证成片 | 验收层 | 对 final MP4 做完整解码、ffprobe、抽帧 | `N7-VERIFY` 是完成门，不是可选项 | decode_ok、ffprobe JSON、verify frames 存在 |

## Repair Playbook

1. 字幕不同步时，先查 `master.srt` 的来源：ASR、停顿边界 fallback、还是比例分配。
2. 若是比例分配，立即回到 `N4-SUBTITLE-TIMELINE`，用音频停顿边界重建。
3. 若是停顿边界 fallback 但仍不贴，检查 cue 数是否明显多于 speech interval；若是，改成“每个真实发声区间绑定一个语义字幕”，只对超过 4 秒的长发声区间做内部拆分。
4. 若 SRT 结构通过但用户反馈“字幕和音频不是很对齐”，检查是否缺少 `dialogue_alignment*.json`；没有逐条 cue-to-audio/script 对齐证据时，不能继续判定通过。
5. 若已有 ASR，但仍不贴，检查是否使用了最终输出时间线而非源音频时间线。
6. 若工具段画面不贴，先检查 `visual_alignment_plan*.json` 是否存在；缺失时不要直接重渲染，先把工具 cue 绑定到 screen state、素材 `segment_id/source_file` 和 `visual_span`。
7. 若操作展示段画面不贴，先检查入选片段是否有 `operation_state/action_phase/step_label`；没有时回到 manifest 或抽帧观察补证据，不要把工具界面规则套用到操作演示。
8. 若三类素材组合顺序不对，先检查是否缺 `material_composition[]`；不要直接重渲染，先按 cue/audio span 重建主视觉时间线。
9. 若大字报时机不对，先检查 `title_card_plan*.json` 的 `cue_indices/audio_span/visual_span`；大字报应随字幕 cue 修，不应单独拖时间轴。
10. 若大字报太多、遮挡或文案像新写的口号，先查 `card_type/text_policy/source_text/duration_policy/safe_zone/layer_order`；缺字段时回 `N5` 重建计划，不要只在渲染命令里调位置。
11. 若用户要求生成、更新、修复或校验 `视频说明.yaml`，不要把任务硬塞进 F1 final 主链；先加载 `video-to-manifest/SKILL.md + CONTEXT.md`，让卫星输出 manifest 和 validator 报告。
12. 若用户要求自定义字体、字号、颜色、位置或盒底，先生成/更新 `subtitle_style*.json`，再渲染短预览和抽帧，不直接改一次性 ffmpeg 命令。
13. 若字幕可读性差，先抽最长 cue 和亮背景帧，再调字号、描边、边距或分行。
14. 若成片长度不对，先比较旁白时长、视频映射速度和 `-shortest` 行为。
15. 若用户要求“按上次那套”，读取最近 PRP、报告和 project.md，但仍重新验证输入路径。
16. 修复后必须更新执行报告和 project.md，避免旧报告误导下一轮。

## Reusable Heuristics

- 对“已有旁白 + 文案”的短视频，旁白音频是主时钟；视频节奏应服务旁白，不应反过来拉伸旁白。
- 参考样片的作用是节奏、画幅、字幕和补位策略，不是素材复用。
- ASR 词级时间戳最好；没有 ASR 时，停顿边界比字数比例可靠很多。
- 没有 ASR 时，停顿边界 fallback 的主单位应该是真实发声区间；全局按文字长度在整段 speech-time 上连续摊分，容易让后半段字幕逐步漂移。
- 字幕验收要区分三件事：结构合法、时间贴近、台词对应。前两项通过不代表第三项通过。
- `dialogue_alignment*.json` 是 F1 字幕台词验收的最小证据：每条 cue 至少要有 cue index、text、audio_span、script_span、source_method 和 verdict。
- 素材说明要区分两层：视频级字段用于快速归类，片段级 `segments[]` 才能支撑自动选段、拼接和字幕避让。只有整条视频摘要时，最多作为人工观察辅助，不应直接生成 EDL。
- 三类标准素材目录的判断顺序：`operation_demo` 看操作动作/步骤连续性，`tool_display` 看屏幕状态/可见 UI，`aigc_content` 看视觉语义/节奏承托。目录名给分类信号，最终选段仍要回到片段证据。
- 三类素材的组合顺序必须跟随旁白和字幕 cue：先判断这句话需要结果画面、工具状态还是操作过程，再选素材；不要先按目录批量拼接。
- 生成或修复素材说明本身属于 `video-to-manifest/` 卫星职责；F1 主链只在 `N1/N5` 消费 manifest，并保留 fallback 到 `ffprobe + 抽帧人工观察` 的能力。
- 自动混剪 EDL 应引用 `segment_id`，并记录选择理由和字幕风险；只记录素材文件名会让后续复查无法知道为什么选这一段。
- 工具类画面不是普通 B-roll；当字幕说到具体按钮、参数、输入框、生成状态或导出结果时，画面必须能回指同一 screen state。
- 大字报应绑定字幕 cue，而不是绑定“差不多的段落时间”；后续修字幕时，大字报也应跟着 cue 映射一起检查。
- 大字报文案要有来源：原文摘录、用户指定或从原文压缩；压缩要记录原因，不能把它当成新的标题创作入口。
- 大字报布局先避让最终硬字幕，其次避让关键 UI、人物脸部和主体动作；位置问题优先修 title-card plan，而不是只调 ffmpeg 坐标。
- 字幕样式应有独立真源：`subtitle_style*.json` 管样式，`master.srt` 管文本和时间；不要把样式藏进 SRT 文本或一次性 shell 命令。
- F1 默认字幕以 720p 字号 20 为基准；字号变大时同步收紧单行字数，优先避免出框和遮挡。
- 自定义大字、花字、盒底或顶部字幕时，必须比默认样式更重视抽帧，因为可读性和遮挡风险会同时变化。
- 硬字幕样式应该先在短预览帧上验证，再跑全片。
- 最终验收必须看 final MP4，而不是只看 SRT 或 ffmpeg 退出码。
- PRP 是复杂任务的可审计入口；报告是完成门的一部分。

## Promotion Backlog

- 为 F1 增加真实端到端样例 fixture，覆盖 ASR 不可用 fallback。
- 将停顿边界 SRT 投影脚本接入更完整的 SRT validator。
- 增加视觉补位模板，用于素材时长不足时自动生成白底/黑底字幕卡。
