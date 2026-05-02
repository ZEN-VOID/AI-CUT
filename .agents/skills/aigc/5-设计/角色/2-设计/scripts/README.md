# Scripts Boundary

`角色/2-设计/scripts` 只承载机械辅助脚本或说明，不承载创作正文生成逻辑。

Allowed:

- 读取 `角色清单.md` 并检查必需列。
- 检查输出目录是否存在。
- 检查每个角色设计稿是否包含必填标题。
- 统计英文提示词字符数。
- 检查研究层八个镜头和 `Prompt Evidence Chain` 标题是否存在。
- 解析 `references/design-slot-review-contract.md` 的 `ROLE-BUNDLE-01`，输出 required slots 供 review gate 逐项验收。
- 汇总文件 manifest 或空字段报告。

Forbidden:

- 自动生成研究考据。
- 自动生成身份、职业、阶层、地域年代、服饰工艺、身体姿态、禁区、不确定性或 prompt evidence chain 正文。
- 自动生成物语、视觉解构、服装设计或摄影描述。
- 自动拼接英文 prompt。
- 根据关键词扩写角色设计稿。
- 修改 `角色清单.md`、registry、父级 skill 或其他 worker 范围。

Any future script must provide a dry-run mode when it changes files, and must document that it is mechanical assistance only.
