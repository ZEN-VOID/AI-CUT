# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/3-Detail` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/3-Detail/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `3-Detail` 在 root / registry 中已被视为 active stage，但阶段目录为空 | 阶段锚点层 | 建立 `SKILL.md + CONTEXT.md + CHANGELOG.md + openai.yaml + shared I/O` | 将空目录视为规则层故障，而不是“以后再补”的待办 | 根技能与 registry 能回指真实阶段合同 |
| 制作组角色目录存在，但 agent 文档全部是 0 字节占位 | agent provisioning 层 | 为 team 与每个角色补齐最小 agent contract | 把“目录存在但文件空白”视为未完成建队，而不是已落地 roster | 每个角色都有明确输入、输出和越权禁令 |
| 多专业角色都在写同一 shot 字段，导致 patch 冲突 | 字段槽位层 | 用 `_shared/IO_CONTRACT.md` 固定 field-slot 与 merge precedence | 将 field-slot contract 视为父 skill 必需共享真源 | 多角色 patch 可被父 skill 稳定合成 |
| 组级导演意图能读，但下不去到 shot skeleton | execution topology 层 | 强制 `分镜规划` 先产出 `分镜ID / 时间段 / coverage` 骨架 | 把 planner skeleton 写成进入专业角色的先决条件 | 专业角色不再自行发明镜序 |
| 下游又开始读取平行 sidecar 或旧 detail 主稿 | output governance 层 | 收口到 `projects/<项目名>/3-Detail/第N集.json` | 在父 skill 与 team 固化“唯一根文件 + patch-in-place” | `query / review / 5-Image / 6-Video` 都以 root JSON 为先 |
| 运镜或摄影角色过度炫技，压过叙事任务 | type routing 层 | 默认以 `叙事派` 为主路由，`炫技派` 只做显式对照 | 在 team 合同中固定 default vs challenger 关系 | 运镜字段先服务剧情任务，再追求表达上限 |
| 制作组角色能分工，但产出仍显单调或质量不稳 | agent prompt contract 层 | 把共享创作方法、质量门禁、失败回退收敛成 team 级真源，再让角色只写局部 delta | 以 `_shared/CREATIVE_QUALITY_PLAYBOOK.md` 作为制作组共享方法真源，避免 15 个角色平行漂移 | 专业角色 `agents_plan / note / report` 变得可解释，patch 更具体且少空话 |

## Repair Playbook

1. 先看阶段问题是“空壳未落合同”“角色未建队”“字段冲突”还是“下游真源漂移”。
2. 若根文件缺失或 shot skeleton 不稳，先回到 `分镜规划`，不要让各 specialist 各写各的镜头。
3. 若字段打架，优先修 `_shared/IO_CONTRACT.md` 的 field-slot 与 merge precedence，而不是靠人工临场裁判。
4. 若输出被平行文稿分裂，强制回收写回权到父 skill，并只保留 `3-Detail/第N集.json`。
5. 若风格化表达压过叙事，优先降级为 `叙事派 + 摄影师` 的保守路线，再决定是否追加挑战方案。
6. 若角色文档只有“定位 + 输入输出 + 禁止项”，应视为提示合同不完整，先补共享创作质量手册，再补角色级局部方法。

## Reusable Heuristics

- `3-Detail` 最稳的定位不是“把导演意图再写一遍”，而是“把组级导演意图投影为 shot-level schema 字段”。
- 这类阶段最容易出错的点不是文采，而是 field ownership；先锁字段槽位，再谈风格发挥。
- `分镜规划` 必须先出手，否则 specialist 角色会各自脑补镜序，最终合不回同一份 JSON。
- `炫技派` 最适合作为挑战者，而不是默认主路由；默认路由必须先保护叙事清晰度。
- reviewer / auditor 没落盘时，父 skill 再强也容易在收尾阶段放过字段漂移与越权写回。
- `3-Detail` 里的串行 tranche 和角色并行只定义 patch 依赖，不定义交互形态；默认应由父 skill 在后台派发并收束，别让多角色前台轮询侵蚀根文件治理边界。
- 制作组的高质量方法不应散落在每个角色文件里；最佳落点是 team 共享方法真源 + 单角色 delta。
- 对 `3-Detail` 来说，`agents_plan` 最适合承载 shot skeleton、字段裁决顺序与冲突上抛摘要；真正写进 episode JSON 的仍应是父 skill 聚合后的 patch。

### Case-20260412-AIGC-DETAIL-AGENTS-PLAN-ALIGNMENT

