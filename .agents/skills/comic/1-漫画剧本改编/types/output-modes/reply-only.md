# Reply-Only 输出模式

## Match Signals

- 用户要求“先在这里给我”“不要写文件”“快速预览”“只回复”。

## Fixed Context

- 在回复中按 `第N组.md` 的同构结构输出。
- 即使不写盘，也必须保留 frontmatter 等效字段、组号、边界判定、正文和组末钩子。
- 可以省略实际 validator 执行，但必须人工检查 required fields 和组号连续性。

## Review Gate

- 回复中的组结构可以无损复制成 `第N组.md`。
- 不输出整篇无分组 prose。
