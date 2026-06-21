# Project Memory

## Session 1 — 2026-06-20

**Strategy:** 以用户提供旁白为主时间轴，参照示例 42-61 秒的短视频节奏，把 57.76 秒主视频整体压缩到 49.15 秒，并烧录用户文案字幕。

**Decisions:** 视频速度调整为 1.1753x；原视频音频移除；旁白音频作为唯一主轨；字幕使用白字黑描边，居中偏下，避开原视频底部小字幕。

**Reasoning log:** 示例在当前阈值下没有明显硬切，节奏主要由旁白和字幕推进；主视频画面完整度高，因此保留全段视觉推进比硬切删段更稳。

**Outstanding:** 当前字幕时间轴为文案比例分配，不是 ASR 词级对齐；若后续提供火山 ASR 凭证，可重新生成更精确的 `master.srt` 后复渲染。

## Session 2 — 2026-06-20

**Strategy:** 用户反馈第一版字幕和音频不够卡点后，保留成片备份并重建字幕时间轴。

**Decisions:** 因当前环境没有火山或 OpenAI ASR 凭证，改用音频停顿边界作为 fallback：`silencedetect=n=-35dB:d=0.08`，实际停顿约 180ms 以上的位置作为字幕切换点。字幕从 27 条比例 cue 改为 31 条停顿 cue。

**Reasoning log:** ASR 不可用时，比例分配只能保证总时长，不保证句子落在真实发声段；停顿边界至少能让字幕切换贴近口播节奏。

**Outstanding:** 若后续提供 ASR 凭证，还可以升级为词级时间戳字幕。

## Session 3 — 2026-06-21

**Strategy:** 按 `$F1` 完整执行路径重新处理 `男声2.mp3`，使用 `projects/测试/素材/视频` 目录下 3 个视频作为混剪素材池，参考 `projects/测试/示例` 的快节奏口播样式，输出新的 canonical final。

**Decisions:** 旧 final 已备份为 `projects/测试/结果/直接他妈大结局了_final_backup_20260621_000644.mp4`。当前环境无火山或 OpenAI ASR 凭证，但 `websocket-client` 依赖已可用，因此 ASR 降级原因为凭证缺失；字幕使用 `silencedetect` 停顿边界加语义分块投影生成，输出 31 条 cue，最大 cue 3.922 秒。视频采用 12 段混剪拼接，统一 1280x720/30fps；素材足够，未使用黑屏补位。

**Validation:** final `projects/测试/结果/直接他妈大结局了_final.mp4` 时长 55.100998 秒，旁白 55.101769 秒，差值 0.000771 秒；完整解码通过；ffprobe 显示 H.264 视频轨和 AAC 音频轨；抽帧首/中/尾可读。

**Artifacts:** PRP 为 `PRPs/F1-自动剪辑-测试项目-男声2-20260621.md`；执行报告为 `reports/F1-自动剪辑-测试项目-男声2-20260621.md`；渲染计划为 `edl.json`；字幕时间轴为 `subtitle_timing_male2_silence_aligned.json`。

**Outstanding:** 若后续提供 ASR 凭证，可用同一文案和 `男声2.mp3` 生成词级 SRT，再按现有 EDL 复渲染。

## Session 4 — 2026-06-21

**Strategy:** 用户反馈 Session 3 字幕与音频仍不够对齐后，进入 `$F1` 的 `repair_sync` 路径，只重建字幕时间轴并复渲染 final，视频 EDL 不变。

**Root cause:** Session 3 虽然不再使用全片比例字幕，但仍把 31 个旧语义 cue 按文字长度连续投影到 24 个真实发声区间上，导致后半段字幕逐步漂移。这个方法不如“每个真实发声区间绑定一个语义字幕”稳定。

**Decisions:** 当前仍无 ASR 凭证，因此继续使用 `silencedetect`，但改为 interval-bound fallback：24 个真实发声区间对应 24 个语义块；第 2 个发声区间超过 4 秒，内部拆成 2 条字幕。最终 `master.srt` 为 25 条 cue，最大 cue 3.733 秒。

**Validation:** 新 final `projects/测试/结果/直接他妈大结局了_final.mp4` 已复渲染；时长 55.100998 秒，旁白 55.101769 秒，差值 0.000771 秒；完整解码通过；SRT 无重叠；关键帧位于 `verify_sync_repair/`。

**Artifacts:** 旧字幕备份为 `master_before_sync_repair_20260621_001356.srt`；可靠旧 final 备份为 `projects/测试/结果/直接他妈大结局了_final_backup_20260621_000644.mp4`；新时间轴证据为 `subtitle_timing_male2_speech_interval_repair.json`。为避免中文输出路径异常，本轮先渲染到 `final_sync_repair_tmp.mp4`，再复制回 canonical final 路径。

## Session 4 — 2026-06-21

