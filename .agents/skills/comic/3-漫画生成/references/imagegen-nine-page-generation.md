# CLI Imagegen 九页漫画生成执行细则

## 默认路径

本技能默认使用仓库内 `.agents/skills/cli/imagegen`，通过其 `scripts/image_gen.py generate-batch` 子命令生成漫画页。

执行口径：

- `provider`: `cli-imagegen`
- `skill_path`: `.agents/skills/cli/imagegen`
- `script`: `.agents/skills/cli/imagegen/scripts/image_gen.py`
- `subcommand`: `generate-batch`
- `model`: `gpt-image-2`
- `size`: `1152x2048`
- `quality`: `medium`
- `output_format`: `png`
- `execution`: 9 JSONL jobs, one page per job, `n=1`

真实执行需要网络与 `OPENAI_API_KEY`。Dry-run 不需要 API key。

## 九页原则

每个 `page-group` 固定 9 页。默认执行方式是 9 个单页 job：

1. `page01` prompt -> CLI imagegen job 1
2. `page02` prompt -> CLI imagegen job 2
3. ...
4. `page09` prompt -> CLI imagegen job 9

不得把 9 页合成一个 prompt，也不得使用 `--n 9` 生成九个变体。`generate-batch` 的意义是提交 9 个不同页 prompt，而不是为同一页生成 9 个候选。

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
CLI imagegen execution for this single page: generate exactly one complete vertical 9:16 comic page for this job, not the full 9-page set. Do not create a collage, contact sheet, or variants sheet. Keep multiple comic panels, consistent cast and scene continuity, and a small bottom-right page number using the exact digit for this page.
```

## 标准产物

默认目标：

```text
projects/comic/[项目名]/3-漫画生成/<group_slug>/imagegen-cli/
  imagegen_generation_plan.json
  imagegen_jobs.jsonl
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

```bash
python3 .agents/skills/comic/3-漫画生成/scripts/run_imagegen_cli_comic_generation.py \
  projects/comic/[项目名]/2-九刀流漫画提示词/page-group-01-nine_blade_comic_prompts.json \
  --dry-run
```

```bash
python3 .agents/skills/comic/3-漫画生成/scripts/run_imagegen_cli_comic_generation.py \
  projects/comic/[项目名]/2-九刀流漫画提示词/page-group-01-nine_blade_comic_prompts.json \
  --execute \
  --quality high
```

底层真实命令由 runner 写入 `imagegen_generation_plan.json`，默认形态为：

```bash
python3 .agents/skills/cli/imagegen/scripts/image_gen.py generate-batch \
  --input <output_dir>/imagegen_jobs.jsonl \
  --out-dir <output_dir> \
  --model gpt-image-2 \
  --size 1152x2048 \
  --quality medium \
  --output-format png \
  --concurrency 3 \
  --no-augment
```

## 验收标准

完成交付至少满足：

- JSON validator 通过。
- `imagegen_jobs.jsonl` 有 9 行，每行 `n=1` 或未显式设置 `n`。
- 每页 prompt 都包含 9:16、非拼图、非变体、多格漫画、连续性和右下角数字页码约束。
- Dry-run 写出计划和报告。
- Execute 模式下 9 个 PNG 存在，文件名按页码稳定排序。
- 报告明确写入 `provider=cli-imagegen`、`model=gpt-image-2`、`size=1152x2048`。

## 失败回退

| 失败 | 回退点 |
| --- | --- |
| JSON 不合格 | `2-九刀流漫画提示词` validator |
| 缺少 API key | 停留 dry-run，提示配置 `OPENAI_API_KEY` |
| prompt 缺少硬约束 | 本技能 page prompt compiler |
| 少于 9 张 | 检查 CLI exit code、JSONL job 数和输出文件名 |
| 九宫格拼图 | 单页 job 规则 + 单页执行后缀 |
| 九个变体 | 2 号 `story_beat_map / pages[]` |
| 多个 group 执行后互相覆盖 | `group target resolve`、默认 output_dir / filename_prefix |
| 需要其他 provider | 用户显式确认后进入 legacy reference |
