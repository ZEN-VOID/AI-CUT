# Type Package Map

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `source-upstream-writing-directing` | `types/source/upstream-writing-directing.md` | 默认项目模式、`2-编导/第N集.md`、编导稿 | stackable | `types/source/upstream-writing-directing.md` | none | none |
| `source-arbitrary-text` | `types/source/arbitrary-text.md` | 用户显式给小说、剧本、任意 Markdown 或非项目 source | stackable | `types/source/arbitrary-text.md` | none | none |
| `motion-character-action` | `types/motion/character-action.md` | 角色动作、身体动作、位置变化、朝向变化、动作链 | stackable | `types/motion/character-action.md` | none | none |
| `continuity-adjacent-frame-state` | `types/continuity/adjacent-frame-state.md` | 需要前后画面位置回顾、时间轴推导、运动连续性 | stackable | `types/continuity/adjacent-frame-state.md` | none | none |

## Default Package Rule

1. 项目模式默认加载 `source-upstream-writing-directing`、`motion-character-action` 和 `continuity-adjacent-frame-state`。
2. 用户显式指定任意小说或剧本来源时，追加加载 `source-arbitrary-text`。
3. 若 source 没有明确角色动作或状态迁移，不进入扩写，输出阻断或 review-only finding。
4. 类型包只提供固定上下文和判型边界；具体运动扩写仍由 LLM 直接完成。

## Loading Flow

1. `N1-MOTION-SOURCE-LOCK` 读取 source 和用户请求。
2. 选择 source 类型包和 motion/continuity 类型包。
3. 将命中包作为固定上下文交给 `steps/motion-workflow.md`。
4. `review/review-contract.md` 按已加载类型包检查覆盖和边界。
