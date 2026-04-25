# aigc/2-Global

`aigc/2-Global` 是 `1-Planning` 与 `3-Detail` 之间的导演前置收束阶段。它围绕 `.agents/skills/aigc/2-Global/templates/episode-root.template.json` 模板，按集直写 `projects/aigc/<项目名>/2-Global/第N集.json`。

## Quick Entry

- 调用技能：`$aigc-global`
- 主入口：`SKILL.md`
- 预加载经验层：`CONTEXT.md`
- creative 输出：`projects/aigc/<项目名>/2-Global/第N集.json`
- 治理侧车：`projects/aigc/<项目名>/2-Global/validation-report.md`

## Directory Tree

```text
2-Global/
├── references/
│   ├── io-contract.md
│   ├── writeback-contract.md
│   ├── 全局风格词最佳实践.md
│   ├── 增量写回与兼容投影.md
│   ├── 字段与验收映射.md
│   └── 思行网络.md
├── scripts/
│   └── validate_director_intent.py
├── templates/
│   ├── README.md
│   ├── episode-root.template.json
│   └── output-template.md
├── review/
│   └── review-contract.md
├── steps/
│   └── 全局风格词生成流程.md
├── knowledge-base/
│   └── global-style-heuristics.md
├── types/
│   └── type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## Notes

- `SKILL.md` 保留入口、模式、动态引用、关键门禁与输出合同。
- `references/全局风格词最佳实践.md` 是真人古装写实影视全局风格词的默认最佳实践参照。
- `references/io-contract.md` 与 `references/writeback-contract.md` 承载输入、输出与写回长合同。
- `steps/全局风格词生成流程.md` 只细化 `N3-PROJECT-GLOBAL` 的风格词生成，不替代主思行网络。
- `review/review-contract.md` 只做质量门禁，不改写业务真源。
- 旧 `全局风格.md / 全集类型元素.md / 分组类型元素.md / 导演意图.md` 已回收进 `第N集.json`，不再作为独立输出维护。
- `templates/` 不再放 Markdown 业务输出内容模板，避免误导；`output-template.md` 只是 Skill 2.0 校验索引，唯一填写模板是 `templates/episode-root.template.json`。
