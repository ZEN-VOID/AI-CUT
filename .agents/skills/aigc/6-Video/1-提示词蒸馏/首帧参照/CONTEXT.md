# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `6-Video/1-提示词蒸馏/首帧参照` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在父级 `6-Video` 合同之后加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| prompt 直接照搬整组 `剧本正文` | 桥段提取层 | 回到目标 `分镜ID`，重做剧情桥段裁切 | 在 `FIELD-VID-FFR-02` 固化“剧情桥段只对应目标帧” | 剧情桥段与目标镜级事实对齐 |
| shared director schema 已升级到 `角色背景面 / 角色站位走位 / 出场角色及穿搭`，并新增可选 `镜头速度`，但首帧 prompt 仍按旧字段心智压缩 | schema handoff 层 | 在帧级 prompt 中显式纳入组级 `出场角色及穿搭`，并把镜级消费口径切到 `角色背景面 / 角色站位走位`；若存在 `镜头速度` 也一并消费 | 在 `SKILL.md` 的输入门、N3/N6、质量清单与根因合同中固定新字段 | 首帧 prompt 能同时读出空间朝向、角色走位、组级视觉识别锚点与运动速度档 |
| `全局风格` 被改写 | 固定文本层 | 恢复原文直贴 | 在输出契约里显式标记“fixed verbatim block” | 与上游逐字一致 |
| prompt 中暴露了字段标题 | 文本编排层 | 重写为无标题融合文本 | 在 `FIELD-VID-FFR-02` 固化只保留组ID/镜ID标签 | 除组ID/镜ID外无显式字段名 |
| 共享文本模板已经切到“自然句优先、`tight` 才局部短语化”，但首帧 prompt 仍默认输出短语/关键词串 | 模板 handoff 层 | 回到 `normal/underflow` 口径，恢复连贯自然语句，只在 `tight` 时局部短语化 | 在 `SKILL.md` 的预算分支、N6/N7 与入口 prompt 中固定“仅 `tight` 允许局部短语化” | 非紧预算组不再退化成短语式清单 |
| prompt 没写出 `分镜 <ID> xx秒-xx秒`，或把时间写成 `分镜 <ID> 的 xx秒-xx秒` / 全集时间线 | 时间锚点层 | 回到目标分镜 `时间段.开始秒 / 结束秒`，重建当前分镜组内的 `xx秒-xx秒` 前缀 | 在 `SKILL.md` 的输入门、N2/N6/N7、质量清单与共享模板口径中固定“组内相对秒位 + 禁用 `的` 连接” | 每个首帧条目都能直接回链目标分镜的组内秒级范围 |
| `reference_images` 被删空字段，或 `image_markers` 的 URL/主体/图号顺序漂移 | 请求模板层 | 回到共享 JSON 模板，恢复双字段骨架，并校正 marker 顺序位 | 在 `SKILL.md` 的 `FIELD-VID-FFR-03 / N7-N9 / Quality And Audit Contract` 固定“字段存在 + 三元结构 + 顺序稳定” | 请求 JSON 可稳定映射后续真实上传顺序 |
| `第N集.txt` 开始承载结构化参数区块，和 JSON 主体争夺真源角色 | 派生视图层 | 回退到 TXT 只展示 prompt 与字数统计 | 在 `SKILL.md` 的 `N8` 与 Hard Rules 中固定“TXT 是 derived display view，不承载结构化参数” | `第N集.txt` 不再与 JSON 主体竞争 completeness carrier 角色 |
| 帧级请求没有带出所属 `分镜组ID` | 来源定位层 | 补回 `meta.group_id` 与显式 `分镜组` 标签 | 在字段表中要求 `group_id + source_shot_ids` 成对存在 | 可同时回链到组级与帧级 |
| 为了凑字数而虚构桥段细节 | 字数预算层 | 回退到保守桥段表达，允许 underflow | 在策略表中固化 `ambiguous/underflow` 保守退化规则 | manifest 中有原因备注且无新事实 |
| 单分镜模式明明只服务 1 个 `分镜ID`，prompt 却仍像组级多镜模式的缩小版，导致当前镜头细节发薄 | 预算策略层 | 回到 `P0/P1/P2/P3` 预算分配，优先把剩余字数补给当前分镜的动作、空间、镜头控制和氛围细节 | 在 `SKILL.md` 的压缩规则、`N6/N7`、Pass 与 Quality 清单中固定“单分镜预算优势 = 细节密度优势” | 同等字数下，首帧 prompt 能读出更丰满的当前镜头信息，而不是稀疏缩写 |
| 规则散落在 `references/*.md` 导致主合同失真 | 真源治理层 | 把字段表、流程、类型策略、输出契约全部回收进 `SKILL.md` | 固化“`SKILL.md` 是唯一规范真源，`CONTEXT.md` 只保留经验层” | 执行无需再依赖 `references/` |
| `6-视频/subtypes/...` 与真实路径 `6-Video/...` 不一致 | 路径合同层 | 统一所有技能内路径与证据路径到真实目录 | 在案例与合同中持续使用真实路径，避免旧路径回潮 | 仓内不再残留命中的旧路径字符串 |
| 只把章节标题改成知行合一口径，但桥段判型、预算压缩、写回与汇流仍是旧线性说明书 | 思行网络层 | 把执行链重排为 `任务归位 -> 判型 -> 提取 -> 压缩 -> 写回 -> 汇流` 的节点网络 | 在 `SKILL.md` 固化 `Business Requirement Analysis + Topology + Thinking-Action Node + Convergence + One-Shot Output` 五层结构 | 关键链路可通过节点与 Mermaid 一眼定位 |
| 概述中的 canonical 路径漂到不存在的仓库根（如 `AIGC-DREAMER`） | 路径真源层 | 回收所有本地目录说明到当前真实技能树路径 | 在 leaf 合同、经验层与 changelog 中统一使用 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/` | 文档路径、evidence path 与仓内真实目录一致 |

## Repair Playbook

1. 先查目标 `分镜ID` 是否真实存在于某个 `分镜组`。
2. 再查 `剧情桥段` 是否只描述该目标分镜可支持的动作、状态或事件阶段。
3. 再查 `全局风格` 是否保持原文。
4. 再查目标镜级是否已补出 `分镜 <ID> xx秒-xx秒`，且时间来自当前分镜组内相对秒位。
5. 再查其余组级与镜级字段是否已按 `P1/P2/P3` 压缩进 prompt，且没有字段标题残留。
6. 最后查 `prompt_char_count`、双输出文件与 manifest 是否一致。

## Reusable Heuristics

- 帧级视频请求最容易失真在“把整组剧情搬过来”，而不是“文字不够华丽”。
- `剧情桥段` 的职责是把整组剧本正文切成目标镜头可见的一小段，不是重写剧情，也不是摘要整组剧情。
- 当一个分镜组只有 1 个分镜时，直接使用整段 `剧本正文` 作为剧情桥段，通常最稳。
- 当一个分镜组有多个分镜而桥段边界不够清晰时，优先锚定目标分镜的可见动作、人物状态和空间关系，保守缩写，不虚构过渡。
- 帧级 prompt 仍然需要组级空气层，所以最稳结构通常是：`剧情桥段 + 全局风格 + 压缩后的类型元素/导演意图 + 目标镜级字段`。
- 当上游 schema 把“角色背后空间”“角色位移”“组级服装摘要”拆成三层时，帧级 prompt 也应同步三层消费：`角色背景面` 提供当前帧的空间朝向，`角色站位走位` 提供动作布局，`出场角色及穿搭` 提供视觉识别锚点。
- 当共享文本模板升级后，首帧叶子也必须同步继承其“时间锚点语法 + 自然句优先 + 压缩优先级”合同，不能只补单个字段名。
- 最稳的时间锚点写法是 `分镜 <ID> xx秒-xx秒`；不要写成 `分镜 <ID> 的 xx秒-xx秒`，也不要把秒数误读成全集时间线。
- 帧级 prompt 的默认体裁应是连贯自然句；只有预算真的进入 `tight` 时，才允许把局部句子收束为更精炼的自然短语。
- 当字数吃紧时，先缩 `镜头属性 / 镜头框架 / 镜头类型 / 分镜表现`，再缩 `角色表现 / 场景氛围 / 道具及状态 / 摄影美学`；`时间段 / 角色站位走位 / 角色背景面 / 景别 / 运镜手法 / 镜头速度（如存在）/ 镜头视角` 应最后才允许受影响，而且仍需保持清晰可辨。
- 单分镜模式最大的预算优势不是“更容易省字”，而是“同样总字数能把当前分镜写得更丰满”；如果写出来仍像组级全能参照的缩小版，说明预算策略还停留在多镜分摊心智。
- 在首帧模式下，`P0` 之外的富余预算应优先补给当前镜头的动作节点、空间朝向、机位控制、人物状态与氛围层，而不是用空泛形容词或抽象修辞把字数填满。
- `reference_images` 与 `image_markers` 在首帧叶子里首先是模板兼容槽位，不是“没有图就可以删掉”的可选字段。
- `第N集.txt` 的角色是人工审阅派生视图，不应开始承载 JSON 才有的结构化参数。
- 帧级提示词的字数窗应低于组级；若上游信息有限，允许 underflow，但必须把原因写进 manifest，而不是用空泛修辞补字数。
- 当叶子技能已经稳定时，字段表、流程、类型策略和输出契约应收束进单一 `SKILL.md`；经验层只保留 failure map、repair playbook 和 milestone case。
- 技能路径一旦完成真实目录切换，后续 case、evidence path 和默认加载路径都必须同步使用真实路径，不能继续沿用旧别名。
- 对帧级 `首帧参照` 做知行合一改造时，最稳的方式不是改变桥段/模板机制，而是把既有机制重织成更细的思行节点，让“判型、提取、预算、写回、汇流”全部显性化。
- 当用户明确要求 `复杂链路的骨架 / 细则分层 = false` 时，应把复杂度体现在节点粒度和 Mermaid 治理密度上，而不是再拆出第二份 references 真源。

## Case Log

### Case-20260413-AIGC-VIDEO-FFR-SCHEMA-SYNC

- milestone_type: source_contract_change
- outcome: 将 `首帧参照` 对上游导演 schema 的消费口径同步到新字段分层：组级新增 `出场角色及穿搭`，镜级显式消费 `角色背景面 / 角色站位走位`。
- root_cause_or_design_decision: 旧合同虽然已锁定“帧级 prompt 要消费组级与镜级上下文”，但输入门和压缩块清单没有显式列出新增组级服装摘要，也没有把镜级新字段写进最小壳与质量门，容易继续按旧字段名理解。
- final_fix_or_heuristic: 在 `必需字段 / 输入完整性门 / N3 / N6 / FIELD-VID-FFR-02 / Quality And Audit Contract` 中固定新字段，确保首帧 prompt 不丢组级服装摘要，也不再依赖旧字段口径。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已将 `出场角色及穿搭` 纳入必需字段与输入门
  - [x] `SKILL.md` 已将 `角色背景面 / 角色站位走位` 纳入推荐字段与质量门
  - [x] `FIELD-VID-FFR-02` 已固定新的压缩块覆盖范围
- evidence_paths:
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/SKILL.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/CONTEXT.md`
  - `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- user_feedback_or_constraint: 用户要求根据更新后的 shared director schema，检查并同步 `6-Video/1-提示词蒸馏/首帧参照`。
