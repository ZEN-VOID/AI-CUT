# Context: video-to-manifest

本文件是 `video-to-manifest` 的经验层知识库，用于沉淀从视频生成 workflow 共享 `视频说明.yaml` 时的可复用失败模式、修复打法和判断启发式。它不重定义 `SKILL.md` 的主合同。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-manifest-generation-heuristics-focused
last_checked_at: 2026-06-29
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 只有视频级摘要，下游仍无法选段 | 片段粒度层 | 回到 LLM 逐段观察，补 `segments[]`、`segment_id/start/end/semantic_tags/best_for/splice_notes` | `视频说明.yaml` 完成门必须要求每个视频至少 1 个可截取片段 | validator 报告无 `missing_segments` fatal error |
| 工具录屏只写“AI 工具界面” | screen-state 证据层 | 补 `tool_state` 或在 `visual_content` 中写清可见按钮、输入框、生成状态、导入导出结果 | 工具段不能只按工具名命中；下游需要 screen state 对齐字幕 cue 或 storyboard beat | workflow asset/storyboard 能引用 `segment_id` 和 `screen_state/match_evidence` |
| 操作展示只写“操作过程” | operation-state 证据层 | 补 `operation_state`、`action_phase`、`step_label` 或前后状态说明 | `操作展示/` 目录标准化为 `operation_demo`，不能被塞进 `tool_display` 或普通 B-roll | workflow asset/storyboard 能引用 `segment_id` 和 `operation_state/selection_reason` |
| 脚本 skeleton 被误当 final manifest | 作者性边界层 | 标记 skeleton 为 `needs_llm_semantic_completion`，由 LLM 重写语义字段后再校验 | 脚本只写媒体参数、样张路径和空字段，不写最终语义判断 | final YAML 中有 LLM observation summary 或 evidence 引用 |
| 字幕遮挡风险低估 | safe-zone 判断层 | 增加高风险抽帧，补 `existing_text_positions`、`recommended_f1_position` 和 notes | UI/白底/字幕密集/强光画面默认更保守；`recommended_f1_position` 是 legacy 字段名，workflow 可转译为 caption/overlay safe zone | `subtitle_safe_zone.risk_level=high` 的片段在下游验证门被抽帧或 preview 复核 |
| 目录更新破坏旧 EDL 引用 | 稳定 ID 层 | 备份旧 manifest，保留仍存在视频和片段的 `id/segment_id` | 更新路径必须先 merge 后写回，不允许重排 ID 当成无害格式化 | merge log 显示 retained_ids 和 new_ids |
| 样例标签被复制到新视频 | 样例误用层 | 回到抽帧证据，删除无证据标签，改写为当前视频可见事实 | 样例 manifest 只作为字段 schema，不作为内容来源 | observation summary 能回指当前视频帧 |
| validator 无法启动导致完成门失效 | 工具链 smoke 层 | 先对 `inspect_video_material.py` 和 `validate_video_manifest.py` 做 `py_compile` 或 `--help` 检查，修复语法/缩进错误后再进入写回路线 | 目录更新前增加最小 smoke 检查；脚本变更同步 `CHANGELOG.md` 与 `test-prompts.json` | `py_compile` 通过，validator 能输出 `fatal_count`/`warning_count` |
| 不同分类目录存在同名视频导致抽帧目录混入 | 证据路径命名层 | 对 `操作展示/工具使用/影像内容` 等分类目录分别取证到隔离 `work_dir`，再合并机械 evidence；最终语义只引用隔离后的帧路径 | 后续脚本修复应把相对目录或稳定 hash 纳入 frame dir，避免只用 `video.stem` 命名 | final manifest 的 `evidence.sample_frames` 指向分类隔离工作目录；validator 通过且报告记录 mitigation |
| “整体读取/逐视频精读”口径不清导致用户担心准确性 | 覆盖语义层 | 明确区分目录级抽样、逐视频关键帧精读、实时完整播放；若用户要求“逐视频精读”，为每条视频生成单独接触表并写回 `evidence.deep_review` | 最终回复和报告必须说明本轮是否为实时完整播放；不要把关键帧精读包装成逐帧/全时长观看 | manifest 中 `deep_reviewed_from_per_video_contact_sheet` 覆盖 100% 视频，报告写明 limitations |
| workflow 批量视频重复率高、平台判重限流 | 标签深度层 | 补 `semantic_vector`、`trigger_profile`、`visual_signature`、`variation_profile`、`reuse_profile`，让下游能按同义不同画面选材 | manifest 不只输出宽泛 `semantic_tags`；面向 workflow consumer 时 validator warning 提醒标签深度不足 | workflow `asset_evidence.json` 能引用深标签和重复风险，不再只按文件路径轮换 |
| 长视频素材总是被选中同一小段 | 长素材覆盖层 | 先生成 `analysis_slices[]`，每个 slice 默认 ≤60 秒，再由 LLM 对 slice/segment 逐段精读 | `inspect_video_material.py` 输出 analysis_slices；SKILL 完成门要求长视频不能只靠整条摘要 | `视频说明.yaml` 中长素材有 slice map，segment 可回指 `analysis_slice_id` |
| 用户要求“拆成短视频”但只得到 `analysis_slices[]` | 物理代理切片语义层 | 补生成 `work_dir/analysis_clips/` 物理代理短视频，并在 `analysis_slices[].proxy_clip` 回指 | 区分逻辑切片、抽帧证据和物理代理短视频；用户明确说“短视频/物理切片”时必须打开代理切片路径 | 代理 clip 数量等于 slice 数量，最长时长不超过 60 秒容差，validator 仍 pass |

