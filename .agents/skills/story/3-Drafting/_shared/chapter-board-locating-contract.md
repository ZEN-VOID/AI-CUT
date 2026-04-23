# Chapter Board Locating Contract

`3-Drafting` 的任何 chapter worker 只要要消费“当前章规划 / 当前章义务 / threads 债务”，都必须先把自己解析成**唯一**章级规划文档；兼容项目才继续解析到唯一 `chapter_board`。

## Required Runtime Keys

- `volume_ref`
- `chapter_num`
- 优先使用：`chapter_ref / episode_id`
- `planning_ref`
- `planning_volume_ref`

上述键优先从当前 `第N章.md` frontmatter 与 `第V卷.写作日志.yaml` 读取；若两处同时存在但不一致，必须阻塞并先修齐正文/批次日志。

## Locate Order

1. 先锁当前章身份：
   - 若存在 `chapter_ref / episode_id`，优先采用它
   - 若只存在 `chapter_num`，保留其数值形态，并派生规范化 token
2. 先读取 `2-Planning/整体规划.md`
3. 再读取当前卷 `2-Planning/第V卷/卷规划.md`
4. 命中当前章 `2-Planning/第V卷/第N章.md`
5. 只有当当前章规划文档收束为唯一目标后，才允许继续解码章级义务：
   - `本章故事概要`
   - `本章冲突`
   - `本章节奏曲线`
     - `selected_pack / selected_mode`
     - `七步职责映射`
     - `规划义务`
     - `义务段位 / 建议写法`
   - `本章任务线`
   - `章末达成`
   - `本章线索 / 本章伏笔`
6. 若项目仍处于兼容态，才允许继续读取 `2-Planning/全息地图.json` 与 `卷分片/*.json.content.holomap_slice.chapter_boards[]` 做补充定位

## Hard Gates

- 禁止用 `chapter_boards` 数组顺序当作默认章节映射。
- 禁止按标题、摘要句子、hook 文案做模糊猜测。
- 章级规划命中 0 个：阻塞当前 worker，优先回源修当前卷目录中的 `第N章.md` 缺失问题。
- 章级规划命中多个或跨卷冲突：阻塞当前 worker，优先回源修 `卷规划.md` 与章节映射。
- frontmatter、卷级日志、planning 三方章节标识冲突：先修 chapter scope，再允许写正文。

## Minimum Resolution Trace

每次定位后至少应能说明：

- 当前使用的 `volume_ref`
- 当前使用的 `chapter_num / chapter_ref`
- 命中的 `planning_volume_ref`
- 命中的 `planning_ref`
- 若走兼容态，再补充 `planning_slice_ref / chapter_board.node_id`
- 若失败，失败类型属于：`zero_match / multi_match / scope_conflict`
