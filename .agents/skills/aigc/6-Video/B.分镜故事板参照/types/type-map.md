# Type Map

本文件定义 `B.分镜故事板参照` 的模式判定和分型策略。

## Mode Matrix

| mode | required_existing_input | route | skipped stages |
| --- | --- | --- | --- |
| `distill_only` | `3-Detail/<episode>.json` | `N1 -> N2 -> N5` | `reference-binding`、`generation-handoff` |
| `bind_references` | stable request JSON from `distill/` or legacy `全能参照` | `N1 -> N3 -> N5` | `distill` if source exists、`generation-handoff` |
| `handoff_provider` | stable request JSON with resolved reference mode | `N1 -> N4 -> N5` | `distill`、`reference-binding` if already resolved |
| `full_chain` | `3-Detail/<episode>.json` | `N1 -> N2 -> N3 -> N4 -> N5` | none |
| `compat_migration` | old artifacts from `全能参照 / 2-参照引用 / 3-视频生成` | targeted node only | all unrelated stages |

## Reroute Signals

| signal | action |
| --- | --- |
| single `分镜ID` / first-frame anchor | reroute to `A.分镜画面参照` or `1-提示词蒸馏/首帧参照` |
| request asks to generate image assets | reroute to `5-Image` |
| provider runtime failure | reroute to provider skill or external provider troubleshooting |
| no stable `3-Detail` root | stop and return to `3-Detail` |
| existing `Assets/` candidates but empty references and no `no_reference` statement | mode becomes `unresolved`, run `bind_references` before handoff |

## Type Profile Output

Every run should establish:

- `mode`
- `project_name`
- `episode_id`
- `group_scope`
- `source_request`
- `reference_state`
- `provider_state`
- `output_root`
