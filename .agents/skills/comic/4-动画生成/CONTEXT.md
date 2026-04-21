# Context: 动画生成

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 3042
current_lines: 47
current_cases: 0
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-17T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

本文件沉淀“九刀流组级 JSON + 漫画页图片 -> man-tui sora 图生视频”的执行经验。

## Type Map

| type_id | 症状 | 根因层 | 立即修复 | 系统预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-CA-01` | 4 号阶段能读到 2 号 JSON，但每页 video prompt 没有固定前缀 | prompt 合同层 | 把固定前缀固化到编译器和 validator，禁止手写漂移 | 4 号 schema + validator 双重检查 prompt prefix | 每页 `video_prompt` 都以前缀原文开头 |
| `TM-CA-02` | 动画结果像单镜头动态海报，不像多分镜 | panel->shot 编译层 | 按 `panels[]` 逐格展开 `shot_plan[]`，默认一个格子一个分镜 | 4 号脚本把 `panel_count` 和 `shot_count` 绑定校验 | 每页 `shot_plan` 数量与 `panels` 一致 |
| `TM-CA-03` | 页级 prompt 正确，但 4 号阶段找不到对应首帧图 | 3/4 handoff 层 | 先按 `page01..page09`，再按 `group_slug-page01..09` 搜索，不靠内容猜图 | 3 号稳定输出短命名，4 号按页码解析 | dry-run 报告中 9 页都有 `source_image` |
| `TM-CA-04` | 画面动起来后角色、场景或文字变形严重 | prompt 保真层 | 在每页 `video_prompt` 显式写“preserve exact composition / text / page number / style / character identity” | 4 号模板和编译器固定加入保真约束 | 页级 prompt 中能读到 preserve 语义 |
| `TM-CA-05` | 视频参数被调用者改成横版或短时长 | 执行参数层 | 固定默认 `10s + 720x1280`，除非用户显式覆盖 | 4 号脚本与输出 JSON 同步写默认参数 | plan/report 中参数稳定为 10 秒、720x1280 |
| `TM-CA-06` | Sora 子命令失败后只看到终端报错，没有组级回溯报告 | 可观测性层 | 先写 pending report，再逐页汇总成功/失败页及其 report 路径 | 4 号执行脚本固定先落组级计划与 pending report | 执行刚开始就能看到 `animation_generation_report.json` |
| `TM-CA-07` | 4 号脚本拿到了本地 `page01..page09`，但真实 execute 直接被 provider 拒绝 | provider 输入合同层 | 识别 `man-tui/video/sora` 只接受公网 `input_reference_url`，把执行前校验前置到 4 号脚本 | 4 号合同和 plan 文件显式声明 `public_url_required`；无 URL 时只允许 dry-run | execute 前能明确指出缺哪几页的公网 URL |
| `TM-CA-08` | 2 号 JSON 的题材味道到 4 号突然消失，video prompt 只剩技术保真句 | type-pack 编译层 | 把 `type_stack_ref / type_pack_context.stage_projection.animation_generation` 注入逐页 `video_prompt` | 4 号 schema、validator 和编译器同步要求 pack context 存在 | 编译后的 animation JSON 能回指 active packs 和 animation_generation 投影 |
| `TM-CA-09` | 4 号阶段明明能读到 group JSON，却在 3 号阶段目录里找不到 `page01..page09` | 3/4 handoff 命名层 | 同时回退识别 `episode-prefixed group slug`、原始 `group_id` 和 `page-group-xx` 目录/文件前缀 | 4 号脚本统一维护 group alias 列表，避免把输出 slug 当成唯一查找键 | dry-run 在 `page-group-01/` 这类目录结构下也能稳定命中 9 页图片 |

## Repair Playbook

1. 先判定是 2 号结构问题、3 号页图问题，还是 4 号 prompt/执行问题。
2. 若每页 prompt 没有固定前缀，先修 4 号编译器和 validator，不要手工补单页。
3. 若 prompt 有前缀但没有多分镜节奏，优先检查 `panels[]` 是否被编译成 `shot_plan[]`。
4. 若找不到图片，优先检查 3 号输出命名和 group 目录，不要让 4 号重新猜测剧情。
5. 若创建、轮询或下载失败，直接沿 `man-tui-sora-video` 技能的 Root-Cause 链回溯。
6. 若视频化后“题材味道断掉”，先检查 `type_pack_context.stage_projection.animation_generation` 是否被注入 prompt。

## Reusable Heuristics

- 4 号阶段的业务真相不是“再写一版剧情”，而是“把 2 号页级漫画信息翻译成可执行的 Sora 视频 prompt”。
- 最稳的页级视频 prompt 结构是：固定前缀 -> 当前页职责 -> 保留原页构图与风格 -> continuity locks -> shot plan -> 禁止项。
- 多分镜动画能否成立，取决于 `panels[]` 是否还保留清晰的镜头和动作粒度；如果 2 号已经把页面压成单幅插画描述，4 号很难救回来。
- 对首帧图生视频，最贵的信息不是“画得漂亮”，而是“页码、中文文字、角色和场景锚点都不漂”。
- 4 号的默认成功路径应该是：从 2 号读 prompt，从 3 号读页图，从 `man-tui/video/sora` 读运行状态；任何一个源漂移都应回源修，而不是在 4 号阶段硬补第二真源。
- 对 `man-tui/video/sora`，本地页图只适合作为业务真源，不足以直接提交 provider；执行前还需要公网 `input_reference_url` 映射。
- 3 号阶段的实际 group 目录可能保留原始 `group_id`，而 4 号阶段的输出 slug 可能额外拼上集号；找图时必须把它们当成 alias，而不是假设两边命名完全相同。
