# Type Map

本文件是 `story-init` 的类型包索引。执行时先读取本文件形成 `type_profile`，再把命中的类型包作为固定上下文加载；`knowledge-base/` 只做按需检索，不替代类型包。

## Package Index

| package_id | selection_signal | context_files | relationship | review_gate |
| --- | --- | --- | --- | --- |
| `init-routing` | 任意 `story-init` 调用、首次初始化、重初始化、自动组队或自定义组队 | `types/init-type-map.md` | default required package | `types` / `integration` |

## Default Package Rule

- 默认必须加载 `init-routing`，因为它包含媒介路由、初始化运行类型、team 编组、证据类型、执行形态和 handoff 类型的基础判型。
- 当用户输入同时包含小说与影视意图时，不得靠默认包强行判为 story；必须先按 `medium_type=ambiguous` 阻断或澄清。
- 当用户未提供 roster 时，`team_lineup_mode` 可默认进入 `auto`，但必须记录 `mode_source=defaulted_by_skill` 或等价来源。
- 若后续新增更细类型包，新增包只能补充 `init-routing`，不得覆盖它的媒介路由和 team 真源边界。

## Loading Flow

1. 读取 `SKILL.md + CONTEXT.md` 后立即读取本文件。
2. 根据用户请求、项目根和已有 runtime 形成 `type_profile`。
3. 加载 `types/init-type-map.md` 作为固定上下文。
4. 将 `type_profile` 传入 `steps/init-workflow.md` 的 `N0 -> N7` 节点。
5. 在 `review/review-contract.md` 与 `review/init-review-gate.md` 中检查类型判定是否造成媒介路由、team 编组或 handoff 写回漂移。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否已先加载类型包索引并选择 `init-routing` 固定上下文？ | `types` | `FAIL-INIT-TYPE-MAP` | `types/type-map.md`、`types/init-type-map.md` | type_profile、loaded type packages |
| 类型判定是否避免把 film/video/aigc 请求误落到 `projects/story/`？ | `route` / `types` | `FAIL-INIT-ROUTE` | `types/init-type-map.md`、`SKILL.md` Scope | medium_type 判定记录 |
| `auto/custom` 编组是否由类型画像进入唯一 team 路线，而不是恢复旧问卷模式？ | `mode` / `types` | `FAIL-INIT-MODE` | `types/init-type-map.md`、`references/mode-and-team-contract.md` | team_lineup_mode、mode_source |
