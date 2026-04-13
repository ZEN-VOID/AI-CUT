# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/道具` 的经验层知识库，不是过程日志。
- 调用本类目父级合同时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 道具链只有 `1-清单`，没有设计 synthesis | 类目路由层 | 建立 `4-道具/SKILL.md` 与 `2-设计` 父 skill | 把 `清单 -> 设计 -> 面板` 固定为父级顺序 | 用户可从 bridge 稳定进入设计 |
| 道具设计把 prompt 当成唯一真源 | 输出治理层 | 区分 `道具设计.json` 与 `prop_design_prompt.json` | 将 canonical facts 与执行话术分层 | 下游能复用设计真值，不依赖单次 prompt |
| subagents 角色存在但 team 层为空 | agent team 层 | 补齐 `.codex/agents/aigc/设计组/道具设计/team.md` 与角色合同 | 让父 skill 永远回指真实 team，而不是口头想象 | team 路径存在且可被 audit 检出 |
| 道具链停在 `2-设计`，没有 panel handoff | 类目路由层 | 建立 `3-面板` 叶子技能，消费 design master 输出逐道具 layout | 把 `清单 -> 设计 -> 面板` 真正闭环，而不是只在父级写顺序 | 用户可从 `道具设计.json` 稳定进入 panel layout |
| 父级合同只能读摘要，必须翻 references 才能看懂执行链 | 合同真源层 | 把类目路由、门禁、节点与汇流收回父级 `SKILL.md` | 固化“父级单文档真源 + 叶子细化节点”的知行合一写法 | 只读父级 `SKILL.md` 也能完成阶段判断 |

## Repair Playbook

1. 先看当前任务是对象池、设计 synthesis 还是展示面板。
2. 若还没有 `prop_design_bridge.json`，先回到 `1-清单`。
3. 若 bridge 已有、目标是设计稿或 prompt sidecar，进入 `2-设计`。
4. 若已经有 design master，再考虑后续面板或画面阶段。

## Reusable Heuristics

- 对道具链来说，`bridge` 不是终点；它只是进入设计 synthesis 的最低门槛。
- 设计阶段最稳的真源不是“长篇 prompt”，而是“可重复消费的设计事实 + 可漂移的 prompt sidecar”。
- 道具设计的多 subagent 协同最适合按结构、材质、痕迹、prompt、审计分层，而不是让一个角色重写所有字段。
- 面板阶段最稳的输入不是重新回读导演 JSON，而是已经固化好的 `道具设计.json + prop_design_prompt.json`。
- 对父级类目技能来说，最稳的重构不是再加一层 references 导航，而是把阶段归类、门禁、回退与汇流直接写进一个可单读的 `SKILL.md`。
