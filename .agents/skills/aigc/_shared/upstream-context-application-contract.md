# Upstream Context Application Contract

本合同治理 AIGC active 主链 `2-美学 -> 3-主体 -> 4-编剧 -> 5-导演 -> 6-分镜 -> 7-摄影 -> 8-分组 -> 9-图像 -> 10-画布` 中“已读取上游上下文但未应用”的漂移风险。它不是第二输出真源，只规定上游 context 如何被当前阶段投影、保真和举证。

## Core Rule

- 读取不等于应用。正式生成、repair 或 review 时，凡阶段消费上游输出，必须在执行报告中记录 `Upstream Context Application Map`。
- “上游上下文”不等于“上一序号阶段产物”。它指本阶段被授权消费的完整 source bundle，可包含非相邻早期阶段、用户指定 source、项目 `MEMORY.md/CONTEXT/`、参考资料、远端运行证据、真实视频证据或顾问 packet；上一序号产物只是默认候选之一。
- 上游输出默认是只读 source 或只读 constraint；当前阶段只能把它投影为本阶段 owning dimension 的局部决策，不得反向改写上游真源。
- 当前阶段新增、改写、注入或选择性省略的任何关键内容，都必须能回指上游 `source_anchor` 或明确 N/A / conflict / degradation reason。
- 若报告只能证明“已读取”，不能证明“如何应用”，不得判定 canonical pass。

## Required Map

`Upstream Context Application Map` 至少包含以下字段：

| field | requirement |
| --- | --- |
| `upstream_source` | 上游文件、阶段、集号、读取状态、来源类型（default / non-adjacent / user_override / evidence_only / side_context）和 source_override 状态 |
| `preserved_truth` | 必须保留的剧情事实、事件顺序、对白、场景、人物关系、画面布局、风格约束或字段结构 |
| `stage_projection` | 当前阶段如何把上游信息转成本阶段 owning dimension 的决策 |
| `source_anchor` | 被应用的上游字段、画面点、分镜行、风格条目或报告证据 |
| `context_used` | 实际使用的上游上下文内容；只读未用不得写成 used |
| `local_decision` | 当前阶段由该上下文导出的具体输出决定 |
| `preservation_check` | 证明没有越权改写上游事实、顺序、对白、空间布局、风格真源或阶段边界 |
| `conflict_or_na` | 冲突、缺失、降级、跳过或 N/A 的原因和返工目标 |

## Application Procedure

1. 锁定授权 source bundle：默认上游路径、非相邻 canonical source、用户指定覆盖、项目记忆、`2-美学/类型风格.md`、相关 `2-美学` 协议、远端/真实视频证据和被授权 side context；不要把“上一序号产物”自动等同为唯一上下文。
2. 拆分上游内容：区分 `truth`、`constraint`、`handoff seed`、`style signal`、`non-applicable material`。
3. 投影到当前 owning dimension：只把上游信息转为本阶段有权处理的题材风格、主体命名/资产、剧本、导演、分镜、摄影或分组决定。
4. 逐项绑定输出：每个关键新增、改写、注入、裁决或省略都要回指 `source_anchor`。
5. 做保真差异检查：确认没有无授权新增事实、重排事件、替换对白、重画空间、复制全局 prompt 或覆盖上游风格真源。
6. 报告并过门：执行报告必须给出 `Upstream Context Application Map`，review gate 必须能检验它。

## Stage-Specific Creative Direction Matrix

当阶段不仅要证明“上游如何被应用”，还需要证明“多个上游上下文如何共同引导本阶段方向”时，owning stage 必须在本合同基础上增加阶段专属方向矩阵。方向矩阵不是平行输出真源；它只说明上游 context 分别扮演什么角色、被用作什么判断、落到哪个本阶段决策和证据位置。

`4-编剧` 必须生成 `Upstream Creative Direction Matrix`，并与 `Upstream Context Application Map`、`Type Style Application Map`、`Subject Registry Application Map` 一起进入完成门。

各阶段矩阵名称固定如下：

