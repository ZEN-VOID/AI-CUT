# CONTEXT.md

本文件是 `story-repair` 的经验层知识库，不是过程日志。它用于沉淀小说局部修改引发跨层一致性修复时的失败模式、修复打法和可复用 heuristic。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-knowledge-base-focused
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 只改当前章，下一轮生成又把旧线索写回来 | upstream planning source | 先 `rg` 旧线索在 `MEMORY.md`、`0-初始化`、`1-设定`、`2-卷章` 和 provider messages 中的分布 | repair 必须先产出 impact map，再决定正文改写 | 旧口径在 source/context 中无正向命中，新口径在 planning 与后续约束中命中 |
| 局部设定改了，但对象卡仍保留旧状态 | cards truth drift | 回到 `1-设定` owning card 更新状态、历史和关系字段 | 对角色/物品/场景/技能改动默认把对象卡列入影响图 | 对象卡、章节规划和正文引用同向 |
| review 返工直接改正文，绕过阶段根技能 | authorship drift | 本技能只写 repair brief，正文创作性修复回 `3-初稿` 或 `4-润色` 根技能 | repair 不直接生成 canonical creative truth；模型字段只作 legacy 元数据 | repair packet 列出 owning_stage 和返工入口 |
| 已 PASS 的终稿被局部覆盖，return actualization 仍指向旧事实 | accepted truth drift | 先失效化或重跑 stage acceptance packet，再刷新 return/STATE 投影 | 已验收内容改动必须把 acceptance/return 列为高风险消费者 | owning stage `第N章.acceptance.json` 与 actualization refs 指向新版事实 |
| 只修本章，不检查同层前列导致动机或伏笔断裂 | sibling continuity drift | 回读同卷前序章、上一章末尾、同线索首次埋点和最近一次兑现 | impact scope 固定包含同层前列与后续最近消费者 | 线索首埋、发展、当前修复和后续兑现连续 |
| 影响范围表只有抽象 surface，执行时仍靠感觉判断 | type matrix underspecification | 回到 `references/impact-scope-contract.md#Universal Type Matrix`，按对象类型加载 `types/scope/*` 包 | 通用规则层固定“当 XX 时检查 XX”，项目层只追加具体章节/对象 | repair packet 列出 `scope_packages_loaded` 与矩阵命中行 |
| story 项目清理只删除文件，`STATE.json` 仍指向已删除产物 | state projection drift | 同轮写入 `state-maintenance` run，重置当前 stage_progress、workflow_state.last_stable_state，并失效依赖这些源稿的下游投影 | 对 `projects/story/<项目名>/` 的移除/清理操作默认把 `STATE.json` 列为必改或必检对象 | 删除路径不存在；`3-drafting`/`4-polishing` 不再 completed 指向缺失文件；orphan projection 已记录 |
| repair workflow 同时存在于 `SKILL.md` 与 `steps/`，升级后 validator 阻断 | runtime spine drift | 将节点表、Mermaid、fail loops、module trigger 和 convergence 收回 `SKILL.md`，删除 `steps/` | story repair 的长期节点真源只允许在 `SKILL.md`；references/review 只能回指节点 ID，不再回指 steps 文件 | `validate_skill_2_0.py --mode delivery` 不再报告 unsupported `steps/`，smoke route 能到达 done |

## Repair Playbook

1. 先判定问题对象：线索、伏笔、角色、设定、章节事件、表达风格、验收结论还是状态投影。
2. 对任何局部修改先做 `rg` 级事实定位，找到旧口径在源层、投影层、正文层和审查层的分布。
3. 再按 `Universal Type Matrix` 选择 typed scope 包；多对象修改必须多选叠加。
4. 先改最早 canonical owner，再改 downstream projection；不要先润色正文来掩盖上游错误。
5. 若改动影响已产出章节，按“同层前列 -> 当前章 -> 后续已产出 -> 后续生成约束”的顺序处理。
6. 若涉及正文或润色创作性改写，repair 只能写 repair brief 和验收意见，不能直接替 `3-初稿` / `4-润色` 根技能改正文。
7. 修复后必须跑 review gate，至少检查旧口径残留、新口径覆盖、前后因果、对象状态、计划正文一致性。
8. 对 story 项目执行移除、清空或阶段产物清理时，不能只看 Git 状态；必须同轮检查并同步 `STATE.json`，把缺失源稿对应的当前 completed 状态改为 pending/in_progress，并记录下游 orphan projection。

## Reusable Heuristics

- 小说 repair 的核心产物不是 patch，而是 impact map；没有 impact map 的局部修复很容易回归。
- “需要动的全身”至少包括：项目记忆、初始化方向盘、对象设定、整体/卷/章规划、同卷前序章、当前章、后续已产出章、润色稿、stage acceptance packet、return actualization 和 provider sidecar。
- 源层修复优先级高于文本漂亮程度；如果上游旧设定仍在，下游任何好看的修文都会被下一轮生成覆盖。
- 已验收事实的改动不是普通文本编辑，必须重新经过 acceptance/return gate。
- repair brief 应写给 owning stage 根技能执行，而不是写成最终正文；这能保住阶段真源、作者性边界和后续审计。
- 通用类型矩阵放在 skill 规则层，项目层只补具体名称、章节和对象；不要让单项目特殊性反向削弱通用必查项。
- 删除 story 项目章节正文时，`STATE.json` 是运行时真源的一部分；即使相关路径被 `.gitignore` 忽略，也必须以磁盘 JSON 校验为准，同步 `stage_progress`、`workflow_state.last_stable_state`、`governance_index` 与 `task_log`。
- `story-repair` 的节点、路由、gate、Mermaid 和 fail-code 覆盖必须留在 `SKILL.md`；长细则可以放在 references/types/review，但只允许回指节点 ID。
- 输出 repair report 时，把 `module_trigger_manifest`、`checkpoint_evidence`、`fallback_or_degradation` 和 `next_generation_constraints` 当成闭环证据，而不是散文式补充。
