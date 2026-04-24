# Reference Binding Contract

## Purpose

把稳定单帧 request JSON 中的 `reference_images / image_markers` 绑定到真实本地图片，同时保留 provider-neutral 与 provider-specific 双层兼容。

## Modes

- `jimeng_cli`: 本地路径直传。
- `nano_banana`: BASE64-compatible，默认 `pending_encode`。
- `dual_mode`: 同时保留两类 provider 兼容槽位。

## Candidate Evidence

| evidence_level | 可绑定条件 | 默认动作 |
| --- | --- | --- |
| `explicit_subject` | 结构化字段出现完整角色名，且本地唯一匹配 | 允许绑定 |
| `explicit_scene_anchor` | 组级主空间锚点唯一 | 允许绑定，每组默认不超过 2 个 |
| `explicit_prop_full_name` | 完整复合道具名唯一 | 允许绑定 |
| `provider_required_ref` | 上游 `image_markers[].related_subject` 显式要求 | 允许绑定 |

## Ambiguity Gate

以下信号不得直接绑定，只能进入 `ambiguous_candidates / rejected_candidates / skipped_candidates`：

1. 单字或泛词，如 `门`、`灯`、`墙`、`水`、`床`、`地面`。
2. 高频空间词，如 `卫生间`、`吊顶`、`楼道`、`洗手池`、`门板`，除非它是组级主空间锚点且同类唯一。
3. 子串命中。
4. 一个 token 命中 2 张及以上资产。
5. 只靠 prompt 全文包含而没有字段位证据的匹配。

## Output

- `第N集.json`
- `_manifest.json`
- `match-report.md`
- `next_entry`

`match-report.md` 必须展示 bound、ambiguous、rejected 三类候选，以及每个候选的 `match_reason / evidence_level / evidence_field / confidence`。

## Script Boundary

旧绑定脚本 `.agents/skills/aigc/5-Image/2-参照引用/scripts/bind_reference_assets.py` 可作为保守绑定辅助。执行后必须用旧审计脚本或等价 review gate 检查路径、槽位、歧义与 `next_entry`。
