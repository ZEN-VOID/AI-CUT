# Context: wjs-reframing-video

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2682
current_lines: 51
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-reframing-video` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

| symptom | root_cause_layer | immediate_fix | systemic_prevention | verification |
| --- | --- | --- | --- | --- |
| 用户说“横转竖/竖转横”，执行成物理旋转或加黑边 | scope math | 改回裁剪窄带并交换宽高比例，不做旋转、不 letterbox | 先根据源尺寸计算 inverted aspect crop window | 输出比例为 16:9↔9:16、4:3↔3:4 等反转关系 |
| 源视频已经是目标比例仍继续处理 | target decision | 报告无需 reframing，除非用户明确要求其他输出尺寸 | Step 1 先 probe 宽高和目标方向 | 没有生成无意义二次裁剪产物 |
| MediaPipe 检出 0 张脸，中心裁剪到背景空区 | detection fallback | 读取 crop log，改用 deterministic fixed crop 并抽帧确认 | 把 `0 face track(s)` / 100% fallback 视为人工裁剪门禁 | 抽帧中目标说话人居中，不再信任中心默认结果 |
| 多人 Q&A 需要每个人独立画面，本技能却只输出一条 crop track | route mismatch | 改路由到 `wjs-editing-multicam` 或先手工分段 | 在接单时确认是否需要 per-speaker split renders | 输出不是单一跟踪窗口硬扛多人需求 |
| 打哈欠、笑、吃东西等嘴部动作被误判为说话 | active-speaker noise | 检查 sidecar speaker timeline，必要时调高 `--mar-var-threshold` 或改 fixed crop | 高风险素材先抽样确认 MAR variance 是否可信 | 错误切换减少，`chunks` 与实际说话轮次一致 |
| 侧脸、低头或远景导致 MAR flatline，只剩 largest fallback | landmark limitation | 考虑 `--face-pick largest`、固定裁剪或先换素材/镜头 | 预检脸部大小和角度，不把视觉 active-speaker 当万能 | sidecar 中 face_sample_count 与 track_count 足够支撑判断 |
| HLG 源直接转 SDR 或 SDR 误套 HLG tone-map 导致偏色 | color pipeline | 先确认色彩元数据；HLG 才套 zscale/tonemap，SDR 删除该段 | 固定把色彩检查放入 fallback 命令前 | 抽帧肤色正常，输出 metadata 为 bt709 时符合预期 |
| 源素材有烧录字幕/lower-third，横转竖后关键信息被裁掉 | source artifact | 先去除烧录元素或改用适合平台的 overlay 版本 | 接单时检查画面边缘是否承载文字信息 | 输出里人脸与必要文字不互相牺牲 |
| 生成后只看文件存在，不检查 sidecar 和抽帧 | verification gap | 同时检查 `<input>.crop.json`、日志摘要和代表帧 | 把 sidecar + 抽帧作为完成门禁 | crop 计划可解释，代表帧构图正确，音频可播放 |

## Repair Playbook

1. 先 probe 源视频尺寸、时长、fps 和色彩信息，确认是否真的需要方向重构。
2. 明确目标是交换宽高比例后的裁剪输出，不是旋转、黑边适配或 AI 扩图。
3. 对有人脸素材先跑 active-speaker 路径，并读取 crop log 与 sidecar；不要只看最终文件是否生成。
4. 若出现 0 face / fallback 100%，立刻切到固定裁剪或手工分段，不调 `mar-var-threshold` 浪费时间。
5. 对多人对谈、串话、远景、侧脸、字幕烧录等素材，先判断是否应改路由或做预处理。
6. 渲染后至少抽取一个代表帧检查构图，必要时再查音频是否按预期保留或重编码。
7. 对 HLG/HDR 素材单独处理色彩转换；SDR 素材不要误套 HLG tone-map。

## Reusable Heuristics

- 本技能的默认智能点是“视觉 active-speaker”，不是音频说话人识别；串话和遮挡天然不稳。
- 固定裁剪不是降级羞耻项；静态机位、一人主讲、脸检失败时，它往往比自动跟踪更可靠。
- `--motion cut` 是 talking-head 的默认审美；平滑 pan 容易让镜头像漂移，除非用户明确要这种效果。
- `<input>.crop.json` 是可审计真源：source_size、target_size、crop_window、chunks、face_sample_count、track_count 都应能解释输出。
- 平台限制要早看：视频号等平台码率限制会影响 `--bitrate`，否则画面正确也可能上传失败。

## Promotion Backlog

- [ ] 候选规则: 为 `0 face track(s)` / fallback 100% 增加自动失败提示，要求用户确认 fixed crop。
  - 证据计数: 0
  - 目标落点: `scripts/crop.py` 日志或 validator
  - 状态: pending
- [ ] 候选规则: 增加渲染后抽帧检查清单，覆盖构图、色彩、字幕边界和音频。
  - 证据计数: 0
  - 目标落点: README/脚本输出提示或独立 smoke check
  - 状态: pending

## Case Log

暂无案例。后续只追加可复用、可验证、可晋升的案例。
