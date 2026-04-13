# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-Design/角色` 的经验层知识库，不是过程日志。
- 调用本类目父级合同时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 角色类目没有先做清单就进入设计 | 类目路由层 | 回退到 `1-清单` 先产出角色对象池 | 固化 `清单 -> 设计 -> 面板` 的默认顺序 | 下游能复用同一份角色清单 |
| 角色清单脚本与 shared schema 不对齐 | 输入契约层 | 改按 `final_output.main_content.分镜组列表[].分镜明细[]` 取数 | 在叶子技能合同中回指 shared schema | `角色及站位和穿搭` 可被稳定读取 |
| `2-设计` 目录存在但没有父 skill 与 team contract | 子技能治理层 | 补齐 `2-设计/SKILL.md + CONTEXT.md + _shared/IO_CONTRACT.md`，并落盘角色设计组 team | 将“active 入口”定义为必须同时具备父 skill 与真实 agent docs | `2-设计` 不再是空目录入口 |
| 角色面板 leaf 已落地，父级合同仍写 pending | 路由状态层 | 同步更新 `2-角色/SKILL.md` 与 `4-Design/SKILL.md` 的 active 列表 | 每新增 active leaf 同步回写父级合同与经验层 | 父级状态与真实入口一致 |
| 子技能主 `SKILL.md` 已改成知行合一，但目录里仍保留并列 steps/reference 真源 | 真源治理层 | 把复杂步骤、字段表与汇流门收回主 `SKILL.md`，旧 `references/` 只保留迁移 stub | 在父级合同中固定 `复杂链路的骨架 / 细则分层=false` 的约束 | 当前类目不再出现主合同外的平行执行真源 |

## Repair Playbook

1. 先查输入是否为 shared director schema。
2. 再查当前任务是否需要角色对象池，而不是角色图。
3. 若只是建立对象清单，固定进入 `1-清单`。
4. 若对象池和设计稿都已存在，继续判断当前是进入 `2-设计` 还是 `3-面板`，不要停在父级口头描述。

## Reusable Heuristics

- 角色链最重要的第一步不是“做得华丽”，而是先把同一角色对象的 canonical identity 锁住。
- 只要上游已经统一成导演 episode JSON，角色链就不该再保留第二套平行输入格式作为第一真源。
- 当 `2-设计` 或 `3-面板` 已落地，父级合同若仍写成 pending，本身就会变成第二真源，必须同步纠正。
- 当用户明确要求 `复杂链路的骨架 / 细则分层=false` 时，角色链子技能的字段主表、思行节点、类型策略与输出合同都应内收到主 `SKILL.md`，旧 `references/` 最多保留迁移 stub。