**Strategy:** 补足 `projects/测试/素材/视频` 中缺少的工具层展示素材，直接从 `projects/测试/示例` 截取软件界面、提示词/分镜、角色场景生成、剪辑时间线、导入剪映和资产证明画面。

**Decisions:** 新增 10 条 `tool-layer-*.mp4` 独立素材；全部统一为 1280x720、30fps、H.264/AAC。未覆盖 `projects/测试/示例` 原文件，未覆盖既有素材。

**Validation:** 所有新增素材通过 ffprobe 参数检查和完整解码检查；抽帧总览位于 `projects/测试/结果/auto-edit/edit/tool_material_selection/verify/tool_layer_new_assets_sheet.jpg`。

**Artifacts:** 素材清单为 `projects/测试/结果/auto-edit/edit/tool_material_selection/material_manifest.md`；执行报告为 `reports/素材整理-20260621.md`。

## Session 5 — 2026-06-21

**Strategy:** 将 `projects/测试/素材/视频` 的素材池升级为可被 F1 快速读取的结构化素材库：重命名所有视频，新增 `视频说明.yaml`，并同步 F1 源层读取规则。

**Decisions:** 视频文件统一改为 `content-*` 和 `tool-*` 两类语义化命名；`视频说明.yaml` 记录每条素材的类别、用途、时长、视觉摘要、适用/避用场景、字幕风险和 F1 选材建议。F1 `SKILL.md` 增加 `Video Description Manifest Contract`，将该索引接入 N1/N5/N7 与报告证据。

**Validation:** `视频说明.yaml` 解析通过且 13 条条目均对应真实文件；`test-prompts.json` 解析通过；13 条视频均可被 ffprobe 读取；旧视频名只保留在 YAML 的 rename 历史映射里。

**Artifacts:** 素材说明为 `projects/测试/素材/视频/视频说明.yaml`；执行报告为 `reports/视频说明索引-20260621.md`。

## Session 6 — 2026-06-21

**Strategy:** 用户反馈 YAML 字段结构需要更细致地服务选取和拼接后，将 `视频说明.yaml` 从视频级摘要升级为 v2 片段级素材索引。

**Decisions:** 每条视频补齐 `media`、`content_profile`、`selection_profile`、`splicing_profile`、`subtitle_safe_zone` 和 `segments[]`。`segments[]` 记录 `segment_id`、起止时间、时长、画面内容、语义标签、镜头类型、运动强度、动作强度、既有文字、适用/避用场景和拼接说明。F1 合同同步要求 EDL/报告记录 `video_id/file/segment_id/source_start/source_end/selection_reason/subtitle_risk`。

**Validation:** `视频说明.yaml` v2 解析通过；13 条视频共 41 个片段；每条视频的片段时长加总与媒体时长一致；F1 `test-prompts.json` 解析通过。

**Artifacts:** 升级后的素材说明仍为 `projects/测试/素材/视频/视频说明.yaml`；源层同步见 `.agents/skills/workflow/F1/SKILL.md`、`.agents/skills/workflow/F1/CHANGELOG.md` 和 `.agents/skills/workflow/F1/test-prompts.json`。

## Session 7 — 2026-06-21

**Strategy:** 按 `$F1` 完整执行 `男声1.mp3` 自动剪辑，参考 `projects/测试/示例` 的口播节奏，但不复用示例画面；基于 `projects/测试/素材/视频/视频说明.yaml` 的片段级索引，把内容画面与工具使用画面混剪成完整成片。

**Decisions:** 输出使用新文件名 `projects/测试/结果/直接他妈大结局了_男声1_final.mp4`，避免覆盖既有 `直接他妈大结局了_final.mp4`。当前环境没有火山或 OpenAI ASR 凭证，因此采用 `silencedetect=n=-35dB:d=0.08` 提取真实发声区间；31 个发声区间绑定 31 条语义字幕，不使用全片总时长比例摊分。EDL 共 18 段，工具展示 28.800 秒，内容画面 20.346 秒，工具层展示占主导。

**Validation:** final 时长 49.166667 秒，旁白 49.145850 秒，差值 0.020817 秒；ffprobe 显示 H.264 1280x720/30fps 视频轨和 AAC 音频轨；完整解码通过；SRT 31 条 cue 无重叠，最大 cue 2.783 秒；`dialogue_alignment_male1.json` 覆盖所有 cue；关键帧抽检显示字幕可读。

**Artifacts:** 成片为 `projects/测试/结果/直接他妈大结局了_男声1_final.mp4`；EDL 为 `projects/测试/结果/auto-edit/edit/edl_male1.json`；字幕为 `projects/测试/结果/auto-edit/edit/master_male1.srt`；执行报告为 `reports/F1-自动剪辑-测试项目-男声1-20260621.md`。

**Outstanding:** 若后续提供 ASR 凭证，可在不改动 EDL 的情况下升级为词级字幕时间轴后复渲染。
