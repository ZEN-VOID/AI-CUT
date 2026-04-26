# Context: aigc 道具 2-设计

本文件是 `$aigc-prop-design` 的经验层知识库，不是过程日志。它沉淀单道具细目设计、上游清单消费、风格监制整合和提示词约束中的可复用经验。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
status: initial
recommended_action: keep-prop-design-heuristics-target-scoped
last_checked_at: 2026-04-25
```

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 系统预防修复 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-PROP-DESIGN-01` | 细目设计变成多个道具的总稿 | 单主体边界层 | 拆成每个道具一个文件 | 在 `SKILL.md` 与模板固定单主体输出 | 文件标题和来源只对应一个清单项 |
| `TM-PROP-DESIGN-02` | 研究考据像百科摘抄，无法转成可生成视觉 | 研究转译层 | 把考据压缩为材质、年代、工艺、磨损和使用痕迹 | 在 `references/` 固定“考据必须服务设计” | 考据之后能直接支撑解构字段 |
| `TM-PROP-DESIGN-03` | 物语只写功能说明，没有叙事生命 | 物语层 | 加入拥有者、行动痕迹、冲突或象征 | 模板要求“为什么它在故事里必须被看见” | 物语不新增上游矛盾事实 |
| `TM-PROP-DESIGN-04` | Photography 与 Prop Design 混在一段里 | 解构层 | 拆成拍摄可见语言与道具造型语言 | 模板固定两个字段 | 两字段均有可执行视觉词 |
| `TM-PROP-DESIGN-05` | 英文 prompt 太长或未引用全局风格 | 提示词层 | 压缩到 2000 字符内并显式引用全局风格 + 物品风格 | review gate 检查字符数和引用关系 | prompt 为英文且可直接进入生成链路 |
| `TM-PROP-DESIGN-06` | team.yaml 中的大师只被点名，未影响设计 | 监制消费层 | 把大师语境转译为材质、构图、年代感、动作性或留白策略 | steps 固定“监制上下文 -> 设计决策”证据 | 文件中能看到至少一条对应设计选择 |
| `TM-PROP-DESIGN-07` | 批量生成的 Skill 2.0 包只有文字合同，缺关键 Mermaid 拓扑 | 包治理层 | 在根 `SKILL.md` 补 `Visual Maps`，在 `references/`、`types/`、`review/` 补来源、分流和汇流图 | README 固定可视化入口索引，后续维护先检查图谱再改流程 | `rg '```mermaid'` 能看到根图、steps 图和关键分区图 |
| `TM-PROP-DESIGN-08` | 研究写了很多，但 prompt 看不出研究贡献 | 证据链层 | 把研究拆成 source cue、confidence、visual translation、prompt token | 模板固定研究证据链和 Prompt Evidence Chain | prompt 核心 token 能回指研究、物语或解构字段 |
| `TM-PROP-DESIGN-09` | 冷门考据被写成确定事实，后续美术和生成都跟着错 | 不确定性治理层 | 将事实分为 source_fact / inference / inspired_by / unknown | references 固定 confidence 和 risk_uncertainty 字段 | 不确定内容以 inspired by 或 uncertain 标注，不进入确定性 design lock |

## Repair Playbook

1. 先确认问题属于输入取证、单主体边界、研究转译、物语、解构、提示词、监制消费还是输出落盘。
2. 若缺上游清单，回到 `道具/1-清单`；不要从分镜正文自行扩充完整道具表。
3. 若缺 `north_star.yaml` 或 `team.yaml`，保留道具设计可执行部分，但在文件或报告中标注监制上下文缺口。
4. 若 prompt 超过 2000 字符，优先删解释性短语，保留主体、材质、使用痕迹、构图、光线、风格锚点和禁止项。
5. 若研究过多，删掉不能改变造型、材质、工艺、年代、磨损或拍摄方式的事实。
6. 若 prompt token 像凭空出现，回到研究证据链补 source cue、confidence、visual translation 和 design lock。
7. 若一个道具存在多状态，先判断是同一主体状态版本还是不同叙事道具；必要时按 `types/prop-design-type-map.md` 分流命名。
8. 若真实 subagent 或 reviewer 被阻断，按 `SKILL.md` 的 Subagent Execution Contract 报告降级路径。
9. 若维护本技能包结构，先确认根 `SKILL.md#Visual Maps` 与关键分区 Mermaid 图仍然覆盖输入、类型、创作、审查和落盘主链。

## Reusable Heuristics

- 单道具设计的好坏不在信息量，而在“能否让生成和美术执行者稳定复现同一个物件”。
- 上游 `原文描述（关键词式）` 是约束，不是天花板；可以深化材质和视觉逻辑，但不得新增与上游冲突的叙事事实。
- 冷门考据应以“可见特征”收束：形制、材料、工艺、年代、磨损、携带方式、使用痕迹。
- 研究进一步升级的关键不是增加资料量，而是建立 `source cue -> confidence -> visual translation -> design lock -> prompt token` 的短链路。
- `confirmed` 才能变成硬锁定；`probable` 和 `inferred` 应写进设计倾向；`uncertain` 更适合成为风险注记或 inspired-by 表达。
- `Photography` 关注镜头如何让物件被看见；`Prop Design` 关注物件本身如何被制造、持握、老化和辨认。
- 物语不应替代剧情扩写；它只说明该道具的叙事压力、象征和使用痕迹。
- 大师监制上下文要落到动作：例如材质克制、构图距离、颜色禁区、年代错位、手作痕迹、功能暴露。
- prompt 的英文 2000 字符限制是硬门禁；中文解释可以在正文中充分，但最终 prompt 必须紧凑可投喂。
- Mermaid 图不是装饰；根图负责主链，分区图负责来源汇入、类型分流和 review 汇流，流程变化时先更新对应 owner 图再更新 README 入口索引。
