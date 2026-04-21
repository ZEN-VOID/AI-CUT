# Chapter Board Locating Contract

`3-Drafting` 的任何 episode worker 只要要消费“当前集 chapter board / 当前章义务 / threads 债务”，都必须先把自己解析成**唯一** `chapter_board`，再进入正文判断。

## Required Runtime Keys

- `volume_ref`
- `chapter_num`
- 优先使用：`chapter_ref / episode_id`
- `planning_ref`

上述键优先从当前 `第N集.md` frontmatter 与 `第V卷.写作日志.yaml` 读取；若两处同时存在但不一致，必须阻塞并先修齐正文/批次日志。

## Locate Order

1. 先锁当前集身份：
   - 若存在 `chapter_ref / episode_id`，优先采用它
   - 若只存在 `chapter_num`，保留其数值形态，并派生规范化 token
2. 先读取 `2-Planning/全息地图.json` 的 `content.holomap.episode_slice_manifest[]` 与 `episode_sequence_axis[]`
3. 进入命中的 `2-Planning/卷分片/*.json.content.holomap_slice.chapter_boards[]` 做精确定位：
   - 首选 `chapter_boards[].episode_ref == chapter_ref`
   - 若无 `chapter_ref`，允许与规范化后的 `chapter_num` 做精确同义匹配
4. 若 slice `chapter_boards[]` 仍未唯一命中，才允许使用 slice 内 `episode_sequence_axis[] -> chapter_board_ref -> node_id` 回指
5. 只有当最终结果收束为**唯一** `chapter_board` 时，才允许继续解码：
   - `node_id`
   - `episode_ref`
   - `bundled_elements`
   - `planned_state`
   - `entry_state / expected_exit_delta`

## Hard Gates

- 禁止用 `chapter_boards` 数组顺序当作默认章节映射。
- 禁止按标题、摘要句子、hook 文案做模糊猜测。
- 命中 0 个 board：阻塞当前 worker，优先回源修 `2-Planning` 的 manifest / axis / slice 绑定。
- 命中多个 board：阻塞当前 worker，优先回源修 `2-Planning/2-章节规划` 的 `episode_slice_manifest / episode_sequence_axis / slice chapter_boards`。
- frontmatter、卷级日志、planning 三方章节标识冲突：先修 chapter scope，再允许写正文。

## Minimum Resolution Trace

每次定位后至少应能说明：

- 当前使用的 `volume_ref`
- 当前使用的 `chapter_num / chapter_ref`
- 命中的 `planning_slice_ref`
- 命中的 `chapter_board.node_id`
- 命中的依据是 `manifest/axis -> slice -> episode_ref` 直连，还是 `slice axis -> node_id` 回指
- 若失败，失败类型属于：`zero_match / multi_match / scope_conflict`
