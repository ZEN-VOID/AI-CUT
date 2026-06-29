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
| F1 初始化目录漏建 `素材/图片`、`素材/视频/操作展示`、`素材/视频/工具使用`、`素材/视频/影像内容` 或误建执行期目录 | 项目初始化骨架层 | 回到 `N0-PROJECT-INIT`，补齐 `示例/`、`素材/`、`素材/音频/`、`素材/图片/`、`素材/文案/`、`素材/视频/`、`素材/视频/操作展示/`、`素材/视频/工具使用/`、`素材/视频/影像内容/`、`结果/`，并移除本轮误建的占位文件/执行期目录 | `Project Initialization Contract` 固定 10 个目录，禁止创建文件、PRP、报告、manifest、`MEMORY.md`、`CONTEXT/` 和执行期工作目录 | 目录清单只包含初始化骨架；10 个目录均存在且没有新增文件 |
| ASR 不可用后字幕与旁白不贴 | fallback 策略层 | 用音频 `silencedetect` 停顿边界重建 cue，替换全片比例分配 | F1 最低 fallback 固定为“LLM 语义分块 + 停顿边界投影” | cue 最大时长 ≤ 4s，用户听感不再明显抢跑/滞后 |
| 停顿边界 fallback 仍然漂移 | fallback 映射层 | 把字幕语义块先绑定到真实发声区间；只有单个发声区间超过上限时才在区间内部拆分 | ASR 不可用时不要让 cue 数量显著多于 speech interval 后再做全局文本长度摊分 | `subtitle_timing*.json` 中 cue 与 speech interval 有明确对应关系，后段字幕不逐步漂移 |
| 静音边界 fallback 被误判为严格同步 | 验收门禁层 | 返修到 ASR word/char timestamps；ASR 不可用时逐 cue 人工听看并写入 strict sync evidence | F1 final 完成门固定运行 `validate_dialogue_alignment.py --strict`；silencedetect/speech interval 只能生成 draft 或人工听看的定位线 | strict validator 通过；每条 cue 有 ASR word/char span 或 `manual_listening_verified=true` |
| SRT 结构通过但台词不对应 | 验收门禁层 | 增加 `dialogue_alignment*.json`，逐条记录 cue 文本、音频区间、文案区间和对齐来源 | 完成门禁必须包含台词对齐证据；SRT validator、final 时长、抽帧可读都不能替代台词对齐验收 | `dialogue_alignment*.json` 覆盖所有 cue，报告记录 pass/fail 和失败返工入口 |
| 有 ASR 证据但字幕文本仍串到相邻台词 | 对齐质量门禁层 | 改用 ASR 真实发声段落或词级边界重建 cue；低 ASR/文案内容匹配率必须返工或逐 cue 人工听看确认 | `validate_dialogue_alignment.py --strict` 默认检查内容匹配率；仅有 ASR span 但缺 match ratio 不再足够 | `match_report.match_ratio` 或 cue 级 `match_ratio` 达到门槛，或有人工听看确认 |
| `视频说明.yaml` 只有视频级摘要导致选段粗糙 | 素材索引粒度层 | 升级为视频级元数据 + `segments[]` 片段级候选；EDL 引用 `segment_id` 而不是只引用文件名 | F1 的 manifest 合同要求 `media/content_profile/selection_profile/splicing_profile/subtitle_safe_zone/segments[]` | EDL/报告记录 `video_id/file/segment_id/source_start/source_end/selection_reason/subtitle_risk` |
| `操作展示/工具使用/影像内容` 被混成普通 B-roll | 素材分类路由层 | 回到 `N5`，按 `operation_demo/tool_display/aigc_content` 分别补 operation state、screen state、semantic match 证据 | 目录分类必须进入 manifest category 和 visual plan；三类素材统一汇入 F1 主链但使用不同解析门 | EDL/visual plan 记录 `category`、类型专属证据和目录-category 校验结果 |
| 三类素材按目录顺序或固定比例拼接 | 素材组合层 | 回到 `N5`，按字幕 cue/audio span 重建 `material_composition[]`，每段只选一个主视觉 category | 三类素材不是三段固定模板；最终必须是一条由旁白主时钟驱动的主视觉时间线 | `material_composition[]` 覆盖 cue，final 抽帧顺序与 composition plan 一致 |
| `素材/图片/` 被按文件名或目录顺序直接铺进视频 | 图片素材索引层 | 回到 `N1/N5`，读取或建立 `素材/图片/图片说明.yaml`，把图片作为 `image_asset` 条目按 cue 语义选择 | 图片说明独立于视频说明；图片进入 `material_composition[]` 必须回指 `image_id/file/role/presentation_policy/subtitle_risk` | 图片段 final 抽帧与 `image_id`、选用理由、裁切/缩放策略和字幕安全区一致 |
| 缺少 `视频说明.yaml` 但用户希望先整理素材 | 素材说明生成入口层 | 调度 `_shared/video-to-manifest/` 共享卫星先生成或更新 manifest，再回到 F1 `N1/N5` 消费 | F1 父技能只消费 manifest；生成/修复由共享卫星负责，避免把视频理解生成链塞进 final 渲染主链 | 共享卫星输出 canonical `视频说明.yaml`、material evidence、validation report 和 handoff verdict |
| 项目提供 BGM 但成片缺失、整段乱铺、节奏不贴或盖住旁白 | BGM 输入发现 / 节奏混音治理层 | 回到 `N1/N5/N6`，发现 `素材/音频/BGM.*`，生成或修复 `bgm_mix_plan*.json`，按画面节奏选段、fade/loop、ducking 后重渲染 | BGM 是可选但受治理的背景音乐层；存在且启用时必须有 source probe、选段、视觉同步点、节奏匹配、音量和旁白优先证据 | `validate_bgm_mix_plan.py --require-bgm` 通过，final 音轨可听到 BGM 但旁白清晰，无硬切、爆音或未节选整段铺底 |
| 字体/字号/样式只能临时改命令 | 字幕样式治理层 | 把最终样式落盘为 `subtitle_style*.json`，并从该 JSON 投影到 ffmpeg/libass | F1 字幕样式合同固定支持字体、全片锁定字号、颜色、描边、阴影、位置、边距、盒底和预览验收 | style JSON 校验通过，最长 cue 和高风险背景抽帧可读 |
| 输出字幕跳行、cue 文本被拆成多行或单行过长 | 字幕输出格式治理层 | 回到 `N4` 按 ASR word span 或同一 speech interval 内说话时间重切 cue；只允许在 `N6/N7` 调整全片锁定样式、边距和单行策略 | F1 最终字幕固定为单行：`master.srt` 每个 cue 只能一行文本；超长内容切成多个单行 cue，每个 cue 必须有独立 `audio_span/script_span` 和 dialogue verdict | `validate_srt.py` 拒绝多文本行、ASS `\N`、HTML `<br>`；`validate_subtitle_style.py` 拒绝 `max_lines!=1`；`dialogue_alignment*.json` 覆盖拆分后的所有 cue |
| 字幕字号忽大忽小、长句被自动缩小或按 cue 改字号 | 字幕样式锁定层 | 回到 `N6/N7` 生成带 `font_size_lock=true`、全片 `font_size_scope`、`auto_shrink=false` 的 `subtitle_style*.json`；长句回 `N4` 拆 cue | 字号是全片样式，不是单条 cue 的避让手段；用户指定字号也应成为全片锁定值 | `validate_subtitle_style.py` 拒绝缺锁定字段、`auto_shrink=true` 和逐 cue 字号覆盖；抽帧中不同 cue 字号一致 |
| 字幕严格同步但观感上半词/串句 | 字幕边界切分层 | 回到 `N4`，用 ASR segment/word 边界和文本边界后处理修复半个模型名、半个中文词、句尾字粘到下一句 | 最终 SRT 固定运行 `validate_srt.py --strict-boundaries`；边界检查和 dialogue alignment 同时通过才算 final | 无 `GPTIma/ges2`、`提/供`、`地现在` 等边界错误；strict SRT + strict dialogue alignment 通过 |
| 工具类字幕和画面状态不对应 | 视觉语义对齐层 | 回到 `N5`，为工具段建立 `visual_alignment_plan*.json.tool_screen_alignment[]`，绑定 cue、screen state 和素材段 | 文案命中工具、提示词、按钮、参数、导入导出时，不允许只铺泛化工具录屏；必须记录 `screen_state/match_evidence` | visual alignment validator 通过，工具段 final 抽帧能看出对应界面状态 |
| 画中画缺失、触发太少、停留过短、来源不明、位置固定/不随机、出现方式不佳或遮挡字幕/关键 UI | PiP overlay 治理层 | 回到 `N5`，建立或修复 `visual_alignment_plan*.json.pip_density_policy` 与 `picture_in_picture[]`，补 `trigger_source/pip_type/pip_role/pip_media_type/duration_policy/overlay_source/base_layer_ref/placement_decision/position_strategy/layout/style/motion/safe_zone/layer_order` | 用户要求强化、参考样片高频 PiP、结果预览、局部放大、前后对比、工具上下文保留或效果证明时，PiP 应先建立候选池、密度预算和媒体停留策略；视频小窗至少 4 秒，图片小窗至少 3 秒，位置随机必须是 seeded/weighted safe random 或轮换安全区，不得固定一个角落，也不得当成第二主视觉或无来源装饰贴片 | `validate_visual_alignment_plan.py --require-pip --min-pip-video-duration 4 --min-pip-image-duration 3 --require-pip-duration-policy` 通过，PiP final 抽帧显示来源、密度、停留时长、位置轮换/随机、入场、尺寸和字幕/关键 UI 避让正确 |
| 大字报或 PiP 计划字段齐全但成片没有真实兑现、只有静态字或没有小窗 | 计划/渲染兑现漂移层 | 重渲染前把 `render_evidence` 写回 `title_cards[]` / `picture_in_picture[]`，并让实际 `render_command.txt` 带可核对的 `filter_evidence` 标记；最终运行 `validate_visual_alignment_plan.py --require-render-parity --render-command` | 视觉计划 validator 不能只验 JSON 字段；凡 title-card/PiP/overlay 有 runtime 视觉承诺，完成门必须核对计划证据和实际渲染命令是否同场存在 | visual validator 的 render parity 通过，抽帧 contact sheet 能看到对应大字报/PiP，报告记录 markers 与 verify frame |
| 转场平淡、触发太少、全是默认硬切/泛化 crossfade、类型单调、效果族单一、节奏不贴或遮挡字幕 | 转场节奏与效果调色板治理层 | 回到 `N5/N6`，建立或修复 `visual_alignment_plan*.json.transition_density_policy` 与 `visual_transitions[]`，补 `trigger_source/transition_type/transition_role/from_material_composition_id/to_material_composition_id/rhythm_sync/effect_style/effect_profile/safe_zone/layer_order`；每个效果档案要有 `effect_family/style_preset/parameters/intensity/variation_reason` | 用户要求转场强化、参考样片高频切点、素材类别/语义阶段切换、工具到结果、BGM/旁白强拍或尾钩时，先建转场候选池、密度预算和 `effect_palette/richness_policy`；静音很少的参考片不要按静音触发；`soft_crossfade` 只能有理由地作 fallback smoothing；相邻转场不能只换类型但重复同一效果族无理由 | `validate_visual_alignment_plan.py --require-transitions` 通过，关键转场 final 抽帧或短预览显示节奏、类型、效果族/预设/参数多样性、层级和字幕安全正确 |
| 大字报与字幕/旁白错位 | 强调层时间锚定层 | 建立 `title_card_plan*.json` 或 `visual_alignment_plan*.json.title_cards[]`，把 card_text 绑定 cue/audio/script/visual span，并补 `presentation_timing` | 大字报是当前画面中的特效文字 overlay，不是字幕样式；用户圈定或自动强调都必须回指字幕 cue，且硬字幕最后烧录 | title-card validator 通过，大字报段抽帧与对应字幕 cue/旁白区间一致 |
| 批量 F1 同一项目中部分文案缺少大字报而其他文案已有大字报 | 批量风格一致性 / 自动强调触发层 | 对缺失线执行 `repair_title_card`：补 `title_card_plan.json`、回写 `visual_alignment_plan.title_cards[]`、重渲染并抽大字报帧 | 同一批次若任一线启用了大字报，或用户反馈“缺少大字报/特效文字”，其余同批输出应检查 `title_cards[]` 是否为空；为空时不应只交付原 final | `validate_visual_alignment_plan.py --require-title-card` 通过，title-card contact sheet 可见且不遮挡底部硬字幕 |
| 大字报过密、遮挡或新增无证据信息 | 强调层处理细则层 | 回到 `N5`，重建 title-card plan：限制自动触发密度，补 `text_determination/supporting_sources/presentation_timing/effect_style/entrance_effect/safe_zone/layer_order`，必要时退回普通字幕或 fallback card | 大字报必须有文字确定依据、呈现时机、文字特效、合适入场效果、尺寸策略、布局安全区和字幕显示策略；不是把好看的标题随意叠上去 | title-card processing validator 通过，final 抽帧不遮挡硬字幕、关键 UI、人物脸部或主体动作 |
| 大字报落在红框式顶部窄条、字号偏小或入场动效弱 | 强调层布局与样式门禁层 | 回到 `N5/N6` 重建 `layout` 和 `effect_style`：`emphasis_overlay` 默认改为 `hero_emphasis_band`，720p `font_size_min>=90`，补允许的 `entrance_effect` 和 `entrance_effect_reason` | 用户反馈“移动到蓝框位置/字更大/更炫酷”时，不应只调 drawtext 坐标；计划必须记录主视觉强调带、百分比位置、字幕安全距离、碰撞避让和 fallback reason | validator 拒绝无理由 `top_banner/top_center`、小于 90 的强强调字号和普通 `fade_in`；抽帧确认落在画面中部偏上宽幅区域 |
| 字幕/大字报计划字段已改但成片或报告仍被质疑字号不符 | 源层漂移与最终证据层 | 先扫 `SKILL.md`、README、templates、validator、CONTEXT、项目 sidecar 和 render filter 中旧字号；再重渲染 canonical final 并抽帧 | 字号规范不能只改一个计划文件；旧 override 报告、模板旧下限或缓存成片都会误导下一轮验收；完成门必须同时校验计划值和 `render_command.txt` 的实际投影 | `validate_subtitle_style.py --expected-font-size 30 --require-render-font-size` 通过，`validate_visual_alignment_plan.py --expected-title-font-size 90 --require-render-title-font-size` 通过；ASS `Fontsize=30`、drawtext `fontsize=90`、ffprobe/decode/contact sheet 三证齐全 |
| 批量视频同一字幕字号但视觉观感一条偏大、一条偏小 | 字幕视觉等效校准层 | 不盲目坚持单一数值；先比较最终抽帧中字体、描边、盒底、ASS/libass/force_style 渲染链，再按项目线写入 `visual_calibration` 并重渲染 | 源层默认字号是起点，不替代最终视觉验收；不同字体和渲染入口可用项目级有效字号/描边做视觉等效校准，但必须保留 source default 与 effective value | 横向 contact sheet 对比通过；`subtitle_style.json` 同时记录 source default 与 effective subtitle size；final decode/style/audit 通过 |
| 大字报入场特效千篇一律 | 强调层动效选择机制层 | 回到 `N5` 补 `effect_style.entrance_effect_selection`：按 cue 角色、语义强度、画面运动、背景复杂度和最近使用记录选择；相邻重复必须写 `repetition_reason` | 入场特效不是固定模板，也不是随机轮换；先匹配语义和画面，再做局部多样化。连续 hero 大字报默认不得重复同一主入场效果 | validator 拒绝缺选择依据、相邻重复且无理由、3 张窗口只有一种主入场效果 |
| 字幕在亮背景或复杂画面不可读 | 字幕样式层 | 白字黑描边，必要时增加 Outline 或上移 MarginV | 每次全片渲染前抽最长 cue 和亮背景帧 | 抽帧中字幕不溢出、不被底部小字完全遮挡 |
| 参考样片无明显场景切换但被误判为高频剪辑 | 参考节奏解释层 | 以时长、画幅、字幕位置、旁白推进为主要参考，而非硬切数量 | 场景检测为 0 时必须写人工观察说明 | `reference_notes.md` 说明参考节奏来源 |
| 直接覆盖旧 final 导致无法比较 | 输出治理层 | 先备份旧 final，再覆盖 canonical 输出 | `CHK-F1-OVERWRITE` 固定为高影响检查点 | 结果目录存在旧版备份 |
| 只验证命令成功未验证成片 | 验收层 | 对 final MP4 做完整解码、ffprobe、抽帧 | `N7-VERIFY` 是完成门，不是可选项 | decode_ok、ffprobe JSON、verify frames 存在 |