| stage | matrix | direction scope |
| --- | --- |
| `4-编剧` | `Upstream Creative Direction Matrix` | 编剧创作方向 |
| `5-导演` | `Director Direction Inheritance Matrix` | 导演意图、信息差、节奏和表演交接方向 |
| `6-分镜` | `Storyboard Direction Inheritance Matrix` | 画面节拍、构图、起始状态帧、空间连续和时值方向 |
| `7-摄影` | `Upstream Camera Direction Matrix` | 机位、运动路径、速度、焦点和一镜到底方向 |
| `8-分组` | `Upstream Grouping Direction Matrix` | 组边界、组级风格、首帧衔接、主体统计和下游 handoff 方向 |
| `9-图像` | `Image Upstream Visual Direction Matrix` | 分镜画面、故事板、平面图的视觉生成方向 |
| `10-画布` | `LibTV Upstream Video Direction Matrix` | LibTV 节点、prompt、参照图顺序、settings 和 rerun 边界方向 |

方向矩阵通用字段：

| field | requirement |
| --- | --- |
| `upstream_context` | 上游文件、阶段、项目记忆、用户示例、远端证据或被授权 side context |
| `direction_role` | 剧情真源、题材方向、主体命名、画面基调、分镜/摄影语法、组级生产真源、视频节点证据、审片证据等角色，不得混淆 |
| `used_as` | 实际用于保真、节奏、主体绑定、构图、镜头、分组、prompt、settings、审片方法、verdict 或 operation 的哪类判断 |
| `stage_decision` | 由该上游上下文导出的本阶段决策；`4-编剧` 可命名为 `script_decision`，其他阶段使用 owning dimension 具体字段 |
| `stage_landing` | 正文、prompt、plan、node、report、finding、operation 或执行证据落点 |
| `boundary_check` | 没有越权改写上游事实、题材风格真源、主体注册表或后续阶段权限的检查 |
| `evidence_map` | 对应 source anchor 或阶段报告 map |

缺少 owning stage 要求的方向矩阵、只列“上游输入物”、或不能说明每类上下文如何影响本阶段决策时，必须触发本阶段 `FAIL-*-UPSTREAM-DIRECTION*`，返工到最近的 intake / understanding / planning / report 节点。`4-编剧` 对应 `FAIL-SCR-UPSTREAM-DIRECTION-MATRIX`。

## Stage Projection Matrix

下表列出各阶段默认或常见的最低 source bundle，并不排除用户指定文稿、非相邻早期真源、项目级记忆、生成侧车、运行证据或审片证据。阶段执行时以用户显式输入、目标 `SKILL.md` 的 Input Contract 和本表的 prohibited drift 共同裁决；若 source override 存在，必须在 `Upstream Context Application Map` 中记录 override 理由、保真边界和缺失项降级。

