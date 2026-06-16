# Context: 漫画生成

本文件沉淀“九刀流 JSON -> built-in image_gen handoff -> 9 张漫画页”的运行经验。当前默认生图工具是 `.agents/skills/cli/imagegen` 的内置 `image_gen` 路径；CLI/API、Seedream、Dreamina 与 AnyFast 只保留为用户显式点名的 legacy/external 路径。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-06-15
```

## Type Map

| type_id | 症状 | 根因层 | 立即修复 | 系统预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-CG-01` | 仍然默认调用 CLI/API、Seedream、Dreamina 或要求 `OPENAI_API_KEY` | runtime 路由层 | 改走 `.agents/skills/cli/imagegen` built-in `image_gen` handoff | `SKILL.md`、types、steps 和父级路由固定 built-in-only 路径 | 报告写 `provider=built-in-imagegen` |
| `TM-CG-02` | 9 页被合成一张九宫格或 contact sheet | batch 语义层 | 每页一个独立 prompt / asset task，输出 `page01..page09` | `references/` 固化单页 asset 约束 | `imagegen_prompt_set.json` 有 9 条 |
| `TM-CG-03` | 输出像同一场景九个变体 | 上游 JSON 层 | 回到 2 号重切 `story_beat_map / pages[]` | 3 号只投影已有剧情，不临场重写 | 9 页 `page_role/action/page_number` 不重复 |
| `TM-CG-04` | 脚本试图直接调用 built-in `image_gen` 或 CLI | 工具边界层 | 脚本只写 handoff plan；真实生图由 agent/tool 执行 | `prepare_builtin_imagegen_comic_generation.py` 不含 API/CLI 调用 | `built_in_tool_invoked_by_script=false` |
| `TM-CG-05` | 输出目录漂移到 `$CODEX_HOME/generated_images`、subagent 路径或 `output/imagegen/` | 项目持久化层 | 父任务把最终 PNG 复制/移动到项目 3 号目录 | imagegen output-persistence gate 成为完成门禁 | 文件位于项目根下 |
| `TM-CG-06` | 页面比例不稳定 | prompt 约束层 | 在每页 prompt 内重复 9:16、vertical comic page、single page asset | Runtime Policy 固定 9:16 prompt target | report 记录 resolution target/value |
| `TM-CG-07` | 多个 group 连续执行互相覆盖 | group 目标解析层 | 默认每组独立 `built-in-imagegen/` 子目录；共享目录时自动加 group 前缀 | N4 gate 检查命名冲突 | report 中 saved_files 不覆盖 |
| `TM-CG-08` | 4 号剧集海报阶段找不到页图 | 跨阶段命名层 | 稳定输出 `page01.png..page09.png` | Output Contract 明确图片命名 | 4 号按页码可定位本集代表性画面 |
| `TM-CG-09` | 页码缺失或不是右下角纯数字 | prompt 编译层 | 从 `page_number_overlay` 和页号字段重复写入 prompt | 单页 prompt 后缀固定页码约束 | 每页 prompt 含对应数字页码 |
| `TM-CG-10` | 3 号脚本尝试“优化剧情” | 主创边界层 | 删除脚本中的创作性改写，只保留投影/拼装 | 遵循 LLM-first creative authorship | prompt 保留 `positive_prompt` 原文 |

## Repair Playbook

1. 先看 `comic_generation_report.json` 中的 `provider / runtime.mode / batch_execution / output_dir / saved_files`。
2. 若 provider 不是 `built-in-imagegen`，先修 3 号 runtime 路由、父级路由和 2 号 schema，不继续排查视觉质量。
3. 若 JSON 不合格，不允许绕过 2 号 validator 直接生图。
4. 若脚本或文档要求 `OPENAI_API_KEY`、`gpt-image-2`、`generate-batch` 或 `scripts/image_gen.py`，这是 legacy 漂移；回到 active built-in contract。
5. 若输出成九宫格，检查是否误把 9 页放进一个 prompt；正确路径是 9 个 prompt specs，每个 spec 只生成一页。
6. 若页面语义不对，回到 2 号 JSON 修源；3 号不负责重写剧情。
7. 若输出目录不在项目根，按 imagegen `references/output-persistence.md` 把最终图复制/移动回项目目录。
8. 若形成稳定故障模式，写回本文件；若稳定到必须执行，再晋升到 `SKILL.md` 或对应分区。

## Reusable Heuristics

- 漫画 3 号选择 built-in `image_gen` 后，最稳的证据形态是 `imagegen_handoff_plan.json + imagegen_prompt_set.json + pageXX prompt + comic_generation_report.json`。
- built-in 路径没有硬 CLI 参数；`resolution_target/resolution_value` 只能作为 prompt/delivery target 传递，不应写成模型参数保证。
- 9 页漫画不是一个 batch prompt，也不是一个 prompt 的 `n=9` 变体；它是 9 个独立页面资产。
- prompt 编译时应保留 `positive_prompt` 原文，再追加执行后缀和硬约束；不要把上游 prompt 摘要化到丢失角色锁。
- plan 不是半成品，它是可审计执行计划；真实执行受工具可用性阻断时，plan 产物仍可作为排障和手动生成证据。
- 多个 group 批量执行时，最稳目录是 `3-漫画生成/<group_slug>/built-in-imagegen/`。
