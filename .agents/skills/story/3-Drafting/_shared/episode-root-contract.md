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
2. 文件允许使用 YAML frontmatter 记录 `episode_num / episode_title / story_name / planning_ref / planning_volume_ref / planning_global_ref / planning_slice_ref / previous_episode_ref / rhythm_type / processed_steps` 等元信息；若项目另有 `chapter_ref / volume_ref` 等扩展键，也允许共存，但正文主体必须保持可直接阅读。
3. 子技能可以覆盖正文全文或以 patch 形式重写，但目标永远是同一文件。
4. 任何会写正文的工序都必须先读取完整 `第N集.md`。

## Frontmatter Ownership Contract

- `story_name`
  - 英文字段名固定为 `story_name`
  - 字段值为当前小说名；优先取项目已锁定题名，若当前轮只存在项目目录名，则可临时回填项目名
  - `Step 1 / 1-单集叙事起盘` 首次 bootstrap 或重写 root 时必须补齐，不得缺席
- `rhythm_type`
  - 英文字段名固定为 `rhythm_type`
  - 字段值固定使用中文标签：`势能式` 或 `动能式`
  - `Step 2 / 2-节奏优化` 只负责兑现 planning 已锁定的 mode，并据此写回正式值
  - 若当前 root 由 Step 1 首次 bootstrap，`rhythm_type` 键位也必须先存在；在 Step 2 尚未判定前可暂为空字符串

## Volume Batch Log Contract

`第V卷.写作日志.yaml` 至少记录：

- `volume_num`
- `volume_ref`
- `planning_ref`
- `planning_volume_ref`
- `planning_global_ref`
- `planning_slice_ref`
- `chapter_refs`
- `worker_status`
- `chapter_step_history`
- `chapter_hook_results`
- `current_resume_pointer`

硬规则补充：

1. `chapter_step_history[chapter_ref]` 必须按正式执行顺序收满 8 条记录，对位 `1-单集叙事起盘 -> ... -> 8-润色`。
2. `chapter_hook_results[chapter_ref]` 必须与上条 8 个 step 一一对应，记录每一步 inline validation 的 `status / checked_dimensions / checked_at / rework_target_step`。
3. 不允许用“单条 Step 8 摘要”或“卷级总评语”回填冒充逐步 step ledger。

## Overwrite Rules

1. 正式正文只能有一份；不得并行留下 `第N集-pass2.md`、`第N集-润色版.md` 等第二真源。
2. 卷级日志与相关正文写回必须成对更新。
3. 若正文与卷级日志状态不一致，以正文为业务真源、以卷级日志为执行真源，二者必须在下一次写入前修齐。

## Projection Rule

- `3-Drafting` 阶段不再从“技术根文件”投影到“发布正文”；`第N集.md` 本身就是当前业务正文根文件。
- 若后续存在平台上传动作，应从 `第N集.md` 派生，而不是重新拼正文。
