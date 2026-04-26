# Legacy Resume Migration Matrix

本文件记录 `.agents/skills/aigc-old/resume` 到 `.agents/skills/aigc/resume` 的语义迁移，避免旧包升级时静默丢失配置意图。

| source_path | source_section | content_class | target_path | operation | semantic_risk | reference_updates | validation_gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `.agents/skills/aigc-old/resume/SKILL.md` | frontmatter | entry metadata | `SKILL.md` | rewrite | low | name 保持 `aigc-resume` | Skill 2.0 validator |
| `.agents/skills/aigc-old/resume/SKILL.md` | Context Loading Contract | loading contract | `SKILL.md` | keep + adapt | low | 加入项目 `MEMORY.md`、项目 `CONTEXT/` 与 `附加预设/` 新口径 | context audit |
| `.agents/skills/aigc-old/resume/SKILL.md` | Purpose / Stage Position | satellite boundary | `SKILL.md` | keep + adapt | low | 挂到新 `.agents/skills/aigc/resume` | manual semantic check |
| `.agents/skills/aigc-old/resume/SKILL.md` | Supported Scope / Workflow | process rules | `steps/resume-workflow.md` | split | medium | 旧 `0-Init` 改为 `0-初始化` | steps review gate |
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
