# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-Validation` 父技能的经验层知识库，不是第二份阶段合同。
- 每次调用 `4-Validation` 时，应与 `SKILL.md` 一起加载，用于识别 pack 缺口、并发聚合错误、返工路由漂移与 review/loopback 接驳问题。
- 冲突优先级固定为：用户显式请求 > AGENTS.md / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 缺少 `validation_fact_pack` 某个 slice，却仍进入子技能验收 | covenant gate | 立刻阻断为 `FAIL-COVENANT`，停止 child dispatch | 在父层写死“先 pack 后 child，缺 slice 不得补猜” | 五维子技能不再消费残缺 pack |
| 5 份 MD 报告被误当成平行总真源 | composite output contract | 只保留 MD 为 sidecar，聚合 JSON 才能拥有 `validation_status` | 在 `_shared/validation-root-contract.md` 固定单一 gate truth | 下游 `review/5-Loopback` 只读取 aggregate JSON |
| 明明是 `0-Init / Cards / Planning` 真源冲突，却被打回 `3-Drafting` 重写 | source trace routing | 把问题改判为 `back_to_source_contract` | 在 issue 级字段中强制保留 `source_layer_owner` | drafting 不再背锅修上游 truth |
| 5 个子技能并发时各自读取了不同版本正文或不同 pack | concurrency contract | 统一锁当前轮正文快照与 pack，重新分发 | 父层合同写死“同一快照、同一 pack、先锁再并发” | 五维报告的 `manuscript_ref` 与 `pack_ref` 一致 |
| 子技能直接给出总分或总路由，抢了父层裁决权 | parent-child boundary | 将子技能收回到 `dimension_packet + report_ref` | 在 child output contract 写死“不得判定最终 validation_status” | 聚合字段只在父层出现 |
| `PASS` 后只生成审查报告，没有 machine-readable gate packet | canonical output design | 把 aggregate JSON 设为正式 gate sink | 采用“JSON canonical + MD sidecar”双层输出 | `review/5-Loopback` 可以直接消费结构化字段 |
| 失败只写“打回 drafting”，没有节点级返工入口 | rework routing contract | 聚合 `rework_targets` 到 step 级别 | 在子技能 issue 字段中要求 `rework_target_step` | 每个 high/critical issue 都能精确回流 |
| `7-润色` 被误当成最终通过，而 `4-Validation` 被降成可选参考 | stage boundary drift | 把 drafting 的终点收回为 `candidate_final_draft` | 在 `3-Drafting` 与 `4-Validation` 合同中明确“最终 PASS 只归终验层” | loopback 不再直接消费 drafting 终稿 |
| 新增 validation 维度时，需要在多个兄弟文件里手动同步 | canonical registry gap | 抽出维度注册表并让父层回指 | 以 `validation-dimension-registry.yaml` 作为 step hook 与终验 mandatory 的单一真源 | 增删维度主要只改 registry + child package |
| 已定义 validator registry，但 runtime 不会自动 dispatch drafting inline validations | runtime landing gap | 把 registry 接到 `workflow_manager.py`，在 `complete-step` 后自动触发 batch，并通过 `record-inline-validation` 写回结果 | 新增 validation 机制时，必须同时核对“合同 + registry + runtime + tests”四层是否已联通 | `story-write` 在 inline validation 未过时会真实阻断下一 step |
| hook batch 已能自动触发，但没有本地 baseline validator runner，仍要人工逐条补结果 | runner automation gap | 补 `validation_runner.py`，先以 rule-based baseline 自动产出 sidecar + structured result，再由 workflow 自动写回 batch | 新增/调整维度时，把“registry + child skill + runner handler + CLI/test”视为同一套真源联动 | manuscript 存在时，inline validation 可以自动完成记录；缺 evidence 时再降级为 pending |
| type-pack 已进入 runtime，但类型兑现问题仍被结构维度吞并，导致返工节点与错误归因不稳定 | validation dimension boundary | 把 `type-pack-fit-validator` 提升为 registry 中的独立维度，并为其补 child skill + runner handler | pack.validation、registry、runner、child skill 四层一起维护独立维度，不再让结构维度顺带背锅 | aggregate JSON 中能单独看到 `类型兑现` verdict，且回流节点更稳定 |

## Repair Playbook

1. 先确认这轮是否重新生成了当前 pack，而不是复用旧验证残包。
2. 再检查 5 个子技能是否都消费了同一份正文快照与同一份 pack。
3. 若 aggregate 与子技能结论冲突，优先修 `_shared/validation-child-output-contract.md` 与聚合字段合同，不先改 child prose。
4. 若某问题看起来像正文缺陷，先问一句：上游 truth 是否其实已经自相矛盾。
5. 若 `PASS` 了却无法接到 `review/5-Loopback`，优先检查 aggregate JSON 的字段齐全度与 route 值，而不是先改下游阶段。
6. 若用户声称“润色后已经算成品”，优先回到阶段边界检查，而不是直接放行 loopback。

## Reusable Heuristics

- `4-Validation` 最值钱的不是“多写 5 篇意见书”，而是把 5 维意见收束成一份可继续驱动系统的 gate packet。
- 子技能并发成立的前提不是“目录分开了”，而是“输入快照先锁住了”。
- 一旦 issue 涉及 source truth owner，就不要再用“正文修一下”掩盖问题；这种返工几乎都会重复失败。
- 5 份 MD 更适合人工阅读和复盘，1 份 JSON 更适合工作流接驳；两者可以共存，但真源只能有一个。
- 对验收阶段来说，`FAIL-COVENANT` 比 `FAIL-QUALITY` 更值得优先处理，因为后者建立在前者输入可靠的前提上。
- 如果 aggregate JSON 已经存在，但没有 issue 级 `rework_targets`，那它仍然不是一个可执行的验收结论。
- 最省维护成本的做法不是减少 validator，而是把“哪些 validator 在什么 step/什么阶段运行”收束到单一 registry。
- 当一个质量问题是“写得不差但完全不像当前项目声明的类型”时，不要继续塞给结构兑现；这类问题要交给独立的类型兑现维度。
