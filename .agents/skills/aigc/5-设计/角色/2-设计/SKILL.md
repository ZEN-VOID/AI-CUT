---
name: aigc-design-character-detail
description: Use when expanding the upstream AIGC character inventory into one detailed LLM-authored character design markdown per character under projects/aigc/<项目名>/5-设计/角色/2-设计.
governance_tier: full
metadata:
  short-description: AIGC detailed character design
---

# aigc 5-设计/角色/2-设计

`角色/2-设计` 消费上游 `角色/1-清单` 的汇总式清单输出，把每个角色主体扩展为可进入后续图像生成、服装设计和镜头设计的细目设计稿。它只负责角色主体设计，不生成最终图片、不替代 `3-生成`，也不改写上游清单真源。

## Context Loading Contract

- 每次调用 `$aigc-design-character-detail` 时，必须同时加载同目录 `CONTEXT.md`。
- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 每次调用本技能时，必须同时识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- 若任务绑定 `projects/aigc/<项目名>/`，必须先加载项目根 `MEMORY.md`，再按需加载项目根 `CONTEXT/` 中与角色、风格、服装、禁区和既有设定相关的上下文文件。
- 项目运行时必须读取 `projects/aigc/<项目名>/0-初始化/north_star.yaml`，用于抽取全局风格、主题方向、影像基调和项目禁区。
- 项目运行时必须读取 `projects/aigc/<项目名>/team.yaml`，只消费与角色、服装、美术、摄影、导演或设计监制相关的大师上下文；不得把无关成员意见硬塞进角色设计稿。
- 默认 subagents 路径启用时，必须读取 `../../../_shared/team-advisor-consultation-contract.md`，调用 `team.yaml` 已指定监制组成员作为资深创作顾问，围绕身份压力、身体姿态、服装材质、定妆照拍法、prompt evidence 和禁区进行请教，并在 LLM 角色设计前形成 `advisor_consultation_packet`。
- 上游角色入口固定为 `projects/aigc/<项目名>/5-设计/角色/1-清单/角色清单.md`；清单字段至少包含 `名称`、`首次登场`、`原文描述（关键词式）`。
- 固定画面约束：角色设计默认是纯色背景全身定妆照，不得置身于剧情场景、建筑空间、街景、室内陈设或复杂环境中；英文提示词必须显式包含 `full-body costume fitting photo, solid color background, no scene environment` 等等价约束。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` / meta 规则 > 本 `SKILL.md` > `references/` / `steps/` / `types/` / `review/` / `templates/` > `agents/openai.yaml` > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md`。
- 研究考据、物语、视觉解构、服装细节、摄影描述和英文提示词必须由 LLM 直接创作；`scripts/` 只能做读取、分发、字段校验、路径创建、长度检查和 manifest 汇总等机械辅助。
- 研究层必须转化为可执行设计证据链：身份、职业、阶层、地域年代、服饰工艺、身体姿态、禁区、不确定性和 prompt evidence chain 均需落到后续角色外观、服装、姿态、摄影或英文提示词，不允许停留在资料摘抄。

## Subagent Dispatch Contract

- 本技能默认启用真实 subagents 模式；用户点名本技能或父级路由命中本技能时，视为已许可按仓库合同启动 subagents。
- 推荐运行时路径：主 agent 先按共享团队顾问合同解析项目 `team.yaml` 监制 roster，向角色、服装、美术、摄影、导演或类型顾问提出具体设计问题；再按单个角色主体启动 `Worker-Character` 子任务。如 runtime 支持更细分 dispatch，可在每个角色内并行启动 `Research`、`Story`、`Visual/Costume`、`Cinematography` reviewer 或 worker。
- 顾问 subagents 输出 `advisor_consultation_packet` 的局部问题回答、可执行指导、risk note 或 inspiration；worker/reviewer subagents 只能返回局部 patch、risk note 或 reviewer finding；最终 canonical markdown 由主 agent 按模板聚合落盘。
- 顾问意见必须转化为身份、服装、姿态、摄影或 prompt 的可执行指导后才能进入设计稿，不得停留在大师名字、人格模仿或抽象审美口号。
- 若当前 system / developer / tool / user 层阻断真实 subagent dispatch，必须显式报告阻断层级、原计划 subagent 路径、实际降级路径和未真实启动的角色/ reviewer。

