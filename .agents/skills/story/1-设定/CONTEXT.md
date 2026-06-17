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
| 用户只说“完善 cards / 卡片体系” | 父层导引需求，不一定是全部对象卡全量创作 | 先锁任务模式与命中对象，再只调度相关子技能 | 输出中能说明本轮调度了哪些子技能、哪些未调度 |
| 根 `1-设定/SKILL.md` 越写越像对象细则 | 父层侵入子技能 owner | 把对象判断、字段细则、模板说明下沉到对应 child skill | 根层只保留路由、依赖、写回、gate |
| 某张卡内容完整但 validator route 报错 | trace parity 漂移 | 先查模板 `source_skill_id / module_route`，再查 writer 和 validator 常量 | gate finding 能指向正确 child path |
| 物品卡开始自造角色专属逻辑 | 依赖链被绕过 | 回读角色卡 `exclusive_item_hooks` 与场景卡 `rule_and_risk` 后重写物品适配 | 物品卡能说明归属、启用条件、代价和场景限制 |
| 技能、科技、法术、武功、枪械、厨艺等能力没有正式 owner | card taxonomy 缺口 | 路由到 `技能卡`，用 `skill_taxonomy + activation_rules + limits_and_costs + progression_model + counterplay` 收束 | `1-设定/5-技能卡/**/*.json` 与技能索引可被 writer/validator 追溯 |
| 风格/全局/类型仍被拆成 `1-设定` 子技能 | north_star owner 漂移 | 把世界规则、写法合同、题材方向盘融合进 `0-初始化/north_star.yaml` | `1-设定` 下只保留角色/场景/物品/技能 |
| 文档改完但脚本仍跑旧路径 | runtime parity 漂移 | 同步检查 `cards_writer.py`、`cards_coverage_validator.py`、相关 tests | 文档、脚本、测试指向同一 child skill 路由 |
| 子技能包保留独立 workflow 目录或把运行经验放进知识库目录 | runtime-spine 真源漂移 | 把节点、路由、gate、Mermaid 收回子技能 `SKILL.md`；执行经验写 `CONTEXT.md`；删除旧 workflow/经验目录 | `skill-2.0` delivery validator 不再报告 unsupported module，活动合同无旧 workflow 引用 |
| 只想修一个对象却生成整套空卡 | 选择性调度失效 | 父层只聚合实际命中的子技能 patch，不补未调度对象 | 输出不包含未执行子技能的占位字段 |
| subagents 启用但没有按项目 team 请教 | 顾问请教层 | 回读 `../_shared/team-advisor-consultation-contract.md`，优先用 `team.yaml -> roles.planning.members` 请教并汇流 | 把 `advisor_consultation_packet` 固定为子技能 LLM 创作前上下文 | 报告能追溯 roster 来源、问题类型、可执行指导或降级说明 |

## Repair Playbook

1. 先判定这是父层问题、子技能问题、运行时问题，还是单卡内容问题。
2. 若父层文档过重，优先删减对象细则并回指子技能，不把根层写成第二套对象规范。
3. 若 gate 报 route / trace / schema 错，先修 source parity，再讨论内容润色。
4. 若涉及角色、场景、物品、技能联动，按 `角色 -> 场景 -> 物品 -> 技能` 回溯，不从技能端倒推世界规则。
5. 若涉及题材与 planning，先确认 `north_star.yaml.genre_contract` 是否正式承接，再处理 planning 投影。
6. 若涉及风格漂移，先确认 `north_star.yaml.style_contract` 是否把上游承诺转成写法 gate，而不是复述 pitch。
7. 非平凡修复后，至少运行对应 cards writer / validator 的局部检查；无法运行时要说明原因。
8. 若本轮启用 subagents，先检查顾问问题是否足够具体：角色问成长/关系，场景问规则/返场，物品问归属/代价，技能问限制/克制；泛泛风格意见不能进入 card payload。
9. 若升级 Skill 2.0 子技能，优先检查旧 workflow 目录、重复运行经验目录、types/references 中的旧 workflow 指向，以及 `test-prompts.json` 是否齐备。

## Reusable Heuristics

- `1-设定` 根层最有价值的能力是“导引技能组”，不是把六类对象的细则全部复制到一个长文档里。
- 子技能越完整，父层越应该薄：父层只保留 topology、route、dependency、writeback、gate 和 root-cause closure。
- `north_star.yaml` 中的 `global_contract / genre_contract / style_contract` 是长篇写作的三个方向盘：世界怎么运作、读者以什么期待阅读、正文应该怎样写。
- `角色卡`、`场景卡`、`物品卡`、`技能卡` 是可写戏的四段依赖链：谁进入什么空间，用什么杠杆，凭什么能力行动，付什么代价。
- 技能卡的“技能”按广义能力理解：科技、法术、武功、枪械、战术、厨艺、才艺、职业能力都可以进入同一 owner。
- 类型方向盘现在归 `north_star.yaml.genre_contract`，在思考顺序上仍早于角色、场景、物品。
- 风格合同不负责兜底世界设定；一旦 `style_contract` 开始写力量体系，说明应回到 `global_contract` 修边界。
- 物品卡不负责发明角色命运；它只能消费角色接口与场景规则，把道具变成剧情杠杆。
- 对内容创作型任务，脚本输出再完整也只能算 carrier 或 projection；canonical creative truth 必须来自 LLM 判断。
- 设定阶段的 team 顾问价值在于帮对象成立：谁能推动戏、什么空间能反复写、什么物件能改变局面、什么能力能制造选择压力。
- 父层聚合时只写入实际发生的有效 patch；“结构看起来完整”的空字段会污染后续 planning 与 drafting。
- cards 系统的长期稳定性取决于五层一致：父层路由、子技能合同、本地模板、writer、validator/tests。

## Stable Boundaries

| boundary | rule |
| --- | --- |
| 父层与子技能 | 父层不决定对象内容，只决定进入哪个 owner |
| 子技能与脚本 | 子技能给出创作真源，脚本只负责机械落盘和校验 |
| 项目记忆与技能经验 | 项目偏好写 `MEMORY.md`，跨项目修复经验写本 `CONTEXT.md` |
| 北极星与 planning | `genre_contract` 是题材真源，planning 只消费最小投影 |
| 北极星与 drafting | `style_contract` 给 gate，drafting 写正文 |
| 角色卡与 上下文回流 | 角色卡给成长合同，上下文回流 只 actualize 已验证变化 |

## Anti-Patterns

- 在根 `SKILL.md` 里新增某类对象的完整字段解释，而不是更新对应子技能。
- 为了“看起来完整”而让未调度子技能生成空 payload。
- 把 `0-初始化` seed、planning 草稿或用户口头承诺直接当 `1-设定` 正式真源。
- 让 validator 只检查文件存在，不检查 route、schema、density 与依赖关系。
- 把脚本生成的字段拼接结果当成已完成的创作判断。
- 修改子技能路径后不扫 writer / validator / tests / registry / markdown 链接。

## Quick Checklist

- 本轮模式是否明确：single / mixed / full-build / repair / source-contract-fix？
- 是否只调度了命中的子技能？
- 是否加载了父层、项目层和命中子技能的上下文？
- 是否保持 LLM-first creative authorship？
- 正式输出是否只落在角色/场景/物品/技能四类设定根？
- writer、validator、tests 是否仍与 child skill route 一致？
- 失败时是否能指向最窄根因，而不是泛泛说“cards 不完整”？
