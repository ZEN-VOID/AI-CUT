# Chapter Board Locating Contract

`3-Drafting` 任何一步只要要消费“本集 chapter board / 本章义务 / threads 债务”，都必须先把当前集解析成**唯一** `chapter_board`，再进入正文判断。

## Required Runtime Keys

- `episode_num`
- 优先使用：`episode_id`
- `planning_ref`

上述键优先从当前 `第N集.md` frontmatter 与 `写作日志.yaml` 读取；若两处同时存在但不一致，必须阻塞并先修齐 root/log。

## Locate Order

1. 先锁当前集身份：
   - 若存在 `episode_id`，优先采用它。
   - 若只存在 `episode_num`，保留其数值形态，并派生规范化 token（如 `1`、`第1集`）。
2. 先读取 `2-Planning/全息地图.json` 的 `content.holomap.episode_slice_manifest[]` 与 `episode_sequence_axis[]`：
   - 优先从 `episode_sequence_axis[]` 命中当前 episode 的 `slice_ref / chapter_board_ref`
   - 若 axis 缺 `slice_ref`，再由 manifest 的 episode range 推导目标 slice
3. 进入命中的 `2-Planning/十集分片/*.json.content.holomap_slice.chapter_boards[]` 做精确定位：
   - 首选 `chapter_boards[].episode_ref == episode_id`
   - 若无 `episode_id`，允许 `chapter_boards[].episode_ref` 与规范化后的 `episode_num` 做精确同义匹配
4. 若 slice `chapter_boards[]` 仍未唯一命中，且 slice `episode_sequence_axis[]` 显式带有当前 episode 与 `chapter_board_ref` 回指，则先命中 axis，再反查 `chapter_boards[].node_id`
5. 只有当最终结果收束为**唯一** `chapter_board` 时，才允许继续解码：
   - `node_id`
   - `episode_ref`
   - `bundled_elements`
   - `planned_state`

## Hard Gates

- 禁止用 `chapter_boards` 数组顺序当作默认集号映射。
- 禁止按标题、摘要句子、hook 文案做模糊猜测。
- 命中 0 个 board：阻塞当前 step，优先回源修 `2-Planning/全息地图.json` 的 manifest / axis，必要时再修目标 slice。
- 命中多个 board：阻塞当前 step，优先回源修 `2-Planning/2-章节规划` 的 `episode_slice_manifest / episode_sequence_axis / slice chapter_boards` 绑定。
- root frontmatter、日志、planning 三方 episode 标识冲突：先修 episode scope，再允许写正文。

## Source-Fix Routing

- `无 board` / `多 board` / `episode_ref 漂移`：
  - 先查 `2-Planning/2-章节规划`
  - 再查 `episode_slice_manifest / episode_sequence_axis`
  - 最后查父层 `3-Drafting/SKILL.md` 的 episode scope 装配
- `frontmatter / 写作日志` 不一致：
  - 先修 `projects/story/<项目名>/3-Drafting/第N集.md`
  - 再修 `写作日志.yaml`

## Minimum Resolution Trace

每次定位后至少应能说明：

- 当前使用的 `episode_num / episode_id`
- 命中的 `planning_slice_ref`
- 命中的 `chapter_board.node_id`
- 命中的依据是 `manifest/axis -> slice -> episode_ref` 直连，还是 `slice episode_sequence_axis -> node_id` 回指
- 若失败，失败类型属于：`zero_match / multi_match / scope_conflict`
