# CONTEXT.md

## Context Health

<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: ~6200
current_lines: ~90
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-04-26T00:00:00-07:00
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

| situation | likely_root | preferred_response | verification_point |
| --- | --- | --- | --- |
| 用户只说“完善 cards / 卡片体系” | 父层导引需求，不一定是六类卡全量创作 | 先锁任务模式与命中对象，再只调度相关子技能 | 输出中能说明本轮调度了哪些子技能、哪些未调度 |
| 根 `1-Cards/SKILL.md` 越写越像对象细则 | 父层侵入子技能 owner | 把对象判断、字段细则、模板说明下沉到对应 child skill | 根层只保留路由、依赖、写回、gate |
| 某张卡内容完整但 validator route 报错 | trace parity 漂移 | 先查模板 `source_skill_id / module_route`，再查 writer 和 validator 常量 | gate finding 能指向正确 child path |
| 物品卡开始自造角色专属逻辑 | 依赖链被绕过 | 回读角色卡 `exclusive_item_hooks` 与场景卡 `rule_and_risk` 后重写物品适配 | 物品卡能说明归属、启用条件、代价和场景限制 |
| 风格卡承载世界规则或力量体系 | 全局卡缺位或父层路由失准 | 把世界规则迁回 `全局卡`，风格卡只保留写法合同 | 风格 gate 不再替代世界观设定 |
| 类型承诺只停留在 init / planning 口头描述 | 类型卡真源缺失 | 补 `1-Cards/5-类型卡`，再让 planning 只导入最小投影 | planning 可回链正式类型卡 |
| 文档改完但脚本仍跑旧路径 | runtime parity 漂移 | 同步检查 `cards_writer.py`、`cards_coverage_validator.py`、相关 tests | 文档、脚本、测试指向同一 child skill 路由 |
| 只想修一个对象却生成整套空卡 | 选择性调度失效 | 父层只聚合实际命中的子技能 patch，不补未调度对象 | 输出不包含未执行子技能的占位字段 |

## Repair Playbook

1. 先判定这是父层问题、子技能问题、运行时问题，还是单卡内容问题。
2. 若父层文档过重，优先删减对象细则并回指子技能，不把根层写成第二套对象规范。
3. 若 gate 报 route / trace / schema 错，先修 source parity，再讨论内容润色。
4. 若涉及角色、场景、物品联动，按 `角色 -> 场景 -> 物品` 回溯，不从物品端倒推世界规则。
5. 若涉及题材与 planning，先确认 `类型卡` 是否正式存在，再处理 planning 投影。
6. 若涉及风格漂移，先确认风格卡是否把上游承诺转成写法 gate，而不是复述 pitch。
7. 非平凡修复后，至少运行对应 cards writer / validator 的局部检查；无法运行时要说明原因。

## Reusable Heuristics

- `1-Cards` 根层最有价值的能力是“导引技能组”，不是把六类对象的细则全部复制到一个长文档里。
- 子技能越完整，父层越应该薄：父层只保留 topology、route、dependency、writeback、gate 和 root-cause closure。
- `全局卡`、`类型卡`、`风格卡` 是长篇写作的三个方向盘：世界怎么运作、读者以什么期待阅读、正文应该怎样写。
- `角色卡`、`场景卡`、`物品卡` 是可写戏的三段依赖链：谁进入什么空间，用什么杠杆，付什么代价。
- `类型卡` 的位置虽然落在 `5-类型卡`，但在思考顺序上通常早于风格、角色、场景、物品。
- 风格卡不负责替全局卡兜底世界设定；一旦风格卡开始写力量体系，说明路由需要回到 `全局卡`。
- 物品卡不负责发明角色命运；它只能消费角色接口与场景规则，把道具变成剧情杠杆。
- 对内容创作型任务，脚本输出再完整也只能算 carrier 或 projection；canonical creative truth 必须来自 LLM 判断。
- 父层聚合时只写入实际发生的有效 patch；“结构看起来完整”的空字段会污染后续 planning 与 drafting。
- cards 系统的长期稳定性取决于五层一致：父层路由、子技能合同、本地模板、writer、validator/tests。

## Stable Boundaries

| boundary | rule |
| --- | --- |
| 父层与子技能 | 父层不决定对象内容，只决定进入哪个 owner |
| 子技能与脚本 | 子技能给出创作真源，脚本只负责机械落盘和校验 |
| 项目记忆与技能经验 | 项目偏好写 `MEMORY.md`，跨项目修复经验写本 `CONTEXT.md` |
| 类型卡与 planning | 类型卡是真源，planning 只消费最小投影 |
| 风格卡与 drafting | 风格卡给 gate，drafting 写正文 |
| 角色卡与 loopback | 角色卡给成长合同，loopback 只 actualize 已验证变化 |

## Anti-Patterns

- 在根 `SKILL.md` 里新增某类对象的完整字段解释，而不是更新对应子技能。
- 为了“看起来完整”而让未调度子技能生成空 payload。
- 把 `0-Init` seed、planning 草稿或用户口头承诺直接当 `1-Cards` 正式真源。
- 让 validator 只检查文件存在，不检查 route、schema、density 与依赖关系。
- 把脚本生成的字段拼接结果当成已完成的创作判断。
- 修改子技能路径后不扫 writer / validator / tests / registry / markdown 链接。

## Quick Checklist

- 本轮模式是否明确：single / mixed / full-build / repair / source-contract-fix？
- 是否只调度了命中的子技能？
- 是否加载了父层、项目层和命中子技能的上下文？
- 是否保持 LLM-first creative authorship？
- 正式输出是否只落在 `projects/story/<项目名>/1-Cards/`？
- writer、validator、tests 是否仍与 child skill route 一致？
- 失败时是否能指向最窄根因，而不是泛泛说“cards 不完整”？
