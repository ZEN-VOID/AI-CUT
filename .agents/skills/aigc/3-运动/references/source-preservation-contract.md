# Source Preservation Contract

本文件定义 `3-运动` 的上游保真和处理范围。

## Scope

`3-运动` 处理：

- 角色身体移动：走、跑、退、靠近、离开、绕过、跨过、跌倒、坐下、起身。
- 身体部位运动：伸手、抬头、回头、转身、偏身、抓握、松开、推开、拉近。
- 位置或状态迁移：从门口到桌边、从站立到跪坐、从握住到放开、从面对 A 到背向 B。
- 多人动作关系：一人靠近、另一人让开、追随、阻挡、被带动或维持背景状态。

默认不处理：

- 纯静态环境描写。
- 单纯心理、主题、氛围或世界观解释。
- 摄影语言、机位、景别、运镜、焦点、分镜编号、图像 prompt 或视频请求。

## Source Preservation Rules

1. 不改写 source 的剧情事实、对白、场景顺序、角色关系和因果。
2. 引号内对白逐字保留；运动扩写只能发生在对白外的原有运动承载字段值中，不得新增字段承接对白解释。
3. 可以补空间和动作连续性，但不得新增原文没有的目标、冲突、攻击、逃跑、摔倒或道具结果。
4. 任意来源模式必须记录 `source_path`、`source_kind` 和用户指定输出路径；不能把任意来源伪装成项目 canonical 产物。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 运动扩写是否只处理角色动作或状态迁移，没有误收纯环境静态描写？ | `GATE-MOTION-02` | `FAIL-MOTION-CANDIDATE` | `steps/motion-workflow.md#N2-MOTION-CANDIDATE-SCAN` | motion unit index 与跳过原因 |
| 输出是否未改写剧情、对白、场景顺序和角色关系？ | `GATE-MOTION-01` | `FAIL-MOTION-SOURCE` | `N5R-MOTION-REPAIR`、source diff | source preservation diff summary |
| 输出是否没有越权写入摄影、图像或视频字段？ | `GATE-MOTION-08` | `FAIL-MOTION-HANDOFF` | `Output Contract`、`guardrails/guardrails-contract.md` | forbidden term scan 和人工 review 结论 |
