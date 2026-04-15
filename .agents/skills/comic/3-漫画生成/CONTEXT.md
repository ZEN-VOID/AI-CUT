# Context: 漫画生成

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: ~2300
current_lines: ~50
current_cases: 0
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-15T00:00:00Z
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

## Repair Playbook

1. 先看 seedream 报告：`ok/result_count/stream_event_types/generated_images`。
2. 若请求层失败，回到 seedream 技能。
3. 若请求成功但画面语义不对，回到 2 号 JSON，而不是重写 3 号脚本。
4. 若 dry-run master prompt 没有“9 separate images / not collage / not variations”，先修编译器。
5. 若 JSON 不合格，不允许绕过 validator 直接生图。

## Reusable Heuristics

- 已验证 Seedream 的 9 图连续生成不是九宫格裁切；下游应该尊重单请求能力，而不是拆成 9 次调用。
- 大批量连续图优先流式；非流式适合 1-4 张轻量验证。
- 3 号技能只负责执行与报告，不负责临场改写剧情；剧情、版式和文字槽错误应回到 2 号技能修源。
