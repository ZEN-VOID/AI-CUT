# Context: 漫画生成

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 4165
current_lines: 60
current_cases: 0
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-17T07:55:00Z
```
<!-- CONTEXT_HEALTH_END -->

本文件沉淀“九刀流 JSON -> Seedream 一次 9 张漫画页”的执行经验。

## Type Map

| type_id | 症状 | 根因层 | 立即修复 | 系统预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-CG-01` | Seedream 非流式 9 图读超时 | 执行参数层 | 使用 `--stream`，必要时提高 timeout | 本技能默认流式 | 生成报告有 9 个 partial 成功事件 |
| `TM-CG-02` | 服务端生成了图但脚本提取 0 张 | SSE 解析层 | 解析 `image_generation.partial_succeeded` 顶层 URL | 继承 seedream 修复后的脚本 | `result_count=9` |
| `TM-CG-03` | 输出成一张九宫格 | prompt 编译层 | master prompt 首段强化 separate images / not collage | 2 号 JSON hard constraints 必填 | dry-run prompt 明确禁拼图 |
| `TM-CG-04` | 输出像九个同场景变体 | 上游 JSON 层 | 退回 2 号重切 `story_beat_map` | validator 检查页号与 page_role | 9 页 page_role 不重复 |
| `TM-CG-05` | 页面比例不稳定 | prompt 与 size 层 | 每页 prompt 强写 vertical 9:16；size 保持 2K | 2 号 schema 固定 layout.aspect_ratio | 文件视觉为竖版页 |
| `TM-CG-06` | 文字槽失败严重 | 上游提示词层 | 减少气泡文本，把解释转 caption | 2 号文字系统限制长度 | 气泡短句、旁白短框 |
| `TM-CG-07` | 生成计划或图片落到 `output/comic` | 项目根合同层 | 改用 `projects/comic/[项目名]/3-漫画生成/`，必要时传 `--project-name` | 脚本默认从 JSON 路径推断项目根 | `generation_plan.json` 位于项目 3 号目录 |
| `TM-CG-08` | `aigc` 项目的漫画生成计划被错误推到 `projects/comic/<json-stem>/3-漫画生成/` | 项目根推断层 | 对 `projects/aigc/[项目名]/5-Image/漫画/2-九刀流漫画提示词/` 显式回推到同级 `5-Image/漫画/3-漫画生成/` | 在执行脚本固化 `aigc` 路径推断，避免依赖人工传 `--output-dir` | dry-run 默认输出目录位于当前 `aigc` 项目内 |
| `TM-CG-09` | 最终页没有页码，或页码不在右下角/不是纯数字 | master prompt 编译层 | 从 2 号 JSON 读取 `pages[].page_number_overlay`，并在每页 block 和总约束里重复写入 `bottom-right` + `digits only` | 3 号编译器和 2 号 validator 同步要求页码覆盖层 | dry-run master prompt 能逐页读到 `page number "N" in the bottom-right corner, digits only` |
| `TM-CG-10` | 多人页或场景在 3 号执行后仍漂移 | 编译上下文稀释层 | 在 master prompt 顶层带上 `scene_continuity_bible`，并在每页 block 显式展开 `active_character_ids` 对应角色锁与 `scene_id` 对应场景锁 | 3 号编译器不再只传 page prompt 字符串，而是把角色/场景锁作为每页上下文一起注入 | dry-run master prompt 中每页都能看到 active character locks 与 scene continuity lock |
| `TM-CG-11` | 9 页长请求已经发出，但目录里长时间只有 `generation_plan.json` 和 master prompt，执行态不可见 | 执行可观测性层 | 在发起 Seedream 子进程前先写 `comic_generation_report.json` 的 `pending` 状态；失败时也回写失败报告 | 3 号脚本固定先落 in-flight 报告，避免把“还在跑”误判成“没启动” | 长请求刚启动时就能看到 `comic_generation_report.json`，且 `status=pending` |
| `TM-CG-12` | 最终图片名过长，直接继承上游 JSON stem，目录可读性差 | 落盘命名层 | 默认改成标准短页码文件名 `page01..page09`；只有用户显式传 prefix 时才保留自定义命名 | 3 号脚本把“最终交付命名”和“Seedream 临时保存前缀”分离，默认回写为规范页码名 | 输出目录默认看到 `page01.ext ... page09.ext` |
| `TM-CG-13` | 同一集多个 page-group 连续执行后，`generation_plan`、report 或图片互相覆盖 | group 目标解析层 | 从上游 JSON 读取 `page_group.group_id`，派生 `group_slug`；默认落到 `3-漫画生成/<group_slug>/`，只有多个 group 明确共用同一 `output_dir` 时才切换到 `group_slug-page01..page09` 命名 | 3 号思维节点新增 `Group Target Resolve`，脚本固定生成 group 级计划、master prompt、pending/completed report 与图片命名 | dry-run 或实跑时，组级产物位于独立 group 子目录或具备独立 group 前缀 |
| `TM-CG-14` | 4 号动画阶段能拿到 group JSON，却找不到对应页图 | 3/4 号 handoff 层 | 优先检查 3 号是否仍按 `page01..page09` 或 `group_slug-page01..page09` 落盘；不要让文件名继续继承冗长 JSON stem | 3 号默认短命名 + 4 号按页码解析 固化为跨阶段合同 | 4 号 dry-run 中 9 页都能定位到 source_image |
| `TM-CG-15` | `--self-test` 返回通过，但样例 JSON 实际过不了 2 号 validator，导致离线门禁给出假阳性 | 自检门禁层 | 自检先把样例落成临时 JSON，再真实跑 2 号 validator，最后才检查 master prompt 编译结果 | 3 号脚本的自检必须覆盖“样例 payload 合法 + 编译结果含关键约束”两层 | `--self-test` 通过时，样例 JSON 必须同时能被 2 号 validator 接受 |
| `TM-CG-16` | 2 号 JSON 带了类型包，但 3 号 master prompt 没编进去，导致生图只剩默认漫画感 | type-pack 编译层 | 在 master prompt 里显式加入 `Type Stack Ref / Type Pack Context` 块 | 3 号编译器把 pack context 与 style_bible 同级注入 | dry-run master prompt 能直接看到 active packs 与 image_generation 投影 |

