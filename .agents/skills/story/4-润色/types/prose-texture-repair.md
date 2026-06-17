# Prose Texture Repair Type

本类型包用于 `4-润色` 中修复“场景空、段落平、题材味被磨平、感官颗粒缺失或被误删”的局部坏点。它只做最小局部修补，不授权新增氛围层。

## Trigger Signals

- 源章有冲突，但润色稿只剩说明和结论。
- 空间、物件、身体反应、声音或沉默被删掉，场景压力变空。
- 为了“顺”把长短不齐和局部粗粝磨成均匀短句。
- 题材质感只剩标签，没有场景密度、信息延迟或心理暗流。
- 增加了漂亮但无 source anchor 的天气、光线、气味或环境描写。

## Repair Method

1. 先回读源初稿，找出已经承载压力的物件、空间距离、声音、沉默、身体反应和信息延迟。
2. 只恢复或微调能服务当前冲突的颗粒，不追加装饰段。
3. 修句群节奏时保留长短不齐、断裂、停顿和必要粗粝。
4. 把抽象质感词转成可读场景事实；没有 source anchor 的氛围新增必须删除。
5. 检查改动是否提高追读力，而不是只让文本更规整。

## Prohibitions

- 不用“氛围感、电影感、高级感、宿命感”替代场景事实。
- 不做五感补全。
- 不让环境描写抢走人物动作链和信息推进。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 修复是否保护源章场景密度和句群节奏，没有通用顺滑化？ | `genre_texture_density` | `FAIL-POLISH-TEXTURE` | `P4-CREATIVE-POLISH` | before/after evidence |
| 是否删除无 source anchor 的装饰性氛围新增？ | `minimal_repair` | `FAIL-POLISH-SCOPE` | `P3-REPAIR-PLAN` | issue list |
