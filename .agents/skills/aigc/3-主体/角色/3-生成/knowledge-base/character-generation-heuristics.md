# Character Generation Heuristics

本文件保存 `角色/3-生成` 可复用经验，不拥有入口路由权。

## Stable Heuristics

- 主图是身份锚点，应优先清晰呈现脸、发型、体型、服装主轮廓和材质，不要先做复杂分栏面板。
- 多视图图要服务制作审阅，重点是同一身份在正面、侧面、背面、表情和动作模块中的一致性。
- `4. 解构` 是角色生成导入 Midjourney V8.1 的主要真源；如果它不足以生图，应回到 `角色/2-设计` 修复，而不是在 `3-生成` 临时补设计或回退使用旧英文整合 prompt。
- JSON prompt 里保留 source path、reference path 和 libTV mode，比只保存最终 prompt 更有复现价值。
- 批量生成最常见错误是角色之间串用参考图；每个角色的主图路径必须在多视图 JSON 中显式回链。

## Failure Repairs

- 图片已生成但不在项目目录：按 libTV persistence 规则复制或移动到 `3-生成/`，再更新 JSON。
- 多视图身份漂移：先检查 reference image 是否对应当前角色，再强化 identity lock 与 upstream prompt priority。
- JSON 解析失败：修复 JSON 格式，不改动 prompt 创作内容；必要时把长 prompt 放入字符串字段。
- 已有产物冲突：没有用户覆盖许可时使用版本化文件名，并在 JSON 中记录 actual_output_path。
