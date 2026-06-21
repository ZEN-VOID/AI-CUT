# Context: wjs-overlaying-video

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2923
current_lines: 47
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-overlaying-video` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
|---|---|---|---|---|
| 把剪辑/裁切任务误路由到后期叠加 | 技能边界 | 转交 `/wjs-segmenting-video` 或 `/wjs-reframing-video`，本技能只做叠加与最终合成 | 先判断输入是否已有固定视频和 SRT | 输入是可直接合成的 clip + 可选 SRT/封面素材 |
| 多次解码/重编码导致画质下降和耗时 | 管线架构 | 收敛到一个 HyperFrames composition，一次最终 encode | 不拆成封面、字幕、动画、CTA 多次级联压制 | 输出只经历一次最终渲染 |
| HLG/HDR 源发白、发黑或渲染卡住 | 色彩管理 | 仅对 HLG/PQ 源先 tone-map 到 Rec.709 SDR，并写入 dense keyframes | 先 probe `color_transfer`，不要凭感觉套 tone-map | 渲染日志显示 SDR，画面肤色和对比正常 |
| 已是 SDR 的素材被错误 tone-map | 色彩管理 | 停止套 HLG recipe，改直转 h264 + dense keyframes | `_is_hlg_hdr` 为唯一入口判断 | 画面不被洗淡或压暗 |
| HyperFrames seek 冻在旧帧 | 编码结构 | 用 `-g 30 -keyint_min 30` 重新编码 body clip | 所有进入 HyperFrames 的视频都做 dense-keyframe 检查 | render log 无 sparse keyframes 警告 |
| 封面比例或参考帧方向不匹配 | 封面生成 | 按输出方向重抽参考帧并用 native aspect 生成封面 | vertical 用 `1024x1792`，horizontal 用 `1536x1024` | Frame 0 全屏、无黑边、无异常裁切 |
| 平台缩略图黑帧 | 封面场景 | cover 第一帧静态显示，不做从 0 opacity fade-in | 导出前强制抽 frame 0 检查 | `ffmpeg -ss 0 -vframes 1` 不是黑帧 |
| 字幕与音频错位 | 时间轴映射 | SRT cue start/end 加 cover duration 后再内联 | 明确区分 body-relative 与 composition timeline | 随机抽查几处口型/声音/字幕同步 |
| 字幕位置跳动或居中失效 | CSS/GSAP 合成 | 固定字幕容器高度，用 `gsap.set(xPercent/yPercent)` 居中 | 避免 CSS transform 被 GSAP tween 覆盖 | 1 行和 2 行字幕视觉中线一致 |
| 同时烧录 libass 与 HTML/CSS 字幕 | 上游交接 | 选择一种字幕系统；本技能默认 HTML/CSS captions | 从 handoff 获取 raw clip，不叠加 burn-in 字幕 | 输出无双层字幕 |
| CTA 或版本追踪错误 | 输出合同 | CTA 固定“王建硕”，END/CTA 场景显示技能名+版本号 | 每次管线变化同步 bump version stamp | 末尾 CTA 和版本戳可见且内容正确 |

## Repair Playbook

1. 先判路由：确认任务是给固定 clip 加封面/字幕/动画/CTA；剪辑、裁切、转录和上传分别交给对应技能。
2. 查 handoff：确认有 clip、segments、SRT；若走 post-segmentation preset，优先用 raw clip + SRT，避免双字幕。
3. 查色彩和 keyframe：probe HDR/SDR；HLG/PQ 才 tone-map，所有 body clip 都确保 dense keyframes。
4. 查封面：按输出比例和方向生成或替换 cover，baked-title cover 不再叠 animated hook。
5. 查字幕：使用用户批准的关键词高亮风格；SRT 时间加 cover offset；长 cue 先缩字号或回到上游切分。
6. 查叠加：每段只选支撑讲话的 1-2 个 stack/hammer/自定义 overlay，避免装饰性堆叠。
7. 查输出门禁：lint、validate、inspect、抽 frame 0、抽查字幕同步、确认 CTA 和版本戳后再交付。

## Reusable Heuristics

- 本技能的核心价值是“所有后期元素进一个 HyperFrames 项目，一次最终 encode”；任何多段级联压制都应先被质疑。
- cover 是输出视频的第一帧，不是另传缩略图；第一帧必须静态、清晰、非黑。
- vertical 默认封面尺寸用 `1024x1792`；从横屏双人源做竖屏封面时，先从竖裁 body clip 抽单人参考帧。
- make_cover 已把标题烙进封面时，不再加 animated hook，避免标题重复。
- 王建硕默认字幕风格是“关键词高亮 + Noto Serif SC”；只有真正有量级、倍数、百分比等关键词时才用金色块。
- 字幕时间线以 composition 为准，不以 body clip 自身 t=0 为准；cover duration 是最常见偏移源。
- `stack` 适合层级/列表/流程，`hammer` 适合一句最强观点；每个 overlay 都要绑定讲话中的 hook moment。
- CTA 署名固定“王建硕”；嘉宾名只能放在描述或元数据，不进 CTA 主位。

## Promotion Backlog

- 可新增一个 preflight 检查脚本：cover aspect、frame 0、HDR/SDR、dense keyframe、CTA 名称、版本戳。
- 可把字幕 cue 长度、cover offset 和双字幕检测纳入 build 阶段 validator。
- 若新的 overlay pattern 被 2+ 项目复用，再沉淀到 `references/illustration_patterns.md`，不要在本文件写成第二模板真源。
