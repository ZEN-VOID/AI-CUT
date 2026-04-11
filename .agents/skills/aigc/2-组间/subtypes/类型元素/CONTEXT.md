# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `2-组间/类型元素` 的经验层知识库，不是执行日志。
- 调用同目录 `SKILL.md` 时，应自动预加载本文件。
- 优先级固定为：用户显式请求 > 根 `AGENTS.md` > 上层 `SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 只有类型名，没有导演后果 | SKILL 合同层 | 补 `类型承诺` 与 `放大与克制` | 固定六区块输出 | 下游能从类型文档中提炼动作 |
| 混合题材被平均分配 | 裁决层 | 回到主副类型裁决 | 在合同中强制“先主后副” | 不再出现“什么都有一点” |
| 世界模式与类型冲突 | 世界成立性层 | 先保世界，再调类型表达 | 在 VSM 固化世界优先检查 | 输出不再自相矛盾 |
| 类型指导未被下游读取 | handoff 层 | 强化 `下游阶段指导` | 在根级路由要求联合消费 | `导演意图 / 3-明细` 可直接引用 |
| `导演意图` 继承到的类型指导过空 | 下游合同层 | 补写给 `导演意图` 的五维继承提示 | 在输出模板强制声明 `主题表达 / 情感基调 / 叙事视点 / 视听法则 / 表演尺度` | `导演意图` 可直接据此翻译为组级执行法则 |

## Repair Playbook

1. 先看 `主副类型裁决` 是否明确。
2. 再看 `观众合同` 与 `类型承诺` 是否可感知。
3. 再看 `误配禁区` 是否充分。
4. 最后检查 `下游阶段指导` 是否真能交给后续阶段。

## Reusable Heuristics

- 类型指导最常见的失败不是“类型判断错一个词”，而是“判断之后没有形成导演后果”。
- 真正稳定的混合题材写法不是折中，而是明确谁为主、谁为辅。
- `误配禁区` 不是附录，而是类型协议的硬护栏。
- 如果 `类型元素` 不能告诉 `导演意图` 哪些维度必须继承，导演意图就会重新发明一套风格语言，造成共享约束与逐组口径漂移。
- 对类型协议这类稳定内容输出技能，主合同应尽量只保留边界与回指，把 VSM、field map、固定区块沉到 `references/`。
- 对长期维护的可执行技能目录，除 `SKILL.md + CONTEXT.md` 外，还应补齐 `agents/openai.yaml`，这样 Codex / OpenAI 侧的展示名、摘要和默认提示才有稳定入口。
- 对项目级 `类型元素` 思维链，真正先裁的不是“像什么类型词”，而是“观众先被什么吸住 + 下游要继承什么导演后果”；主副类型只是这场裁决的外显结果。
- 类型协议的可见层应只保留六区块快照与 Gate，淘汰掉的备选类型组合、比较废案和中途摇摆应留在隐藏推理层，不混入正文。

## Case Log

### Case-20260409-AIGC-DIRECTING-TYPE-ELEMENTS-BASELINE

- milestone_type: source_contract_change
- outcome: 为 `2-组间/类型元素` 建立了项目级内容输出合同与经验层。
- root_cause_or_design_decision: 参考仓 `2-类型指导` 的核心价值在“主副类型裁决 + 类型导演后果 + 污染防护”，但当前仓不应直接复制 JSON 输出与旧目录；当前真源应收束为统一根文件中的 `类型元素` 字段区块，而不是继续保留旧 `type-playbook.md` 主稿叙述。
- final_fix_or_heuristic: 固定 `主副类型裁决 / 观众合同 / 类型承诺 / 放大与克制 / 误配禁区 / 下游阶段指导` 六区块。
- prevention_or_replication_checklist:
  - [x] 已明确主副类型裁决
  - [x] 已把类型结论翻译成导演后果
  - [x] 已设置误配禁区
- evidence_paths:
  - `.agents/skills/aigc/2-组间/subtypes/类型元素/SKILL.md`
  - `.agents/skills/aigc/2-组间/subtypes/类型元素/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/2-类型指导/SKILL.md`
- user_feedback_or_constraint: 用户要求参照 `2-类型指导` 完善当前 `2-组间` 子技能，并保持内容输出型定位。

### Case-20260409-AIGC-DIRECTING-TYPE-ELEMENTS-REFERENCES

- milestone_type: source_contract_change
- outcome: 将 `类型元素` 重构为“主合同 + references 模块细则”结构，保留既有类型区块、路径与项目级边界。
- root_cause_or_design_decision: 旧版单文件合同虽完整，但不利于后续在不改语义的前提下维护 VSM、field map 与输出模板；按最新规范应收束成主合同 + 模块细则。
- final_fix_or_heuristic: 保留 `类型元素` 六区块与硬规则不变，只调整承载位置，把思维链、流程、策略、输出模板拆到 `references/*.md`，并统一回写到根文件 `类型元素` 字段区块。
- prevention_or_replication_checklist:
  - [x] 已建立 `references/` 四件套
  - [x] 主 `SKILL.md` 已收束为主合同
  - [x] 统一根文件中的 `类型元素` 字段区块已成为 canonical 真源字段区块
- evidence_paths:
  - `.agents/skills/aigc/2-组间/subtypes/类型元素/SKILL.md`
  - `.agents/skills/aigc/2-组间/subtypes/类型元素/references/chain-of-thought.md`
  - `.agents/skills/aigc/2-组间/subtypes/类型元素/references/execution-flow.md`
  - `.agents/skills/aigc/2-组间/subtypes/类型元素/references/type-strategies.md`
  - `.agents/skills/aigc/2-组间/references/output-template.md`
- user_feedback_or_constraint: 用户要求在不改变内容基础的前提下按最新规范重构。

### Case-20260409-AIGC-DIRECTING-TYPE-ELEMENTS-DIRECTOR-HANDOFF

- milestone_type: source_contract_change
- outcome: 强化了 `类型元素 -> 导演意图` 的 handoff，要求类型结论必须明确下沉到导演意图的五个继承维度。
- root_cause_or_design_decision: 仅写“下游阶段指导要覆盖导演意图”仍然过粗，容易让集级 `导演意图` 重新发明自己的情感、视点与表演语言；项目级类型协议需要更直接地规定哪些维度必须被继续继承。
- final_fix_or_heuristic: 在 `类型元素` 输出契约与执行流程里新增给 `导演意图` 的五维继承要求：`主题表达 / 情感基调 / 叙事视点 / 视听法则 / 表演尺度`。
- prevention_or_replication_checklist:
  - [x] `下游阶段指导` 已明确覆盖 `导演意图`
  - [x] 已补五维继承要求
  - [x] 已同步执行流程的 handoff 步骤
- evidence_paths:
  - `.agents/skills/aigc/2-组间/subtypes/类型元素/CONTEXT.md`
  - `.agents/skills/aigc/2-组间/references/output-template.md`
  - `.agents/skills/aigc/2-组间/subtypes/类型元素/references/execution-flow.md`
- user_feedback_or_constraint: 用户要求优化 `导演意图` 模板，并同步调整相关源层规则。

### Case-20260409-AIGC-DIRECTING-TYPE-ELEMENTS-CHAIN-REFRESH

- milestone_type: source_contract_change
- outcome: 按最新 `think-think` 规范重写了 `类型元素` 的思维链真源，使其从“字段检查表”升级为“可见快照 + 三轴三重 + 工具后反思 + 验证闭环”合同。
- root_cause_or_design_decision: 旧版 `references/chain-of-thought.md` 只有字段表、thought pass 与 pass table，能做静态检查，但不能指导模型先裁什么、删什么、比什么，也缺少可见/隐藏分层与 Gate 闭环。
- final_fix_or_heuristic: 保留原有 `FIELD-TE-01` 到 `FIELD-TE-06` 与六区块接口不变，补入 `模式与对象`、`Think-Think Design Snapshot`、`工具后反思与 Gate Summary`、`Validation Matrix`，并把判断压力对齐到 `类型裁决 -> 导演后果 -> 下游 handoff`。
- prevention_or_replication_checklist:
  - [x] 已保留原字段接口与输出区块
  - [x] 已补齐启发式工作链与三轴三重裁决
  - [x] 已建立可见/隐藏分层与 Gate Summary
  - [x] 已把验证项接回 `FAIL-TE-01` 到 `FAIL-TE-06`
- evidence_paths:
  - `.agents/skills/aigc/2-组间/subtypes/类型元素/references/chain-of-thought.md`
  - `/Users/vincentlee/.codex/skills/meta/解构/思维/think-think/SKILL.md`
  - `.agents/skills/aigc/2-组间/subtypes/导演意图/references/chain-of-thought.md`
- user_feedback_or_constraint: 用户要求“按照最新的思维链设计规范”优化 `类型元素` 子技能的思维链文件。
