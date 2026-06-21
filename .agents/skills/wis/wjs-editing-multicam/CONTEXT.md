# Context: wjs-editing-multicam

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2339
current_lines: 60
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-editing-multicam` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

- `missing_or_stale_sync_sidecar`
  - 症状：机位错位、开头覆盖异常，或修正 `.sync.json` 后重渲染仍不对。
  - 根因层：EDL 在 edit 阶段已经烘焙 `deltas[]`，不能只改 sidecar 后复用旧 EDL。
  - 立即修复：先用 `wjs-syncing-multicam` 补齐或修正 sidecar，再重新运行 `polysync edit`。
  - 系统预防：把“sidecar 存在且新于 EDL”列为渲染前检查。
  - 验证点：EDL 的 `deltas` 和 coverage 与 sidecar 对齐。
- `raw_camera_preflight_missed`
  - 症状：画面灰、人物横躺、竖屏素材被塞进横屏黑边。
  - 根因层：渲染前未检查 Log、旋转标记和交付方向。
  - 立即修复：检查 XML 或 `ffprobe` 色彩信息，抽帧目检方向，按需加 `--log slog3`、`--rotate`、`--width/--height --fill`。
  - 系统预防：所有原始相机素材渲染前先做 2 分钟 preflight。
  - 验证点：预览帧肤色正常、方向正确、目标平台画幅无非预期黑边。
- `audio_energy_wrong_speaker`
  - 症状：镜头长期切到错误说话人，wide/room mic 被选中，或节奏缺少反应镜头。
  - 根因层：纯 loudest-mic 规则受串音、房间声和基线差异影响。
  - 立即修复：手工审 EDL，按基线归一化判断说话人；`--duck-audio` 时用 `--audio-cams` 排除 wide/room cam；必要时插入 listener/wide cutaway。
  - 系统预防：重要访谈先跑短样片调 `--mode`、`--min-dwell` 和音频源，再跑全片。
  - 验证点：30 秒试听里主音轨清晰，镜头跟随真实说话人与反应节奏。
- `deep_window_render_slow`
  - 症状：只渲染长素材中段小窗口，却长时间从 4K 源头解码。
  - 根因层：`polysync render-cuts` 的 filter graph trim 没有输入级 seek。
  - 立即修复：先按同一个 reference window 预切每个机位，旋转、调色、缩放后再用 0-based EDL 渲染。
  - 系统预防：分段输出不要把绝对时间 EDL 直接喂给长 4K 原片。
  - 验证点：预切片覆盖同一 reference window，渲染耗时与窗口长度近似相关。

## Repair Playbook

1. 先读取同目录 `SKILL.md`，确认任务是多机位合成，且每个原始相机文件旁有 `.sync.json`。
2. 缺 sidecar 时先路由到 `wjs-syncing-multicam`；sidecar 变更后必须重建 EDL。
3. 渲染前固定做 raw footage preflight：色彩 Log、旋转、交付画幅、camera start stagger。
4. 先跑 2 分钟样片验证 pacing、PiP、音频源和说话人跟随，再跑全片。
5. 若用户需要字幕、片头、转场、品牌包装或 face-driven framing，先输出本技能 MP4，再转交 overlay/hyperframes 等后续技能。
6. 对长素材中段交付，先预切各机位窗口，避免从源头解码造成无谓耗时。

## Reusable Heuristics

- 本技能只做 audio-energy-driven hard cuts/PiP；不要承诺脸部识别、淡入淡出、字幕或品牌动画。
- `audio_source` 是代理判断，不是听感保证；正式长片前至少试听 30 秒。
- Wide cam 的麦克风常有房间声和相近电平，适合画面 cutaway，不适合参与 speaker-gated 主音频选择。
- 竖屏平台优先把交付画幅设为 1080x1920 并 crop-to-fill；横屏默认不适合小红书/Reels/Shorts。
- `rotation` 更稳、更像自然剪辑；`greedy` 更贴近能量但可能更跳，需结合用户对节奏的偏好确认。
- `polysync` 是执行入口；本技能不应恢复旧的本地脚本真源。

## Promotion Backlog

- 增加 preflight checklist 脚本：读取 sidecar、XML/ffprobe 色彩、旋转标记和目标画幅建议。
- 为长素材窗口渲染沉淀“预切 -> 0-based EDL -> render”辅助流程。
- 向 `polysync` 上游反馈基线归一化 speaker attribution 与 listener/wide cutaway 策略。
- 增加 EDL freshness 检查，提示 sidecar 新于 EDL 时必须重新 edit。

## Case Log

暂无案例。后续只追加可复用、可验证、可晋升的案例。
