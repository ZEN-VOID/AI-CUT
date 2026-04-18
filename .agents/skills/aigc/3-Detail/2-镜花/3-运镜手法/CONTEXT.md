# CONTEXT.md

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: ~1800
current_lines: ~50
current_cases: 0
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-17T18:30:00Z
```
<!-- CONTEXT_HEALTH_END -->

## Purpose & Loading Contract

- 本文件保存 `3-运镜手法` 的经验层。
- 命中本 skill 时必须和同目录 `SKILL.md` 一起加载。
- 经验层只沉淀可复用的失效模式、修复顺序与高价值 heuristic，不重写主合同。

## Type Map

| failure_or_outcome_type | immediate_fix | verification_point |
| --- | --- | --- |
| 镜头在动，但说不清“不动会损失什么” | 回到静镜基线，先重写 `运动动机` 与 `默认路线` | 运镜不再是空炫技 |
| `变化 / 组合 / 速度` 各自改目标 | 先锁单一主观看收益，再按 `变化 -> 组合 -> 速度` 串行重做 | 三个叶子围绕同一默认路线工作 |
| `academy_hit_note` 被当成第二次镜头设计 | 只吸收与当前默认路线兼容的运动提示，其余显式放弃 | 上游提示不再改写构图、空间或表演任务 |
| `速度` 开始反推运动路径 | 把“怎么动”退回 `变化`，`速度` 只保留快慢、停顿和变速 | `speed_profile` 不再越权 |
| `camera_patch` 直接外溢成最终真相 | 在写回时固定投影为 `运镜手法`，并检查 target path | 不再出现 branch 局部槽位与 root 双重真源 |
| 挑战变体更花哨但偷换了表现目标 | 取消挑战案，只保留默认路线 | 默认路线仍是唯一 canonical patch |

## Repair Playbook

1. 先锁前置：当前 root、`分镜构图`、可选 `摄影美学` 是否已就位。
2. 先做静镜基线，再决定镜头是否真的要动。
3. 默认路线锁定后，再串行细化 `变化 -> 组合 -> 速度`。
4. 所有 side input 先过兼容性过滤，不兼容就放弃。
5. 先写本地 `camera_patch`，再投影为 canonical `运镜手法`。
6. 若需要挑战变体，只保留比较结论，不得覆盖默认路线。

## Reusable Heuristics

- 运镜最稳的起点不是“这里能怎么动”，而是“这里其实能不能不动”。
- 一个镜头的默认路线最好只服务一个主观看收益；同时想服务三件事，通常已经过量。
- `变化` 决定运动路径，`组合` 决定观看流，`速度` 决定节奏呼吸；三者混写通常会失真。
- `academy_hit_note` 最好的用法是当过滤后的补强提示，而不是再次发明镜头。
- 本 branch 的本地装配槽位可以叫 `camera_patch`，但项目级业务真相只能叫 `运镜手法`。
