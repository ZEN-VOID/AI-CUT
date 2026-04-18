# Episode Root Contract

`projects/story/<项目名>/3-Drafting/第N集.md` 是 `3-Drafting` 阶段的单一 Markdown 正文真源。

## Canonical Paths

- 正式正文：`projects/story/<项目名>/3-Drafting/第N集.md`
- 工序日志：`projects/story/<项目名>/3-Drafting/写作日志.yaml`

## Root File Contract

1. `第N集.md` 承载本集当前最新正文，不额外维护 sibling manuscript。
2. 文件允许使用 YAML frontmatter 记录集号、标题、planning ref、previous episode ref、processed steps，但正文主体必须保持可直接阅读。
3. 子技能可以覆盖正文全文或以 patch 形式重写，但目标永远是同一文件。
4. 任何会写正文的工序都必须先读取完整 `第N集.md`。

## Writing Log Contract

`写作日志.yaml` 至少记录：

- `episode_num`
- `manuscript_path`
- `planning_ref`
- `previous_episode_ref`
- `completed_steps`
- `step_history`
- `current_resume_pointer`

## Overwrite Rules

1. 正式正文只能有一份；不得并行留下 `第N集-pass2.md`、`第N集-润色版.md` 等第二真源。
2. 日志与正文必须成对更新。
3. 若正文与日志状态不一致，以正文为业务真源、以日志为工序真源，二者必须在下一次写入前修齐。

## Projection Rule

- `3-Drafting` 阶段不再从“技术根文件”投影到“发布正文”；`第N集.md` 本身就是当前业务正文根文件。
- 若后续存在发布投影或平台上传动作，应从 `第N集.md` 派生，而不是重新拼正文。
