# Type Map

## Type Profile

| variable | states | meaning |
| --- | --- | --- |
| `entry_state` | `from_detail | from_request | from_bound_request | repair` | 本轮从哪个产物层进入 |
| `storyboard_scope` | `storyboard_group | single_frame | comic_page` | 对象范围 |
| `reference_state` | `none | unresolved | bound | prompt_only_override` | 参照图状态 |
| `provider_state` | `builtin_image_gen | jimeng_cli | nano_banana | dual_mode | pending` | provider 选择状态 |
| `output_mode` | `json_only | full_trace | handoff_pack` | 输出模式 |

## Mapping Matrix

| type signal | route | reference impact | review impact |
| --- | --- | --- | --- |
| `entry_state=from_detail` + `storyboard_scope=storyboard_group` | `S0 -> S1 -> S2 -> S3 -> S4` | 可先保留空引用槽位 | 审计锁组、组内顺序、prompt 和模板映射 |
| `entry_state=from_request` + `reference_state=unresolved` | `S0 -> S5 -> S6` | 必须保守绑定或显式 prompt-only | 审计候选证据 |
| `entry_state=from_bound_request` | `S0 -> S7 -> S8` | 保持 provider-neutral 字段 | 审计 provider 解析 |
| `storyboard_scope=single_frame` | reroute | 不在本包执行 | 回 `A.分镜画面` |
| `storyboard_scope=comic_page` | reroute | 不在本包执行 | 回 repo-local `comic` |
| `provider_state=dual_mode/pending` | hold | 不落最终 provider plan | 输出推荐主案和缺口 |
| `reference_state=none` + Assets 非空且无覆盖 | block | 先回绑定 | 防止静默 prompt-only |

## Default Type Profile

```yaml
domain_type: aigc
artifact_type: markdown+json
execution_type: hybrid
topology_type: serial-with-branches
review_type: structural-validator+local-checklist
output_type: package
```
