# Context: aigc 2-美学

本文件是 `2-美学` 整体主入口的经验层知识库，不是规范真源。调用同目录 `SKILL.md` 时必须同时加载本文件；它只沉淀整体路由、6 subagents 并发、父级汇流、依赖缺口和下游 handoff 的可复用经验，不改写 `SKILL.md` 的节点、输入、输出或门禁。

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
| `TM-AES-01` | 用户调用 `2-美学` 整体，但只执行了 `画面基调` | 父级入口缺路由属性 | 回到父级 `N1/N3`，按 6 subagents 并发 fan-out | `SKILL.md` 固定 `overall_parallel` 和 Subagent Routing Matrix | `subagent_dispatch_matrix` 有 6 行 |
| `TM-AES-02` | 整体调用被改成“画面基调先、其他后”的串行链 | 依赖继承误读 | 保持并发；缺上游协议的子技能标记 `candidate/dependency_gap` | 父级明确“展示顺序不是执行顺序” | 报告含 `parallel_semantics` 和 `dependency_gap_matrix` |
| `TM-AES-03` | 父级总览写成完整美学总稿，覆盖子技能协议 | 业务真源漂移 | 收缩父级总览为索引、摘要、状态和 handoff | Output Contract 禁止父级替代 6 个 canonical outputs | 每个子协议有独立路径和报告 |
| `TM-AES-04` | 子技能缺执行报告，父级仍判定 pass | 报告证据门缺失 | 将父级 verdict 改为 `candidate` 或 `blocked`，要求补对应子报告 | Convergence Contract 要求每个子技能报告路径 | `subagent_result_matrix.report_output` 无空项 |
| `TM-AES-05` | 角色/场景/道具风格与画面基调冲突，父级直接改局部文本 | 父级越权修复 | 父级只记录冲突并返工对应子技能 | Review Gate 绑定 `FAIL-AES-CROSS-CONFLICT` | `cross_style_consistency_report` 有冲突字段和返工目标 |
| `TM-AES-06` | 部分命中 2-5 个子技能时被自动补齐 6 个 | 整体/部分路由混淆 | 只有用户明确整体调用时才 6 路并发；部分命中只调度点名项 | Mode Selection 区分 `overall_parallel` 与 `partial_named_route` | `child_route_manifest` 与用户点名一致 |
| `TM-AES-07` | 总览中的 prompt 摘要被下游当作唯一风格真源 | handoff 边界不清 | 总览标注“索引，不替代局部协议”并链接 canonical output | Field Mapping 将 prompt index 限定为快速索引 | 下游 handoff 同时列出 canonical path |
| `TM-AES-08` | 6 个 subagents 使用不同项目资料，汇流不可比 | 输入包不统一 | 先构造共享 `Aesthetic Task Packet`，再 fan-out | N2 作为并发前置节点 | 6 个结果回指同一 `source_manifest` 或解释差异 |
| `TM-AES-09` | 6 路协议像同一模板换对象名、换参考锚点或同义改写 | 源层主创缺失 | 不在父级总览润色补救；定位对应 subagent，废弃候选协议并回子技能主创节点重做 | 父级 `GATE-AES-09` 和各子技能 anti-scripted gate 独立阻断 | `anti_scripted_suite_audit` 标记无模板句架复用和锚点替换 |
| `TM-AES-10` | 单集 2-美学执行把场景/角色/道具/分镜/摄影风格全部写到项目级路径，导致不同集互相覆盖 | output scope 漂移 | 若来源或目标是 `第N集`，5 个非画面基调子技能写入 `2-美学/第N集/<子技能>/`，父级总览写入 `2-美学/第N集/` | `SKILL.md` 固定 Output Object Scope Contract | `subagent_result_matrix.canonical_output` 对应当前 `episode_scope`，且 `画面基调` 仍在全局路径 |
| `TM-AES-11` | 为每集复制一份 `画面基调/全局风格协议.md` | global singleton 误读 | 删除逐集画面基调写回要求；报告只记录单集样本范围或候选状态 | `画面基调` 子技能声明 global singleton，不支持 `2-美学/第N集/画面基调/` | 路径扫描无逐集 `画面基调` canonical 要求 |
| `TM-AES-12` | 子技能把艺术家锚点、负面禁区、prompt 摘要或下游执行项混入核心风格维度，导致维度专业性不稳 | dimension taxonomy drift | 回到父级 `Style Dimension Taxonomy Contract`，把核心维度、校准锚点、边界负面和 handoff 分层；各子技能只在 `N4` 写自身拥有的风格属性 | 父级 `SKILL.md` 固定分层合同；子技能 `N4` 维度表只含 owning layer 属性 | `rg` 检查核心维度不再把锚点/负面/执行项混作同层真源 |

