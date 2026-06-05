# CONTEXT.md

本文件是 `lesson-resume` 的经验层知识库，不是执行流水账，也不是第二份恢复合同。它用于沉淀课程项目恢复中的证据识别、断点判断、卫星边界和唯一回接 heuristics。

## Purpose & Loading Contract

- 每次调用 `$lesson-resume` 时，必须同时加载同目录 `SKILL.md + CONTEXT.md`。
- 本文件只保存经验性 Type Map、Repair Playbook 与 Reusable Heuristics，不改写 `SKILL.md` 的入口、节点、gate、输出合同或权限边界。
- 优先级遵循：用户显式请求 > `AGENTS.md` / meta 规则 > lesson 根 `SKILL.md` > `lesson-resume/SKILL.md` > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md`。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 20000
hard_limit_chars: 40000
status: ok
last_checked_at: 2026-06-05
recommended_action: keep-resume-heuristics-only
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 把仓库根或 `.agents/skills/lesson` 误判为课程项目根 | project-root guard | 先锁定 `projects/lesson/<项目名>/` | 在 `N1-INTAKE` 固定项目根判定顺序 | 输出中只有一个 `PROJECT_ROOT` |
| 只凭最近修改时间判断进度 | evidence chain | 同时检查 `MEMORY.md`、`CONTEXT/`、阶段目录、canonical files 和交付叶子 | `N2-EVIDENCE` 必须形成 evidence packet | 恢复结论列出已查证据和缺口 |
| 空阶段目录被当成阶段完成 | scaffold vs artifact boundary | 空目录标为 skeleton，回 owning stage | Stage Evidence Matrix 固定 canonical file 清单 | 下一入口指向最早缺文件阶段 |
| 缺 `MEMORY.md` 或 `CONTEXT/` 仍继续阶段创作 | project context baseline | 回 `0-初始化` 或 blocker | Review gate 绑定 memory/context 检查 | 恢复报告有 memory_context_status |
| `content-model/` 被当成第二套课程主稿 | content-model drift | 回 owning stage 或第 8 父包修 handoff/manifest | lesson 根保持 `content-model/` 为共享模型和投影边界 | 三端状态可追溯到阶段 canonical |
| DOC/PPT/HTML 各自形成不同课程真源 | delivery leaf drift | 回 `8-多端交付生成` 父包或唯一叶子 | 第 8 父包先统一 delivery plan 和 manifest | 下一入口不同时指向多个叶子 |
| 查询状态被误当成恢复续跑 | satellite route drift | 只给只读证据摘要或建议 `query` | `query_reroute` 单列模式 | 输出不建议阶段执行 |
| repair 需求被 resume 直接修正文 | satellite overreach | 建议 `repair` 或 owning stage；resume 不写内容 | `N5-GATE` 阻断主创和阶段直接续写 | authorship note 明确不主创 |
| 建议未实现的 `query/repair` 卫星直接执行 | implementation status gap | 检查目标卫星 `SKILL.md`；缺失时 blocker 或回 owning stage | `N4-ROUTE` 固定 satellite implementation check | 输出说明卫星是否可执行 |
| 输出多个下一入口 | convergence failure | 回 `N4-ROUTE` 选 1 个，或 blocker | Output Contract 要求 one_next_entry | 最终答复没有无序候选列表 |
| 默认建议删除、覆盖或重置项目文件 | safety contract | 改成只读检查、diff 或人工确认 | Runtime Guardrails 禁止 destructive 默认动作 | 答复不含默认 destructive 操作 |
| 恢复裁决像路径扫描模板 | scripted conclusion layer | 回 `N4/N5`，由 LLM 解释证据如何收束 | 脚本只做证据扫描，不生成唯一入口 | final packet 有 rationale 和 gate evidence |

## Repair Playbook

1. 先锁定 `projects/lesson/<项目名>/`；无法唯一定位时停止猜测。
2. 先检查 `MEMORY.md` 和 `CONTEXT/`，再检查 0-8 阶段目录与 canonical files。
3. 将证据分为 project baseline、stage artifacts、content model、delivery leaves、satellite implementation 五类。
4. 找最早阻断点：上游阶段缺口优先于下游交付缺口；空目录不算完成。
5. 交付恢复先看第 8 父包 `delivery-plan.md` 与 `delivery-manifest.json`，再看 doc/ppt/html 叶子。
6. 内容质量或真源漂移问题不要用 resume 补正文，回 `repair` 或 owning stage。
7. 纯查询不要进入续跑；只输出事实证据和建议的查询入口。
8. 任何时候都只给一个下一入口；无法裁决时给 blocker 和最小补充信息。

## Reusable Heuristics

- `resume/` 恢复的不是聊天记忆里的上一步，而是磁盘、项目记忆、项目上下文和阶段工件能够证明的最后稳定入口。
- 课程项目的恢复优先级是项目基线、上游阶段、共享内容模型、第 8 父包、doc/ppt/html 叶子。
- `MEMORY.md` 缺失是项目基线缺口；项目长期偏好不应散落在阶段输出里。
- 项目 `CONTEXT/` 是共享运行期上下文；它缺失时，后续阶段容易重新发明项目事实。
- 第 8 阶段不是课程质量补写阶段；缺课程结构、课时正文、题库或视觉约束时应回 owning stage。
- `content-model/` 可以帮助三端一致，但不能替代阶段 canonical files。
- 最稳的恢复输出是“证据 -> 缺口 -> 风险 -> 唯一入口”，不是阶段清单越长越好。
- 当 `query/repair` 目录只有空壳时，恢复结论要显式说明不能直接调度该卫星。
- 用户说“继续做 PPT”时，先确认第 8 父包和 PPT 叶子 manifest；不要直接组装幻灯片。
- 用户说“上次做到哪了”时，优先给证据摘要和 blocker，而不是启动下一阶段。

## Case Log

> 仅记录可复用里程碑案例，避免过程流水账。

### Case-001

- milestone_type: satellite_runtime_spine_initialization
- outcome: 建立 `lesson-resume` core layout，固定只读恢复、证据重建、缺口定位、唯一下一入口和 no content authoring 边界。
- design_decision: 本技能不创建 optional modules；所有恢复节点、gate、量化口径和输出合同收束在 `SKILL.md`。
- evidence_paths: `.agents/skills/lesson/resume/SKILL.md`, `.agents/skills/lesson/resume/CONTEXT.md`
