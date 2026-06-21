# next CONTEXT

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 1523
current_lines: 32
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

- 编号邻接误判：看到 `1-`、`2-` 就直接写成线性下一步，通常是跳过组级 `SKILL.md` 的显式路由导致。修复时先回读组级或共享合同，再把每个叶子落到 `sequential`、`parallel_fork`、`router_return`、`bundle_gate` 或 `endpoint`。
- 组级/叶子颗粒度混淆：目标是大目录却只更新组级说明，或目标是叶子却继续扫描全树。修复点是先判断目标路径颗粒度；大目录默认刷新每个直接子技能，叶子目录只刷新自身 `Interaction`。
- 外部工程残留：`Interaction` 里混入 `AskUserQuestion`、`/aigc-*`、旧项目命令或失效路径。修复时替换为仓库中性 `interaction_contract`，并用真实目录或真实技能名填 `target_hint`。
- 上游合同空缺被补写：组级合同没有定义路由时，强行发明推荐目标会制造第二真相。修复动作是报告空缺，把修复落点指回上游合同，而不是在叶子里隐式覆盖。

## Repair Playbook

1. 先回读同目录 `SKILL.md`，再读取目标根目录的组级 `SKILL.md` 或上游合同，锁定显式耦合、禁止跳转和终点条件。
2. 判断目标是叶子还是组级目录；组级目录只扫描直接子技能，并过滤 `_shared`、`templates`、`references`、`assets` 等支撑目录。
3. 为每个目标建立 `next_route_table`：`source_path`、`trigger_type`、`recommended_target`、`secondary_targets`、`evidence`，先证据后写入。
4. 写回时只替换或追加 `## Interaction`，统一使用 `interaction_contract` 与 runtime fallback；不写具体外部提问工具依赖。
5. 验证所有 `target_hint` 真实存在，且新内容不含 `AskUserQuestion`、`/aigc-`、影视专属旧命令或过期 stage。
6. 若显式合同与编号顺序冲突，保留显式合同并报告冲突；不要静默按编号覆盖。

## Reusable Heuristics

- `/next` 的稳定性来自“显式组级路由 > 编号顺序 > 名称语义”。
- 如果上游合同缺位，正确动作是回指源层空缺，而不是编一个看起来顺的下一步。
- 编号目录只是默认语义，不是完成门禁；`5-Validation` 这类专项并行目录不能按相邻编号串成流水线。
- `Interaction` 的稳态目标是让下游选择可迁移：同一份 `header/question/options` 应能同时支持结构化提问和普通中文单题消息。
- 大目录的完成标准通常是“每个直接子技能都有可验证的下游合同”，而不是根目录里有一段总说明。

## Promotion Backlog

- 为 `Interaction` 增加轻量 validator：检查 `trigger_type` 枚举、`target_hint` 存在性和禁用词残留。
- 固化 `next_route_table` 模板，降低手写路由证据时漏掉 `evidence` 或 `secondary_targets` 的概率。
- 若 `story2026` 特例继续扩展，把阶段链特殊规则拆成可维护的参考表，但仍由主 `SKILL.md` 授权加载。
