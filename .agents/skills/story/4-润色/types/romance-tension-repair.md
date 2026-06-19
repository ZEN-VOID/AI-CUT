# Romance Tension Repair Type

本类型包用于 `4-润色` 中修复言情、暧昧、甜虐、替身、破镜、追妻、宫廷/职场/幻想恋爱等关系场面的“拉扯弱、情绪模板化、亲密边界不清”的局部坏点。它只强化源章已有关系压力，不新增关系结果。

## Trigger Signals

- 用户要求强化言情拉扯、暧昧张力、内心推拉、甜虐、吃醋、误会或关系边界。
- 场面只有脸红、心跳、占有、宠溺、虐感标签，没有欲望和回避。
- 对白没有潜台词，人物直接把爱恨和误会说透。
- 亲密动作与身份、关系阶段、场景风险不匹配。
- 关系场景没有改变信任、债务、试探、边界或下一步行动。

## Repair Method

1. 锁定当前关系状态、误会/债务/承诺、不可改关系结果和 affected span。
2. 判断本场关系功能：靠近、退让、试探、误读、拒绝、保护、嫉妒、亏欠或破裂预兆。
3. 只补潜台词、停顿、距离、物件误触、称谓变化、共同风险或选择代价。
4. 保留人物身份和声口；不把所有关系都写成强占、有奖宠爱或高甜高虐模板。
5. 修后确认关系有微推进或微反转，但没有改变源章关系结果。

## Prohibitions

- 不新增告白、亲吻、和解、分手、误会解除、怀孕、掉马或关系定性。
- 不用脸红、心跳、眼神拉丝、占有欲清单替代关系压力。
- 不把人物写油、写降智或写成纯奖励对象。
- 不把言情拉扯修成动作戏或权力压迫戏。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 关系修补是否保留源章关系结果和人物身份边界？ | `minimal_repair` | `FAIL-POLISH-SCOPE` | `P3-REPAIR-PLAN` | relationship source anchor |
| 是否把欲望/回避、边界、潜台词和选择代价落到 prose？ | `genre_texture_density` | `FAIL-POLISH-TEXTURE` | `P4-CREATIVE-POLISH` | before/after evidence |
| 是否避免脸红模板、占有奖励和纯糖/纯虐清单？ | `genre_scene_integrity` | `FAIL-POLISH-GENRE-SCENE` | `P4-CREATIVE-POLISH` | boundary check |
