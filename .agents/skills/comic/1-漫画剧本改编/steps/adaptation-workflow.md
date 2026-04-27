# 漫画剧本改编思行网络

本文件承载 `漫画剧本改编` 的执行拓扑、证据门与返工路由。根 `SKILL.md` 只引用本文件，不复制节点细则。

## Business Requirement Analysis

| slot | question | default |
| --- | --- | --- |
| `business_goal` | 本轮改编要服务什么后续动作 | 直接服务 `2-九刀流漫画提示词` |
| `business_object` | 处理对象是什么 | 文本、图片、视频、新闻热搜或多源混合 |
| `constraint_profile` | 主要约束来自哪里 | 事实边界、版权边界、项目类型包、输出格式 |
| `success_criteria` | 用户如何判断完成得好 | 分组清楚、读得下去、看得见、有钩子、能进入九刀流 |
| `complexity_source` | 复杂度主要来自哪里 | 来源判型、事实边界、重排许可、分组汇流 |
| `topology_fit` | 应采用什么拓扑 | 来源判型树 + 创作串行主干 + review 汇流 |

## Node Schema

| field | requirement |
| --- | --- |
| `node_id` | 稳定节点标识 |
| `objective` | 当前节点要解决的判断和动作目标 |
| `inputs` | 所需输入、上下文、文件或上游产物 |
| `actions` | 实际执行动作，不只写“思考” |
| `evidence` | 可复核证据、文件、命令或结论 |
| `route_out` | 下一节点、分支或失败回路 |
| `gate` | 允许通过的条件 |

## Node Network

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE-LOCK` | 锁定任务目标、素材范围、项目根与输出模式 | 用户请求、素材、项目路径 | 判断 `source_type`、`output_mode`、是否允许写盘 | 用户原始请求、已给路径 | `N2-TYPE-PACK-LOCK` | 输入足以判断来源类型或已明确需要追问 |
| `N2-TYPE-PACK-LOCK` | 锁定本轮固定上下文包 | `types/type-map.md`、comic 根层 type-pack | 选择来源类型包、改编姿态包、输出模式包；继承或推断 comic type stack | 命中包路径、`type_stack_ref` | `N3-SOURCE-NORMALIZE` | 类型包已加载，冲突包已裁决 |
| `N3-SOURCE-NORMALIZE` | 把不同来源压成统一素材摘要 | 原始素材、来源类型包 | 文本抽情节链；图片抽前后因；视频抽时间序列；新闻抽事实表；多源裁主锚点 | `source_digest` 覆盖事实、画面、情绪、关系、未解点 | `N4-TRUTH-BOUNDARY` | 摘要能回答“谁想要什么、被谁阻拦” |
| `N4-TRUTH-BOUNDARY` | 锁定事实边界、虚构许可与禁区 | `source_digest`、用户限制 | 选择 `truth_boundary`，区分事实锚点、公共情绪、虚构承载线 | `boundary_note` | `N5-STORY-ENGINE` | 现实事实不被虚构冒充 |
| `N5-STORY-ENGINE` | 生成可连载的漫画剧情发动机 | `source_digest`、`boundary_note`、类型投影 | 锁主角、对手、欲望、代价、卖点、保核范围、重排许可、刺激曲线和高冲击候选 | `adaptation_brief`、`fidelity_floor`、`impact_beats` | `N6-GROUP-SCAFFOLD` | 能说清最值钱的冲突和不可改丢的核心 |
| `N6-GROUP-SCAFFOLD` | 生成分组方案与组边界理由 | `adaptation_brief`、输出模式包 | 按约 1000 字一组；尊重场景、动作、钩子、payoff 边界；处理尾组规则 | 组号、估算原文字数、尾组决议、边界判定 | `N7-SCENE-WRITE` | 不机械截断同一动作或同一钩子 |
| `N7-SCENE-WRITE` | 写成场景化、可画、可念的漫剧正文 | 分组方案、写作规格、类型投影、编导字段桥接包 | 写对白、旁白、动作、环境、冲突推进；必要时同步基础格式化层和漫画扩展字段；确保声音文本与画面承托就近配对 | `【漫剧正文】`、声画配对证据 | `N8-HOOK-VISUAL-POLISH` | 正文不是摘要；声音不混动作，画面不写抽象心理，至少包含可入镜动作和关系变化 |
| `N8-HOOK-VISUAL-POLISH` | 注入组末钩子、视觉锚点、场景锚点和下游 handoff | 正文草稿、钩子手册、视觉奇观细则、编导字段桥接规范 | 补 `【组末钩子】`、高冲击画面、页末停笔、场景锚点、类型包 handoff、SFX/气泡/规则显影提示 | 组文件 frontmatter、末尾钩子、`scene_anchor` | `N9-ACCEPTANCE-GATE` | 每组有追更理由、稳定空间/核心物件/最贵一格，且可作为九页处理单元 |
| `N9-ACCEPTANCE-GATE` | 验收结构与语义质量 | 组文件集合、review 合同、validator | 跑结构校验；执行语义 review；失败回到 owner 节点 | validator 输出、review verdict | pass 或返工 | verdict 为 `pass` 或 `pass_with_followups` |

## Branch Rules

- `N2` 可多选类型包，但必须先裁决互斥冲突，再进入 `N3`。
- `news_event / hot_search` 必须经 `N4` 强门禁，不得直接进入自由虚构正文。
- `comic-first / spectacle-first` 只放开虚构来源或 `truth_boundary=free_reimagining` 的衍生线，不放开现实事实。
- 命中 `projection-directing-field-bridge` 时，`N7-N8` 必须执行声画配对与字段纯度 pass。
- `N6` 可以依据场景边界偏离机械字数，但必须在 `【边界判定】` 中说明。
- 任一节点发现 `type_stack_ref` 丢失，必须回到 `N2`。

## Rework Routing

| symptom | direct_cause | rework_node |
| --- | --- | --- |
| 只有氛围，没有事件发动机 | 来源归一没有转成冲突链 | `N3` |
| 现实事实和虚构段落混成一个口径 | 事实边界未锁 | `N4` |
| 前段平、后段挤 | 未启用或误用 `comic-first` 重排 | `N5` |
| 分组边界不可审查 | 尾组规则或场景边界证据缺失 | `N6` |
| 正文像摘要 | 场景、动作、对白不足 | `N7` |
| 声音、动作、心理和规则文字混写 | 未执行编导字段桥接 pass | `N7-N8` |
| 组末像总结句 | 钩子没有留缺口 | `N8` |
| 下游无法逐组进入九刀流 | frontmatter、类型投影或正文完整性缺失 | `N8-N9` |

## Evidence Gate

交付前至少保留以下证据：

- 命中的 `source_type / truth_boundary / adaptation_posture / output_mode`
- 命中的类型包路径
- 每组 `估算原文字数 / 尾组决议 / 边界判定`
- 命中编导字段桥接时，每组 `scene_anchor` 与声画配对检查结论
- `validate_grouped_manga_script.py` 的文件级或目录级校验结果