## Repair Playbook

1. 下游报告 `FAIL-VIDEO-MANIFEST`、`FAIL-CONSUMER-COMPATIBILITY` 或素材证据不足时，先运行或查看 `validate_video_manifest.py` 的 fatal errors，再判断是字段缺失、路径错误、时长冲突还是 segment 粒度不足。
2. 若只有 video-level 摘要，优先补 2-6 个片段级候选；长视频按情绪/画面状态切分，不按固定等分直接定稿。
3. 若 `操作展示/` 目录下的视频没有映射为 `operation_demo`，先判断是否是目录-内容冲突；无冲突时修正 category，并补 `operation_state`。
4. 若工具段与字幕不匹配，补 `tool_state`：界面状态、操作阶段、可见按钮/参数/结果，并绑定对应 `evidence_frames`。
5. 若字幕安全区不确定，宁可把 `risk_level` 调高并写明抽帧复核需求，不要为了通过校验写低风险。
6. 更新已有 manifest 时，先保留旧 `id/segment_id`，只给新增视频和新增片段分配新 ID。
7. 无法抽帧或视频不可读时，只输出阻断报告或 skeleton，不输出 pass manifest。
8. 若 validator 在写回前无法启动，先停在源层 smoke 修复，不要改用人工目测替代完成门禁。
9. 若同一批素材在不同分类目录下存在同名视频，单次全目录取证前先检查 frame 目录是否只按 `video.stem` 落盘；若存在混入风险，改为按分类目录独立 `work_dir` 取证并合并 evidence，报告中记录这是 mitigation 而不是脚本语义裁决。
10. 若用户追问“是否全部读取”“会不会不准”或直接要求“逐视频精读”，不要只重复“已整体读取”；应升级为每条视频单独接触表复核，写回 `evidence.deep_review`、覆盖数、页码和精度限制。
11. 若下游反馈“同义文案成片重复”，不要只在 workflow 端随机换素材；先修 manifest 深标签，让每个 segment 具备触发条件、视觉签名、可替换关系和复用风险。
12. 超过 60 秒的素材不要只做整条摘要；先做 `analysis_slices[]`，再写 segments。整条摘要适合归类，不足以支撑批量去重。
13. 若用户说“拆成短视频”“切成短素材”或质疑“没有将长视频拆成短视频”，不要只解释 `analysis_slices[]`；应补 `analysis_clips/` 物理代理切片并回写 `proxy_clip`，同时说明原视频仍保持只读。

## Reusable Heuristics

- `视频说明.yaml` 的价值在片段级索引；`videos[].content_profile.visual_summary` 只是快速归类，不足以支撑 workflow EDL 或 asset/storyboard evidence。
- 工具类素材的核心不是“这是某工具”，而是“此刻界面处于什么状态，能否对应字幕正在说的操作”。
- 操作展示素材的核心不是“这是一个工具画面”，而是“动作进行到哪一步，能否对应字幕说的步骤或前后对比”。
- AIGC 剧情素材的 `best_for` 应围绕下游文案、旁白或 storyboard 可匹配的语义功能写：开场、铺垫、冲突升级、爆点、转折、尾钩、收束。
- `text_overlay_density`、`existing_text_positions` 和 `subtitle_safe_zone.notes` 要比普通素材描述更保守，因为下游通常会叠加字幕或图文层。
- 均匀抽帧适合建立观察入口，不适合直接决定最终 segment 边界；最终片段应由 LLM 结合画面状态变化裁决。
- “逐视频关键帧精读”是比目录级抽样更高的覆盖层级，但仍不同于实时完整播放；长视频的对白、细微动作和最终入剪点必须交给下游片段预览 gate 二次确认。
- `renames[]` 是事实记录，不是执行改名指令；真正改名必须由用户显式要求并同步全仓引用。
- 对 workflow 来说，`semantic_tags` 是入口，不是差异化答案；真正帮助避重的是 `visual_signature` 和 `variation_profile`，因为它们能告诉下游“同义但长得不同”的替代选项。
- `analysis_slices[]` 不应被理解成改动原素材，它是把长素材拆成可观察证据窗口，减少 LLM 用一个粗标签概括整条视频。
- `proxy_clip` 才表示已经产出可打开的物理代理短视频；没有 `proxy_clip` 时，只能称为逻辑切片或切片证据，不能对用户说“已拆成短视频”。

## Promotion Backlog

- 为 `validate_video_manifest.py` 增加 JSON Schema 输出，方便 workflow N3 机械读取。
- 增加 contact sheet 生成，减少长目录逐帧查看成本。
- 增加真实小 fixture，覆盖单视频 skeleton、目录更新和 manifest repair。
- 为 `validate_video_manifest.py` 增加更强的 consumer profile 模式，例如 `--consumer workflow-batch` 时把深标签 warning 升为 fatal。
