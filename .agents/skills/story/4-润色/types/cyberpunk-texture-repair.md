# Cyberpunk Texture Repair Type

本类型包用于 `4-润色` 中修复赛博朋克段落里的“只有霓虹标签、科技与阶层压迫脱节、高科技低生活不成立”的局部坏点。它只把已有赛博元素压回身体、债务、监控、公司权力和城市生活成本，不新增世界观真源。

## Trigger Signals

- 用户要求强化赛博、赛博朋克、义体、公司监控、霓虹城市、黑客、低生活质感。
- 源章只有霓虹、雨夜、广告屏、机械义肢等表层符号。
- 技术没有让身体、身份、债务、医疗、权限、隐私或劳动处境变得更沉重。
- 巨型企业、平台、安保、数据信用或义体厂商只是背景名词。
- 黑客/义体/脑机段落像万能技能，没有代价、权限和风险。

## Repair Method

1. 锁定已有赛博元素：义体、芯片、广告屏、城市网格、公司安保、数据权限、医疗债务、黑客工具等。
2. 选择 2-3 个压迫锚点：身体租赁、维修费用、权限封锁、监控记录、算法评级、企业安保、药物依赖、数据抵押。
3. 把“高科技低生活”落成人物动作和处境：付款失败、权限拒绝、义体疼痛、广告追踪、身份被平台改写。
4. 保持题材边界：赛博质感服务当前冲突、关系或信息推进，不变成城市设定说明。
5. 修后确认赛博元素改变了人物选择或风险，而不是只增加视觉装饰。

## Prohibitions

- 不新增公司、帮派、义体等级、黑客能力、城市制度或科技规则。
- 不把赛博朋克写成霓虹雨夜、蓝紫光、广告屏的装饰清单。
- 不让黑客或义体无代价解决问题。
- 不输出设定集、道具说明、分镜或视觉 prompt。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 赛博修补是否来自源章已有赛博元素和项目题材轴？ | `minimal_repair` | `FAIL-POLISH-SCOPE` | `P3-REPAIR-PLAN` | cyber source anchor |
| 是否把高科技低生活落到身体、债务、权限、监控或公司权力？ | `genre_texture_density` | `FAIL-POLISH-TEXTURE` | `P4-CREATIVE-POLISH` | pressure anchor evidence |
| 是否避免霓虹装饰清单和新世界观设定？ | `genre_scene_integrity` | `FAIL-POLISH-GENRE-SCENE` | `P4-CREATIVE-POLISH` | boundary check |
