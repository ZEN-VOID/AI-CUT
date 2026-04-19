# CONTEXT.md

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: ~9200
current_lines: ~120
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-04-17T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 初始化已经有 `world_system / golden_finger`，但 cards 没有正式全局卡 | cards object coverage | 新增 `全局卡` 子技能包、模板、writer/validator/tests 接口 | 固定“世界观、规则体系、年代、文化艺术、科技/武功、金手指都属于 1-Cards 对象真源” | `1-Cards/0-全局卡/**/*.json` 可正式落盘 |
| 初始化已经有 `reader_promise / aesthetic_axes / style_system`，但 cards 没有正式风格卡 | cards object coverage | 新增 `风格卡` 子技能包、模板、writer/validator/tests 接口 | 固定“整书风格契约也属于 1-Cards 对象真源” | `1-Cards/1-风格卡/**/*.json` 可正式落盘 |
| 仍把角色/场景/物品当 `references` 模块加载 | parent routing contract | 回到 `1-Cards/SKILL.md`，改为直连 child skill dispatch | 在父技能、writer、validator、tests 同时锁定 child skill 路由 | `module_route` 不再出现 `references/*-module` |
| 子技能文档已改，但 writer/validator 仍写旧 route | runtime parity | 同步改 `cards_writer.py`、`cards_coverage_validator.py` 与 tests 常量 | 把 route parity 提升为 completeness audit 必检项 | 文档、脚本、测试命中同一 child path |
| template 改了 `source_route`，但 validator 不检查 | trace contract | 在 validator 增加 `meta.source_route / source_skill_id / loaded_references` 校验 | 任何 child skill path 升级都要做 trace parity 测试 | 错 route 会被 gate 拦住 |
| 对象子技能已经独立，但模板仍留在 `1-Cards/templates` 根层 | canonical source layering | 把模板下沉到对应 child skill 包内，并让 writer/validator/tests 都消费 child-local template path | 固定“对象私有模板跟对象子技能同包，父层只保留总线合同” | 根层不再出现对象私有 `templates/` |
| 写卡流程每次正常结束后仍在项目目录残留大量空 `.lock` | writeback lock cleanup policy | 在 `security_utils.atomic_write_json()` 增加“释放后清理空锁文件”开关，并让 `cards_writer.py` 默认开启、同时保留显式关闭入口 | 对写卡流程固定“默认清理空锁壳、需要保留时显式声明”的策略，并用 `test_cards_writer.py` 锁住默认/保留两条路径 | 默认写卡后项目目录不再堆积空 `.lock`，显式 `keep` 时仍可保留 |
| 物品卡重新绕过角色/场景接口直接补设定 | cross-skill consistency | 回到 `物品卡`，强制读取角色接口与场景规则 | 在父技能写死 mixed/full-build 顺序为 `角色 -> 场景 -> 物品` | 物品 blocking finding 能指回缺失上游 |
| 只改文档，不改 tests | source-layer closure | 反查 `test_cards_writer.py` 与 `test_cards_coverage_validator.py` | cards 系统改动视为“文档 + runtime + tests”三件套 | pytest 覆盖 route parity 与 schema parity |
| cards 系统看起来有卡，但 route trace 不可信 | completeness audit | 跑 `cards-check` 并核对 trace 输出 | validator 既查存在，也查 route/source parity | 报告里能看到正确 child skill trace |
| cards gate 只读取原始 `type_stack`，没有消费 resolved pack bias，导致不同类型包在 Cards 侧几乎没有差异 | cards type-pack projection gap | 让 `cards_coverage_validator.py` 消费 resolved `type_pack_profile.semantic_tags / cards_projection` | pack 差异必须进入 cards 的规模/密度/线索/关系 gate，而不只停在 trace block | 规则悬疑、女频悬疑、修仙等 pack 会拉高对应 cards coverage 门槛 |

## Repair Playbook

1. 先判断问题是父层路由、child 合同、writer、validator 还是 tests 漂移。
2. 若文档与运行时分离，优先修 runtime parity，不先润色 prose。
3. 若 trace 不可信，先看 template/source_route，再看 writer，再看 validator。
4. 若物品侧异常，先回查角色接口和场景规则是否稳定，再修物品内容。
5. 非平凡重构结束后，必须重跑 cards 相关定向测试。

## Reusable Heuristics

- `1-Cards` 的高杠杆不是把对象细则放在根文档里，而是让父 skill 只做总线，把判断权稳定下沉到 child skills。
- 对 `story2026` 来说，世界观、规则体系、年代约束、文化艺术、科技/武功与金手指不该散落在 `0-Init` 旁注里，而应进入正式 cards 真源，通过 `全局卡` 持有。
- 对 `story2026` 来说，`reader_promise / aesthetic_axes / cards.style_system` 不是抽象上游附录，而应进入正式 cards 真源，通过 `风格卡` 持有。
- cards 体系一旦从 `references` 迁到 child skills，最容易漏掉的不是文档，而是 writer/validator/tests 的 route 常量。
- 对 `1-Cards` 这类高频批量写入链路，锁文件本身只是并发保护载体，不是业务工件；若写入结束后只剩空壳 `.lock`，默认应在释放后清理，避免项目目录被锁壳淹没。
- 风格卡不应该替全局卡兜底世界设定；一旦风格卡开始承载力量体系和金手指，说明 cards 真源分层又塌了。
- `module_route` 只检查“存在”不够，必须检查“是否指向正确 child skill”。
- 角色、场景、物品三类卡的强依赖关系没有变，变的是承载它们的源层形态：从 governed reference 升格为 governed child skill。
- 真正的系统完善度，不是“新增了 child skills”，而是 template / writer / validator / tests / child contracts 五层同时对齐。
- 对 `1-Cards` 来说，模板若还挂在父层，就说明真源分层还没收完；最稳的形态是“父层管总线，模板跟着对象子技能走”。
- 若 pack 已经能改变 planning/drafting/validation 的判断，却还进不了 cards coverage，系统很快会出现“正文像这个题材，但对象支撑不像这个题材”的断层。