| stage | upstream context | allowed projection | prohibited drift |
| --- | --- | --- | --- |
| `2-美学` | `1-分集` 全量故事源、项目记忆、参考资料 | `类型风格.md`、视觉基调、场景/角色/道具/分镜/摄影风格协议 | 父级代写子协议、题材脱离故事源、复制单一口号 |
| `3-主体` | `1-分集` 全量故事源、`2-美学/类型风格.md`、画面基调、角色/场景/道具风格协议 | 主体注册表、角色/场景/道具清单、设计与生成 handoff；输出 `主体注册表.md` 和 `subject-registry.yaml` | 从 `8-分组` 或剧情印象新增主体、无 source anchor 命名、把设计稿写成注册表 |
| `4-编剧` | `1-分集` 或用户指定小说/剧情 source、`2-美学/类型风格.md`、`3-主体/主体注册表.md`、项目 `MEMORY.md/CONTEXT/` | 剧本化事实保真、题材类型继承、主体命名对齐、声画字段、节奏、高潮和尾钩 handoff；必须额外输出 `Upstream Creative Direction Matrix` 说明每类上游如何引导本集创作方向 | 改因果、改结局、无证据推翻题材风格真源、越权写导演/摄影/分镜/prompt、改写主体注册表、只列上游输入物但不说明创作方向 |
| `5-导演` | `4-编剧`、`2-美学/画面基调`、项目 `MEMORY.md/CONTEXT/`、导演风格来源 | 逐画面导演意图、信息差、节奏、表演交接；必须额外输出 `Director Direction Inheritance Matrix` | 改剧本、替换对白、把风格名套成批注、只列上游不说明导演方向 |
| `6-分镜` | `5-导演` 或指定文稿、`2-美学/画面基调`、`2-美学/分镜风格`、项目 `MEMORY.md/CONTEXT/` | 画面点识别、节拍、构图、起始状态帧、空间连续、0.5 秒时值；必须额外输出 `Storyboard Direction Inheritance Matrix` | 改剧情、漏导演意图/声画字段、重写上游正文、只列上游不说明分镜方向 |
| `7-摄影` | `6-分镜`、`2-美学/画面基调`、`2-美学/摄影风格`、项目 `MEMORY.md/CONTEXT/` | 基于既有空间布局的机位、运动、速度、焦点和一镜到底链路；必须额外输出 `Upstream Camera Direction Matrix` | 重新发明空间、改分镜秒数、随机套术语、只列上游不说明运镜方向 |
| `8-分组` | `7-摄影` 或指定文稿、`2-美学/画面基调`、`2-美学/分镜风格`、`3-主体/subject-registry.yaml`、项目 `MEMORY.md/CONTEXT/` | 分镜组边界、组内累计时间码、首帧衔接、组级风格整理和引用注册表主体的 YAML 统计；必须额外输出 `Upstream Grouping Direction Matrix` | 改写上游分镜正文、伪造时间码来源、拆断 atomic unit、在分组 YAML 中新增未登记主体、只列上游不说明分组方向 |
| `9-图像` | `8-分组`、`3-主体` 参照资产与 registry、`2-美学` 可用风格边界、项目 `MEMORY.md/CONTEXT/`、可选 `分镜平面图` 侧车 | 分镜画面、故事板或平面图的 source comprehension、visual prompt atoms、source_spatial_comprehension、参照绑定和 prompt authorship；必须额外输出或映射 `Image Upstream Visual Direction Matrix` | 把完整组稿当万能 prompt、无主体参照绑定、把上游电影风格直接写成画风、空间侧车替代画面裁决 |
| `10-画布` | `8-分组`、`3-主体` / `9-图像` 参照图、`10-画布` queue/submit plan、LibTV runtime evidence、项目 `MEMORY.md/CONTEXT/` | LibTV prompt、视频节点、imageList/mixedList 顺序、settings、run/rerun 边界；必须额外输出 `LibTV Upstream Video Direction Matrix` | 脚本压缩分镜组正文、主体错绑、settings 无依据、用节点证据替代源组真源、把执行诊断写进 prompt |

## Review Gate

| review_question | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- |
| 是否只记录了读取，而没有说明上下文如何进入当前阶段决策？ | `FAIL-UPSTREAM-CONTEXT-APPLICATION` | 最近的理解、计划或注入节点 | `Upstream Context Application Map` |
| 当前阶段是否把上游 truth 错当成可重写对象？ | `FAIL-UPSTREAM-CONTEXT-DRIFT` | source lock / preservation diff 节点 | `preservation_check` |
| 当前阶段是否把上游风格/批注/分镜/prompt 机械复制为本阶段正文？ | `FAIL-UPSTREAM-CONTEXT-PROJECTION` | owning dimension 计划节点 | `stage_projection`、`local_decision` |
| 缺失上游时是否给出降级、N/A 或阻断原因？ | `FAIL-UPSTREAM-CONTEXT-NA` | intake / source manifest 节点 | `conflict_or_na` |

## Report Boundary

`Upstream Context Application Map` 只保存可审计摘要、证据锚点和裁决结果，不保存冗长思维链、完整草稿或未筛选推演。它服务保真和下游交接，不替代 canonical 创作正文。
