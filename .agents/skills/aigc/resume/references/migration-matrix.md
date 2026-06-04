# Legacy Resume Migration Matrix

本文件记录 `.agents/skills/aigc-old/resume` 到 `.agents/skills/aigc/resume` 的语义迁移，避免旧包升级时静默丢失配置意图。

| source_path | source_section | content_class | target_path | operation | semantic_risk | reference_updates | validation_gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `.agents/skills/aigc-old/resume/SKILL.md` | frontmatter | entry metadata | `SKILL.md` | rewrite | low | name 保持 `aigc-resume` | Skill 2.0 validator |
| `.agents/skills/aigc-old/resume/SKILL.md` | Context Loading Contract | loading contract | `SKILL.md` | keep + adapt | low | 加入项目 `MEMORY.md`、项目 `CONTEXT/` 与 `CONTEXT/` 新口径 | context audit |
| `.agents/skills/aigc-old/resume/SKILL.md` | Purpose / Stage Position | satellite boundary | `SKILL.md` | keep + adapt | low | 挂到新 `.agents/skills/aigc/resume` | manual semantic check |
| `.agents/skills/aigc-old/resume/SKILL.md` | Supported Scope / Workflow | process rules | `SKILL.md#Thinking-Action Node Map` | split | medium | 旧 `0-Init` 改为 `0-初始化` | node review gate |
| `.agents/skills/aigc-old/resume/SKILL.md` | Project Root Guard | runtime guard | `references/project-runtime-layout.md` | rewrite | medium | 新 runtime 使用中文目录 | runtime evidence check |
| `.agents/skills/aigc-old/resume/SKILL.md` | Step 1 / Step 3 commands | read-only evidence commands | `references/workflow-resume.md` | rewrite | medium | 阶段目录改为 `1-分集` 等 | hard guard review |
| `.agents/skills/aigc-old/resume/SKILL.md` | Recovery mode table | type strategy | `types/resume-type-map.md` | split | low | 新增 `review_repair_reentry` | type review |
| `.agents/skills/aigc-old/resume/SKILL.md` | Root-Cause Execution Contract | root cause | `SKILL.md` | keep + shrink | low | field owner 指向新版分区 | validator marker |
| `.agents/skills/aigc-old/resume/CONTEXT.md` | Type Map | experience | `CONTEXT.md` | keep + adapt | low | 新增中文 runtime 漂移案例 | context baseline |
| `.agents/skills/aigc-old/resume/CONTEXT.md` | Repair Playbook / Heuristics | experience | `CONTEXT.md` and `knowledge-base/resume-heuristics.md` | split | low | 保留非流水知识 | context review |
| `.agents/skills/aigc-old/resume/references/workflow-resume.md` | Recovery Evidence Chain | detailed reference | `references/workflow-resume.md` | keep + adapt | medium | `0-Init` 改 `0-初始化`，阶段路径改中文 | reference review |
| `.agents/skills/aigc-old/resume/agents/openai.yaml` | product metadata | metadata | `agents/openai.yaml` | keep + adapt | low | 默认提示显式 `$aigc-resume` | validator |
| `.agents/skills/aigc-old/resume/SKILL.md` | `7-Cut` blocked scope | shelved-stage rule | `references/project-runtime-layout.md`, `types/resume-type-map.md` | keep + adapt | medium | legacy `7-Cut` 映射为 `root_reroute` 或 `blocked_safety_stop` | shelved-stage review |

## Non-Loss Notes

