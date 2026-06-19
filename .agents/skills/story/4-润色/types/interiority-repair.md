# Interiority Repair Type

本类型包用于 `4-润色` 中修复“内心戏浅、心理转折突兀、人物只做外部反应”的局部坏点。它补的是源章已成立压力下的心理暗流和认知过程，不新增人物动机、创伤、关系结果或剧情事实。

## Trigger Signals

- 用户要求加强内心戏、心理暗流、欲望压抑、创伤回声、第一人称内在节奏。
- 人物行为成立但心理承托太薄，读者看不到为什么此刻选择沉默、退让、反击或失控。
- 情绪只剩“愤怒、难过、害怕、心动”等标签。
- 人物心理突然转向，缺少触发物、记忆回声、误读、恐惧或欲望牵引。
- 关键关系场景里只有动作和对白，没有未说出口的压力。

## Repair Method

1. 锁定 `source_anchor`：当前事件压力、人物欲望/恐惧、关系位置和不可改事实。
2. 判断内心戏承担的功能：解释选择、制造误读、压住真相、暴露欲望、延迟爆发或形成章末牵引。
3. 只补 1-3 处短促心理暗流，优先落在触发物、错觉、记忆闪回、未说出口的句子或身体反应之后。
4. 保留源章声口和视角距离；第一人称可更贴近意识流，第三人称不强塞全透明心理说明。
5. 修后确认心理补丁推动行为、对白或关系压力，而不是独立抒情段。

## Prohibitions

- 不新增源章没有的人物创伤、隐藏动机、爱恨转折或关系结论。
- 不把内心戏写成作者解释、心理分析报告或长篇自白。
- 不让人物把所有推理、情绪和欲望都说透。
- 不用抽象词堆叠替代具体触发物和选择压力。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 内心戏是否来自源章压力和人物既有状态，而非新增动机？ | `minimal_repair` | `FAIL-POLISH-SCOPE` | `P3-REPAIR-PLAN` | pressure/desire evidence |
| 心理补丁是否推动选择、对白、关系或章末牵引？ | `genre_texture_density` | `FAIL-POLISH-TEXTURE` | `P4-CREATIVE-POLISH` | before/after evidence |
| 是否避免作者解释腔、心理报告腔和全透明说明？ | `chinese_prose` | `FAIL-POLISH-PROSE` | `P4-CREATIVE-POLISH` | offending excerpt |
