# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `$aigc-scene-design` 的经验层知识库，不是过程日志。
- 调用本目录 `SKILL.md` 时必须同时加载本文件。
- 本文件不改写 `SKILL.md` 的输入、输出和门禁；只沉淀可复用判断经验、失败模式和修复打法。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 22000
hard_limit_chars: 44000
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-25
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 设计稿新增上游清单没有的场景 | 来源真源层 | 删除该设计稿或回到 `1-清单` 正式补主体 | 固定从清单行派生 `S###` | 每个文件可回指清单行 |
| 只写视觉形容词，没有研究考据 | 研究层 | 补地域、年代、建筑、材质或文化依据 | 先判 `type_profile` 再写考据 | 研究段能说明依据和适用范围 |
| 研究像百科摘抄，不能指导画面 | 研究翻译层 | 提炼 `research_brief` 并把每条证据转为可见设计 | 模板固定 `visual_translation` | 每条关键研究都能落到结构、材质、光线、陈设或构图 |
| 把推断写成事实 | 来源姿态层 | 将该判断改标为 `scene_inference` 或 `unresolved` | `source_posture` 必须逐项填写 | 高风险事实有来源或保守处理 |
| prompt token 无法回指依据 | 提示词证据链层 | 补 `prompt_evidence_chain` 或删除无依据 token | prompt 生成前先完成 visual translation | 关键 token 能回指 research/design/cinematography |
| 场景物语写成剧情复述 | 叙事功能层 | 改写为空间如何承载主题、行动和情绪 | 模板区分 `原文描述复述` 与 `物语` | 物语不新增剧情事件 |
| Scene Design 与 Cinematography 混写 | 解构层 | 拆成空间/材质/色彩/动线与镜头/光线/运动/焦段 | 模板固定双字段 | 两组字段互不替代 |
| 提示词没有承接全局风格 | 风格继承层 | 回读 `north_star.yaml` 并补全局风格引用 | 提示词前固定记录 source style | prompt 有 global style anchor |
| 解构区缺少主体 ID | 结构投影层 | 在 `## 4. 解构` 下方补 `主体ID号：<主体ID>`，并同步 `## 5. 提示词设计` 与英文 prompt 前缀 | 模板和 review gate 固定三处 ID 一致性 | 解构 ID、提示词字段 ID、prompt 开头完全一致 |
| 建筑风格缺失或空泛 | 建筑策略层 | 从场景类型、team 监制或用户要求中确定建筑风格 | `types/` 对不同场景给出建筑/空间风格入口 | prompt 有 architecture style anchor |
| 英文提示词缺少时间或地域 | 时间地域锚点层 | 从 `research_brief`、`type_profile`、上游清单或项目资料中补 period / region token；无法确认时使用有来源姿态的保守锚点 | prompt evidence chain 固定加入 `period_region_tokens` | final English prompt 同时含时间与地域 |
| 英文提示词只补前缀后缀，未整合解构主体 | Prompt 整合层 | 回到 `## 4. 解构`，逐项压缩 Scene Design 与 Cinematography 的有效槽位进英文 prompt，并在 `deconstruction_coverage` 说明合并或剔除理由 | 模板和 review gate 固定“整合对象是解构全部有效信息” | final English prompt 可反查到空间、材质、光线、构图和镜头槽位 |
| 初始化综合消费 启用但没有请教项目监制 | 顾问请教层 | 按共享团队顾问合同优先解析 `team.yaml.init_synthesis.stage_seed_summary."6-设计"`，让场景/建筑/美术/摄影/导演顾问代入其角色意识、创作风格和专业水准，围绕当前 `steps/scene-design-workflow.md` 节点提出判断、局部 patch 或风险提示 | `init_team_synthesis_context` 固定在 LLM 场景设计前消费，并记录 `node_ref / pass_ref / gate_ref` | 可见指导改变当前节点的判断、执行取舍、局部 patch 或风险提示 |
| references 细则存在但未进入执行/验收 | 合同汇流层 | 把 reference 同步接入 Reference Loading Guide、steps 节点、review gate 和必要的机械 resolver | 新增硬规则 reference 时必须同时声明加载场景、消费节点和阻断门禁 | `rg` 能在 SKILL、steps、review、scripts/README 中找到该 reference 的消费点 |
| 英文提示词超 2000 characters | 输出约束层 | 压缩冗余形容词、合并同义短语、删除过程解释 | 交付前字符计数 | prompt <= 2000 characters |
| 冷门信息无来源 | 考据可靠性层 | 标注为推断或在许可下网络搜索 | 区分本地资料、常识推断、网络来源 | 冷门信息有来源策略 |
| 脚本生成创作正文 | LLM-first 层 | 停用该脚本输出，改为 LLM 直写 | scripts 只保留机械辅助说明 | 没有脚本主创痕迹 |

