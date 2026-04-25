# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/3-Detail` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/3-Detail/SKILL.md` 时，应自动预加载本文件。
- 当前阶段已切到“单技能根包 + references 细则模块”模式；旧 `1-水月 / 2-镜花` 结构仅作为历史参考，不再视为当前主执行合同。

## Context Health

- soft_limit_chars: 22000
- hard_limit_chars: 44000
- status: ok
- last_checked_at: 2026-04-24

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 还没做 `分镜构图` 就先写别的字段 | 思行顺序层 | 回到 `P1` 先锁镜数、切分点和镜级骨架 | 在根 `SKILL.md` 固定 `分镜构图` 先行，并在 references 中把后续 pass 的前置写死 | `分镜数 / 时间 / 剧本正文 / 主体锚定 / 分镜构图` 总是先出现 |
| `episode_detail.json` 与当前 detail root 不同构 | 模板真源层 | 按 `_shared/episode_detail.json` 回收字段 | 让模板、根技能、validator 和 runtime layout 同时引用同一结构 | 模板字段与 `validate_stage_output.py` 一致 |
| 模板里又漂回旧摄影字段名 | 字段命名层 | 把旧键改回当前 canonical 名称 | 在模板和 references 中锁定 canonical 名称 | 不再出现旧摄影命名残留 |
| `剧本正文` 只停留在组级，没有落到每镜 | 镜级骨架层 | 回到 `P1` 为每镜补上对应正文 | 在模板和 field guide 中固定每镜都必须有 `剧本正文` | 每镜都能独立成立 |
| `主体锚定` 写成抽象情绪，而不是场景/角色/道具 | 字段边界层 | 把镜头锚点改回具体实体 | 在 `模板字段填写指南.md` 固定 `主体锚定` 的写法 | 能直接被下游抽取 |
| `分镜构图` 只写审美口号，没锁镜数和切分点 | 骨架层 | 把 `P1` 的目标改回结构先行 | 在 `思行网络` 中显式把 `分镜数 / 时间 / 剧本正文 / 主体锚定 / 分镜构图` 归给 `P1` | `P1` 能单独生成 detail skeleton |
| `摄影表现 / 运镜手法` 反向推翻已锁骨架 | pass 依赖层 | 回退到 `P1` 或 `P4/P5` 重做，不在后序偷改结构 | 在根技能和 rubric 中固定“后序不改骨架” | 镜数、时间和镜级正文稳定 |
| 字段写得顺，但不具像、不艺术 | 创作质量层 | 回到字段级写法要求，补动作、空间、物件、光气和关系证据 | 用 examples 与 review rubric 固定“反抽象、反空话”门 | 抽检字段时能看到具像抓手 |
| 结构完整，但镜头之间不连续 | 连续性层 | 回查 `时间 / 剧本正文 / 运镜手法 / 转场特效` 的衔接 | 在 `P6/P7` 固定 continuity 复核 | 前后镜不再像独立卡片 |
| 已经挂接电影学院派知识库，但字段仍像教材摘抄 | 知识转译层 | 回到当前字段对象，把术语翻译成镜内动作、空间、光色和观看任务 | 用 `references/电影学院派知识接线.md` 固定“先判问题，再选知识包，再翻译回字段” | 字段可读、可拍，而不是知识点堆砌 |
| 只读摄影知识就把整组戏写满，人物和戏剧支点反而变弱 | 知识偏置层 | 回到 `导演手册/分镜脚本/电影摄影` 三域分工，重新按 pass 配权 | 在 `路由画像.yaml` 固定每类组型的知识包优先级 | 字段里同时保住戏剧、空间和视听三条线 |
| 空间关系混乱、轴线不稳、切镜像随手拼接 | 分镜语法层 | 优先补读 `导演手册/电影导演方法.md` 与 `分镜脚本/*`，回到 `P1` 重建镜头骨架 | 把“镜头怎么落”问题固定先走 `分镜脚本` 知识包 | 抽检时能说清楚谁在看谁、从哪边看、为什么切 |
| 新知识合同写进 SKILL 了，但运行时产物和 validator 仍看不出是否真正使用 | 验收脱节层 | 把知识使用证据写入 `validation-report.md`，并让 stage validator 强制检查 `knowledge_mode / knowledge_domain / selected_bundles / applied_passes / translation_targets` | 任何新增“知识增强”合同都要同时补 `report slot + validator + rubric` 三件套 | validator 失败时能明确区分“没用知识”与“用了但未写证据” |
| 新模板要求 `meta + groups`，但现有运行时仍是 `metadata + final_output`，导致 validator 只会把真实项目判死 | schema 漂移层 | 让 `validate_stage_output.py` 同时识别 canonical 与 legacy runtime 结构，再逐步收敛到单一 schema | 模板升级时，validator 必须先支持受控双读，直到现有 runtime 全迁完 | 校验失败不再停在“顶层缺少 meta/groups”这类低价值报错 |
| 只保留固定 pass 说明，没有把业务分析、拓扑、节点网和汇流门写成知行合一骨架 | 技能拓扑层 | 在根 `SKILL.md` 增加 `Business Requirement Analysis / Topology / Mermaid / Thinking-Action Node / One-Shot Output` 五层合同 | 凡命中 `skill-知行合一` 的升级，不允许只加术语不加节点与汇流 | 读 `SKILL.md` 时能直接看到主干、返工入口和唯一 closure |
| `validation-report.md` 有知识证据，但没有 `思考过程 / 关键证据 / 风险/例外 / 下一入口` | 结案闭环层 | 把 closure 四段提升为阶段报告硬门槛，并让 validator 校验 | 任何知行合一升级都要同步补 `report token + validator + audit` | 阶段结案可以复核，不再只剩“已完成” |
| 入口 `SKILL.md` 长到重新承载完整节点正文，Skill 2.0 分区变成摆设 | 动态引用层 | 保留关键审计标题和门禁摘要，把节点动作、review、types、模板分别迁入 `steps/ / review/ / types/ / templates/` | 升级后让 `SKILL.md` 只做入口、路由、字段总表和 Output Contract；兼容旧 validator 的 reference 路径可暂留但要标注 owner | Skill 2.0 validator 通过，且 `steps/detail-thinking-action-workflow.md` 能独立承载节点执行细则 |

