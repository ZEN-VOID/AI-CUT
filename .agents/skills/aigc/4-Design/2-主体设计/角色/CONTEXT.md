# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/角色/2-设计` 的经验层知识库，不是过程日志。
- 调用本父 skill 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-13

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `2-设计` 跳过 `1-清单` 直接发明角色设计 | 输入锚点层 | 强制回到 `角色清单.json` 锁角色 canonical identity | 在 `SKILL.md` 和 team 合同中固化“先清单、再设计” | 不再出现无对象池设计 |
| 四个 specialist 各写一整份角色稿，父 skill 无法收束 | 编排边界层 | 收回写回权到父 skill，只允许返回 `agents_plan + patch / note / report` | 在 `team.md` 与 `_shared/IO_CONTRACT.md` 固化 agents-plan-aware handoff | canonical 输出只由父 skill 写回 |
| `形象建模` 与 `服装 / 妆容 / 个性` 三条线互相打架 | reviewer 合同层 | 进入 `角色一致性复核`，要求指出冲突字段与返工入口 | 将跨字段一致性检查设为默认 tranche | reviewer 能给出明确 rework |
| 角色设计只剩 Markdown，没有 machine-first carrier | 输出治理层 | 补回 `character_design.json` 并让 Markdown 与其同源 | 在输出模板中固定 JSON 为 canonical | 下游面板/生图能稳定消费 JSON |
| 角色设计吞掉场景或道具职责 | 边界治理层 | 将场景/道具信息降级为只读 context packet | 在父 skill 中固化“只读桥接，不并入常驻团队” | 不再出现跨模块越权 |
| `.codex/agents/aigc/设计组/角色设计/*.md` 只有空文件或断链 | subagent 真源层 | 补齐 `team.md + planner + 4 specialists + reviewer + auditor` | 让父 skill 只回链真实存在的 agent docs | team 引用与物理文件一致 |
| 主合同改成知行合一后，类型策略/输出模板仍留在并列 `references/` | 真源治理层 | 把角色分型、冲突 tie-break、思行节点和输出合同全部收回主 `SKILL.md` | 对 `复杂链路的骨架 / 细则分层=false` 的父 skill，只保留迁移 stub，不保留并列 reference 真源 | `SKILL.md` 成为唯一可执行真源 |
| 演员联想被直接写成角色定稿，导致角色像明星模仿而不是自身 identity | 视觉锚点治理层 | 将“第一联想演员”降级为 `casting_reference` 具象代理，并强制转译成 `feature_markers / signature_elements` | 在 `N5-VISUAL-ANCHOR`、shared I/O 与 reviewer 合同里固化“演员联想只作桥，不作定稿” | 下游 specialist 消费的是角色特征而非明星名字 |

## Repair Playbook

1. 先查 `1-清单/角色清单.json` 是否存在且角色 identity 稳定。
2. 再看 `team.md` 是否仍把写回权保留在父 skill。
3. 再看 `character_design.json` 是否与逐角色 Markdown 同源。
4. 若角色设计冲突，优先回到 `角色一致性复核` 指定的字段槽位返工。
5. 最后才调整单次角色文案或 prompt 话术。

## Reusable Heuristics

- 角色设计最稳的入口不是“从镜头里直接想象角色”，而是先有角色对象池，再做结构化设计。
- `形象建模` 先跑不是为了抢权，而是为了给服装、妆容、个性三条线提供同一个视觉锚点。
- reviewer 最有价值的工作不是润色，而是阻止多个 specialist 把角色拉向不同的人设。
- 对 `2-设计` 来说，`character_design.json` 不是附属 sidecar，而是下游面板和生图可持续复用的 canonical carrier。
- 场景和道具信息适合作为只读兼容约束，不适合让角色设计组扩张成跨模块常驻团队。
- 对角色设计来说，`agents_plan` 最适合承载角色批次、字段补位顺序与 reviewer/auditor 返工摘要；最终 design carrier 仍只能由父 skill 写回。
- 当用户显式要求知行合一且 `复杂链路的骨架 / 细则分层=false` 时，`2-设计` 的 role tier 策略、world mode 约束、并行 tranche 和 one-shot output 都应内收到主 `SKILL.md`，不再让 `references/` 承载并列步骤真源。
- “第一时间想到谁来演”最适合放在 `形象建模` 节点，作为把抽象人设压成具象视觉锚点的桥，而不是放到所有 specialist 各自发散。
- 演员联想必须马上下沉为 `feature_markers / signature_elements`，这样服装、妆容、个性三条线消费的是角色特征，而不是直接追着某个真人脸跑。
- 当角色设计 Markdown 要服务后续面板或生图时，最稳的结构不是按 specialist 分栏展示，而是固定三段式：`物语 -> 解构 -> prompt整合`；感性叙述、人设拆解和模型提示词各自承担不同职责，不要混写。
- 当用户给出精确字段矩阵时，Markdown 模板可以采用一套展示投影命名，但必须在主 `SKILL.md` 同步声明“展示投影不等于 canonical JSON 字段”，否则模板层和 machine-first carrier 会再次漂移。
- 当角色设计字段开始细到 `种族 / 年龄 / 肤色 / 身高 / 体重 / 景别 / 发饰` 这一级时，最容易漂移的不是文案，而是“把缺证据写成事实”与“把角色主体拍法越权写成导演调度”；因此必须在 specialist 并行前先锁 `attribute_certainty + photo_contract`。
