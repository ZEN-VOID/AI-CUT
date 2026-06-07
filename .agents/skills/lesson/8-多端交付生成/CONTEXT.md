# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `lesson/8-多端交付生成` 的经验层知识库，不是第二份交付合同。
- 调用 `.agents/skills/lesson/8-多端交付生成/SKILL.md` 时，必须同时加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / meta 规则 > lesson 根 `SKILL.md` > 本阶段 `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 24000
- hard_limit_chars: 48000
- status: ok
- recommended_action: keep-delivery-heuristics-focused

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 三端输出各自改写课程事实 | shared delivery map 缺失 | 回到父包 `N4-CONTENT-MODEL-FUSION`，先建立共享 delivery map | 所有叶子都从同一 manifest 和 leaf packet 消费 | manifest 中 doc/ppt/html 指向同一课程模块和目标 |
| 第 8 阶段补写上游缺失正文 | owning stage 边界漂移 | 回到 `N2-UPSTREAM-AUDIT`，把缺口路由到第 `3` 到 `7` 阶段 | delivery gate 阻断缺核心上游的成品生成 | 缺口清单可定位 owning stage |
| 未指定目标端时补出空叶子产物 | leaf selection 过度补全 | 父包只生成目标端 leaf packet；未选中端记录 not selected | Default leaf routing 只影响路由，不补空产物 | manifest targets 标记 selected/omitted |
| manifest 与 plan 不一致 | 写回同步缺口 | 回到 `N6-MANIFEST-WRITEBACK` 同步字段和路径 | plan 和 JSON manifest 必须同轮更新 | `DEL-01` 到 `DEL-07` 均可互相追踪 |
| 脚本生成讲义、幻灯片或网页正文 | LLM-first 违规 | 废弃机械产物，回到 LLM delivery map 或 leaf 适配节点 | 脚本只做格式转换、组装、校验、manifest 回写 | authorship note 明确 LLM-approved source |
| HTML artifact leaf packet 缺少 design executor | html leaf handoff 缺口 | 回到 `N5-LEAF-WORK-PACKETS`，给 HTML packet 写入 `.agents/skills/claude-design` | 父包不生成 HTML artifact，只声明 html leaf 和 executor | manifest leaf packet 含 `design_executor` |

## Repair Playbook

1. 先确认任务是父级多端计划、单端叶子执行还是 manifest repair。
2. 若上游不足，优先修第 `3` 到 `7` 阶段或 `content-model/`，不要在第 8 阶段编造正文。
3. 若只要求一个端，只生成对应 leaf packet；未选端写 omitted，不创建空成品。
4. 若跨端内容冲突，保留共享 delivery map 为真源，叶子产物回到对应叶子修复。
5. 若工具链输出看似可用正文，先判定为机械产物，不进入 canonical delivery truth。
6. 若 HTML 目标包含真实网页 artifact，父包只在 leaf packet 中声明 `8/html -> .agents/skills/claude-design`；不要由父包直接生成或美化 HTML。

## Reusable Heuristics

- 父包的价值是把三端交付从同一课程模型投影出来，而不是让每个端重新写一套课程。
- DOC 重视完整讲义和引用脉络，PPT 重视授课节奏和视觉密度，HTML 重视可浏览结构和交互状态；这些差异应在 leaf packet 中表达。
- HTML 的真实 artifact 设计执行交给 `.agents/skills/claude-design`，但课程事实、delivery map 和目标端选择仍由 lesson 父包与 HTML 叶子控制。
- `delivery-manifest.json` 是交付目录和叶子执行状态索引，不替代课程正文或三端成品。
- Consistency gate 内置在第 8 阶段即可；新增外部审查或封版阶段会制造第二治理真源。
- 如果用户只说“生成课件”，父包先裁决目标端，再调度叶子；不要直接跳到 PPT。

## Case Log

> 仅记录里程碑级经验，避免过程流水。

### Case-001

- milestone_type: runtime_spine_creation
- outcome: 建立 lesson 第 8 阶段父包的 Skill 2.0 runtime spine。
- design_decision: 父包拥有 delivery plan、manifest 和叶子路由；doc/ppt/html 拥有各自成品交付。
- replication_checklist: 先审上游，再建共享 delivery map，再生成 leaf packets，最后写 manifest 并跑 consistency gate。
- evidence_paths: `.agents/skills/lesson/8-多端交付生成/SKILL.md`