## Repair Playbook

1. 字幕不同步时，先查 `master.srt` 的来源：ASR、停顿边界 fallback、还是比例分配。
2. 若是比例分配，立即回到 `N4-SUBTITLE-TIMELINE`，优先重建 ASR word/char 时间轴；停顿边界只能作为 draft 定位线。
3. 若是停顿边界 fallback，不能直接判定 final 通过；必须补 ASR word/char timestamps，或逐 cue 人工听看并在 `dialogue_alignment*.json` 写入 `manual_listening_verified=true` / 等价 strict evidence。
4. 若是停顿边界 fallback 但仍不贴，检查 cue 数是否明显多于 speech interval；若是，改成“每个真实发声区间绑定一个语义字幕”，只对超过 4 秒的长发声区间做内部拆分，然后仍需 ASR 或人工听看 strict 验收。
5. 若 SRT 结构通过但用户反馈“字幕和音频不是很对齐”，检查是否缺少 `dialogue_alignment*.json` 或 strict validator verdict；没有逐条 cue-to-audio/script 严格对齐证据时，不能继续判定通过。
6. 若已有 ASR word/char span 但用户反馈“台词和字幕不匹配”，优先查 ASR/文案 `match_ratio` 和 cue 是否跨真实发声段；低于门槛、缺 `match_ratio` 或串到相邻 segment 时，回到 `N4` 用 ASR segment/word 边界重建，而不是沿用旧 SRT 重渲染。
7. 若已有 ASR，但仍不贴，检查是否使用了最终输出时间线而非源音频时间线。
8. 若工具段画面不贴，先检查 `visual_alignment_plan*.json` 是否存在；缺失时不要直接重渲染，先把工具 cue 绑定到 screen state、素材 `segment_id/source_file` 和 `visual_span`。
9. 若操作展示段画面不贴，先检查入选片段是否有 `operation_state/action_phase/step_label`；没有时回到 manifest 或抽帧观察补证据，不要把工具界面规则套用到操作演示。
10. 若三类素材组合顺序不对，先检查是否缺 `material_composition[]`；不要直接重渲染，先按 cue/audio span 重建主视觉时间线。
11. 若图片素材错用、被裁坏、遮挡字幕或只是按文件名铺上去，先查 `图片说明.yaml` 与 `material_composition[]` 的 `image_asset` 条目；缺 `image_id`、图片语义证据、呈现策略或字幕安全区时回到 `N1/N5`，不要只在渲染命令里调图片时长。
12. 若画中画缺失、触发数量太少、停留过短、位置固定不随机、出现方式突兀、像装饰贴片或遮挡字幕/关键 UI，先查 `visual_alignment_plan*.json.pip_density_policy` 与 `picture_in_picture[]`；缺 `target_count/actual_count/density_basis/min_video_duration_sec/min_image_duration_sec/pip_media_type/duration_policy/overlay_source/base_layer_ref/content_evidence/placement_decision/position_strategy/layout/style/motion/safe_zone/layer_order` 时回 `N5`，不要只在渲染命令里临时叠图或拉长。
13. 若大字报或 PiP 计划看起来合规但用户反馈“成片没有按规则来”，不要只复查 JSON；同时打开 `render_command.txt`、final 抽帧和 `verify_contact_sheet`，确认 `render_evidence.filter_evidence` 标记在命令中存在，并用 `--require-render-parity --render-command` 重新跑 visual validator。
14. 若用户指出字幕或大字报字号不对，先按 F1 当前 720p 合同核验硬值：台词字幕 `font_size=30` 且最终 ASS `Fontsize=30`，大字报 `font_size=90` 且最终 drawtext `fontsize=90`。不能只改 `subtitle_style.json` 或 `visual_alignment_plan.json`；必须同步 `render_command.txt`、重渲染 final、抽帧，并运行 `validate_subtitle_style.py --expected-font-size 30 --require-render-font-size` 与 `validate_visual_alignment_plan.py --expected-title-font-size 90 --require-render-title-font-size`。
15. 若多个画中画同时出现时“不整齐”、数量偏少或与当前讲述关联弱，先查同一 `cluster_id` 下的 PiP 组：默认 3 个一组，写 `layout_group.group_size=3`、`slot=1/2/3`、左中右对齐，并给每个条目写当前 `cue_text` 与 `content_evidence`；若大字报占用主强调带，改用下方对齐行。修复后运行 `validate_visual_alignment_plan.py --expected-pip-group-size 3 --require-pip-aligned-groups --require-pip-cue-text-evidence --min-pip-video-duration 4 --min-pip-image-duration 3 --require-pip-duration-policy`。
16. 若用户反馈画中画停留太短，先按媒体类型重算 `visual_span`：视频源小窗至少 4 秒，图片/静态源至少 3 秒；补 `pip_media_type`、计划级 `min_video_duration_sec/min_image_duration_sec` 和条目级 `duration_policy`，再重渲染并抽帧，不要只改最终命令而不回写计划。
17. 若转场平淡、触发太少、类型单调、效果族单一、节奏不贴、全是默认硬切/泛化 crossfade 或遮挡字幕，先查 `visual_alignment_plan*.json.transition_density_policy` 与 `visual_transitions[]`；缺 `target_count/actual_count/density_basis/effect_palette/richness_policy/from_material_composition_id/to_material_composition_id/rhythm_sync/effect_style/effect_profile/safe_zone/layer_order` 时回 `N5`，不要只在渲染命令里临时换滤镜。每个拼接点必须有 `effect_family/style_preset/parameters/intensity/variation_reason`，相邻同效果族无 `repeat_effect_family_reason` 时应返工。
17. 若大字报时机不对，先检查 `title_card_plan*.json` 的 `cue_indices/audio_span/visual_span/presentation_timing`；大字报应随字幕 cue 修，不应单独拖时间轴。
18. 若同一批次部分文案有大字报、部分没有，或用户反馈“没有大字报/特效文字”，先查各线 `visual_alignment_plan.json.title_cards[]`；缺失线按 `repair_title_card` 补 title-card plan、重渲染、抽帧，并运行 `validate_visual_alignment_plan.py --require-title-card`。
19. 若大字报太多、遮挡、文字像新写的口号、缺合适入场效果或样式不对，先查 `text_determination/supporting_sources/presentation_timing/effect_style/entrance_effect/safe_zone/layer_order`；缺字段时回 `N5` 重建计划，不要只在渲染命令里调位置。
20. 若大字报在画面顶部窄条、字号偏小或动效不够，先查 `layout.layout_zone`、`effect_style.font_size_min` 和 `effect_style.entrance_effect`；强强调默认改为 `hero_emphasis_band`，720p 字号默认/下限 90，普通 `fade_in` 或静态黑底小条不应通过。
21. 若用户反馈大字报入场特效千篇一律，先查 `effect_style.entrance_effect_selection` 和最近 3 张 hero 大字报的主 `entrance_effect`；缺选择依据或相邻重复无 `repetition_reason` 时回 `N5` 重新分配，不要只批量替换成另一个固定特效。
22. 若用户要求生成、更新、修复或校验 `视频说明.yaml`，不要把任务硬塞进 F1 final 主链；先加载 `_shared/video-to-manifest/SKILL.md + CONTEXT.md`，让共享卫星输出 manifest 和 validator 报告。
23. 若用户要求自定义字体、字号、颜色、位置或盒底，先生成/更新 `subtitle_style*.json`，再渲染短预览和抽帧，不直接改一次性 ffmpeg 命令。
24. 若字幕字号忽大忽小、长句被自动缩小或不同 cue 字号不同，先查 `subtitle_style*.json` 是否有 `font_size_lock=true`、全片 `font_size_scope`、`auto_shrink=false`，以及是否存在 `font_size_overrides/per_cue_font_size/cue_font_sizes`；缺失或违规时回 `N6/N7` 修样式，长句回 `N4` 拆成多个单行 cue。
25. 若字幕跳行、被拆成多行或单行过长，先查 `master.srt` 是否含多文本行、ASS `\N` 或 HTML `<br>`，再查 `subtitle_style*.json` 的 `max_lines/line_break_policy` 和 `dialogue_alignment*.json` 的 cue-to-audio/script 映射；不要用分行或缩小单条字号解决超长文本，优先按 ASR word span 或 speech interval 内说话时间重切 cue，确保每个拆分 cue 仍对应真实台词。
26. 若字幕台词对应但观感像串词，检查相邻 cue 是否把模型名、中文词或句尾字切开；典型失败是 `GPTIma/ges2`、`提/供`、`地现在`、`已经` 被拆断。修复后运行 `validate_srt.py --strict-boundaries`。
27. 若字幕可读性差，先抽最长 cue 和亮背景帧，再调全片锁定字号、描边、边距或重切 cue，避免用跳行或逐 cue 缩小解决。
28. 若批量视频使用相同字幕字号但观感不一致，先不要继续改大字报或全局默认；比较最终抽帧、字体、描边、盒底、`force_style` 与 ASS 样式后，为单条线写入 `visual_calibration_YYYYMMDD`，记录 source default 和 effective subtitle size，再重渲染并生成横向 contact sheet。
29. 若成片长度不对，先比较旁白时长、视频映射速度和 `-shortest` 行为。
30. 若用户要求“按上次那套”，读取最近 PRP、报告和 project.md，但仍重新验证输入路径。
31. 修复后必须更新执行报告和 project.md，避免旧报告误导下一轮。
32. 若项目 `素材/音频/` 里有 BGM，或用户明确给出 BGM 路径，但 final 没有 BGM、BGM 整段乱铺、节奏不贴画面或盖住旁白，先查 `background_music_status` / `bgm_mix_plan*.json`；缺 source probe、选段、visual sync、ducking 或 volume 证据时回到 `N1/N5/N6`，不要只在最终命令里临时加 `amix`。

