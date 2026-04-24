# Context: 漫画生成

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 7280
current_lines: 63
current_cases: 0
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-24T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

本文件沉淀“九刀流 JSON -> Codex built-in image_gen -> 9 张漫画页”的执行经验。当前默认路径已经从 Seedream/API 切换为内置 `image_gen`，默认模型口径为 `GPT-IMAGE-2-default`。外部 API 仅作为 legacy/fallback 资料保留。

## Type Map

| type_id | 症状 | 根因层 | 立即修复 | 系统预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-CG-01` | 仍然默认调用 Seedream / Dreamina / AnyFast 等 API | runtime 路由层 | 改走 Codex built-in `image_gen`，逐页调用 9 次 | `SKILL.md` 将 API provider 降级为 legacy fallback | 执行报告写 `provider=built-in-image_gen` |
| `TM-CG-02` | 用户要求“默认 GPT-IMAGE-2”，但内置工具不暴露 `model` 参数 | 模型口径层 | 记录 `model_policy=GPT-IMAGE-2-default`，不得伪造工具参数 | 若需要可审计 `model=gpt-image-2`，先征得用户确认再走 CLI/API fallback | 报告区分 `model_policy` 与 `model_parameter_exposed=false` |
| `TM-CG-03` | 输出成一张九宫格或 contact sheet | prompt 执行层 | 每页 prompt 末尾追加“only this one page, not the full 9-page set” | 内置路径固定 9 次单页调用，不做单 prompt 9 页 | 9 个独立 PNG，非一张合集 |
| `TM-CG-04` | 输出像九个同场景变体 | 上游 JSON 层 | 回到 2 号重切 `story_beat_map / pages[]` | validator 检查页号与 page_role | 9 页 page_role、action、page_number 不重复 |
| `TM-CG-05` | 生成后图片只留在 `$CODEX_HOME/generated_images` | 项目持久化层 | 复制新增图片到项目 `3-漫画生成/<group_id>/imagegen/` | 执行节点必须记录 baseline、新增文件和 saved_files | 项目目录有 `page01.png..page09.png` |
| `TM-CG-06` | 生成数量少于 9 或顺序错乱 | baseline 识别层 | 生成前记录 `$CODEX_HOME/generated_images` 列表；生成后按 mtime 取新增 9 张并映射页码 | 报告写入 source path -> target path manifest | manifest 有 9 项且 page 1-9 连续 |
| `TM-CG-07` | 页面比例不稳定 | prompt 与工具默认层 | 每页 prompt 强写 vertical 9:16；验收检查宽高为竖版 | 2 号 schema 固定 layout.aspect_ratio | 文件尺寸为竖版 |
| `TM-CG-08` | 文字槽失败严重 | 上游提示词层 | 减少气泡文本，把解释转 caption | 2 号文字系统限制长度 | 气泡短句、旁白短框 |
| `TM-CG-09` | 生成计划或图片落到 `output/comic` | 项目根合同层 | 改用 `projects/comic/[项目名]/3-漫画生成/`，必要时传 `project_name` | 从 JSON 路径推断项目根 | `imagegen_generation_plan.json` 位于项目 3 号目录 |
| `TM-CG-10` | `aigc` 项目的漫画生成计划被错误推到 `projects/comic/<json-stem>/3-漫画生成/` | 项目根推断层 | 对 `projects/aigc/[项目名]/5-Image/漫画/2-九刀流漫画提示词/` 显式回推到同级 `5-Image/漫画/3-漫画生成/` | 把 `aigc` 路径推断固化为技能合同 | dry-run 默认输出目录位于当前 `aigc` 项目内 |
| `TM-CG-11` | 最终页没有页码，或页码不在右下角/不是纯数字 | 单页 prompt 编译层 | 从 2 号 JSON 读取 `pages[].page_number_overlay`，并逐页重复 `bottom-right` + `digits only` | 3 号 prompt plan 和 2 号 validator 同步要求页码覆盖层 | prompt 能逐页读到 page number "N" |
| `TM-CG-12` | 多人页或场景在 3 号执行后仍漂移 | 编译上下文稀释层 | 保留 `positive_prompt` 内的角色/场景锁，不在 3 号临场删减 | 3 号不再重写剧情，只加执行后缀 | prompt plan 内仍有 character locks / scene locks |
| `TM-CG-13` | 同一集多个 page-group 连续执行后，计划、report 或图片互相覆盖 | group 目标解析层 | 从上游 JSON 读取 `page_group.group_id`，默认落到 `3-漫画生成/<group_slug>/imagegen/` | 每组独立目录；共享目录时启用 group 前缀 | dry-run 或实跑产物位于独立 group 子目录 |
| `TM-CG-14` | 4 号动画阶段能拿到 group JSON，却找不到对应页图 | 3/4 号 handoff 层 | 3 号稳定落盘 `page01..page09`；4 号按页码解析 | 文件名稳定性写入跨阶段合同 | 4 号 dry-run 中 9 页都能定位 source_image |
| `TM-CG-15` | 内置 image_gen 效果明显好于 API，但技能仍优先 API | 经验未晋升层 | 将本次成功晋升到 `SKILL.md` 默认路径 | API 只保留 legacy/fallback；默认不再触发授权、额度或 provider 漂移问题 | 新任务默认走内置 imagegen |

## Repair Playbook

1. 先看执行报告：`provider / model_policy / page_prompts / saved_files / manifest`。
2. 若仍出现 API 命令或 API report，先修 3 号技能路由，不要继续排查 provider 认证。
3. 若内置工具不可用，告知用户 built-in 路径受当前会话工具能力限制，再询问是否切换 CLI/API fallback；不得静默切回 Seedream。
4. 若 JSON 不合格，不允许绕过 2 号 validator 直接生图。
5. 若输出成九宫格，先检查是否误把 9 页合进一个 prompt；正确路径是 9 次单页 `image_gen`。
6. 若新增文件识别错乱，重新生成前后 baseline，并按生成时间映射 `page01..page09`。
7. 若页面语义不对，回到 2 号 JSON，而不是在 3 号临场重写剧情。
8. 若用户要求“确切指定 GPT-IMAGE-2”，说明内置工具只支持 `model_policy` 口径；显式 `model=gpt-image-2` 需要用户确认 CLI/API fallback。

## Reusable Heuristics

- 已验证 Codex built-in `image_gen` 对九刀流漫画页的视觉效果非常好，适合成为 3 号技能默认生图路径。
- 内置 `image_gen` 的强项是逐页质量、中文漫画风格稳定性和免 API 授权；代价是不能通过脚本直接传 `model`、`n`、`size` 等 provider 参数。
- 对内置路径，最稳的执行方式是“每页一个完整 prompt + 单页执行后缀 + 生成后复制到项目目录”。
- 3 号技能只负责执行与报告，不负责临场改写剧情；剧情、版式和文字槽错误应回到 2 号技能修源。
- 当 2 号 JSON 位于 `projects/aigc/<项目名>/5-Image/漫画/2-九刀流漫画提示词/` 时，3 号技能应把 `5-Image/漫画` 视为当前生成阶段根，而不是回退创建新的 `projects/comic/<json-stem>/` 项目壳。
- 页码如果只存在于 `page_number` 数值字段里，模型不会自动画出来；必须把 `page_number_overlay` 编进单页 prompt，且逐页重复。
- 最终交付文件名应优先服务人工浏览和选片；默认短命名 `page01..page09` 比把上游 JSON stem 传播到图片名更稳。
- 一旦 2 号技能切成 `page-group` 集合，3 号技能的执行目标就不再是“整集唯一目录”，而是“每组一个稳定落点”；否则批量执行时报告和图片会互相踩写。
- 4 号动画阶段默认按 `page01..page09` 读取首帧；因此 3 号的图片命名稳定性本身就是跨阶段合同，不只是目录美观问题。