## Multi-Subskill Continuous Workflow

本叶子技能以单角色或批量角色为执行粒度；当父级域包或用户整体命中本技能时，视为已授权按本级声明的内部节点和 subagent 合同连续完成角色细目设计。

- 无序号同级子技能包若未来出现，默认全选并发执行，由本技能汇总、裁决和写回唯一 canonical 输出。
- 数字序号子技能包或节点（如 `1-`、`2-`、`3-`）默认按数字升序串行执行，前一节点产物自动作为后一节点输入。
- 英文序号子技能包或路线（如 `A-`、`B-`、`C-`）默认按用户意图、父级路由或输入类型单选分流；只有用户明确要求对比、并跑或批量多路线时才多选。
- 卫星技能只承担查询、恢复、审查承接或辅助动作；不会自动改写本技能的角色设计 canonical 输出，除非父级合同或用户明确要求回接。
- 每个被调度的子技能、卫星技能或 reviewer 仍必须加载自身 `SKILL.md + CONTEXT.md`；脚本只能承担机械辅助，不得替代 LLM 角色设计主创或主 agent 最终裁决。

## Input Contract

Accepted input:

- 项目名、项目路径、单个角色名、角色范围，或“角色 2-设计 / 角色细目设计 / 从角色清单生成角色设计稿”等任务。
- 已存在的 `projects/aigc/<项目名>/5-设计/角色/1-清单/角色清单.md`。
- 项目初始化文件 `0-初始化/north_star.yaml` 与 `team.yaml`。

Required input:

- 可定位、可读取的项目根 `projects/aigc/<项目名>/`。
- 可读取的上游 `角色清单.md`，且每个待设计角色至少有 `名称`、`首次登场`、`原文描述（关键词式）`。
- 可读取的 `north_star.yaml` 和 `team.yaml`；若缺失，必须在输出中标记上下文缺口，不得伪造全局风格或大师监制。

Optional input:

- 用户指定的角色优先级、单角色目标、时代/地域考据要求、服装材质偏好、摄影风格偏好或禁区。
- 项目 `CONTEXT/` 中已有视觉设定、服装设定、世界观材料、角色关系说明或风格提示词。
- 网络搜索许可；仅用于冷门历史、地域、职业、器物、服饰或文化考据，且必须记录来源摘要和使用边界。

Reject or clarify when:

- 用户要求跳过 `角色/1-清单`，直接凭剧情印象批量生成角色设计稿。
- 用户要求脚本自动生成研究、设计、物语或提示词正文。
- 用户要求把场景、道具、最终图片或视频生成结果写入本路径。
- 同一角色主体在清单中无法区分，且没有足够上下文裁决，应先返回上游清单修复建议。

## Mode Selection

| mode | 触发信号 | 输出 |
| --- | --- | --- |
| `single_character` | 指定单个角色名或清单行 | 单个角色细目设计 markdown |
| `batch_from_list` | 给定项目且未限制角色 | 每个清单角色一个 markdown，可附批量执行报告 |
| `incremental_fill` | 上游清单 merge 后存在新增角色或 `design-manifest.yaml` 标出 `design_gaps` | 只为缺设计稿的角色补齐设计，不覆盖既有设计稿 |
| `repair` | 已有设计稿缺字段、提示词超长、与清单或项目风格冲突 | 最小修复后的角色设计稿 |
| `review_only` | 用户只要求检查角色设计稿 | 审查报告，不改写 canonical 设计稿，除非用户随后要求修复 |

## Reference Loading Guide

