# Review Type Map

`4-Review` 存在多模式处理：正式终验、运行时修复、维度维护和 Skill 2.0 结构修复。本文件负责先形成 `type_profile`，再让 `steps/` 与 `review/` 消费。

## Type Profile

| variable | allowed values | meaning |
| --- | --- | --- |
| `domain_type` | `story` | 小说 workflow |
| `artifact_type` | `volume_manuscript`、`aggregate_json`、`dimension_sidecar`、`skill_package` | 本轮主要处理对象 |
| `execution_type` | `provider-assisted`、`script-assisted`、`manual-governed`、`hybrid` | 执行方式 |
| `topology_type` | `hybrid` | 串行锁包、并行维度、串行聚合 |
| `review_type` | `code-reviewer`、`structural-validator`、`local-checklist` | 审计方式 |
| `output_type` | `validation_json`、`repair_route`、`skill_patch` | 交付类型 |

## Mapping Matrix

| type signal | step impact | reference impact | review impact |
| --- | --- | --- | --- |
| `artifact_type=volume_manuscript` | 进入 `N1 -> N5` 正式终验主干 | 读取 fact pack spec 与 registry | 聚合维度 verdict |
| `artifact_type=aggregate_json` | 先检查 JSON 字段完整度和下游 route | 读取 root runtime contract | 运行 aggregate gate |
| `artifact_type=dimension_sidecar` | 回到对应 child skill 与 child output contract | 读取 registry report filename | 检查 sidecar 不越权 |
| `artifact_type=skill_package` | 进入 Skill 2.0 结构修复 | 读取 legacy upgrade matrix | 运行工作车间 validator |
| `execution_type=provider-assisted` | N3 必须收 provider sidecar | 读取 provider aggregation rules | findings 必须进 aggregate |
| `review_type=local-checklist` | 仅在上层阻断 provider 时使用 | 最终报告说明降级 | 不得伪称真实 provider 已运行 |

## Anti-Patterns

- 不要把子技能 sidecar 当成 `validation_status` 真源。
- 不要为修单个 child 的 prose 改写父层 registry。
- 不要在 `steps/` 中复制完整维度表；维度名单只看 registry。
