# Context: aigc 3-主体

本文件是 `3-主体` 整体主入口的经验层知识库，不是规范真源。调用同目录 `SKILL.md` 时必须同时加载本文件；它只沉淀整体路由、3 subagents 并发、父级汇流、主体注册表、旧编号路径漂移、后置 `8-分组` reconciliation 和下游 handoff 的可复用经验，不改写 `SKILL.md` 的节点、输入、输出或门禁。

## Context Health

```yaml
monitor_version: 2
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-parent-routing-heuristics-only
last_checked_at: 2026-06-16
```

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 系统预防修复 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-SUBJ-01` | 用户调用 `3-主体` 整体，但只执行了 `角色` 或单个叶子 | 父级入口缺路由属性 | 回到父级 `N1/N3`，按 3 subagents 并发 fan-out | `SKILL.md` 固定 `overall_parallel` 和 Subagent Routing Matrix | `subagent_dispatch_matrix` 有 3 行 |
| `TM-SUBJ-02` | 整体调用被改成 `场景 -> 角色 -> 道具` 串行链 | 域内顺序门误读为域间顺序 | 保持三域并发；域内再按各自 `1-清单 -> 2-设计 -> 3-生成` 顺序门处理 | 父级明确“展示顺序不是执行顺序” | 报告含 `parallel_semantics` 和 `domain_route_manifest` |
| `TM-SUBJ-03` | 父级总览写成完整资产总稿，覆盖域级清单或设计稿 | 业务真源漂移 | 收缩父级总览为索引、摘要、状态和 handoff | Output Contract 禁止父级替代 3 个域级 outputs | 每个域级输出有独立路径和报告 |
| `TM-SUBJ-04` | 上游仍指旧编号分组路径、把 `8-分组` 当初始主体来源，或输出仍指旧编号主体路径 | 阶段重编号 / 主体前置引用漂移 | 改为默认消费 `1-分集` 全量故事源、`2-美学/类型风格.md` 与三域风格协议，先生成 `3-主体/subject-registry.yaml` | 引用扫描同步 `.agents`、`.codex/registry`、`scripts` 和模板；`8-分组` 只作后置 reconciliation | 旧编号路径残留扫描无命中，且清单 gate 均指向 registry |
| `TM-SUBJ-05` | 子技能缺执行报告，父级仍判定 pass | 报告证据门缺失 | 将父级 verdict 改为 `candidate` 或 `blocked`，要求补对应子报告 | Convergence Contract 要求每个 subagent 报告路径或阻断原因 | `subagent_result_matrix.report_output` 无空项，blocked 有 fail code |
| `TM-SUBJ-06` | 场景、角色、道具主体边界冲突，父级直接改局部文本 | 父级越权修复 | 父级只记录冲突并返工对应域级 subagent | Review Gate 绑定 `FAIL-SUBJ-CROSS-CONFLICT` | `cross_subject_consistency_report` 有冲突字段和返工目标 |
| `TM-SUBJ-07` | 部分命中 2 个主体域时被自动补齐 3 个 | 整体/部分路由混淆 | 只有用户明确整体调用时才 3 路并发；部分命中只调度点名项 | Mode Selection 区分 `overall_parallel` 与 `partial_named_route` | `domain_route_manifest` 与用户点名一致 |
| `TM-SUBJ-08` | 下游仍写成旧阶段或已移除阶段 | 下游 handoff 未随阶段链同步 | 改为 `9-图像`、`10-画布` | 父级 handoff gate 固定当前编号链 | `downstream_handoff_map` 无旧编号阶段 |
| `TM-SUBJ-09` | 子技能字段、字数、数量都达标，但三域输出像同一模板换名、关键词锚点替换或同义改写批量产物 | 形式指标绕过 LLM-first 层 | 父级不得润色后放行；将 verdict 改为 `blocked/candidate` 并返工到对应叶子创作节点 | `GATE-SUBJ-ANTI-PSEUDO-DIFF` 汇总叶子 fail code | 叶子报告有反脚本化/反模板伪差异 verdict |
| `TM-SUBJ-10` | 父级 runtime spine 更新了路由或 gate，但没有同步 agent metadata、test prompts 或 README | Skill 2.0 核心布局同步缺口 | 同轮补齐 `agents/openai.yaml`、`test-prompts.json`、`README.md`，并在 `CHANGELOG.md` 记录 | 父级结构变更默认检查 core layout 与 prompts 覆盖 | delivery validator、JSON/YAML 解析和 prompt ids 检查通过 |
| `TM-SUBJ-11` | router root smoke 报大量子目录 `review/`、`templates/`、`references/` broken refs，但对应叶子单独 smoke 为 ACCEPT | 递归扫描把叶子相对路径按父级 root 解析 | 不在父级批量改写叶子本地引用；先跑叶子目录独立 smoke 区分真实断链与递归误判 | 父级 final 报告标注 root 为 conditional、叶子为 accept，并保留 `.smoke-test-report.json` | 4 个 router root 允许 conditional，9 个叶子 smoke 均 ACCEPT |
| `TM-SUBJ-12` | `Type Routing Matrix.module_load` 或 `Module Trigger Matrix.required_modules` 使用多模块逗号列表后，smoke 报 `-> ,` missing module | validator 的矩阵 token 解析把逗号视作模块项 | root/domain 级矩阵优先使用一个已授权模块 token；多叶子分发写在节点 actions 或 mechanical_check | 模块矩阵使用可解析 token：`CONTEXT.md`、`1-清单/`、`2-设计/`、`3-生成/`、`SA-*` | smoke 不再出现 `MISSING MODULE LOAD/TRIGGER -> ,` |
| `TM-SUBJ-13` | 跨集执行主体生成时，父级未把既有主体图复用规则传给叶子，导致同主体同状态重复生成、本地 canonical 已有仍重复下载，或画布/本地缺口未互补 | 共享生成合同未回指 | 在父级 task packet 中提示叶子加载 `_shared/主体图复用与状态变体规则.md` | `3-生成` 叶子固定 asset preflight 和 local canonical ensure gate：本地已有跳过下载，画布缺上传，本地缺下载 | 叶子报告有 `asset_reuse_decision`、`canvas_action`、`local_sync_status`、状态变体 `Lib Image` 证据 |

## Repair Playbook

1. 先判断用户是否真的整体调用：出现 `3-主体`、`主体系列整体`、`全套主体`、`完整主体阶段` 等信号，默认 `overall_parallel`。
2. 整体调用时不要推理“先角色清单再场景/道具”；三域并发，域内顺序由各自组根处理。
3. 默认上游是 `projects/aigc/<项目名>/1-分集/` 全量故事源、`2-美学/类型风格.md` 和三域风格协议；父级先生成 `3-主体/subject-registry.yaml`，再分发给角色、场景、道具叶子。
4. 若漏掉任一主体域，不在父级总览补空白字段；必须返工调度缺失 subagent。
5. 若某个 subagent blocked，父级 verdict 不能写 `pass`；应写 `blocked` 或 `partial/candidate` 并指向该 subagent fail code。
6. 父级只聚合 `路径、状态、摘要、dependency gap、handoff`，不要改写域级或叶子技能正文。
7. 当主体边界冲突跨域出现时，优先定位冲突字段和拥有真源的域级 subagent；父级只提出返工目标，不直接合并文本。
8. 单域或部分域请求不自动补齐 3 个，除非用户明确说“整体”“全套”“完整阶段”。
9. 下游 handoff 必须同时给出“继承什么”和“不继承什么”，避免 `9-图像` 或 `10-画布` 拿父级摘要替代域级设计稿。
10. 发现旧编号路径或 `8-分组` 被当成主体新增来源时，先同步源层合同、registry 和脚本常量，再修模板/README/报告文案。
11. 发现脚本化、偷懒、未思考或未差异化产物时，不做表层润色或替换几个形容词；废弃候选稿，回到拥有真源的清单/设计/生成叶子重新由 LLM 判断和创作。
12. 修改父级路由、汇流 gate、上下文处理或 anti-scripted gate 时，同步检查 `test-prompts.json` 是否覆盖整体并发、单域路由和修复审查三类路径。
13. 处理 router root smoke 时，先看 Phase E/F 是否有硬拒绝；若只剩子目录相对路径 broken refs，必须用叶子独立 smoke 复核真实可运行性。
14. 编写矩阵单元格时避免逗号分隔多模块；需要表达多文件加载时，用一个授权模块 token 承载触发，细节写入节点 action、mechanical_check 或对应叶子合同。
15. 若任务进入任一 `3-生成` 叶子，父级不直接生图，但必须保留共享生成规则回指：Midjourney V8.1 默认后缀来自 `_shared/midjourney风格参数.yaml`，跨集复用、本地 canonical 已有跳过、画布缺失时上传、本地缺失时下载补齐和状态变体来自 `_shared/主体图复用与状态变体规则.md`。
16. 生图执行时不要把 `--ar`、`--hd`、`--style raw` 或武侠片 `--profile lsp4mxl cce1fkr qe4r8p2` 只落到 libTV 参数或 JSON 记录里；这些后缀必须出现在实际节点 `prompt` 文本末尾。若已产图缺后缀，先隔离本地文件并更新节点 prompt 后重跑，不继续批量生成。
17. libTV `Midjourney V8.1` 当前 schema 暴露 `count: [4]`，不要在主体技能里强制改成 `count=1`；自 2026-06-19 起主体图片生成默认只收束为一个 canonical 主图 stem，`-多视图` 已取消，不再作为缺口、补齐目标或完成门。
18. 用户要求“图片生成时取消多视图”时，源层落点必须同步到 `角色/3-生成`、`场景/3-生成`、`道具/3-生成` 三个叶子的 Output Contract、Type Routing、节点表和 review gate；只停掉当前运行任务不足以闭环。

## Reusable Heuristics

- `3-主体` 父级的价值是协调 3 个主体域，而不是成为第 4 个创作作者。
- 并发模式下，场景、角色、道具不互相等待；互相依赖只能消费已有 canonical 文件或标记候选依赖。
- 父级总览适合给制片、资产管理和下游阶段快速扫描，但 canonical truth 仍在 3 个域级组根和叶子技能目录。
- `3-主体/subject-registry.yaml` 是当前主体命名真源；`8-分组` 理论上不新增主体，只能在后置阶段校验 YAML 中主体是否命中 registry。
- prompt index 或主体摘要是目录，不是 prompt 真源；下游需要完整边界时必须读对应域级设计稿。
- 发现“父级总览比域级输出更详细”通常就是越权信号。
- 整体阶段的 pass 不等于每个域都完成了生成资产；它要求清单/设计/生成状态和缺口被明确记录，并有可执行返工入口。
- 父级技能变更只改 `SKILL.md` 不够；核心布局资产和 test prompts 是回归门的一部分，缺失时会让 subagents 并发语义不可复现。
- root/domain 矩阵追求机器可解析优先于自然语言完整列举；多模块的业务含义可在 `actions` 和 `mechanical_check` 展开。

## Parent-Child Boundary Notes

- `场景` 拥有场景清单、场景设计和场景生成交接，不拥有角色卡或道具清单。
- `角色` 拥有角色清单、角色设计和角色生成交接，不拥有场景空间设计或道具功能设计。
- `道具` 拥有道具清单、道具设计和道具生成交接，不拥有背景杂物的无限扩张权。
- 父级 `3-主体` 拥有路由、汇流、冲突审查和 handoff，不拥有上述任何局部正文真源。
