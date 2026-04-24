# TODO

- [x] 补齐 `review/`、`steps/`、`types/`、`knowledge-base/`、`README.md` 与本文件，完成 Skill 2.0 最小非空分区。
- [x] 将真人版古装写实影视全局风格最佳实践接入 `SKILL.md`、字段映射、思行网络、模板、review gate 与入口元数据。
- [x] 将旧模板中的动画/国漫并列示例降级，避免污染默认真人古装风格词。
- [x] 移除独立 `分组类型元素` 模板与投影引用，组级类型信号统一回收到 `groups[].global.类型元素`。
- [x] 将 `SKILL.md` 收束为 input/output 首尾合同，并把运行时 creative 输出统一为按集 `第N集.json`。
- [x] 移除 `templates/` 中的旧 Markdown 输出模板，仅保留 README 边界说明，避免误导为业务输出内容模板。
- [x] 回收本技能内部 `_shared/`：将 I/O、写回合同迁入 `references/`，将按集 JSON 模板迁入 `templates/`。
- [x] 为 Skill 2.0 校验器补 `templates/output-template.md` 索引，并声明它不是业务输出内容模板。
- [ ] 后续若其他项目类型稳定复用，补充分类型风格基线示例。
- [ ] 后续若新增全局风格机械校验器，将 `review/review-contract.md` 的人工 gate 同步为脚本辅助检查。
