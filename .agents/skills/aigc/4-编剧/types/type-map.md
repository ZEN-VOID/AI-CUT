# 4-编剧 Type Map

`types/` 保存题材类型与叙事情节分型策略。类型包只提供分型上下文，不替代 `SKILL.md` 的 `Type Routing Matrix`、节点、gate 或输出合同。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `genre-narrative` | `types/default/default.md` | 任意小说转剧本、题材解析、叙事情节解析、短剧节奏匹配 | always | `types/default/default.md` | none | `SKILL.md` |

## Type Profile Schema

```yaml
type_profile:
  primary_genre: ""
  secondary_genre: ""
  narrative_pattern: ""
  audience_contract: ""
  pleasure_engine: ""
  risk_engine: ""
  episode_shape: "hook-escalation-cliffhanger | payoff-reset-hook | bridge-reveal-hook"
  rewrite_scope: "faithful_projection | controlled_rewrite | user_authorized_restructure"
```

## Default Package Rule

- `genre-narrative` 是当前唯一默认类型包，所有 `4-编剧` 任务都加载它。
- 用户显式指定题材时，先把题材写入 `primary_genre` 或 `secondary_genre`，再用 source 事实校验。
- 用户未指定题材时，按角色欲望、阻碍、信息差、情绪承诺和生产限制推断，不使用空泛市场标签。

## Loading Flow

1. 收集用户输入、source、项目记忆、平台/时长/制作限制。
2. 加载 `types/default/default.md`，建立 `type_profile`。
3. 回到 `N2-SCR-GENRE-NARRATIVE`，把类型画像转成 `genre_narrative_profile` 和 `beat_inventory`。
4. 由 `N4-SCR-RHYTHM-ENGINE` 消费类型画像选择节奏机制。

## Anti-Patterns

- 不要把题材写成单个标签后直接套节奏。
- 不要让 `types/` 自己决定输出路径、改写权限或 review verdict。
- 不要在类型包里保存执行经验；经验写 `CONTEXT.md`。
