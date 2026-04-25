# Frame Image Heuristics

## Stable Heuristics

- 单帧链路的第一门禁是对象范围，不是 provider。
- `source_shot_ids` 长度为 1 是单帧请求能被后续阶段信任的最低证据。
- prompt 的固定英文前缀负责约束单帧、无多格、无文字覆盖；不要再并行维护第二套私有前缀。
- 参照绑定阶段的“少而准”比“多而全”更稳。
- provider handoff 的最小完成物是 `submit-plan.json + submit-brief.md`，不是一张已生成图片。

## Failure Smells

- request JSON 有 `prompt`，但无法回链 `group_id` 和 `source_shot_ids`。
- `match-report.md` 只列已绑定资产，不列 rejected 或 ambiguous。
- `submit-plan.json` provider 是 `dual_mode`。
- `expected_outputs[]` 指向 `Assets/` 或 provider cache。
- 闭环说明只说“已生成”，但没有区分 request ready、handoff ready 和 result outputs。
