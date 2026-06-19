# Xuanhuan Power Repair Type

本类型包用于 `4-润色` 中修复玄幻、修仙、高武、异能、系统或奇幻能力兑现段落里的“只有光效和爽点、规则边界不清、代价消失”的局部坏点。它只强化已有能力的触发、边界、资源消耗和环境反馈，不新造体系。

## Trigger Signals

- 用户要求强化玄幻能力表现、修仙法术、高武气血、异能兑现、系统奖励或升级爽点。
- 能力段只有光芒、威压、爆裂、碾压，没有规则触发、代价或边界。
- 升级/突破缺少身体、资源、环境或见证者认知变化。
- 战力表现与既有等级、技能卡、道具或世界规则不一致。
- 能力让冲突无代价解决，削弱人物选择和后续后果。

## Repair Method

1. 锁定已有能力、境界、资源、技能卡或章级 planning 约束。
2. 标出能力兑现的 3-5 个必要点：触发条件、资源消耗、可见反馈、边界/失败风险、余波后果。
3. 用身体、环境、道具、见证者认知或对手判断表现能力，不用纯光效替代因果。
4. 若源章没有升级结果，不新增突破；若已有突破，只补清过程和代价。
5. 修后确认能力没有越级、无代价、无规则地解决问题。

## Prohibitions

- 不新增境界、功法、技能、系统奖励、法宝效果或战力等级。
- 不把所有能力写成金光、威压、爆炸和旁人震惊。
- 不改胜负、伤亡、突破结果或后续任务状态。
- 不把玄幻能力写成现代科技或视频特效说明。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 能力修补是否锁定既有能力真源和 affected span？ | `minimal_repair` | `FAIL-POLISH-SCOPE` | `P3-REPAIR-PLAN` | power source anchor |
| 能力是否有触发、边界、资源代价和可见反馈？ | `genre_scene_integrity` | `FAIL-POLISH-GENRE-SCENE` | `P4-CREATIVE-POLISH` | power boundary evidence |
| 是否避免纯光效爽点、越级和新造能力体系？ | `regression_structure_logic` | `FAIL-POLISH-REGRESSION` | `P4-CREATIVE-POLISH` | no-rule-change check |