## Reusable Heuristics

- 对“已有旁白 + 文案”的短视频，旁白音频是主时钟；视频节奏应服务旁白，不应反过来拉伸旁白。
- F1 初始化是目录骨架任务，不是成片任务；默认只建 10 个目录，`素材/图片/` 和 `素材/音频/文案/视频/` 同级，且 `素材/视频/` 下固定包含 `操作展示/`、`工具使用/`、`影像内容/`，不创建文件或执行期目录。
- 参考样片的作用是节奏、画幅、字幕和补位策略，不是素材复用。
- ASR 词级时间戳最好；没有 ASR 时，停顿边界比字数比例可靠很多。
- 严格同步不是“停顿边界更好一点”：最终交付必须有 ASR word/char span 或逐 cue 人工听看确认；停顿边界只负责缩小人工检查范围。
- 没有 ASR 时，停顿边界 fallback 的主单位应该是真实发声区间；全局按文字长度在整段 speech-time 上连续摊分，容易让后半段字幕逐步漂移。
- 字幕验收要区分三件事：结构合法、时间贴近、台词对应。前两项通过不代表第三项通过。
- `dialogue_alignment*.json` 是 F1 字幕台词验收的最小证据：每条 cue 至少要有 cue index、text、audio_span、script_span、source_method、strict sync evidence、ASR/文案内容匹配率或人工听看确认，以及 verdict；final 必须用 strict validator 复核。
- ASR word span 只能说明“有时间锚点”，不能单独说明“这段文字就是这段声音”。ASR 路径必须记录 `match_report.match_ratio` 或 cue 级 `match_ratio`；低于门槛时先修映射，不能只重烧同一 SRT。
- 素材说明要区分两层：视频级字段用于快速归类，片段级 `segments[]` 才能支撑自动选段、拼接和字幕避让。只有整条视频摘要时，最多作为人工观察辅助，不应直接生成 EDL。
- 三类标准素材目录的判断顺序：`operation_demo` 看操作动作/步骤连续性，`tool_display` 看屏幕状态/可见 UI，`aigc_content` 看视觉语义/节奏承托。目录名给分类信号，最终选段仍要回到片段证据。
- 三类素材的组合顺序必须跟随旁白和字幕 cue：先判断这句话需要结果画面、工具状态还是操作过程，再选素材；不要先按目录批量拼接。
- `素材/图片/图片说明.yaml` 应与 `素材/视频/视频说明.yaml` 分开维护；图片素材是静态候选池，进入主视觉时间线时使用 `primary_category=image_asset`，必须记录 `image_id`、选图依据、呈现方式和字幕风险。
- 图片适合承接截图、对比图、流程说明、证据图、封面候选和短时补位；若文案需要动作过程或界面状态变化，优先找视频段，图片只能作为保守降级或补充 overlay。
- 画中画停留时长按媒体类型定门槛：视频源小窗至少 4 秒，图片/静态源小窗至少 3 秒。cue 本身短于门槛时，应让 `visual_span` 与 cue 有交集并记录 `duration_policy`，而不是缩短小窗或只改渲染命令。
- 生成或修复素材说明本身属于 `_shared/video-to-manifest/` 共享卫星职责；F1 主链只在 `N1/N5` 消费 manifest，并保留 fallback 到 `ffprobe + 抽帧人工观察` 的能力。
- BGM 的默认发现位置是 `素材/音频/BGM.*` / `素材/音频/bgm.*`；`.mp4` 只取音频流，不把它当视觉素材。不存在 BGM 不阻断成片，存在且启用时必须进入计划和验证。
- BGM 不是把整首歌压到最终视频底下；先找 hook、工具证明、结果展示、高潮和尾钩附近的 beat/drop/rise，再把源音频片段映射到目标视觉节奏，必要时短 loop、交叉淡入淡出或留 intentional gap。
- BGM 混音永远让旁白优先：默认做 ducking 和低电平 bed，宁可保守降低或禁用冲突音乐，也不要让音乐抢台词主时钟。
- 自动混剪 EDL 应引用 `segment_id`，并记录选择理由和字幕风险；只记录素材文件名会让后续复查无法知道为什么选这一段。
- 工具类画面不是普通 B-roll；当字幕说到具体按钮、参数、输入框、生成状态或导出结果时，画面必须能回指同一 screen state。
- 画中画是结果预览、局部放大、前后对比、证明画面或工具上下文保留的 overlay 证据层，不是第二条主视觉轨。参考样片只提供 PiP 的节奏、触发密度和构图范式，除非用户授权，不直接复用参考视频内容。PiP 必须先判断候选触发、密度目标、最佳出现位置、呈现样式和入场方式；缺 `pip_density_policy/position_strategy/placement_decision/style/motion` 的小窗通常只是缩小贴片，不应通过 final 验收。
- PiP 默认适合“工具界面仍要看见，但需要同步展示结果/对比/局部细节”的句子；常用方案是 `hero_pip_preview` 压在工具或主画面中部安全区，或 `tool_detail_zoom` 局部放大关键 UI。所有 PiP 都要在硬字幕之前渲染，并预留底部字幕安全距离。
- 当用户要求画中画强化、参考视频中 PiP 高频出现，或脚本连续出现结果证明/局部放大/前后对比时，先写 `pip_density_policy`：记录可触发 cue 数、目标数量、实际数量、节奏窗口、屏幕占用和防霸屏护栏。15-45 秒视频有足够候选时通常不应只落 1 个 PiP。
- PiP 的“随机位置”要可复现：用 `weighted_safe_random` / `seeded_safe_random` / `rotating_safe_zone` 从安全候选区中选择，并写 `randomization_seed`、候选区、选中区、被拒绝区和碰撞检查。相邻 PiP 不应无理由重复同一 `layout_zone`；局部放大因源区域锁定时写 `position_lock_reason`。
- 多个 PiP 同时出现时，“随机位置”不应压过组内秩序：同一触发组默认 3 个一组，使用 `layout_group` 左中右对齐；每个画框必须携带当前 `cue_text` 和对应 `content_evidence`。
- PiP 和大字报的完成证据必须落到两个层面：计划层有 `render_evidence`，执行层的 `render_command.txt` 有可核对标记，画面层有包含对应时间点的 contact sheet。只通过计划字段不等于成片兑现。
- 转场强化先看边界池，而不是直接套滤镜：素材类别切换、语义阶段切换、工具到结果、BGM/旁白强拍、参考样片高分切点、PiP/大字报入场前后和尾钩都可成为候选边界。
- 参考片如果像本轮样片一样 40 秒左右出现 20+ 个视觉切点、平均约 1-2 秒一个切点且几乎没有长静音，转场应跟视觉/语义/BGM 强拍走；不要把静音检测当转场触发主依据。
- 高频转场不是全片乱加特效：`hard_cut_on_beat`、`match_cut`、`whip_pan_blur`、`zoom_push`、`flash_cut`、`glitch_snap`、`film_burn`、`particle_wipe`、`radial_blur_zoom` 等要按前后素材关系选择；`soft_crossfade` 只适合 fallback smoothing 或情绪缓冲，连续使用会让参考高频节奏退化。
- 转场丰富度应由 `effect_palette` 和 `richness_policy` 管：`tool_display -> aigc_content` 多用工具故障闪切、结果闪白揭示、推近；`operation_demo -> tool_display` 多用节奏硬切、UI 遮罩或 match cut；`aigc_content -> aigc_content` 多用甩动、速度坡、光感揭示或纵深推拉；图片与视频之间优先用视差、luma wipe 或缩放纵深。
- 只换 `transition_type` 但连续使用同一 `effect_family`，观感仍会单调。局部 3 个转场窗口至少应有 2 种效果族；连续同族只用于动作连续、品牌节奏或工具状态连击，并写 `repeat_effect_family_reason`。
- 转场和 overlay 要错峰：强大字报、PiP、关键 UI 操作同时发生时，优先把转场放在主视觉层、短化或改为节奏硬切；最终硬字幕始终最后烧录，不能被转场闪烁、拖影或遮挡。
- 大字报应绑定字幕 cue，而不是绑定“差不多的段落时间”；后续修字幕时，大字报也应跟着 cue 映射和 `presentation_timing` 一起检查。
- 大字报文字要有确定依据：原文摘录、用户指定，或从已有文案及本轮已加载资料分析后压缩；压缩要记录原因和支持证据，不能把它当成新的标题创作入口。
- 大字报样式是独立决策：`effect_style` 至少要说明文字特效、尺寸/字号策略、合适的 `entrance_effect`、入场适配理由、退场或动效、颜色/描边/阴影等关键视觉参数。
- 大字报布局先避让最终硬字幕，其次避让关键 UI、人物脸部和主体动作；位置和样式问题优先修 title-card plan，而不是只调 ffmpeg 坐标。
- 强强调大字报的默认观感应是画面中部偏上的宽幅主视觉强调带，而不是顶部小黑条。720p 可用 `hero_emphasis_band` 作为基线：x 约 12%-88%，y 约 30%-56%，字号默认/下限至少 90，并以 kinetic pop、zoom blur、light sweep、slam bounce 或 glitch snap 这类短促入场建立存在感。
- 入场特效选择要有局部多样性，但不能随机：工具/参数类更适合 `typewriter_snap` / `glitch_snap`，飞行/纵深画面更适合 `parallax_push_in` / `zoom_blur_in`，短痛点词更适合 `kinetic_pop` / `slam_bounce`，结果质感更适合 `light_sweep_reveal` / `shimmer_scale_in`。相邻 hero 大字报默认换主效果，重复时写清连续节奏理由。
- 字幕样式应有独立真源：`subtitle_style*.json` 管样式，`master.srt` 管文本和时间；不要把样式藏进 SRT 文本或一次性 shell 命令。
- F1 输出字幕默认单行不跳行；超长字幕应通过 ASR word span、同一 speech interval 内说话时间拆分、缩短单 cue、全片样式校准或调边距解决，不应通过 SRT 显式换行、自动缩小单条字号或逐 cue 改字号解决。
- 单行切分也要守住词边界：模型名、英文/数字 token、双字中文词和明显句尾字不能被切成相邻两条字幕；严格交付时用 `validate_srt.py --strict-boundaries` 复核。
- 停顿 fallback 中如果一个真实发声区间承载多条单行字幕，`project_silence_srt.py` 的 chunks 应使用对象数组标注 `interval_index`；脚本只投影已确认子块，后续仍必须生成 `dialogue_alignment*.json` 证明拆分 cue 与音频台词一致。
- F1 默认字幕以 720p 字号 30 为全片锁定基准；用户指定字号时，该字号也应成为全片锁定值。长句优先拆 cue，不使用 `auto_shrink`、`font_size_overrides` 或逐 cue 字号变化。
- 自定义大字、花字、盒底或顶部字幕时，必须比默认样式更重视抽帧，因为可读性和遮挡风险会同时变化。
- 硬字幕样式应该先在短预览帧上验证，再跑全片。
- 最终验收必须看 final MP4，而不是只看 SRT 或 ffmpeg 退出码。
- PRP 是复杂任务的可审计入口；报告是完成门的一部分。

## Promotion Backlog

- 为 F1 增加真实端到端样例 fixture，覆盖 ASR 不可用 fallback。
- 将停顿边界 SRT 投影脚本接入更完整的 SRT validator。
- 增加视觉补位模板，用于素材时长不足时自动生成白底/黑底字幕卡。
