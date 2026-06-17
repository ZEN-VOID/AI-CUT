# Visual Readability Repair Type

本类型包用于 `4-润色` 中修复“读者看不清谁在哪里、动作如何发生、视线/明暗/空间信息混乱”的局部坏点。它吸收旧光影技能的可读性部分，但不做独立光影美化。

## Trigger Signals

- 动作段缺少站位、距离、方向或遮挡，读者无法判断人物关系。
- 光线、阴影、明暗、视线或物件反射被写成抽象气氛，不能帮助读者理解现场。
- 场景转换后空间状态不清，动作像漂浮在空中。
- 关键证据、物件或表情被修得太顺，反而失去可见性。
- 段落中多个主体同时动作，但没有主次和视觉落点。

## Repair Method

1. 锁定读者必须看清的主体、物件、空间边界或信息落点。
2. 用最少文字补足方向、距离、遮挡、明暗或视线关系。
3. 光影只服务可读性：谁被照到、哪里看不清、什么材质反光、哪个动作被遮住。
4. 保留源初稿事实和段落骨架，不改动作结果。
5. 修后检查读者能否用一句话复述“谁在哪里，对谁做了什么，什么信息被看见或遮住”。

## Prohibitions

- 不把光影变成审美展示。
- 不新增灯、火、窗、屏幕、雨雪、烟雾等源章没有的实体。
- 不输出摄影、灯位、镜头或视频 prompt 语言。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 修复是否让动作、空间、视线或信息落点更可读，而不改剧情事实？ | `regression_structure_logic` | `FAIL-POLISH-REGRESSION` | `P3-REPAIR-PLAN` / `P4-CREATIVE-POLISH` | regression issue map |
| 光影/明暗是否只服务阅读可见性，没有变成独立美化层？ | `genre_texture_density` | `FAIL-POLISH-TEXTURE` | `P4-CREATIVE-POLISH` | before/after evidence |
