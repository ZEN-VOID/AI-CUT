# Atmosphere Pressure Repair Type

本类型包用于 `4-润色` 中修复“氛围淡、场景空、压迫感弱、感官颗粒没有服务当前戏”的局部坏点。它不是装饰性氛围层，而是把源章已有空间、物件、声音、沉默和环境反应转成场景压力。

## Trigger Signals

- 用户要求补氛围、压迫感、现场感、沉浸感，但不希望改剧情。
- 源章有冲突或危险，但场景像空白背景。
- 氛围只靠“压抑、阴冷、诡异、暧昧、肃杀”等抽象词。
- 感官描写很多，却没有推动信息延迟、空间限制、关系压力或行动选择。
- 润色后删掉了源章中有用的物件、距离、声音、沉默或身体反应。

## Repair Method

1. 先找源章已有的压力锚：门、窗、走廊、桌面、纸张、伤口、脚步、灯、屏幕、雨声、沉默、人群距离等。
2. 选择 1-2 类最有效感官，不做五感补全。
3. 让场景颗粒承担功能：遮蔽、逼近、误会、犹豫、暴露、隔断、倒计时或章末追问。
4. 环境反应必须由人物动作、道具状态、空间结构、既有天气或既有设定触发。
5. 修后检查氛围是否让冲突更难逃开，而不是形成独立装饰段。

## Prohibitions

- 不新增源章没有的雨、雪、烟、火、光源、气味、人群、警报或灾害。
- 不用“电影感、氛围感、高级感、宿命感”替代小说内事实。
- 不让环境描写抢走人物动作链、信息推进和关系压力。
- 不把每个场景都写成同一种暗色、压抑或诗性语气。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 氛围修补是否锁定源章已有物件、空间、声音或沉默？ | `minimal_repair` | `FAIL-POLISH-SCOPE` | `P3-REPAIR-PLAN` | source anchor list |
| 场景颗粒是否服务冲突、信息、关系、空间限制或章末牵引？ | `genre_texture_density` | `FAIL-POLISH-TEXTURE` | `P4-CREATIVE-POLISH` | pressure-function evidence |
| 是否避免无源天气、光源、气味和装饰性环境段？ | `genre_scene_integrity` | `FAIL-POLISH-GENRE-SCENE` | `P4-CREATIVE-POLISH` | boundary check |
