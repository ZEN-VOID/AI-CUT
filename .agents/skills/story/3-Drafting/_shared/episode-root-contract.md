# Episode Root Contract

`projects/story/<项目名>/3-Drafting/第N集.md` 仍然是 `3-Drafting` 阶段的单集 Markdown 正文真源。

但在当前模型下：

- 正文真源是集级
- 批次真源是卷级

## Canonical Paths

- 正式正文：`projects/story/<项目名>/3-Drafting/第N集.md`
- 卷级批次日志：`projects/story/<项目名>/3-Drafting/第V卷.写作日志.yaml`

## Root File Contract

1. `第N集.md` 承载当前章节的最新正文，不额外维护 sibling manuscript。
2. 文件允许使用 YAML frontmatter 记录 `chapter_ref / volume_ref / planning_ref / processed_steps` 等元信息，但正文主体必须保持可直接阅读。
3. 子技能可以覆盖正文全文或以 patch 形式重写，但目标永远是同一文件。
4. 任何会写正文的工序都必须先读取完整 `第N集.md`。

## Volume Batch Log Contract

`第V卷.写作日志.yaml` 至少记录：

- `volume_num`
- `volume_ref`
- `planning_ref`
- `planning_slice_ref`
- `chapter_refs`
- `worker_status`
- `chapter_step_history`
- `current_resume_pointer`

## Overwrite Rules

1. 正式正文只能有一份；不得并行留下 `第N集-pass2.md`、`第N集-润色版.md` 等第二真源。
2. 卷级日志与相关正文写回必须成对更新。
3. 若正文与卷级日志状态不一致，以正文为业务真源、以卷级日志为执行真源，二者必须在下一次写入前修齐。

## Projection Rule

- `3-Drafting` 阶段不再从“技术根文件”投影到“发布正文”；`第N集.md` 本身就是当前业务正文根文件。
- 若后续存在平台上传动作，应从 `第N集.md` 派生，而不是重新拼正文。
