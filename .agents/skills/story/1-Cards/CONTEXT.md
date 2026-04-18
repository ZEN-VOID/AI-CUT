# CONTEXT.md

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: ~14534
current_lines: ~237
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-04-08T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 执行者仍把角色/场景/物品当三个 skill 调度 | source-layer routing contract | 回到 `1-Cards/SKILL.md` 与 `workflow_manager.py`，统一改为单 skill + references | 在主技能中写死 `references` 不是子技能，并移除旧 skill id | 全仓不存在活跃 `story2026-character-cards / scene-cards / item-cards` 入口 |
| 全量建卡时顺序被打乱 | cards orchestration contract | 恢复 `角色 -> 场景 -> 物品` 固定顺序 | 在主技能和 references index 中同时写死顺序 | 物品卡不再缺角色钩子 |
| 角色/场景/物品都产出了，但覆盖率仍明显偏薄 | coverage gate contract | 先跑 `cards-check`，定位缺失桶位与密度断层 | 把 blocking finding 直接升级为 `FAIL-QUALITY` | gate 不再默认 PASS |
| 物品卡又回到模板化通用道具 | reference loading contract | 强制补读角色模块 reference 与角色卡切片 | 在 item module 中把专属适配写成硬门禁 | 专属物能一眼看出归属角色 |
| 场景卡重新滑回“漂亮布景板” | scene function contract | 回到 scene module，先补功能、规则、危险 | 在 scene module 中固定“规则先于奇观” | 场景能回答“谁来、做什么、代价是什么” |
| cards 仍依赖 `0-Init` 私有 worldbuilding 文档，导致共享工法和对象层消费链断裂 | shared worldbuilding routing | 改为从 `templates/worldbuilding/` 读取 character / faction / power / rule 工法 | 固化“跨阶段世界构建知识进 shared templates root，cards modules 只声明消费关系” | 角色/场景/物品 module 都能说明自己读取哪份共享 worldbuilding 资产 |
| `cards-check` 只看桶数量与索引，不看单卡 schema/正文结构，导致空壳卡也能过 gate | coverage gate contract | 在 `cards_coverage_validator.py` 下钻到每张正式卡，校验 `core/current_state/history` 与模块强制字段 | 让 S8 同时承担“trace + index + single-card structure”三层门禁，并用壳卡失败测试锁住 | `{\"ok\": true}` 这类占位卡不再通过 coverage gate |
| cards profile 只读 `.webnovel/state.json`，未消费 `north_star_contract / 初始化简报`，导致规则刚性与对象约束低估 | upstream truth consumption | 在 validator 合并 `north_star_contract.json + 初始化简报.json + state.json` 做 profile 推断 | 将 `north_star` / handoff 设为 coverage gate 的正式上游，并把规则刚性写入 profile 输出 | 强规则项目即使 state 较弱，也会提高 surreal / scene_link / ownership 门槛 |
| 模板和 validator 已声明 trace 字段，但正式建卡链路没有统一 writer 落盘这些字段 | formal writeback contract | 新增 `cards_writer.py`，统一从模板写卡/索引并强制注入 `module_route / loaded_references / writeback_plan` | 把 `cards-write` 接入 `story.py`，并用“写卡后再跑 cards-check”回归锁住真实产物 | 正式 `Cards/**/*.json` 不再出现 trace 字段只存在于模板、实际产物为空的情况 |
| governed reference 模块已经目录化，但 `module-spec.md` 仍像字段摘要卡，导致执行者要回父技能猜阶段与门禁 | reference module governance | 回到各模块 `module-spec.md`，按共享模板补齐 `适用场景 / 预加载上下文 / 思维链 / Phase / 交付 / 验收机制` 六块合同 | 把“目录化只是外壳，六块合同才是 governed reference 成立条件”写进根 CONTEXT 与模块 CONTEXT | 仅读模块文档即可判断何时进入、怎么执行、何时回接 gate |
| 模块已经有 `Think-Think Design Snapshot`，但只有三轴三重标题，没有进入字段锋利度与增强验证层 | think-think execution depth | 回到模块 `## 3. 思维链`，补 `Observed Facts / Inferred Gaps / Protected Constraints / Proposed Rewrite`、`驱动/判废/对比` 字段、`轴权归属检查 / 近邻替换压测 / 落盘扰动测试` | 把“执行到位”的门槛从“看得见三轴三重”提升为“字段可归属、可压测、可扰动、可落盘” | 关键字段改动后会真实影响 `FIELD-CD-*` 或模板/说明槽位，而不只是文案变好看 |
| 初始化已生成 `TEAM.toml`，但 `1-Cards` 执行时不读取 `策划` 布阵 | stage team governance | 在 `1-Cards/SKILL.md` 把 `TEAM.toml` 升级为必读输入，并要求有策划 AGENTS 时必须伴随后台多 subagents 会诊 | 将“策划团队参与 cards 决策并落盘”写成根技能硬规则，而不是初始化提示语 | 执行 `1-Cards` 时能明确区分“无策划组单跑”与“有策划组并行会诊后落盘” |

## Repair Playbook

1. 先判断问题是路由错、reference 漏载，还是单卡内容失真。
2. 若是多模块同时失真，先修主 `SKILL.md` 与 `references/README.md`。
3. 若是单模块失真，先修对应 module reference，再修卡片内容。
4. 若是“看起来有卡但不够厚”，直接跑覆盖率校验，不做体感争论。
5. 若是增量回写，最后回查是否污染了无关卡层。

## Reusable Heuristics

- `1-Cards` 最容易失控的不是写不出卡，而是路由漂移；所以单技能真源比“三个看似清楚的子技能”更稳。
- 角色卡的最高杠杆不是多加设定，而是先补功能桶和关系边。
- 场景卡最值钱的是“可写戏”，不是“有画面”。
- 物品卡最值钱的是“归属 + 代价 + 剧情作用”，不是“设定说明”。
- 长篇项目的 cards 问题，常常不是 schema 不对，而是密度不够。
- reference 模块应该像手术刀，而不是第二套权力中心。
- 一旦某份 cards reference 进入治理范围，最稳的结构不是继续堆单文档，而是直接升格成 `references/<module>/module-spec.md + CONTEXT.md`，这样路由合同和局部经验层才不会互相污染。
- 如果某份世界构建知识会同时服务初始化和对象建卡，就应提升到共享 `templates/worldbuilding/`，而不是继续从 `0-Init` 私有 `references/` 借读。
- `cards-check` 只有同时消费索引层、单卡层、north star 约束层，才配叫最终 gate；任何只看“数量”的 validator 都会把空壳 cards 放过去。
- 强规则项目的门槛不能只看 `state.json` 的摘要词；若 `north_star_contract.cards` 已经写了规则系统与 enforcement focus，coverage gate 必须把它算进 profile。
- 对 `1-Cards` 来说，模板、writer、validator 必须三件套一起成立；只改其中一层，trace 合同最终都会漂回“文档存在、产物缺席”。
- 对 governed references 来说，“已经拆目录”不等于“已经治理完成”；只有父技能路由、模块六块合同和模块 `CONTEXT` 三件套同时成立，模块才算真正接回主链路。
- 对 `think-think` 来说，“已经写出三轴三重”也不等于“已经执行到位”；真正过线的是：事实/推断已分层，关键字段已拆成驱动/判废/对比，且至少经过轴权、替换、扰动三类验证中的核心项。
- `1-Cards` 这类大 skill 的 frontmatter `description` 若开始解释流程而不是触发条件，会让执行者跳过后文真源与路由合同；保持 `Use when...` 式触发描述更稳。
