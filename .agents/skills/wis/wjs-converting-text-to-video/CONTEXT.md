# Context: wjs-converting-text-to-video

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 3443
current_lines: 51
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-converting-text-to-video` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 用户只有想法、没有 `article.md` | 路由边界层 | 先转到写作/公众号发布流程产出 `article.md` | 入口判断先确认文章文件存在；不要把想法直接塞进视频流水线 | 目标目录内存在可读取的 `article.md` |
| 视频像文章朗读或 slideshow | scene design 层 | 回到 Step 1，按论证结构重拆 5-10 个视觉时刻 | 设计阶段先过 Scene Mix Rule，再写 HTML | scene 设计满足 A/D/C/E、至少 4 类模板、时长和字号有跨度 |
| B1 双行划线、居中版式被滥用 | 反单调门禁层 | 限制 B1 最多 2 个，补非居中、留白、几何和 color-flip scene | 把缩略图并排自检作为视觉设计必检项 | 8 个缩略图不会一眼看成同一种排版 |
| 第一帧黑屏或看不到水彩背景 | first-frame / GSAP 层 | 保持 `bg-image` 默认可见，s1 主标题默认可见，A3 color-flip 放到 s2+ | HTML 模板中禁止对背景做 fade-in，s1 只动 y/scale | t=0 snapshot 可见背景和标题 |
| 背景渲染成纯黑 | asset path 层 | 重新生成 `video/bg.png`，HTML 用 `url('bg.png')` | 不使用 `../illustration.png` 或跨目录相对路径作背景 | snapshot/render 中水彩背景可见且不是均匀黑底 |
| 中文 TTS 静默失败或发音不可接受 | Volcano TTS 参数/声音层 | 去掉 `emotion` / `emotion_scale`，改用推荐 `zh_*_bigtts` 声音；中文不用 kokoro | TTS helper 保持 Volcano 默认阿虎对话男声，并记录备用声音清单 | `narration.mp3` 与 `timing.json` 正常生成，抽听无循环 hallucinate |
| 改了旁白但音频没变 | TTS cache 层 | 删除 `narration/`、`narration.mp3`、`timing.json` 后重跑 | 修改 chunk 文案时同步提醒缓存失效条件 | 新旧 `timing.json` 时长随文案变化 |
| 旁白被下一个 scene 截断 | timing alignment 层 | scene end 覆盖 narration end 并加约 0.3s 缓冲 | 以 `timing.json` 为 scene 时间真源，不手写猜时长 | 每个 scene 覆盖对应 chunk 的 start/end |
| 文本溢出或竖屏排版挤压 | layout inspect 层 | 缩字号、分行、减少 nowrap，必要时给 `.em` 加 `line-height: 1` | `npx hyperframes inspect` 必须 0 errors 才 render | inspect 通过，关键 snapshot 无裁切 |
| 音效或旁白 silent | HyperFrames audio contract 层 | 给每个 `<audio>` 加唯一 `id`，同 track 避免时间重叠 | 音频节点生成时把 `id`、`data-start`、`data-duration`、`track-index` 作为必填 | render 后可听到 narration；SFX 不互相覆盖 |
| 自动上传误触发或配额耗尽 | 发布边界层 | 渲染流程只产出 MP4，不主动跑 YouTube 上传 | 保持上传交给 cron 或用户显式手动触发 | 最终交付只报告 `<article-folder>/<slug>.mp4` 路径 |

## Repair Playbook

1. 先确认输入：目标目录必须有 `article.md`；没有文章稿时不启动视频流程。
2. 读文章后先做视觉重构，不做逐段朗读：拆成 5-10 个 scene，每个 scene 是一个对比、数字、排比、比喻或金句落点。
3. 写完 scene 设计后先过 Scene Mix Rule：模板类别、B1 次数、color-flip、非居中、留白、几何、字号跨度和节奏跨度都要满足。
4. 写 `narration_chunks.json` 时保持口语、短句和纯文字；删除 markdown、括号注释、`...`、破折号，并剥离 `SKILL.md` 明确禁止进入视频的百姓网过时事实。
5. 生成或重生成 TTS 前检查缓存；文案改过就清掉旧 `narration/`、`narration.mp3`、`timing.json`。
6. 背景必须生成到 `video/bg.png`；普通 scene 让水彩背景透出，只有 A3 color-flip 写纯色背景。
7. 写 `index.html` 时以 `timing.json` 设 scene 时间，s1 保证第一帧可见，每个音频节点必须有 `id`。
8. 先跑 lint，再跑 inspect，再看 snapshot，最后 render；inspect 有任何 overflow 都先修，不带错渲染。
9. 最终只交付与 `video/` 平行的 `<slug>.mp4`，不把 YouTube 上传混入渲染流程。

## Reusable Heuristics

- 本技能的核心判断是“视觉重构”，不是“把文章可视化朗读”；每屏只承载一个视觉时刻。
- 反单调应在 scene 设计阶段解决；等 HTML 写完再补变化，通常只会变成装饰堆叠。
- 竖屏 1080 宽对中文大字很敏感；hero 字号越大，越要提前决定分行和留白。
- s1 不做 color-flip，标题元素不要从 `opacity: 0` 入场；第一帧黑屏是硬失败。
- 水彩背景下灰色文字容易消失；层级优先用 `#f5efe5` 加 opacity、字号和字重处理。
- Volcano `_bigtts` 声音不要传 emotion 参数；中文默认不用 kokoro。
- SFX 是节奏标点，不是背景音乐；tick 用于转场，chime/bell 只在必要节点少量使用。
- 每次旁白文案改动都默认 TTS 缓存失效；不清缓存就不能信任旧时长。
- HyperFrames 渲染前的 lint/inspect 是完成门禁，不是优化建议。

## Promotion Backlog

- 增加 scene manifest validator：自动检查模板类别配比、B1 次数、scene 时长跨度、字号跨度和连续同类 scene。
- 增加 HTML preflight：扫描 `../illustration.png`、无 `id` 的 `<audio>`、s1 opacity fade-in、过多 scene-level background 和禁止的 TTS 参数。
- 增加 TTS cache guard：当 `narration_chunks.json` 内容变更而旧音频仍存在时，提示重生成。
- 固化一份 render checklist：lint 0 errors、inspect 0 errors、关键 snapshot 可见背景/标题/无裁切、最终 MP4 位于文章目录根层。
