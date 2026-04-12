# Chain Of Thought Summary

## Field Master Snapshot

| field_id | 对应输出 | 最低要求 | 失败码 |
| --- | --- | --- | --- |
| FIELD-PROP-DESIGN-01 | 阶段定位 | 必须把 `2-设计` 定位为 bridge 下游 synthesis | FAIL-PROP-DESIGN-01 |
| FIELD-PROP-DESIGN-02 | 角色路由 | 必须声明 parallel specialists + prompt + audit | FAIL-PROP-DESIGN-02 |
| FIELD-PROP-DESIGN-03 | shared I/O | 必须锁定 bridge 输入与三份输出 | FAIL-PROP-DESIGN-03 |
| FIELD-PROP-DESIGN-04 | `道具设计.json` | 必须只保留稳定设计事实 | FAIL-PROP-DESIGN-04 |
| FIELD-PROP-DESIGN-05 | `prop_design_prompt.json` | 必须只保留 prompt sidecar | FAIL-PROP-DESIGN-05 |
| FIELD-PROP-DESIGN-06 | 聚合写回 | 必须由父 skill 独占最终写回 | FAIL-PROP-DESIGN-06 |
| FIELD-PROP-DESIGN-07 | 审计报告 | 必须产出 coverage 与 drift flags | FAIL-PROP-DESIGN-07 |
| FIELD-PROP-DESIGN-08 | 下游回接 | 必须明确 `5-Image / multiview-prop` 入口 | FAIL-PROP-DESIGN-08 |

## Thought Pass Snapshot

1. 先锁定 bridge 是否存在。
2. 再锁定本轮是否需要 design master、prompt sidecar 或二者都要。
3. 并行收集结构 / 材质 / 痕迹 patch。
4. 父 skill 先聚合 canonical design，再让 prompt 架构师消费。
5. 最后由审计角色检查 coverage、path normalization 与 drift。

## Hard Gates

1. 不得让 prompt sidecar 反向改写 canonical truth。
2. 不得把错位路径写成新的输出真源。
3. 不得跳过 `1-清单` 直接发明道具设计。