## Repair Playbook

1. 先看 seedream 报告：`ok/result_count/stream_event_types/generated_images`。
2. 若请求层失败，回到 seedream 技能。
3. 若请求成功但画面语义不对，回到 2 号 JSON，而不是重写 3 号脚本。
4. 若 dry-run master prompt 没有“9 separate images / not collage / not variations”，先修编译器。
5. 若 JSON 不合格，不允许绕过 validator 直接生图。
6. 若 9 页长请求执行较久，先看 `comic_generation_report.json` 是否已是 `pending`；有 `pending` 说明子进程已发出，优先判断是否继续等待，而不是误判脚本未启动。
7. 若 episode 有多个 `page-group`，先确认当前输出是否落在 `<group_slug>/` 子目录，或显式共享目录下是否启用了 `group_slug-page01..` 命名，再继续批量执行。
8. 若脚本自检通过，但真实输入仍在 2 号门禁前失败，优先排查自检样例是否覆盖了当前 schema/validator，而不是先怀疑 Seedream。
9. 若风格像是“题材掉线”，先看 master prompt 里是否仍然有 `Type Stack Ref / Type Pack Context`。

## Reusable Heuristics

- 已验证 Seedream 的 9 图连续生成不是九宫格裁切；下游应该尊重单请求能力，而不是拆成 9 次调用。
- 大批量连续图优先流式；非流式适合 1-4 张轻量验证。
- 3 号技能只负责执行与报告，不负责临场改写剧情；剧情、版式和文字槽错误应回到 2 号技能修源。
- 长任务可观测性本身也是 3 号技能合同的一部分；若只有 `generation_plan.json` 没有执行态报告，排障成本会显著上升。
- 当 2 号 JSON 位于 `projects/aigc/<项目名>/5-Image/漫画/2-九刀流漫画提示词/` 时，3 号技能应把 `5-Image/漫画` 视为当前生成阶段根，而不是回退创建新的 `projects/comic/<json-stem>/` 项目壳。
- 页码如果只存在于 `page_number` 数值字段里，模型不会自动画出来；必须把 `page_number_overlay` 编进 master prompt，且逐页重复。
- 最终交付文件名应优先服务人工浏览和选片；默认短命名 `page01..page09` 比把上游 JSON stem 传播到图片名更稳。
- 一旦 2 号技能切成 `page-group` 集合，3 号技能的执行目标就不再是“整集唯一目录”，而是“每组一个稳定落点”；否则批量执行时报告和图片会互相踩写。
- 4 号动画阶段默认按 `page01..page09` 读取首帧；因此 3 号的图片命名稳定性本身就是跨阶段合同，不只是目录美观问题。
- 3 号技能的 `--self-test` 不能只做 prompt 片段烟雾测试；它必须至少证明“内置样例仍然通过 2 号 validator”，否则自检绿灯没有实际门禁价值。