| 场景 | 必读文件 |
| --- | --- |
| 任意角色细目设计任务 | `references/character-design-contract.md`、`steps/character-design-workflow.md` |
| 默认 subagents / team advisor consultation | `../../../_shared/team-advisor-consultation-contract.md` |
| 清单 merge 后的设计缺口补齐 | `../../references/incremental-reconciliation-contract.md` |
| 角色类型、主体粒度和设计深度分流 | `types/character-design-type-map.md` |
| 输出验收、subagent/reviewer 汇流和风险分级 | `review/review-contract.md` |
| 输出样板 | `templates/output-template.md` |
| 脚本辅助边界与机械校验 | `scripts/README.md` |
| 可复用经验 | `knowledge-base/character-design-heuristics.md` |
| 产品入口元数据 | `agents/openai.yaml` |

## Visual Maps

```mermaid
flowchart TD
    A["触发角色/2-设计"] --> B["加载 SKILL.md + CONTEXT.md"]
    B --> C["加载项目 MEMORY.md / CONTEXT/ / north_star.yaml / team.yaml"]
    C --> D["读取角色/1-清单/角色清单.md"]
    D --> E{"选择模式"}
    E -->|"single_character"| F["锁定单角色清单锚点"]
    E -->|"batch_from_list"| G["枚举清单角色主体"]
    E -->|"repair"| H["读取既有设计稿与缺口"]
    E -->|"review_only"| I["读取待审查设计稿"]
    F --> J["形成 type_profile"]
    G --> J
    H --> J
    I --> N["review/review-contract.md"]
    J --> K["形成 research_profile / prompt evidence chain"]
    K --> L["steps/character-design-workflow.md"]
    L --> Q["LLM-first 创作与汇流"]
    Q --> M["templates/output-template.md"]
    M --> N
    N --> O{"通过门禁?"}
    O -->|"yes"| P["写入 5-设计/角色/2-设计/<角色名>.md"]
    O -->|"no"| K
```

```mermaid
flowchart LR
    A["角色清单锚点"] --> D["canonical 角色设计稿"]
    B["项目风格与禁区"] --> D
    C["team.yaml 设计相关监制"] --> D
    E["Research profile / evidence chain"] --> D
    F["Story patch"] --> D
    G["Visual / Costume patch"] --> D
    H["Cinematography patch"] --> D
    D --> I["Review Gate"]
    I --> J["Output Contract"]
```

```mermaid
stateDiagram-v2
    [*] --> Intake
    Intake --> ContextReady
    ContextReady --> AnchoredToList
    AnchoredToList --> Typed
    Typed --> Researched
    Researched --> Dispatching
    Dispatching --> Drafting
    Dispatching --> Downgraded: upper policy blocks subagents
    Downgraded --> Drafting
    Drafting --> Reviewing
    Reviewing --> Rework: blocking finding
    Rework --> Drafting
    Reviewing --> Accepted
    Accepted --> Written
    Written --> [*]
```

## Execution Contract

1. 读取本 `SKILL.md + CONTEXT.md`，并在项目任务中加载项目 `MEMORY.md`、相关项目 `CONTEXT/`、`north_star.yaml` 和 `team.yaml`。
2. 读取上游 `角色清单.md` 和可选 `projects/aigc/<项目名>/5-设计/角色/design-manifest.yaml`，锁定待设计角色主体、首次登场和原文描述关键词；不得新增清单外角色作为 canonical 输出。
3. 按用户指定、清单缺口或 manifest 的 `design_gaps` 选择目标角色；已有设计稿默认跳过，除非用户明确要求 repair / regenerate。
4. 按 `types/character-design-type-map.md` 判定角色主体类型，形成 `type_profile`。
5. 形成 `research_profile`：将清单、项目上下文与必要考据转化为身份、职业、阶层、地域年代、服饰工艺、身体姿态、禁区、不确定性和 prompt evidence chain。
6. 按 subagent 合同和共享团队顾问合同分发角色任务：先请教项目监制顾问并形成 `advisor_consultation_packet`，再把可执行指导作为额外上下文交给角色 worker/reviewer 或主 agent 创作；若真实 dispatch 被阻断，按降级口径执行并记录。
7. 由 LLM 完成研究考据、物语、视觉解构、服装解构、摄影描述和英文提示词；创作时必须吸收 `advisor_consultation_packet` 中已裁决的可执行指导，冷门信息可按允许条件搜索并保留来源摘要。
8. 摄影描述和英文提示词固定为纯色背景全身定妆照，不得把角色置入具体场景或复杂环境。
9. 使用 `templates/output-template.md` 为每个角色生成唯一 markdown，写入 `projects/aigc/<项目名>/5-设计/角色/2-设计/`，并可更新 `design-manifest.yaml` 的 `design_file` 与 `design_gaps`。
10. 按 `review/review-contract.md` 检查字段完整、清单可回指、项目风格一致、研究证据链、LLM-first、英文提示词不超过 2000 字符。

