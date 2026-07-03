# Type Package Map

`types/` 保存 text-to-speech 的类型策略和子类型知识包。任务需要分型时，先选择命中的类型包，再形成 `type_profile` 供 `SKILL.md` 的 `Thinking-Action Node Map` 消费。

`knowledge-base/` 另走标准知识库模式：按需检索、切片、向量召回或关键词召回，不作为固定上下文全量加载。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `default` | `types/default/default.md` | no concrete subtype package has been defined yet | fallback | `types/default/default.md` | concrete subtype packages that replace it | none |

## Default Package Rule

- 如果用户显式指定子类型，按用户给定类型建立包。
- 如果用户未指定，基于 text-to-speech 的业务对象预设 3-5 个具体类型包。
- 默认包必须有入口文件，说明用途、命中信号、固定加载内容和与其他包的关系。
- 允许多层级类型，例如 `types/[parent-type]/[child-type]/[child-type].md`。

## Loading Flow

1. 收集用户输入、对象、产物、风格和限制。
2. 根据本索引选择命中的类型包。
3. 加载命中包的 `context_files` 作为固定上下文。
4. 回到 `SKILL.md` 的 `Thinking-Action Node Map`，按节点消费 `type_profile`。
5. 如果 `SKILL.md` 授权 `knowledge-base/`，再按需检索外部资料；思行节点和 Mermaid 执行拓扑仍以主入口 `SKILL.md` 为准。

## Anti-Patterns

- 不要让 `types/` 只有抽象变量表而没有实际知识包。
- 不要把大型检索资料库放入 `types/`。
- 不要在 `references/` 或 `knowledge-base/` 维护第二套类型包真源。
