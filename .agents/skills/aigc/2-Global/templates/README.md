# 2-Global Templates

`2-Global` 不再在 `templates/` 中维护 Markdown 业务输出模板。

## Current Rule

- 唯一 creative business output：`projects/aigc/<项目名>/2-Global/第N集.json`
- 唯一 JSON 填写模板：`.agents/skills/aigc/2-Global/templates/episode-root.template.json`
- `output-template.md` 只是 Skill 2.0 校验器需要的输出合同索引，不是业务输出内容模板
- `validation-report.md` 是治理侧车，不是创作业务输出模板

## Removed Legacy Templates

以下旧模板不得恢复为新链路模板：

- `全局风格.template.md`
- `全集类型元素.template.md`
- `分组类型元素.template.md`
- `导演意图.template.md`

若历史项目迁移需要读取旧 Markdown 结构，应优先从已确认的 `第N集.json` 派生一次性迁移材料，不得让 Markdown 模板重新成为 `2-Global` 的业务输出真源。
