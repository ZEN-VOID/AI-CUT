# Type Map

## Variables

| var_id | layer | observed_signal | states | route |
| --- | --- | --- | --- | --- |
| `V-VISREF-01` | task | 用户目标覆盖哪段链路 | `distill_only / bind_references / handoff_provider / full_chain / compat_migration` | 决定 workflow 起点 |
| `V-VISREF-02` | source | `3-Detail` 是否稳定 | `ready / incomplete / missing` | `ready` 才能 distill |
| `V-VISREF-03` | reference | 引用状态 | `bound / empty / unresolved / ambiguous` | `unresolved/ambiguous` 阻断 handoff |
| `V-VISREF-04` | provider | provider 是否明确 | `explicit / recommend_only / missing` | 决定 handoff 形态 |
| `V-VISREF-05` | execution | provider 是否本地可执行 | `skill_available / external_skill / manual_only` | 决定下一入口 |

## Case Strategy

| case_id | predicate | strategy | pass_standard | fallback |
| --- | --- | --- | --- | --- |
| `C-VISREF-01` | `V-VISREF-01=distill_only` | 只写 `distill/` 三件套 | 不补 reference/handoff 占位 | 无 |
| `C-VISREF-02` | `V-VISREF-01=bind_references` | 读取稳定请求对象并绑定 Assets | match-report 可复核 | 回 distill 补请求 |
| `C-VISREF-03` | `V-VISREF-01=handoff_provider` | 直接做提交前组织 | input_mode 清楚 | 回 reference-binding |
| `C-VISREF-04` | `V-VISREF-01=full_chain` | 串行执行三段 | 任一 gate 失败即停 | 对应节点返工 |
| `C-VISREF-05` | `V-VISREF-03=ambiguous` | 阻断并列候选 | 不猜测绑定 | 人工裁决 Assets |
| `C-VISREF-06` | `V-VISREF-04=recommend_only` | 输出推荐主案与等待裁决 | 不伪造唯一 provider | 等用户确认 |
