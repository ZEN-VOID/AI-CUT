# Context: aigc 11-主体

本文件是 `11-主体` 整体主入口的经验层知识库，不是规范真源。调用同目录 `SKILL.md` 时必须同时加载本文件；它只沉淀整体路由、3 subagents 并发、父级汇流、上游 `10-分组` 分组稿消费、旧编号路径漂移和下游 handoff 的可复用经验，不改写 `SKILL.md` 的节点、输入、输出或门禁。

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
| `TM-SUBJ-01` | 用户调用 `11-主体` 整体，但只执行了 `角色` 或单个叶子 | 父级入口缺路由属性 | 回到父级 `N1/N3`，按 3 subagents 并发 fan-out | `SKILL.md` 固定 `overall_parallel` 和 Subagent Routing Matrix | `subagent_dispatch_matrix` 有 3 行 |
| `TM-SUBJ-02` | 整体调用被改成 `场景 -> 角色 -> 道具` 串行链 | 域内顺序门误读为域间顺序 | 保持三域并发；域内再按各自 `1-清单 -> 2-设计 -> 3-生成` 顺序门处理 | 父级明确“展示顺序不是执行顺序” | 报告含 `parallel_semantics` 和 `domain_route_manifest` |
| `TM-SUBJ-03` | 父级总览写成完整资产总稿，覆盖域级清单或设计稿 | 业务真源漂移 | 收缩父级总览为索引、摘要、状态和 handoff | Output Contract 禁止父级替代 3 个域级 outputs | 每个域级输出有独立路径和报告 |
| `TM-SUBJ-04` | 上游仍指旧编号分组路径或输出仍指旧编号主体路径 | 阶段重编号引用漂移 | 改为默认消费 `10-分组/第N集.md`，输出到 `11-主体/` | 引用扫描同步 `.agents`、`.codex/registry`、`scripts` 和模板 | 旧编号路径残留扫描无命中 |
| `TM-SUBJ-05` | 子技能缺执行报告，父级仍判定 pass | 报告证据门缺失 | 将父级 verdict 改为 `candidate` 或 `blocked`，要求补对应子报告 | Convergence Contract 要求每个 subagent 报告路径或阻断原因 | `subagent_result_matrix.report_output` 无空项，blocked 有 fail code |
| `TM-SUBJ-06` | 场景、角色、道具主体边界冲突，父级直接改局部文本 | 父级越权修复 | 父级只记录冲突并返工对应域级 subagent | Review Gate 绑定 `FAIL-SUBJ-CROSS-CONFLICT` | `cross_subject_consistency_report` 有冲突字段和返工目标 |
| `TM-SUBJ-07` | 部分命中 2 个主体域时被自动补齐 3 个 | 整体/部分路由混淆 | 只有用户明确整体调用时才 3 路并发；部分命中只调度点名项 | Mode Selection 区分 `overall_parallel` 与 `partial_named_route` | `domain_route_manifest` 与用户点名一致 |
| `TM-SUBJ-08` | 下游仍写成 `12-图像`、`13-画布` 或 `14-审片` | 下游 handoff 未随阶段重编号同步 | 改为 `12-图像`、`13-画布`、`14-审片` | 父级 handoff gate 固定当前编号链 | `downstream_handoff_map` 无旧编号阶段 |
| `TM-SUBJ-09` | 子技能字段、字数、数量都达标，但三域输出像同一模板换名、关键词锚点替换或同义改写批量产物 | 形式指标绕过 LLM-first 层 | 父级不得润色后放行；将 verdict 改为 `blocked/candidate` 并返工到对应叶子创作节点 | `GATE-SUBJ-ANTI-PSEUDO-DIFF` 汇总叶子 fail code | 叶子报告有反脚本化/反模板伪差异 verdict |

## Repair Playbook

1. 先判断用户是否真的整体调用：出现 `11-主体`、`主体系列整体`、`全套主体`、`完整主体阶段` 等信号，默认 `overall_parallel`。
2. 整体调用时不要推理“先角色清单再场景/道具”；三域并发，域内顺序由各自组根处理。
3. 默认上游文稿是 `projects/aigc/<项目名>/10-分组/第N集.md`；如果用户显式给了其他源，记录 `source_override=true`，但不要把旧编号分组目录当作当前 canonical。
4. 若漏掉任一主体域，不在父级总览补空白字段；必须返工调度缺失 subagent。
5. 若某个 subagent blocked，父级 verdict 不能写 `pass`；应写 `blocked` 或 `partial/candidate` 并指向该 subagent fail code。
6. 父级只聚合 `路径、状态、摘要、dependency gap、handoff`，不要改写域级或叶子技能正文。
7. 当主体边界冲突跨域出现时，优先定位冲突字段和拥有真源的域级 subagent；父级只提出返工目标，不直接合并文本。
8. 单域或部分域请求不自动补齐 3 个，除非用户明确说“整体”“全套”“完整阶段”。
9. 下游 handoff 必须同时给出“继承什么”和“不继承什么”，避免 `12-图像` 或 `13-画布` 拿父级摘要替代域级设计稿。
10. 发现旧编号路径时，先同步源层合同、registry 和脚本常量，再修模板/README/报告文案。
11. 发现脚本化、偷懒、未思考或未差异化产物时，不做表层润色或替换几个形容词；废弃候选稿，回到拥有真源的清单/设计/生成叶子重新由 LLM 判断和创作。

## Reusable Heuristics

- `11-主体` 父级的价值是协调 3 个主体域，而不是成为第 4 个创作作者。
- 并发模式下，场景、角色、道具不互相等待；互相依赖只能消费已有 canonical 文件或标记候选依赖。
- 父级总览适合给制片、资产管理和下游阶段快速扫描，但 canonical truth 仍在 3 个域级组根和叶子技能目录。
- `10-分组` 分组稿是当前主体阶段的默认抽取源；旧编号分组目录只可能是迁移痕迹，不应出现在新执行合同中。
- prompt index 或主体摘要是目录，不是 prompt 真源；下游需要完整边界时必须读对应域级设计稿。
- 发现“父级总览比域级输出更详细”通常就是越权信号。
- 整体阶段的 pass 不等于每个域都完成了生成资产；它要求清单/设计/生成状态和缺口被明确记录，并有可执行返工入口。

## Parent-Child Boundary Notes

- `场景` 拥有场景清单、场景设计和场景生成交接，不拥有角色卡或道具清单。
- `角色` 拥有角色清单、角色设计和角色生成交接，不拥有场景空间设计或道具功能设计。
- `道具` 拥有道具清单、道具设计和道具生成交接，不拥有背景杂物的无限扩张权。
- 父级 `11-主体` 拥有路由、汇流、冲突审查和 handoff，不拥有上述任何局部正文真源。