## Field Mapping

| field_id | 输出/证据 | 内容要求 | 失败码 |
| --- | --- | --- | --- |
| `FIELD-CHAR-DESIGN-01` | 上游清单锚点 | 名称、首次登场、原文描述复述可回指 `角色/1-清单` | `FAIL-CHAR-DESIGN-01` |
| `FIELD-CHAR-DESIGN-01A` | 增量补缺 | 只处理缺设计稿或用户指定 repair 的主体，未静默覆盖既有设计稿 | `FAIL-CHAR-DESIGN-01A` |
| `FIELD-CHAR-DESIGN-02` | 项目风格锚点 | `north_star.yaml` 的全局风格、主题、禁区已消费并显式折入提示词 | `FAIL-CHAR-DESIGN-02` |
| `FIELD-CHAR-DESIGN-03` | 监制上下文 | `team.yaml` 中设计相关大师语境已选择性消费，不无关堆砌 | `FAIL-CHAR-DESIGN-03` |
| `FIELD-CHAR-DESIGN-04` | 解构字段 | `Identity & Story Pressure`、`Visual Drivers`、`Detailed Character Design`、`Detailed Costume Design`、`Cinematography` 全部存在 | `FAIL-CHAR-DESIGN-04` |
| `FIELD-CHAR-DESIGN-05` | 提示词 | 英文、含全局风格提示词与服装风格、不超过 2000 字符 | `FAIL-CHAR-DESIGN-05` |
| `FIELD-CHAR-DESIGN-06` | LLM-first | 脚本没有生成研究、物语、解构或提示词正文 | `FAIL-CHAR-DESIGN-06` |
| `FIELD-CHAR-DESIGN-07` | Subagents | 默认真实 dispatch；阻断时有完整降级报告 | `FAIL-CHAR-DESIGN-07` |
| `FIELD-CHAR-DESIGN-08` | 定妆照约束 | 默认为纯色背景全身定妆照，不置身剧情场景或复杂环境 | `FAIL-CHAR-DESIGN-08` |
| `FIELD-CHAR-DESIGN-09` | 研究证据链 | 身份、职业、阶层、地域年代、服饰工艺、身体姿态、禁区、不确定性和 prompt evidence chain 均有结论并回流到设计字段 | `FAIL-CHAR-DESIGN-09` |
| `FIELD-CHAR-DESIGN-10` | Team advisor consult | 已按 `team.yaml` 请教项目监制顾问，并把身份、服装、姿态、摄影和 prompt 指导作为创作前上下文；阻断时有降级报告 | `FAIL-CHAR-DESIGN-10` |

## Root-Cause Execution Contract (Mandatory)

出现以下问题时，必须沿链路上溯并修复源层合同：

- 设计稿脱离 `角色/1-清单`，新增或替换 canonical 角色主体。
- 上游清单增量更新后，没有识别缺设计稿主体，或覆盖了已有角色设计稿。
- 没有消费 `north_star.yaml` / `team.yaml`，却声称符合项目风格或大师监制。
- 研究考据、物语、设计解构或提示词由脚本拼接、模板灌字或启发式扩写生成。
- 角色设计变成图片生成执行、场景设计、道具设计或最终视频提示词。
- 英文提示词未引用全局风格与服装风格，或超过 2000 字符。
- 角色 prompt 或摄影字段把角色放进具体场景、建筑空间、街景、室内陈设或复杂背景，而不是纯色背景全身定妆照。
- 研究层只写资料、风格口号或世界观摘要，没有转化为身份/职业/阶层/地域年代/服饰工艺/身体姿态/禁区/不确定性和 prompt evidence chain。
- 默认 subagents 路径被静默跳过，且没有报告阻断层级和降级路径。
- 启用 subagents 时只按角色 worker 分工，没有调用 `team.yaml` 项目监制顾问进行具体请教，或没有把顾问意见转成可执行设计指导。

