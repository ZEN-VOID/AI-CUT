# Character Reaction Repair Type

本类型包用于 `4-润色` 中修复“人物像在被作者摆布、反应虚、对白说明腔或表演腔”的局部坏点。它只辅助 `P3-REPAIR-PLAN` 与 `P4-CREATIVE-POLISH`，不得扩大为整章重写。

## Trigger Signals

- 人物只被写成情绪标签，没有可见反应。
- 对白只传达信息，缺少身份、关系、试探、遮掩或冲突。
- 连续句子堆微表情、呼吸、眼神，像在做表演示范。
- 关键情绪默认落到脸色变化或抽象心理说明。
- 润色后人物气口被统一成作者口吻。

## Repair Method

1. 锁定 affected span，不动无关段落。
2. 标出当前事件压力、人物欲望/回避、关系位置和不可改事实。
3. 只替换虚的表达坏点：优先用动作、停顿、物件接触、站位、对白潜台词或沉默承载。
4. 保留初稿已成立的声口、句群骨架和信息顺序。
5. 修后检查人物反应是否推动信息揭示、关系变化或下一步行动。

## Prohibitions

- 不新增人物动机、关系转折或剧情结果。
- 不把“更有表演感”理解为补更多身体通道。
- 不把所有对白改得更锋利；身份、地位和处境不支持时应保留笨拙、迟疑或沉默。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 修复是否保留初稿事实和人物气口，只修虚反应/说明腔坏点？ | `minimal_repair` | `FAIL-POLISH-SCOPE` | `P3-REPAIR-PLAN` | diff summary |
| 人物反应是否从情绪标签变成可读行为、对白潜台词或关系动作？ | `genre_texture_density` | `FAIL-POLISH-TEXTURE` | `P4-CREATIVE-POLISH` | before/after evidence |