## Repair Playbook

1. 先查本轮是否真的从 `P1-分镜构图` 开始。
2. 再查模板是否仍与 `_shared/episode_detail.json` 同构。
3. 再看当前问题属于 `导演手册 / 分镜脚本 / 电影摄影` 哪一个知识域。
4. 再看 `detail.分镜数` 与 `分镜列表` 是否一致。
5. 若镜级骨架没锁住，不要继续修表演、摄影或运镜。
6. 若字段空泛，优先补可见动作、空间关系、物件状态、光影条件和视线重心。
7. 若字段像教材摘抄，回到 `references/电影学院派知识接线.md`，把术语翻译回当前字段语言。
8. 若技能合同仍像线性说明书，先补 `Topology / Mermaid / Node Register`，再修局部字段 prose。
9. 若报告只有结果没有 closure 四段，先修 `validation-report` 合同与 validator，再结案。
10. 若 Skill 2.0 升级后发现新旧分区双写，先判断旧路径是否被 validator 或下游引用；能保留兼容索引就先保留，等引用迁移完成后再精简旧正文。

## Academy Bundle Picker

- 当问题是“这场戏为什么这样组织、支点在哪里、揭示顺序是否成立”，先读 `导演手册/`。
- 当问题是“这镜怎么切、方向线索是否清楚、机位和运镜有没有逻辑”，先读 `分镜脚本/`。
- 当问题是“光色质和空间压强怎么被看见”，先读 `电影摄影/`。
- 当一组戏同时有对白压强和强空间运动时，优先 `导演手册 -> 分镜脚本 -> 电影摄影`，不要反过来。
- 当一组戏主要靠环境、天气、材质和留白托举时，优先 `导演手册 -> 电影摄影`，最后再回到 `分镜脚本` 做最少必要调整。

## Reusable Heuristics

- `3-Detail` 最稳的主链不是“先表演再慢慢补镜头”，而是“先定镜数和镜级正文，再让其余字段往骨架上长”。
- `3-Detail` 做知行合一升级时，最稳的方式不是推翻原 pass，而是把原有 `P1-P7` 重织进 `N0-N8` 节点网，让“固定顺序”和“可返工路由”同时显性化。
- `分镜构图` 在这里不是纯审美字段，它首先是结构字段。
- 每镜保留自己的 `剧本正文`，比额外维护桥接字段更稳。
- `主体锚定` 的价值在于给下游稳定抽取的实体入口，不在于写漂亮话。
- 字段真正高质量时，通常同时具备四件事：可见、可拍、可连续、可被下游抽取。
- `角色表现` 回答“人物怎么演”，`氛围表现` 回答“环境如何施压”，`摄影表现` 回答“画面怎么被光和质感组织”，`运镜手法` 回答“观众如何被带着看”。
- `转场特效` 应该是少而准的补强，不该成为掩盖镜级结构不稳的补丁。
- 电影学院派知识库最有价值的不是“名词更多”，而是能帮 `3-Detail` 把每个字段的判断变得更可解释、更不撞车。
- `导演手册` 更适合解决戏剧单元、关系变化、支点和揭示；`分镜脚本` 更适合解决镜数、方向、机位路径；`电影摄影` 更适合解决光色质和视觉重力。
- 一旦某条知识不能回写成当前字段对象，就先不用它；`3-Detail` 要的是可消费的镜级真源，不是课堂笔记。
- 只在 `SKILL.md` 里写“必须使用知识库”是不够的；真正可靠的落点是 `rubric + validation-report slot + validator` 同时存在。
- 对 `3-Detail` 这类单技能阶段，`思考过程` 最稳的落点不是新建 sidecar，而是并入 `validation-report.md` 的 closure 段，和知识证据一起形成可复核结案视图。
- 模板升级期最怕 validator 只认新模板、不认现有 runtime；双读不是妥协，而是为了把错误收束到真正有价值的层面。
- `3-Detail` 做 Skill 2.0 化时，最稳的做法是新增 canonical `steps/review/types/templates/knowledge-base` owner，同时暂时保留 `_shared/` 与关键 `references/` 兼容路径，避免下游 schema 引用和本地 validator 同时断链。
