# Style Card Review Contract

| dimension | pass condition |
| --- | --- |
| route | `module_route` 指向 `风格卡` |
| projection | 风格字段是写法合同，不是上游字段镜像 |
| gate | `style_gate` 可被 drafting/review 消费 |
| template | payload 对齐 `templates/style-card.json` |
| trace | `loaded_references` 包含本 `SKILL.md`、`CONTEXT.md` 与本地模板 |