- milestone_type: source_contract_change
- outcome: 将 `3-Detail` 从 patch-only handoff 统一升级为 `agents_plan + patch / note / report` 的制作组合同。
- root_cause_or_design_decision: `1-Planning` 已切到“subagents 负责思考计划、skills 负责执行闭环”的新口径，但 `3-Detail` 仍要求制作组只返 patch/note/report，导致阶段间 subagent 语义不一致。
- final_fix_or_heuristic: 同步更新父 skill、shared I/O、制作组 team、共享质量/提示合同与角色入口元数据，明确 `agents_plan` 只用于说明 shot-level 裁决路径、字段计划与阻塞摘要，不冒充 canonical episode JSON。
- prevention_or_replication_checklist:
  - [x] 父 skill 已改为 agents-plan-aware handoff
  - [x] shared I/O 已补 `agents_plan_<role>` 命名
  - [x] team 与角色入口元数据已同步 `allowed_return_types`
  - [x] 共享质量/提示合同已统一新口径
- evidence_paths:
  - `.agents/skills/aigc/3-Detail/SKILL.md`
  - `.agents/skills/aigc/3-Detail/_shared/IO_CONTRACT.md`
  - `.codex/agents/aigc/制作组/team.md`
  - `.codex/agents/aigc/制作组/_shared/CREATIVE_QUALITY_PLAYBOOK.md`
  - `.codex/agents/aigc/制作组/_shared/PROMPT_STABILITY_CONTRACT.md`
  - `.codex/agents/aigc/制作组/分镜表现/分镜规划.md`
- user_feedback_or_constraint: 用户要求把 `1-Planning` 已确定的“取消 thinking sidecar 硬要求，统一改为 agents plan + skill execution”口径继续推广到 `3-Detail` 及其后续阶段。

## Case Log

### Case-20260412-AIGC-DETAIL-STAGE-BOOTSTRAP

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/3-Detail` 建立父 skill、shared I/O、经验层、变更记录与 `openai.yaml`，并同步落盘 `.codex/agents/aigc/制作组/team.md` 与 16 个角色合同。
- root_cause_or_design_decision: 当前仓内 `aigc` 根技能、registry、query/review 与 shared runtime 都已经把 `3-Detail` 当作 active stage 使用，但阶段目录与制作组 roster 仍是空壳；继续空置会让 `2-Global -> 3-Detail -> 3-Detail/第N集.json` 的责任链长期漂移。
- final_fix_or_heuristic: 建立 `3-Detail/SKILL.md + CONTEXT.md + CHANGELOG.md + agents/openai.yaml + _shared/IO_CONTRACT.md`，并把制作组 team、14 个专业角色、1 个 reviewer 与 1 个 auditor 的合同一起补齐，锁定“父 skill 独占 JSON 写回，subagents 只返 agents_plan + patch / note / report”的治理边界。
- prevention_or_replication_checklist:
  - [x] `3-Detail` 父 skill 已建立
  - [x] 制作组 team 已建立
  - [x] 所有角色文件已从 0 字节占位升级为最小合同
  - [x] shared I/O 已锁定 field-slot 与 merge precedence
- evidence_paths:
  - `.agents/skills/aigc/3-Detail/SKILL.md`
  - `.agents/skills/aigc/3-Detail/_shared/IO_CONTRACT.md`
  - `.codex/agents/aigc/制作组/team.md`
  - `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- user_feedback_or_constraint: 用户要求以 `skill-subagents` 为基线，用 `brainstorming + senior-prompt-engineer` 深度重构 `3-Detail`，并让 subagents 负责思考、父 skill 统筹输入输出。

### Case-20260412-AIGC-DETAIL-CREATIVE-QUALITY-UPGRADE

- milestone_type: source_contract_change
- outcome: 将制作组从“字段分工卡”升级为“共享创作方法 + 角色 delta”的高质量 agent 合同。
- root_cause_or_design_decision: 原有制作组 team 与角色 agent 主要约束输入、输出、越权边界和 patch handoff，能保证不乱写，但无法稳定保证写得好；缺的不是更多文采，而是共享创作方法、质量门禁、失败回退和 `note / report` 最小合同。
- final_fix_or_heuristic: 新增 `.codex/agents/aigc/制作组/_shared/CREATIVE_QUALITY_PLAYBOOK.md` 作为共享方法真源，并让 `team.md`、`3-Detail/SKILL.md` 与角色 agent 统一回指；角色文件只保留本角色的创作方法、质量门禁和保守回退 delta。
- prevention_or_replication_checklist:
  - [x] 制作组共享创作质量真源已建立
  - [x] 父 skill 已把共享质量手册加入强制读取链路
  - [x] team 已把质量门禁升级为共享合同
  - [x] 各角色输出合同已补 `report` 路径与局部质量 delta
- evidence_paths:
  - `.codex/agents/aigc/制作组/_shared/CREATIVE_QUALITY_PLAYBOOK.md`
  - `.codex/agents/aigc/制作组/team.md`
  - `.codex/agents/aigc/制作组/分镜表现/分镜规划.md`
  - `.codex/agents/aigc/制作组/摄影美学/摄影师.md`
  - `.agents/skills/aigc/3-Detail/SKILL.md`
- user_feedback_or_constraint: 用户明确指出 `.codex/agents/aigc/制作组` 相关智能体“仅有简单目标和规范明确，没有确保高质量创作的方法和引导”，要求直接升级。
