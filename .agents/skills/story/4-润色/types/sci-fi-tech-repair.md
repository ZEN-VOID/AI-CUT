# Sci-Fi Tech Repair Type

本类型包用于 `4-润色` 中修复科幻、硬科幻、软科幻、机甲、星际或未来技术段落里的“科技感弱、技术像标签、代价不显、规则不清”的局部坏点。它只强化已有技术的可感知性、边界、代价和伦理压力，不新造科技体系。

## Trigger Signals

- 用户要求强化科技元素、硬科幻质感、机甲/星舰/AI/义体/算法/能源等技术表现。
- 源章只是写“高科技、先进设备、系统启动”，缺少操作过程、限制、成本或反馈。
- 技术解决问题太万能，没有能源、延迟、权限、故障率、副作用或伦理后果。
- 科技段像说明书，缺人物选择、风险、误判或社会后果。
- 科幻题材味被润成普通都市/动作/悬疑场景。

## Repair Method

1. 锁定已有技术名、用途、操作者、场景目标和不可改规则。
2. 选择 2-4 个技术锚点：接口、权限、延迟、功耗、噪声、热量、材料、故障、数据残留、监管记录、伦理代价。
3. 让技术表现进入人物行动：操作、误判、等待、取舍、被监控、付出代价或承担后果。
4. 若是硬科幻，只修到“逻辑可追踪”；若是软科幻，只修到“规则一致且代价可感”。
5. 修后确认技术没有替代人物选择，且没有凭空解决核心冲突。

## Prohibitions

- 不新造源章没有的黑科技、能源体系、AI 能力、武器等级或文明设定。
- 不把技术写成百科说明、参数表或作者科普段。
- 不用炫酷名词替代技术因果和代价。
- 不让技术无代价解决悬疑、战斗、关系或现实压力。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 科技修补是否只强化源章已有技术，不新造体系？ | `minimal_repair` | `FAIL-POLISH-SCOPE` | `P3-REPAIR-PLAN` | technology source anchor |
| 技术是否有可感知边界、代价、反馈或后果？ | `genre_scene_integrity` | `FAIL-POLISH-GENRE-SCENE` | `P4-CREATIVE-POLISH` | tech boundary evidence |
| 技术表现是否服务人物选择和当前场景功能，而不是说明书？ | `genre_texture_density` | `FAIL-POLISH-TEXTURE` | `P4-CREATIVE-POLISH` | before/after evidence |
