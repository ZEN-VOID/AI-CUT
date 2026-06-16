# Built-in Imagegen 九页漫画生成执行细则

## 默认路径

本技能默认使用 `.agents/skills/cli/imagegen` 的 built-in `image_gen` 路径生成漫画页。`.agents/skills/cli/imagegen/scripts/image_gen.py`、Image API 与 `generate-batch` 不是本技能默认执行路由。

执行口径：

- `provider`: `built-in-imagegen`
- `skill_path`: `.agents/skills/cli/imagegen`
- `mode`: `built_in_image_gen`
- `batch_execution`: `subagents_parallel_default`
- `max_concurrency`: `10`
- `resolution_target`: inherited from upstream or `2k_default`
- `resolution_value`: inherited from upstream or `2K`
- `output_format`: `png`
- `execution`: 9 prompt specs, one page asset per built-in image_gen call

真实执行不需要 `OPENAI_API_KEY`。脚本只能写 handoff plan；实际生成由 agent/tool 通过 built-in `image_gen` 完成。

## 九页原则

每个 `page-group` 固定 9 页。默认执行方式是 9 个单页资产任务：

1. `page01` prompt -> built-in image_gen call 1
2. `page02` prompt -> built-in image_gen call 2
3. ...
4. `page09` prompt -> built-in image_gen call 9

不得把 9 页合成一个 prompt，也不得把 9 页当成同一 prompt 的 9 个变体。built-in batch 语义是提交 9 个不同页 prompt，并由父任务汇总结果。

## 单页 Prompt 结构

每页 prompt 按以下顺序组织：

1. 单页执行声明：只生成当前页，完整竖版 9:16 漫画页。
2. `page_group` 与 `continuity_context`。
3. `type_stack_ref` 与 `type_pack_context` 的 image-generation 投影。
4. 风格、角色、场景、文字系统锁。
5. 原始 `pages[].positive_prompt`。
6. 本页 `layout / panels / page_number_overlay`。
7. 顶层 `generation_contract.hard_constraints`。
8. 顶层 `global_negative_prompt`。

标准执行后缀：

```text
Built-in image_gen request for this single page: generate exactly one complete vertical 9:16 comic page as this one image asset, not the full 9-page set. Do not create a collage, contact sheet, or variants sheet. Keep multiple comic panels, consistent cast and scene continuity, and a small bottom-right page number using the exact digit for this page.
```

## 标准产物

默认目标：

```text
projects/comic/[项目名]/3-漫画生成/<group_slug>/built-in-imagegen/
  imagegen_handoff_plan.json
  imagegen_prompt_set.json
  page01-imagegen_prompt.txt
  ...
  page09-imagegen_prompt.txt
  page01.png
  ...
  page09.png
  comic_generation_report.json
```

`projects/aigc/[项目名]/5-Image/漫画/` 项目按同级阶段目录推断，不得漂移到 `projects/comic/`。

## 推荐命令

准备 built-in handoff plan：

```bash
python3 .agents/skills/comic/3-漫画生成/scripts/prepare_builtin_imagegen_comic_generation.py \
  projects/comic/[项目名]/2-九刀流漫画提示词/page-group-01-nine_blade_comic_prompts.json
```

自检：

```bash
python3 .agents/skills/comic/3-漫画生成/scripts/prepare_builtin_imagegen_comic_generation.py --self-test
```

脚本不能执行 built-in `image_gen`。若用户要求真实生图，agent 读取 `imagegen_prompt_set.json` 后按 `.agents/skills/cli/imagegen` 执行：

1. 每条 prompt 一个 image_gen call。
2. 默认 subagents 并发 fan-out，最大并发 10。
3. 父任务把每页结果复制/移动到 `output_dir`。
4. 更新 `comic_generation_report.json` 的 `saved_files` 和 review verdict。

## 验收标准

完成交付至少满足：

- JSON validator 通过。
- `imagegen_prompt_set.json` 有 9 条 prompt spec。
- 每页 prompt 都包含 9:16、非拼图、非变体、多格漫画、连续性和右下角数字页码约束。
- Plan 写出 handoff plan、prompt set 和报告。
- Execute 模式下 9 个 PNG 存在，文件名按页码稳定排序，且位于项目 `output_dir`。
- 报告明确写入 `provider=built-in-imagegen`、`runtime.mode=built_in_image_gen`、`runtime.batch_execution=subagents_parallel_default` 或显式用户串行。

## 失败回退

| 失败 | 回退点 |
| --- | --- |
| JSON 不合格 | `2-九刀流漫画提示词` validator |
| prompt 缺少硬约束 | 本技能 page prompt compiler |
| built-in 工具不可用 | 报告 blocker，不静默切换 CLI/API/provider |
| 输出仍在 `$CODEX_HOME/generated_images` | imagegen `references/output-persistence.md` + 父任务 gather/persist |
| 少于 9 张 | 检查 built-in 调用结果、prompt set 和输出文件名 |
| 九宫格拼图 | 单页 asset 规则 + 单页执行后缀 |
| 九个变体 | 2 号 `story_beat_map / pages[]` |
| 多个 group 执行后互相覆盖 | `group target resolve`、默认 output_dir / filename_prefix |
| 需要其他 provider 或 CLI/API | 用户显式确认后进入 legacy external reference |