- 旧包“恢复不伪造 workflow state”的意图保留在 `references/workflow-resume.md` 与 `review/resume-review-gate.md`。
- 旧包“主动回到初始化态重来不属于 resume”的边界保留在 `SKILL.md`、`types/resume-type-map.md` 与 `CONTEXT.md`。
- 旧包引用的 `.agents/skills/aigc/_shared/project-runtime-layout.md` 在当前新树中不存在，因此新版将恢复所需 runtime 口径内收为 `references/project-runtime-layout.md`，避免悬空引用。
- `aigc-old` 的英文阶段名不作为新版输出真源，只作为 legacy 兼容输入。
- 旧包 `7-Cut` blocked / 搁浅语义已保留为新版 `root_reroute` 或 `blocked_safety_stop`，不得直接续跑。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 旧 `aigc-old/resume` 的入口元数据、加载合同、阶段定位、流程规则、类型策略、经验层、reference、metadata 和搁浅阶段语义是否都有新版 owner、迁移动作、风险和验证项？ | `GATE-RESUME-MIGRATION-COVERAGE` | `FAIL-RESUME-MIGRATION-COVERAGE` | `N2-TRUTH-LOCK` | 报告列出 migration matrix 覆盖行、缺失 source section、对应 target owner 与 validation gate。 |
| `Context Loading Contract` 迁移后是否保留同目录 `CONTEXT.md`、项目 `MEMORY.md` 与项目 `CONTEXT/` 的加载口径，且未把旧经验层升格为新版规范真源？ | `GATE-RESUME-MIGRATION-NONLOSS` | `FAIL-RESUME-MIGRATION-LOSS` | `N1-INTAKE` | 报告记录加载合同检查结果、旧 CONTEXT 迁移落点和未晋升为规范真源的说明。 |
| 旧包的卫星技能边界是否保留为“恢复裁决与回接”，没有迁移成阶段业务真稿生成入口或新的主阶段？ | `GATE-RESUME-TRUTH-BOUNDARY` | `FAIL-RESUME-TRUTH-BOUNDARY` | `N4-PLAN` | 报告说明 resume 输出是否只给恢复裁决、唯一入口和 repair list，未生成阶段业务正文。 |
| 旧 `0-Init / 1-Planning / 3-Detail / 5-Image / 6-Video` 等英文 runtime 是否只作为 legacy 输入兼容，并映射到当前中文 runtime 判定？ | `GATE-RESUME-RUNTIME-PROFILE` | `FAIL-RESUME-RUNTIME` | `N2-TRUTH-LOCK` | 报告列出检测到的 legacy 路径、对应中文 runtime、是否需要 root reroute。 |
| 旧 workflow 中只读命令和证据检查是否迁移为新版 evidence chain，而不是伪造或补写不存在的 workflow state？ | `GATE-RESUME-EVIDENCE-CHAIN` | `FAIL-RESUME-EVIDENCE` | `N2-TRUTH-LOCK` | 报告记录实际读取的状态文件、初始化工件、阶段产物与只读命令边界。 |
| 旧 recovery mode table 是否迁移到类型矩阵，并保留 `review_repair_reentry`、`init_rebootstrap_reroute` 等新版分流，不把用户重起盘误判为续跑？ | `GATE-RESUME-MODE-INTENT` | `FAIL-RESUME-MODE` | `N3-TYPE` | 报告写明命中的 mode、用户意图证据、被排除的 query/review/rebootstrap 分支。 |
| 旧 `7-Cut` blocked / 搁浅语义是否只允许 `root_reroute` 或 `blocked_safety_stop`，未被输出为可直接续跑阶段？ | `GATE-RESUME-LEGACY-SHELVED` | `FAIL-RESUME-LEGACY-STAGE` | `N4-PLAN` | 报告记录 `7-Cut` 证据、阻断原因、返回根路由或 blocker 的唯一入口。 |
| `Non-Loss Notes` 中“不伪造 workflow state”“rebootstrap 不属于 resume”“legacy 只作兼容输入”等旧包意图是否都能在新版 review gate 或 `SKILL.md` 节点中被复核？ | `GATE-RESUME-MIGRATION-NONLOSS` | `FAIL-RESUME-MIGRATION-LOSS` | `N5-GATE` | 报告引用对应 review gate、SKILL 节点和未通过时的返工入口。 |
| 迁移矩阵本身是否只作为升级追踪与验证合同，不越权决定当前项目的实际下一入口？ | `GATE-RESUME-TRUTH-BOUNDARY` | `FAIL-RESUME-TRUTH-BOUNDARY` | `N4-PLAN` | 报告说明 migration matrix 是否仅用于 source non-loss 复核，当前项目入口仍由 runtime evidence 和 type profile 决定。 |
