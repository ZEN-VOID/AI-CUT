# Context: aigc 3-美学

本文件是 `3-美学` 整体主入口的经验层知识库，不是规范真源。调用同目录 `SKILL.md` 时必须同时加载本文件；它只沉淀整体路由、6 subagents 并发、父级汇流、依赖缺口和下游 handoff 的可复用经验，不改写 `SKILL.md` 的节点、输入、输出或门禁。

## Context Health

```yaml
monitor_version: 2
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-parent-routing-heuristics-only
last_checked_at: 2026-06-04
```

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 系统预防修复 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-AES-01` | 用户调用 `3-美学` 整体，但只执行了 `画面基调` | 父级入口缺路由属性 | 回到父级 `N1/N3`，按 6 subagents 并发 fan-out | `SKILL.md` 固定 `overall_parallel` 和 Subagent Routing Matrix | `subagent_dispatch_matrix` 有 6 行 |
| `TM-AES-02` | 整体调用被改成“画面基调先、其他后”的串行链 | 依赖继承误读 | 保持并发；缺上游协议的子技能标记 `candidate/dependency_gap` | 父级明确“展示顺序不是执行顺序” | 报告含 `parallel_semantics` 和 `dependency_gap_matrix` |
| `TM-AES-03` | 父级总览写成完整美学总稿，覆盖子技能协议 | 业务真源漂移 | 收缩父级总览为索引、摘要、状态和 handoff | Output Contract 禁止父级替代 6 个 canonical outputs | 每个子协议有独立路径和报告 |
| `TM-AES-04` | 子技能缺执行报告，父级仍判定 pass | 报告证据门缺失 | 将父级 verdict 改为 `candidate` 或 `blocked`，要求补对应子报告 | Convergence Contract 要求每个子技能报告路径 | `subagent_result_matrix.report_output` 无空项 |
| `TM-AES-05` | 角色/场景/道具风格与画面基调冲突，父级直接改局部文本 | 父级越权修复 | 父级只记录冲突并返工对应子技能 | Review Gate 绑定 `FAIL-AES-CROSS-CONFLICT` | `cross_style_consistency_report` 有冲突字段和返工目标 |
| `TM-AES-06` | 部分命中 2-5 个子技能时被自动补齐 6 个 | 整体/部分路由混淆 | 只有用户明确整体调用时才 6 路并发；部分命中只调度点名项 | Mode Selection 区分 `overall_parallel` 与 `partial_named_route` | `child_route_manifest` 与用户点名一致 |
| `TM-AES-07` | 总览中的 prompt 摘要被下游当作唯一风格真源 | handoff 边界不清 | 总览标注“索引，不替代局部协议”并链接 canonical output | Field Mapping 将 prompt index 限定为快速索引 | 下游 handoff 同时列出 canonical path |
| `TM-AES-08` | 6 个 subagents 使用不同项目资料，汇流不可比 | 输入包不统一 | 先构造共享 `Aesthetic Task Packet`，再 fan-out | N2 作为并发前置节点 | 6 个结果回指同一 `source_manifest` 或解释差异 |

## Repair Playbook

1. 先判断用户是否真的整体调用：出现 `3-美学`、`美学系列整体`、`全套美学`、`完整美学阶段` 等信号，默认 `overall_parallel`。
2. 整体调用时不要推理“画面基调应该先跑所以先跑一个”；用户已明确 6 个 subagents 并发，依赖问题写入 `dependency_gap_matrix`。
3. 若漏掉任一子技能，不在父级总览补空白字段；必须返工调度缺失 subagent。
4. 若某个子技能 blocked，父级 verdict 不能写 `pass`；应写 `blocked` 或 `partial/candidate` 并指向该子技能 fail code。
5. 父级只聚合 `路径、状态、摘要、prompt index、dependency gap、handoff`，不要改写子技能协议正文。
6. 当风格冲突跨子技能出现时，优先定位冲突字段和拥有真源的子技能；父级只提出返工目标，不直接合并文本。
7. 单子技能或部分子技能请求不自动补齐 6 个，除非用户明确说“整体”“全套”“完整阶段”。
8. 下游 handoff 必须同时给出“继承什么”和“不继承什么”，避免设计、图像或视频阶段拿父级摘要替代局部协议。

## Reusable Heuristics

- `3-美学` 父级的价值是协调 6 个美学面向，而不是成为第 7 个创作作者。
- 并发模式下，画面基调不再是实时前置产物；它是 6 路结果之一。其他子技能如果需要画面基调，只能消费已有协议或标记候选依赖。
- 父级总览适合给制片、导演和下游阶段快速扫描，但 canonical truth 仍在 6 个子技能目录。
- prompt index 是目录，不是 prompt 真源；下游需要完整边界时必须读对应子协议。
- 发现“父级总览比子协议更详细”通常就是越权信号。
- 整体阶段的 pass 不等于每个子技能完美一致；它要求冲突和缺口被明确记录，并有可执行返工入口。

## Parent-Child Boundary Notes

- `画面基调` 拥有全局视觉协议，不拥有角色/场景/道具/摄影/分镜的局部细则。
- `角色风格` 拥有角色层视觉风格，不拥有具体角色卡。
- `场景风格` 拥有空间风格协议，不拥有具体场景清单。
- `道具风格` 拥有道具层风格协议，不拥有具体道具清单或单件设计。
- `摄影风格` 拥有观看方式、构图秩序、景别、机位和运动纪律，不拥有分镜正文或视频生成参数。
- `分镜风格` 拥有节奏、镜头组合和连接语法，不拥有具体分镜镜头表。
- 父级 `3-美学` 拥有路由、汇流、冲突审查和 handoff，不拥有上述任何局部协议正文真源。
