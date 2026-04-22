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
| 初始化已经有 `reader_promise / genre`，但 cards 没有正式类型卡 | cards type coverage | 新增 `类型卡` 子技能包、模板、writer/validator/tests 接口 | 固定“题材方向盘先落 `1-Cards/5-类型卡`，再由 planning 导入” | `1-Cards/5-类型卡/**/*.json` 可正式落盘 |
| 初始化已经有 `reader_promise / aesthetic_axes / style_system`，但 cards 没有正式风格卡 | cards object coverage | 新增 `风格卡` 子技能包、模板、writer/validator/tests 接口 | 固定“整书风格契约也属于 1-Cards 对象真源” | `1-Cards/1-风格卡/**/*.json` 可正式落盘 |
| 风格卡只复述上游承诺，没有把风格投射成写法合同 | style projection gap | 把风格卡主字段改成 `总体基调 + 叙事/对白/画面/语言/场面风格` | 固定“风格卡输出写法主骨架，而不是上游字段镜像” | 风格卡能直接指导 Drafting/Validation |
| 仍把角色/场景/物品当 `references` 模块加载 | parent routing contract | 回到 `1-Cards/SKILL.md`，改为直连 child skill dispatch | 在父技能、writer、validator、tests 同时锁定 child skill 路由 | `module_route` 不再出现 `references/*-module` |
| 子技能文档已改，但 writer/validator 仍写旧 route | runtime parity | 同步改 `cards_writer.py`、`cards_coverage_validator.py` 与 tests 常量 | 把 route parity 提升为 completeness audit 必检项 | 文档、脚本、测试命中同一 child path |
| template 改了 `source_route`，但 validator 不检查 | trace contract | 在 validator 增加 `meta.source_route / source_skill_id / loaded_references` 校验 | 任何 child skill path 升级都要做 trace parity 测试 | 错 route 会被 gate 拦住 |
| 对象子技能已经独立，但模板仍留在 `1-Cards/templates` 根层 | canonical source layering | 把模板下沉到对应 child skill 包内，并让 writer/validator/tests 都消费 child-local template path | 固定“对象私有模板跟对象子技能同包，父层只保留总线合同” | 根层不再出现对象私有 `templates/` |
| 写卡流程每次正常结束后仍在项目目录残留大量空 `.lock` | writeback lock cleanup policy | 在 `security_utils.atomic_write_json()` 增加“释放后清理空锁文件”开关，并让 `cards_writer.py` 默认开启、同时保留显式关闭入口 | 对写卡流程固定“默认清理空锁壳、需要保留时显式声明”的策略，并用 `test_cards_writer.py` 锁住默认/保留两条路径 | 默认写卡后项目目录不再堆积空 `.lock`，显式 `keep` 时仍可保留 |
| 物品卡重新绕过角色/场景接口直接补设定 | cross-skill consistency | 回到 `物品卡`，强制读取角色接口与场景规则 | 在父技能写死 mixed/full-build 顺序为 `角色 -> 场景 -> 物品` | 物品 blocking finding 能指回缺失上游 |
| 只改文档，不改 tests | source-layer closure | 反查 `test_cards_writer.py` 与 `test_cards_coverage_validator.py` | cards 系统改动视为“文档 + runtime + tests”三件套 | pytest 覆盖 route parity 与 schema parity |
| cards 系统看起来有卡，但 route trace 不可信 | completeness audit | 跑 `cards-check` 并核对 trace 输出 | validator 既查存在，也查 route/source parity | 报告里能看到正确 child skill trace |
| 类型判断停留在 seed 或口头说明，没有进入正式 cards 真源 | cards type truth gap | 让 `cards_writer.py` / `cards_coverage_validator.py` 统一只认 `类型卡` | 固定“题材承诺必须是卡，不是 seed 附注” | cards gate 能直接检查 `类型卡` 是否存在且字段完整 |

## Repair Playbook

1. 先判断问题是父层路由、child 合同、writer、validator 还是 tests 漂移。
2. 若文档与运行时分离，优先修 runtime parity，不先润色 prose。
3. 若 trace 不可信，先看 template/source_route，再看 writer，再看 validator。
4. 若物品侧异常，先回查角色接口和场景规则是否稳定，再修物品内容。
5. 非平凡重构结束后，必须重跑 cards 相关定向测试。

## Reusable Heuristics

- `1-Cards` 的高杠杆不是把对象细则放在根文档里，而是让父 skill 只做总线，把判断权稳定下沉到 child skills。
- 对 `story2026` 来说，世界观、规则体系、年代约束、文化艺术、科技/武功与金手指不该散落在 `0-Init` 旁注里，而应进入正式 cards 真源，通过 `全局卡` 持有。
- 对 `story2026` 来说，题材承诺、主副类型组合、禁飞区与题材走廊不该继续挂在 planning 临时 artifact 上，而应进入正式 cards 真源，通过 `类型卡` 持有。
- 对 `story2026` 来说，`reader_promise / aesthetic_axes / cards.style_system` 不是风格卡的最终字段，而是上游种子；风格卡应把它们投射成总体基调、叙事风格、对白风格、画面风格等写法合同。
- cards 体系一旦从 `references` 迁到 child skills，最容易漏掉的不是文档，而是 writer/validator/tests 的 route 常量。
- 对 `1-Cards` 这类高频批量写入链路，锁文件本身只是并发保护载体，不是业务工件；若写入结束后只剩空壳 `.lock`，默认应在释放后清理，避免项目目录被锁壳淹没。
- 风格卡不应该替全局卡兜底世界设定；一旦风格卡开始承载力量体系和金手指，说明 cards 真源分层又塌了。
- `module_route` 只检查“存在”不够，必须检查“是否指向正确 child skill”。
- 角色、场景、物品三类卡的强依赖关系没有变，变的是承载它们的源层形态：从 governed reference 升格为 governed child skill。
- 真正的系统完善度，不是“新增了 child skills”，而是 template / writer / validator / tests / child contracts 五层同时对齐。
- 对 `1-Cards` 来说，模板若还挂在父层，就说明真源分层还没收完；最稳的形态是“父层管总线，模板跟着对象子技能走”。
- 若题材承诺已经会改变 planning/drafting/validation 的判断，却还进不了 cards coverage，系统很快会出现“正文像这个题材，但对象支撑不像这个题材”的断层。
