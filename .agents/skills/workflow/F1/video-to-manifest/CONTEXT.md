# Context: video-to-manifest

本文件是 `video-to-manifest` 的经验层知识库，用于沉淀从视频生成 F1 `视频说明.yaml` 时的可复用失败模式、修复打法和判断启发式。它不重定义 `SKILL.md` 的主合同。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-manifest-generation-heuristics-focused
last_checked_at: 2026-06-22
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 只有视频级摘要，F1 仍无法选段 | 片段粒度层 | 回到 LLM 逐段观察，补 `segments[]`、`segment_id/start/end/semantic_tags/best_for/splice_notes` | `视频说明.yaml` 完成门必须要求每个视频至少 1 个可截取片段 | validator 报告无 `missing_segments` fatal error |
| 工具录屏只写“AI 工具界面” | screen-state 证据层 | 补 `tool_state` 或在 `visual_content` 中写清可见按钮、输入框、生成状态、导入导出结果 | 工具段不能只按工具名命中；F1 需要 screen state 对齐字幕 cue | F1 visual plan 能引用 `segment_id` 和 `screen_state/match_evidence` |
| 操作展示只写“操作过程” | operation-state 证据层 | 补 `operation_state`、`action_phase`、`step_label` 或前后状态说明 | `操作展示/` 目录标准化为 `operation_demo`，不能被塞进 `tool_display` 或普通 B-roll | F1 visual plan 能引用 `segment_id` 和 `operation_state/selection_reason` |
| 脚本 skeleton 被误当 final manifest | 作者性边界层 | 标记 skeleton 为 `needs_llm_semantic_completion`，由 LLM 重写语义字段后再校验 | 脚本只写媒体参数、样张路径和空字段，不写最终语义判断 | final YAML 中有 LLM observation summary 或 evidence 引用 |
| 字幕遮挡风险低估 | safe-zone 判断层 | 增加高风险抽帧，补 `existing_text_positions`、`recommended_f1_position` 和 notes | UI/白底/字幕密集/强光画面默认更保守 | `subtitle_safe_zone.risk_level=high` 的片段在 F1 N7 被抽帧复核 |
| 目录更新破坏旧 EDL 引用 | 稳定 ID 层 | 备份旧 manifest，保留仍存在视频和片段的 `id/segment_id` | 更新路径必须先 merge 后写回，不允许重排 ID 当成无害格式化 | merge log 显示 retained_ids 和 new_ids |
| 样例标签被复制到新视频 | 样例误用层 | 回到抽帧证据，删除无证据标签，改写为当前视频可见事实 | 样例 manifest 只作为字段 schema，不作为内容来源 | observation summary 能回指当前视频帧 |
| validator 无法启动导致完成门失效 | 工具链 smoke 层 | 先对 `inspect_video_material.py` 和 `validate_video_manifest.py` 做 `py_compile` 或 `--help` 检查，修复语法/缩进错误后再进入写回路线 | 目录更新前增加最小 smoke 检查；脚本变更同步 `CHANGELOG.md` 与 `test-prompts.json` | `py_compile` 通过，validator 能输出 `fatal_count`/`warning_count` |

## Repair Playbook

1. F1 报告 `FAIL-VIDEO-MANIFEST` 时，先运行或查看 `validate_video_manifest.py` 的 fatal errors，再判断是字段缺失、路径错误、时长冲突还是 segment 粒度不足。
2. 若只有 video-level 摘要，优先补 2-6 个片段级候选；长视频按情绪/画面状态切分，不按固定等分直接定稿。
3. 若 `操作展示/` 目录下的视频没有映射为 `operation_demo`，先判断是否是目录-内容冲突；无冲突时修正 category，并补 `operation_state`。
4. 若工具段与字幕不匹配，补 `tool_state`：界面状态、操作阶段、可见按钮/参数/结果，并绑定对应 `evidence_frames`。
5. 若字幕安全区不确定，宁可把 `risk_level` 调高并写明抽帧复核需求，不要为了通过校验写低风险。
6. 更新已有 manifest 时，先保留旧 `id/segment_id`，只给新增视频和新增片段分配新 ID。
7. 无法抽帧或视频不可读时，只输出阻断报告或 skeleton，不输出 pass manifest。
8. 若 validator 在写回前无法启动，先停在源层 smoke 修复，不要改用人工目测替代完成门禁。

## Reusable Heuristics

- `视频说明.yaml` 的价值在片段级索引；`videos[].content_profile.visual_summary` 只是快速归类，不足以支撑 F1 EDL。
- 工具类素材的核心不是“这是某工具”，而是“此刻界面处于什么状态，能否对应字幕正在说的操作”。
- 操作展示素材的核心不是“这是一个工具画面”，而是“动作进行到哪一步，能否对应字幕说的步骤或前后对比”。
- AIGC 剧情素材的 `best_for` 应围绕 F1 文案可匹配的语义功能写：开场、铺垫、冲突升级、爆点、转折、尾钩、收束。
- `text_overlay_density`、`existing_text_positions` 和 `subtitle_safe_zone.notes` 要比普通素材描述更保守，因为 F1 最终会烧字幕。
- 均匀抽帧适合建立观察入口，不适合直接决定最终 segment 边界；最终片段应由 LLM 结合画面状态变化裁决。
- `renames[]` 是事实记录，不是执行改名指令；真正改名必须由用户显式要求并同步全仓引用。

## Promotion Backlog

- 为 `validate_video_manifest.py` 增加 JSON Schema 输出，方便 F1 N1 机械读取。
- 增加 contact sheet 生成，减少长目录逐帧查看成本。
- 增加真实小 fixture，覆盖单视频 skeleton、目录更新和 manifest repair。
