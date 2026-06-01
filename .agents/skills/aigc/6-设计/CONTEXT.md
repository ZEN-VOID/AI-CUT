# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc-design` 父级阶段路由经验层，不是执行日志。
- 调用 `.agents/skills/aigc/6-设计/SKILL.md` 时，必须同时加载本文件。
- 域级经验分别沉淀在 `场景/CONTEXT.md`、`角色/CONTEXT.md`、`道具/CONTEXT.md`。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 20000
hard_limit_chars: 40000
status: ok
recommended_action: keep-router-scoped
last_checked_at: 2026-04-24
```

## Type Map

| type_id | 触发症状 | 立即修复 | 验证点 |
| --- | --- | --- | --- |
| `DESIGN-TM-01` | 用户仍按 `1-清单/2-设计/3-面板` 命中旧入口 | 路由到 `场景/角色/道具` 域级包，再在域内执行顺序门 | registry 和 routes 不再指向旧目录 |
| `DESIGN-TM-02` | 父级试图直接写业务主体正文 | 退回域级子技能包 | 父级只写路由和 validation report |
| `DESIGN-TM-03` | 父级、registry 或 closeout 仍要求根目录平铺业务真源 | 回到域级 Output Contract | 最终文件在对应域内 `1-清单/2-设计/3-生成/` |
| `DESIGN-TM-04` | 多域任务误补未命中域 | 只调度用户命中域或显式推断域 | 未命中域无占位输出 |
| `DESIGN-TM-05` | 上游 `5-分组` 分批追加后，6-设计试图重新全量覆盖清单/设计/生成 | 先走 `references/incremental-reconciliation-contract.md`，再由域内清单 merge、设计补缺、生成补缺 | 既有主体、设计稿、生成资产被跳过或版本化，不静默覆盖 |
| `DESIGN-TM-06` | closeout 发现域级失败后，父级直接补清单/设计/生成正文 | 回到 `Stage-Closeout Review-Repair Contract`，把 finding 路由回对应域级 leaf 修复并复审 | `validation-report.md` 只记录 route、repair_actions、re_review_verdict，不出现父级伪造业务真源 |
| `DESIGN-TM-07` | 设计叶子仍调用 team 身份、解析旧 stage profile、补造顾问问答，或没有优先消费 `init_synthesis.stage_seed_summary."6-设计"` | 父级不本地模拟，回到命中叶子与共享初始化综合消费合同；只允许生成 `init_team_synthesis_context` | `validation-report.md` 或域级报告能看到 init synthesis 状态，且没有 creative-stage team persona dispatch |

## Repair Playbook

1. 先判断当前问题属于父级路由、域级业务执行、输出路径漂移还是引用同步。
2. 父级只修 `SKILL.md`、`references/阶段路由矩阵.md`、`references/思行网络.md` 和 registry/routes。
3. 域级清单、设计、生成问题下钻到对应域级包。
4. 旧路径引用修复后必须重新搜索 `6-设计/1-清单`、`6-设计/2-设计`、`6-设计/3-面板`。
5. 若仍需兼容旧 JSON，必须明确标成 sidecar 或 legacy，不得恢复为 active skill 入口。
6. 分批上游场景中先问“本轮新增了哪些 `第N集.md`，已有清单/设计/生成覆盖到哪里”，再决定是否进入叶子。
7. 阶段 closeout 中发现域级 `needs_rework` 时，父级只做路由和汇总：把 finding 交回具体域级 leaf，等待 direct repair 和 re-review 后再写最终 validation report。
8. 如果命中 `角色/2-设计`、`道具/2-设计` 或 `场景/2-设计` 且项目存在初始化综合，父级只检查 `init_team_synthesis_context` 状态；不得要求叶子执行 roster 解析、顾问提问或 team 身份代入。

## Reusable Heuristics

- 这次结构升级的稳定锚点是“域优先”，不是“阶段 tranche 优先”。
- 父级越薄越稳：它只回答“进哪个域、输出根在哪里、是否验收”。
- 旧脚本可以继续提供机械投影，但新的 creative truth 必须由域级 LLM 流程主创。
- 6-设计的批量执行不等于覆盖执行；默认是对账、merge、补缺和跳过既有资产。
- `6-设计` 的终稿感来自域级 leaf 闭环，不来自父级补写：父级 closeout 只能聚合 verdict，不能替场景/角色/道具直接主创。
- 设计父级的 team 责任是传递和验收初始化综合消费机制，不是替叶子阶段请教、代入 team 身份或改写业务正文。
