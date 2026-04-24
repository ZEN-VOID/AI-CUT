# Imagegen 九页漫画生成执行细则

## 1. 默认路径

本技能默认使用 Codex 内置 `image_gen` 工具，而不是任何外部图像 API。

执行口径：

- `provider`: `built-in-image_gen`
- `model_policy`: `GPT-IMAGE-2-default`
- `model_parameter_exposed`: `false`
- `execution`: one built-in tool call per comic page
- `image_count`: 9
- `output`: project-local PNG files

说明：内置 `image_gen` 当前不暴露 `model` 参数。不得在工具调用中伪造 `model=gpt-image-2` 字段。若用户要求可审计的显式模型参数，必须先说明需要切换到 `imagegen` CLI/API fallback，并在用户确认后执行。

## 2. 九页原则

每个 `page-group` 有 9 页。默认执行方式是 9 次单页生成：

1. Page 1 prompt -> built-in `image_gen`
2. Page 2 prompt -> built-in `image_gen`
3. ...
4. Page 9 prompt -> built-in `image_gen`

不得把 9 页合成一次 prompt 交给内置工具生成。这样会显著提高九宫格、合集、contact sheet 或同图变体风险。

当上游 2 号技能已经把一个 episode 切成多个 `page-group` 时：

- 3 号技能一次只消费一个 group JSON。
- 多个 group 按 `group_index` 顺序分别执行。
- 默认把执行产物落到 `3-漫画生成/<group_slug>/imagegen/`。

## 3. 单页 Prompt 结构

每页 prompt 按以下顺序组织：

1. 原始 `pages[].positive_prompt`
2. 本页页码与右下角数字页码要求
3. 单页执行后缀
4. 顶层 `generation_contract.hard_constraints`
5. 顶层 `global_negative_prompt`

单页执行后缀标准文本：

```text
Execution for this single built-in image_gen call: generate only this one page, not the full 9-page set. Preserve vertical 9:16 comic-page feeling, multiple panels, readable page number overlay.
```

硬约束标准文本：

```text
Hard constraints from project contract: Do not create a nine-grid collage, contact sheet, or one image containing all pages. Do not create nine variations of the same scene. Every page must contain multiple comic panels, never a single full-page illustration. Keep character and scene consistency across all pages. Place a small page number in the bottom-right corner of every page, using digits 1-9 only.
```

## 4. 落盘与 Manifest

内置工具会先把图片保存到 `$CODEX_HOME/generated_images/...`。项目型漫画生成不得只引用该默认目录。

标准持久化流程：

1. 生成前记录 `$CODEX_HOME/generated_images/**/*.png` baseline。
2. 逐页生成 9 张图片。
3. 生成后识别新增 PNG。
4. 按生成顺序映射到 `page01..page09`。
5. 复制到项目目录，保留默认目录原件。
6. 写 manifest 与 `comic_generation_report.json`。

默认目标：

```text
projects/comic/[项目名]/3-漫画生成/<group_slug>/imagegen/
  page01.png
  page02.png
  ...
  page09.png
  imagegen_generation_plan.json
  comic_generation_report.json
  imagegen_manifest.json
```

`projects/aigc/[项目名]/5-Image/漫画/` 项目按同级阶段目录推断，不得漂移到 `projects/comic/`。

## 5. 验收标准

完成交付至少满足：

- 项目目录中存在 9 个图片文件。
- 文件可打开。
- 宽高为竖版比例。
- 文件名按页码稳定排序。
- manifest 中有 9 条 source -> target 映射。
- 报告中明确写入 `provider=built-in-image_gen` 与 `model_policy=GPT-IMAGE-2-default`。

视觉抽查重点：

- 不是九宫格、contact sheet 或合集。
- 不是单张海报式整页插画；每页应有多个漫画 panel。
- 页码在右下角且使用对应数字。
- 角色、场景和风格延续上游 JSON 锁定。

## 6. 失败回退

| 失败 | 回退点 |
| --- | --- |
| JSON 不合格 | `2-九刀流漫画提示词` validator |
| prompt 缺少硬约束 | 本技能 page prompt plan |
| 内置 `image_gen` 不可用 | 向用户说明并询问是否切换 CLI/API fallback |
| 少于 9 张 | 检查 baseline、新增图片识别和 9 次工具调用完整性 |
| 九宫格拼图 | 单页执行后缀 + 2 号 `hard_constraints` |
| 九个变体 | 2 号 `story_beat_map / pages[]` |
| 多个 group 执行后互相覆盖 | 本技能 `group target resolve`、默认 output_dir / filename_prefix |
| 需要显式 `model=gpt-image-2` | 用户确认后转 `imagegen` CLI/API fallback |

## 7. Legacy Provider

`references/seedream-nine-page-generation.md` 仅保留为 legacy Seedream/API 追溯资料。除非用户显式要求切换 provider，或当前会话没有内置 `image_gen` 且用户确认 fallback，否则不得默认调用 Seedream、Dreamina 或其他外部图像 API。