## Repair Playbook

1. 先判断用户是否真的整体调用：出现 `2-美学`、`美学系列整体`、`全套美学`、`完整美学阶段` 等信号，默认 `overall_parallel`。
2. 整体调用时不要推理“画面基调应该先跑所以先跑一个”；用户已明确 6 个 subagents 并发，依赖问题写入 `dependency_gap_matrix`。
3. 若漏掉任一子技能，不在父级总览补空白字段；必须返工调度缺失 subagent。
4. 若某个子技能 blocked，父级 verdict 不能写 `pass`；应写 `blocked` 或 `partial/candidate` 并指向该子技能 fail code。
5. 父级只聚合 `路径、状态、摘要、prompt index、dependency gap、handoff`，不要改写子技能协议正文。
6. 当风格冲突跨子技能出现时，优先定位冲突字段和拥有真源的子技能；父级只提出返工目标，不直接合并文本。
7. 用户指出“脚本化/偷懒/未思考/未差异化”时，父级不要做表层整合润色；先跑 `anti_scripted_suite_audit`，再把失败项返给对应 subagent 源层重做。
8. 单子技能或部分子技能请求不自动补齐 6 个，除非用户明确说“整体”“全套”“完整阶段”。
9. 下游 handoff 必须同时给出“继承什么”和“不继承什么”，避免设计、图像或视频阶段拿父级摘要替代局部协议。
10. 单集执行时先锁 `episode_scope`：`画面基调` 不分集，其他 5 个子技能优先写 `2-美学/第N集/<子技能>/`；整季或项目级基线才写回非逐集目录。

## Reusable Heuristics

- `2-美学` 父级的价值是协调 6 个美学面向，而不是成为第 7 个创作作者。
- 并发模式下，画面基调不再是实时前置产物；它是 6 路结果之一。其他子技能如果需要画面基调，只能消费已有协议或标记候选依赖。
- 父级总览适合给制片、导演和下游阶段快速扫描，但 canonical truth 仍在 6 个子技能目录。
- prompt index 是目录，不是 prompt 真源；下游需要完整边界时必须读对应子协议。
- 发现“父级总览比子协议更详细”通常就是越权信号。
- 整体阶段的 pass 不等于每个子技能完美一致；它要求冲突和缺口被明确记录，并有可执行返工入口。
- 父级最容易误把“六路格式统一”看成治理一致；格式可以统一，句式、锚点和审美判断不能由同一模板替换生成。
- `画面基调` 是全片底层渲染协议，保持项目级 singleton；单集差异由场景、角色、道具、分镜和摄影 5 类风格覆盖承接。
- 核心风格维度只放 owning layer 的专业属性；艺术家/作品/工作室锚点进入 calibration matrix，负面项进入 `Negative Traits` 或扫描报告，下游继承进入 handoff，不要混成同一组维度。

## Parent-Child Boundary Notes

- `画面基调` 拥有全局视觉协议，不拥有角色/场景/道具/摄影/分镜的局部细则。
- `角色风格` 拥有角色层视觉风格，不拥有具体角色卡。
- `场景风格` 拥有空间风格协议，不拥有具体场景清单。
- `道具风格` 拥有道具层风格协议，不拥有具体道具清单或单件设计。
- `摄影风格` 拥有观看方式、构图秩序、景别、机位和运动纪律，不拥有分镜正文或视频生成参数。
- `分镜风格` 拥有节奏、镜头组合和连接语法，不拥有具体分镜镜头表。
- 父级 `2-美学` 拥有路由、汇流、冲突审查和 handoff，不拥有上述任何局部协议正文真源。
