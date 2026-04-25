# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc-design` 父级阶段路由经验层，不是执行日志。
- 调用 `.agents/skills/aigc/4-Design/SKILL.md` 时，必须同时加载本文件。
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
| `DESIGN-TM-03` | 域级输出落到旧嵌套目录 | 回到域级 Output Contract | 最终文件在 `4-Design/` 根 |
| `DESIGN-TM-04` | 多域任务误补未命中域 | 只调度用户命中域或显式推断域 | 未命中域无占位输出 |

## Repair Playbook

1. 先判断当前问题属于父级路由、域级业务执行、输出路径漂移还是引用同步。
2. 父级只修 `SKILL.md`、`references/阶段路由矩阵.md`、`references/思行网络.md` 和 registry/routes。
3. 域级清单、设计、面板问题下钻到对应域级包。
4. 旧路径引用修复后必须重新搜索 `4-Design/1-清单`、`4-Design/2-设计`、`4-Design/3-面板`。
5. 若仍需兼容旧 JSON，必须明确标成 sidecar 或 legacy，不得恢复为 active skill 入口。

## Reusable Heuristics

- 这次结构升级的稳定锚点是“域优先”，不是“阶段 tranche 优先”。
- 父级越薄越稳：它只回答“进哪个域、输出根在哪里、是否验收”。
- 旧脚本可以继续提供机械投影，但新的 creative truth 必须由域级 LLM 流程主创。
