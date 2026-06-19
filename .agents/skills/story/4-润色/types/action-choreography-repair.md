# Action Choreography Repair Type

本类型包用于 `4-润色` 中修复已有章节里的动作设计弱点：动作像流水账、站位不清、攻防没有判断、受力没有代价、余波没有承接。它只修源章已有动作场面的可读性和戏剧功能，不从零设计新战斗，不改胜负、伤亡、能力规则或关系结果。

## Trigger Signals

- 动作不精彩、打斗像技能列表、追逐没有空间路线。
- 读者看不清谁先动、从哪里打到哪里、为什么这一招有效。
- 只有“快、狠、强、爆开”等结果词，没有动作路径、受力、材质响应或身体代价。
- 动作段与人物选择、关系压力或章末牵引脱节。
- 用户要求“强化动作设计 / 动作细节扩写 / 打斗更有设计感”，但同时要求不改剧情结果。

## Repair Method

1. 锁定 `source_anchor` 和 `affected_span`，确认源章已经存在动作场面。
2. 标出动作链的 3-7 个必要 beat：入场压力、起手、抵抗/变招、破局、代价、余波。
3. 只补清方向、距离、接触点、受力、材质响应和人物代价；不新增新招式结果。
4. 把动作和人物意图绑定：动作必须体现选择、迟疑、试探、保护、报复、留手或失控。
5. 修后检查动作段是否仍服务当前章义务、信息推进和章末牵引。

## Prohibitions

- 不把非武侠动作默认写成武侠剑气。
- 不输出动作设计说明书、分镜、摄影、视频 prompt 或招式表。
- 不新增胜负、伤亡、爆炸、能力规则、道具效果或场景破坏等级。
- 不为了“更燃”把人物智商、身体限制或既有规则写崩。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 是否锁定源章动作场面的 source anchor 和 affected span？ | `minimal_repair` | `FAIL-POLISH-SCOPE` | `P3-REPAIR-PLAN` | `source_anchor`、`affected_span` |
| 动作修补是否补清方向、距离、受力、代价和余波，且不改胜负或能力规则？ | `genre_scene_integrity` | `FAIL-POLISH-GENRE-SCENE` | `P4-CREATIVE-POLISH` | before/after evidence、beat map |
| 动作是否服务人物选择、信息推进或章末牵引，而不是独立炫技？ | `genre_texture_density` | `FAIL-POLISH-TEXTURE` | `P4-CREATIVE-POLISH` | action-function evidence |
