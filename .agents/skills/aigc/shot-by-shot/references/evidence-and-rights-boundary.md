# Evidence And Rights Boundary

本文件定义 `shot-by-shot` 的证据可信度、临摹边界和禁止复制规则。

## Evidence Grade

| grade | meaning | allowed conclusion |
| --- | --- | --- |
| `confirmed` | 直接看见视频、截图或带时间码的素材 | 可给强结论和阶段临摹建议 |
| `partial` | 只看到截图、短片段或用户提供局部描述 | 可给局部结论，必须标注缺口 |
| `inferred` | 依赖用户概述、记忆或间接材料 | 只能给假设性分析和补证需求 |
| `insufficient` | 无可观察证据 | 停止逐镜结论，要求补视频/截图/时间码 |

## Imitation Boundary

允许临摹：

- 镜头功能：建立空间、信息揭示、压迫关系、反应余波、声画交接。
- craft principle：景别变化逻辑、注意力转移方式、停顿/切点策略、光色关系、空间权力。
- 抽象节奏：慢推压迫、急停兑现、反应延迟、声音先行、遮挡揭示。
- AIGC 可执行结构：主体、动作、构图锚点、光色材质、交出点、资产材质和设计画面合同。

禁止照搬：

- 参考片具体台词、角色、剧情事件、标志性姿势、独特造型。
- 参考片具体镜头序列、逐帧构图、镜头数量和剪辑顺序。
- 可识别的 copyrighted set piece、特殊设计、专属视觉符号。
- 明显指向原片的命名、台词梗、独特场面调度组合。

## Rights Gate

每个临摹建议必须回答：

1. 学到的是不是 craft principle？
2. 是否仍依赖参考片具体表达才成立？
3. 替换角色、空间、道具和剧情后是否还能服务目标项目？
4. 是否能用目标项目自己的 `MEMORY.md`、相关 `CONTEXT/`、角色和场景重建？
5. 是否能被项目初始化回读、`4-编剧`、`5-导演`、`6-分镜`、`7-摄影`、`8-分组` 或 `3-主体` 以自己的字段主创吸收？显式 legacy 目标中的 `5-表演 / 9-光影` 必须标注 archived 只读边界。

任何一项失败，建议必须移入 `forbidden-copy ledger` 或降级为风险提示。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每条重要结论是否标注 `confirmed`、`partial`、`inferred` 或 `insufficient`？ | `GATE-SBS-RIGHTS-01` | `FAIL-RIGHTS-EVIDENCE-GRADE` | `N1-INTAKE` | evidence grade table 与 source anchors |
| 证据为 `insufficient` 时，是否停止逐镜强结论并提出最小补证需求？ | `GATE-SBS-RIGHTS-02` | `FAIL-RIGHTS-INSUFFICIENT` | `N1-INTAKE` | blocked reason、补视频/截图/时间码清单 |
| 临摹建议是否只学习镜头功能、craft principle、抽象节奏和 AIGC 可执行结构？ | `GATE-SBS-RIGHTS-03` | `FAIL-RIGHTS-COPY` | `N4-PRINCIPLE` | imitation principle map 与 source_shot_refs |
| 是否排除参考片台词、角色、剧情事件、标志性姿势、独特造型、镜头序列和剪辑顺序？ | `GATE-SBS-RIGHTS-03` | `FAIL-RIGHTS-COPY` | `N4-PRINCIPLE` | forbidden-copy ledger 的逐项禁用记录 |
| 替换成目标项目自己的角色、空间、道具和剧情后，该原则是否仍成立？ | `GATE-SBS-RIGHTS-04` | `FAIL-RIGHTS-PROJECT-FIT` | `N4-PRINCIPLE` | project_fit 与项目记忆 / stage owner 对齐说明 |
| 失败的临摹建议是否移入 forbidden-copy ledger 或降级为风险提示，而不是留在阶段桥接字段？ | `GATE-SBS-RIGHTS-05` | `FAIL-RIGHTS-LEDGER` | `N4-PRINCIPLE` | forbidden-copy / risk ledger 与降级原因 |
