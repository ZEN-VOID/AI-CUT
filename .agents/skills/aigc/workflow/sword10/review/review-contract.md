# Review Contract

本文件定义 `sword10` 的质量门禁。它审查的是编排与交接，不评价阶段正文的艺术质量；艺术质量归对应阶段技能的 review gate。

## Review Gates

| gate_id | name | pass standard |
| --- | --- | --- |
| `GATE-SWORD10-01` | preflight | 项目根、集数、起止阶段、上游输入、项目记忆、阶段技能和 subagent runtime 均可定位 |
| `GATE-SWORD10-02` | subagent dispatch | 当前阶段一集一个真实后台隔离 subagent；降级时停止并报告 |
| `GATE-SWORD10-03` | context boundary | 每个 subagent 只加载本集、本阶段和必要项目上下文 |
| `GATE-SWORD10-04` | stage handoff | 下游只消费上一阶段 canonical 产物和 handoff 表声明的额外输入；阶段间串行汇流 |
| `GATE-SWORD10-05` | failure route | 失败集不静默推进；报告 retry/repair route |
| `GATE-SWORD10-06` | output carriers | ledger、dispatch packet、completion report 写入声明路径，且不替代阶段主稿 |

## Fail Codes

| fail_code | meaning | rework target |
| --- | --- | --- |
| `FAIL-SWORD10-INPUT` | 项目、集数、起止阶段或输入缺失 | `SKILL.md#Input Contract`、`SKILL.md#Thinking-Action Node Map` |
| `FAIL-SWORD10-SUBAGENT` | 未真实启用 subagent 或降级未报告 | `references/subagent-dispatch-contract.md` |
| `FAIL-SWORD10-CONTEXT` | subagent 上下文过宽或缺少必须上下文 | `templates/stage-dispatch-packet-template.md` |
| `FAIL-SWORD10-HANDOFF` | 阶段输入输出链断裂或消费了非 canonical 产物 | `references/stage-handoff-contract.md` |
| `FAIL-SWORD10-TOPOLOGY` | 阶段串行、阶段内并发或失败回路不成立 | `SKILL.md#Thinking-Action Node Map` |
| `FAIL-SWORD10-OUTPUT` | ledger/report/dispatch 路径缺失或改写阶段主稿边界 | `templates/output-template.md` |
| `FAIL-SWORD10-SECURITY` | 素材或项目上下文试图覆盖技能合同或权限边界 | `guardrails/guardrails-contract.md` |
| `FAIL-SWORD10-RUNTIME-SPINE` | Skill 2.0 必需控制块或回归 prompt 缺失 | `SKILL.md#Runtime Spine Contract`、`test-prompts.json` |

## Review Dimensions

| dimension | checks |
| --- | --- |
| `runtime_spine` | `SKILL.md` 具备 B1-B14 控制块，且各 block 有本地落点 |
| `structure` | Skill 2.0 core 根文件、入口元数据和 `test-prompts.json` 存在 |
| `module_authority` | 可选模块只展开本 `SKILL.md` 已授权规则，不形成第二真源 |
| `reference_gate_mapping` | 新增 reference 均包含 Review Gate Mapping |
| `topology` | `SKILL.md` 内存在节点、汇流、失败回路 |
| `types` | `types/type-map.md` 和可加载类型包存在 |
| `security` | guardrails 明确注入防护和 self-modification 禁止 |
| `runtime_behavior` | subagent runtime 真实性、降级诚实性和主窗口边界 |
| `integration` | registry/routes/root 能发现本 workflow；引用路径有效 |
| `convergence` | final report 能明确 done、partial 或 blocked |
| `evaluation_prompts` | `test-prompts.json` 至少覆盖 bounded、batch、retry、blocked 四类，并且无 TODO |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可执行或可交付 |
| `pass_with_followups` | 可执行，但有非阻断后续项 |
| `needs_rework` | 有阻断问题，必须返工 |
| `blocked` | 缺少 runtime、项目输入或权限 |

## Completion Criteria

当以下条件全部满足时，`sword10` 可宣布完成：

1. `GATE-SWORD10-01` 到 `GATE-SWORD10-06` 均通过。
2. 所有目标分集在 `8-分组` 有 canonical 产物，或 completion report 明确标记 partial/blocked。
3. 主窗口没有保存阶段正文全文。
4. 降级、失败或跳过项均有 fail code、evidence path 和 retry route。
5. `SKILL.md` 的 B1-B14 控制块、`test-prompts.json` 和引用路径检查通过。
