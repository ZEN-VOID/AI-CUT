# Upstream Context Application Contract

本合同治理 AIGC 主链 `2-编剧 -> 3-美学 -> 4-导演 -> 5-表演 -> 6-氛围 -> 7-分镜 -> 8-摄影 -> 9-光影` 中“已读取上游上下文但未应用”的漂移风险。它不是第二输出真源，只规定上游 context 如何被当前阶段投影、保真和举证。

## Core Rule

- 读取不等于应用。正式生成、repair 或 review 时，凡阶段消费上游输出，必须在执行报告中记录 `Upstream Context Application Map`。
- 上游输出默认是只读 source 或只读 constraint；当前阶段只能把它投影为本阶段 owning dimension 的局部决策，不得反向改写上游真源。
- 当前阶段新增、改写、注入或选择性省略的任何关键内容，都必须能回指上游 `source_anchor` 或明确 N/A / conflict / degradation reason。
- 若报告只能证明“已读取”，不能证明“如何应用”，不得判定 canonical pass。

## Required Map

`Upstream Context Application Map` 至少包含以下字段：

| field | requirement |
| --- | --- |
| `upstream_source` | 上游文件、阶段、集号、读取状态和 source_override 状态 |
| `preserved_truth` | 必须保留的剧情事实、事件顺序、对白、场景、人物关系、画面布局、风格约束或字段结构 |
| `stage_projection` | 当前阶段如何把上游信息转成本阶段 owning dimension 的决策 |
| `source_anchor` | 被应用的上游字段、画面点、分镜行、风格条目或报告证据 |
| `context_used` | 实际使用的上游上下文内容；只读未用不得写成 used |
| `local_decision` | 当前阶段由该上下文导出的具体输出决定 |
| `preservation_check` | 证明没有越权改写上游事实、顺序、对白、空间布局、风格真源或阶段边界 |
| `conflict_or_na` | 冲突、缺失、降级、跳过或 N/A 的原因和返工目标 |

## Application Procedure

1. 锁定上游 source bundle：默认上游路径、用户指定覆盖、项目记忆和相关 `3-美学` 协议。
2. 拆分上游内容：区分 `truth`、`constraint`、`handoff seed`、`style signal`、`non-applicable material`。
3. 投影到当前 owning dimension：只把上游信息转为本阶段有权处理的剧本、风格、导演、表演、氛围、分镜、摄影或光影决定。
4. 逐项绑定输出：每个关键新增、改写、注入、裁决或省略都要回指 `source_anchor`。
5. 做保真差异检查：确认没有无授权新增事实、重排事件、替换对白、重画空间、复制全局 prompt 或覆盖上游风格真源。
6. 报告并过门：执行报告必须给出 `Upstream Context Application Map`，review gate 必须能检验它。

## Stage Projection Matrix

| stage | upstream context | allowed projection | prohibited drift |
| --- | --- | --- | --- |
| `2-编剧` | `1-分集` 或用户指定小说/剧情 source | 剧本化事实保真、声画字段、节奏、高潮和尾钩 handoff | 改因果、改结局、越权写导演/摄影/分镜/prompt |
| `3-美学` | `2-编剧`、项目记忆、参考资料 | 视觉基调、场景/角色/道具/分镜/摄影风格协议 | 父级代写子协议、风格脱离剧情、复制单一口号 |
| `4-导演` | `2-编剧`、`3-美学/画面基调` | 逐画面导演意图、信息差、节奏、表演交接 | 改剧本、替换对白、把风格名套成批注 |
| `5-表演` | `4-导演`、`3-美学` 三类协议 | 同字段融合表演、角色意识、身体/声音/环境响应 | 保留批注、改字段结构、新增剧情事实 |
| `6-氛围` | `5-表演`、`3-美学` 三类协议 | 选择性 `氛围画面`、物理氛围、时间锚点、材质响应 | 每点硬加、无源天气/火/烟/事件、抢走表演焦点 |
| `7-分镜` | `6-氛围` 或指定文稿、`3-美学/画面基调`、`3-美学/分镜风格` | 画面点识别、节拍、构图、起始状态帧、0.5 秒时值 | 改剧情、漏心理/表演/氛围字段、重写上游正文 |
| `8-摄影` | `7-分镜`、`3-美学/画面基调`、`3-美学/摄影风格` | 基于既有空间布局的机位、运动、速度、焦点和一镜到底链路 | 重新发明空间、改分镜秒数、随机套术语 |
| `9-光影` | `8-摄影`、`3-美学/画面基调`、`3-美学/场景风格`、`3-美学/摄影风格` | 可见光源、受光、阴影、色温、材质、动态光和光影连续性 | 新增无源光源/事件、复制全局 prompt、抽象套词 |

## Review Gate

| review_question | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- |
| 是否只记录了读取，而没有说明上下文如何进入当前阶段决策？ | `FAIL-UPSTREAM-CONTEXT-APPLICATION` | 最近的理解、计划或注入节点 | `Upstream Context Application Map` |
| 当前阶段是否把上游 truth 错当成可重写对象？ | `FAIL-UPSTREAM-CONTEXT-DRIFT` | source lock / preservation diff 节点 | `preservation_check` |
| 当前阶段是否把上游风格/批注/分镜/prompt 机械复制为本阶段正文？ | `FAIL-UPSTREAM-CONTEXT-PROJECTION` | owning dimension 计划节点 | `stage_projection`、`local_decision` |
| 缺失上游时是否给出降级、N/A 或阻断原因？ | `FAIL-UPSTREAM-CONTEXT-NA` | intake / source manifest 节点 | `conflict_or_na` |

## Report Boundary

`Upstream Context Application Map` 只保存可审计摘要、证据锚点和裁决结果，不保存冗长思维链、完整草稿或未筛选推演。它服务保真和下游交接，不替代 canonical 创作正文。
