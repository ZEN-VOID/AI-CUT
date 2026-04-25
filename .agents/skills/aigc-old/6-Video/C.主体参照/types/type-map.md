# Type Map

本文件定义 `C.主体参照` 的模式判定和分型策略。

## Mode Matrix

| mode | required_existing_input | route | skipped stages |
| --- | --- | --- | --- |
| `distill_only` | `3-Detail/<episode>.json` | `N1 -> N2 -> N6` | `reference-binding`、`generation-handoff` |
| `identify_subjects` | `3-Detail/<episode>.json` or stable request JSON | `N1 -> N3 -> N6` | `distill` if source exists、asset binding、`generation-handoff` |
| `bind_subject_references` | stable request JSON and subject index or enough detail evidence | `N1 -> N3 -> N4 -> N6` | `distill` if source exists、`generation-handoff` |
| `handoff_provider` | stable request JSON with resolved reference mode | `N1 -> N5 -> N6` | `distill`、`reference-binding` if already resolved |
| `full_chain` | `3-Detail/<episode>.json` | `N1 -> N2 -> N3 -> N4 -> N5 -> N6` | none |
| `compat_migration` | old artifacts from `全能参照 / 2-参照引用 / 3-视频生成` | targeted node only | all unrelated stages |

## Subject Scope Matrix

| subject_scope | primary directories | default policy |
| --- | --- | --- |
| `角色` | `Assets/角色/` | 只绑定角色身份参照，服装可作为关联说明 |
| `服装` | `Assets/服装/` | 只绑定服装参照，必须关联角色或穿搭来源 |
| `道具` | `Assets/道具/` | 只绑定可见且对动作或叙事有贡献的道具 |
| `场景` | `Assets/场景/` | 只绑定稳定场景空间，不把氛围词当场景 |
| `全部主体` | `Assets/角色/`、`Assets/服装/`、`Assets/道具/`、`Assets/场景/` | 按角色、服装、道具、场景顺序绑定 |

## Reroute Signals

| signal | action |
| --- | --- |
| single `分镜ID` / first-frame anchor | reroute to `A.分镜画面参照` or `1-提示词蒸馏/首帧参照` |
| storyboard / manga board is the primary reference | reroute to `B.分镜故事板参照` |
| request asks to generate image assets | reroute to `5-Image` |
| provider runtime failure | reroute to provider skill or external provider troubleshooting |
| no stable `3-Detail` root | stop and return to `3-Detail` |
| existing subject `Assets/` candidates but empty references and no `no_reference` statement | mode becomes `unresolved`, run `bind_subject_references` before handoff |

## Type Profile Output

Every run should establish:

- `mode`
- `project_name`
- `episode_id`
- `group_scope`
- `subject_scope`
- `source_request`
- `subject_index_state`
- `reference_state`
- `provider_state`
- `output_root`