必经链路：

`Symptom -> Direct Script/Subagent/Prompt Overreach -> 角色/2-设计 Section Owner -> AGENTS.md LLM-first / Subagent / Skill 2.0 Rule`

## Output Contract

### Required output

1. 每个待设计角色输出一份细目设计 markdown。
2. 输出必须包含：`名称 / 首次登场 / 原文描述复述`、`研究考据`、`物语`、`解构`、`提示词设计`。
3. `研究考据` 必须包含字段：`Identity Evidence`、`Occupation / Class Evidence`、`Region & Era Evidence`、`Costume Craft Evidence`、`Body & Posture Evidence`、`Taboo / Safety Constraints`、`Uncertainty Notes`、`Prompt Evidence Chain`。
4. `解构` 必须包含字段：`Identity & Story Pressure`、`Visual Drivers`、`Detailed Character Design`、`Detailed Costume Design`、`Cinematography`。
5. `提示词设计` 必须为英文、引用全局风格提示词与服装风格，并控制在 2000 字符内。
6. 画面固定为纯色背景全身定妆照，不得置身具体场景、建筑空间、街景、室内陈设或复杂环境。
7. 可选更新 `projects/aigc/<项目名>/5-设计/角色/design-manifest.yaml`，记录 `design_file` 和剩余 `design_gaps`；manifest 不替代设计稿真源。

### Output format

| output_id | format |
| --- | --- |
| `OUTPUT-CHARACTER-DESIGN` | Markdown 单角色设计稿，使用 `templates/output-template.md` |
| `OUTPUT-CHARACTER-DESIGN-REPORT` | Markdown 执行或审查报告，可选 |

### Output path

| output_id | canonical path |
| --- | --- |
| `OUTPUT-CHARACTER-DESIGN` | `projects/aigc/<项目名>/5-设计/角色/2-设计/<角色名>.md` |
| `OUTPUT-CHARACTER-DESIGN-REPORT` | `projects/aigc/<项目名>/5-设计/角色/2-设计/执行报告.md` |
| `OUTPUT-CHARACTER-MANIFEST` | `projects/aigc/<项目名>/5-设计/角色/design-manifest.yaml` |

### Naming convention

- 角色设计稿默认命名为 `<角色名>.md`。
- 若角色名包含路径分隔符、控制字符或与现有角色冲突，使用安全名 `<角色名>__<首次登场ID>.md`。
- 首次登场沿用上游清单格式，例如 `第N集.md / 1-1-1`。
- 已有 `<角色名>.md` 不因清单 merge 或 canonical 名称变化而静默覆盖；名称变化默认记录映射，重命名需先同步引用。
- 本技能不改写 `角色清单.md`；发现清单问题时只在报告中提出上游修复建议。

### Completion gate

- 已读取本 `SKILL.md + CONTEXT.md`，并在项目任务中加载项目 `MEMORY.md`、相关项目 `CONTEXT/`、`north_star.yaml` 和 `team.yaml`。
- 待设计角色均来自 `角色/1-清单/角色清单.md`。
- 已识别并跳过既有设计稿；仅补齐缺设计稿或用户明确指定 repair 的主体。
- 每份设计稿字段齐全，且研究、物语、解构和提示词由 LLM 直接创作。
- 研究层已从资料转化为设计证据链，并明确不确定性与禁区。
- 已按 `team.yaml` 监制 roster 形成 `advisor_consultation_packet`，且采纳内容已落到身份压力、服装、姿态、摄影或 prompt evidence；若被上层阻断，已记录降级报告。
- 英文提示词含全局风格提示词与服装风格，且长度不超过 2000 字符。
- Cinematography 与英文提示词固定为 `full-body costume fitting photo`、纯色背景、无场景环境。
- 已执行 `review/review-contract.md` 的人工审查或等价机械校验。
- subagents 默认路径已真实启动；若被上层阻断，已记录降级报告。