## Repair Playbook

1. 先确认目标设计稿对应上游清单的哪一行，避免从正文想象新增主体。
2. 读取 `north_star.yaml` 时优先抓取全局视觉口味、母题、禁区、色彩和风格提示词；不要把它改写成单场景设定。
3. 读取 `team.yaml` 时只提取设计、建筑、美术、摄影、导演或大师监制视角；没有相关角色时记录为 `未声明`，不要虚构。
4. 对现实或半现实场景，先确定年代、地域、建筑类型、材质和空间使用方式，再写视觉描述。
5. 对超现实、梦境、异化或象征空间，仍要建立可制作的空间规则：尺度、边界、材质、光源、动线。
6. 执行初始化综合消费时，先锁定当前 `node_id / pass_id / gate_id`，再让项目监制顾问代入其角色意识、创作风格和专业水准参与该节点判断；不要把顾问请教写成固定字段问卷，也不要只问风格评价。
7. 先写 `research_questions`，再写答案；没有问题意识的研究段通常会滑向百科摘抄。
8. 每个关键判断都给出来源姿态：项目资料、用户资料、常识、推断、网络来源或未解不确定性。
9. 对 `uncertainty_register` 中的高风险项，优先采用非特指化、保守化或可替换视觉方案，不要硬写具体事实。
10. `visual_translation` 要把研究转成能被画出来的东西：结构、材料、表面、光线、陈设、标识、地形、构图或负向约束。
11. `原文描述复述` 应保留上游关键词并转成自然短段，不补新的剧情事实。
12. `物语` 解释“这个空间为什么在故事中重要”，而不是继续写镜头调度或美术清单。
13. `Scene Design` 关注空间、构造、材质、色彩、陈设、动线和可制作资产。
14. `Cinematography` 关注镜头距离、运动、光线、焦段、构图、景深、氛围节奏。
15. 英文提示词先确认 `## 4. 解构` 下的主体 ID，再继承全局风格、建筑风格、时间锚点、地域锚点和场景专属细节；少用抽象赞美词，多写可见物。
16. 英文整合 prompt 的主体是 `## 4. 解构` 全部有效信息：Scene Design 与 Cinematography 中的空间、材质、色彩、陈设、动线、光线、构图、焦段、景深和氛围节奏都应被压缩进 prompt，不能只写前缀、后缀或风格/负向词。
17. Prompt 最后反查 `prompt_evidence_chain`：每组关键 token 都应能回指研究、视觉翻译、Scene Design 或 Cinematography，且 subject_id_prefix 与解构 ID 一致；若某个解构槽位被合并或剔除，必须在 `deconstruction_coverage` 说明原因。

## Reusable Heuristics

- 场景设计稿是图像和视频生成前的可制作蓝图，不是散文。
- 好的场景设计应同时回答“它是什么空间”“为什么存在”“如何被拍到”。
- 建筑风格不是标签堆叠；它要能解释形制、材料、比例和光线。
- 顾问请教的最佳产物不是固定字段答案或大师名字清单，而是能改变当前思维·执行节点判断、取舍、局部 patch 或风险提示的短指令。
- 摄影语言要服务空间，不要把所有场景都写成同一种电影感。
- 冷门考据宁可标注不确定，也不要把猜测写成事实。
- 研究的终点不是“知道得更多”，而是“哪些事实能被翻译成稳定可生成的画面”。
- `source_posture` 是防止幻觉的刹车；`visual_translation` 是防止研究空转的油门。
- 不确定性可以保留，但必须变成设计上的保守处理、非特指化或后续确认点。
- Prompt 证据链越清楚，后续生成阶段越容易判断是 prompt 偏移还是设计源头不清。
- 主体 ID 是场景设计稿的结构锚点；`S###` 应同时出现在解构区、提示词字段和英文 prompt 开头。
- 批量设计时最容易风格同质化；每个场景至少应有一个独特空间锚点。
