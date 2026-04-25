# Planning Workflow

本文件是 `aigc/1-Planning` 融合包的思行网络真源。根 `SKILL.md` 负责入口和门禁；本文件负责 mode 内执行拓扑、分支、汇流和失败回路。

## Business Requirement Analysis

| slot | question |
| --- | --- |
| `business_goal` | 本轮要完成分集、2-剧本、分组、完整规划链，还是只做验收/修复？ |
| `business_object` | 输入对象是 `Story/`、`1-分集` 输出、`2-剧本` 主稿、`3-分组` 结果，还是技能包结构本身？ |
| `constraint_profile` | 约束来自故事源 readiness、剧本策略、组界量化、项目 runtime，还是 Skill 2.0 结构？ |
| `success_criteria` | 哪些文件、validator、报告或 handoff 能证明本轮完成？ |
| `non_goals` | 本轮不写 `2-Global`、不生成 `3-Detail`、不伪造未执行模式输出。 |
| `complexity_source` | 复杂度来自模式分型、上游覆盖、正文保真、量化边界、脚本校验或引用同步。 |
| `topology_fit` | 默认使用“前置判型 -> 命中模式执行 -> 统一验收”的 hybrid 拓扑。 |

## Thinking-Action Node Network

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 锁定项目、用户目标与可用产物 | 用户请求、项目根、父技能上下文 | 读取项目记忆、runtime、manifest 与现有 planning 产物 | 输入清单、缺口清单 | `N2-TYPE` | 项目与目标明确 |
| `N2-TYPE` | 形成 `type_profile` 和 mode | `N1` 输出、`types/planning-type-map.md` | 判定 `episode_split/script_format/grouping/full_chain/stage_validation/repair` | route reason | `N3-LOAD` | mode 唯一或全链顺序明确 |
| `N3-LOAD` | 读取命中模式细则 | `Reference Loading Guide` | 只加载命中的 `references/`、`scripts/`、`templates/`、`knowledge-base/` | loaded references | `N4-EXECUTE` | 无缺失文件 |
| `N4-EXECUTE` | 执行命中模式 | mode-specific 输入 | LLM 做业务判断和正文/边界/组界主创，脚本只做辅助校验 | 写回文件、patch、verdict | `N5-VALIDATE` | 产物落在 owned runtime |
| `N5-VALIDATE` | 运行模式质量门 | 模式产物、脚本、review 合同 | 运行 validator/quantizer 或本地 checklist | PASS/FAIL、失败码 | pass -> `N6-MERGE`; fail -> `N4-EXECUTE` 或 `N7-REPAIR` | 失败不得宣布完成 |
| `N6-MERGE` | 聚合已执行结果 | 有效 patch、执行报告 | 写或更新 `validation-report.md`，只登记本轮真实发生的产物 | stage verdict、handoff | done | 未执行模式不补空 |
| `N7-REPAIR` | 修复结构或引用问题 | 失败码、Root-Cause 链路 | 回到对应 owner 修复 `SKILL.md/references/scripts/templates` | 最小修复 patch | `N5-VALIDATE` | 修复后重跑验证 |

## Mode Branches

| mode | branch steps | convergence gate |
| --- | --- | --- |
| `episode_split` | 锁 Story 输入 -> readiness -> `P1>P2>P3` 边界 -> 写 `1-分集` 与索引 | `episode-split-plan.json`、执行报告与 handoff 字段一致 |
| `script_format` / `2-剧本` | 锁 `1-分集` 输出 -> 业务分析 -> 标准剧本策略 -> 正文整形 -> validator -> 汇总报告 | `2-剧本` 主稿（runtime: `2-格式/第N集.md`）与唯一 `2-格式/执行报告.md` 通过或有返工入口 |
| `grouping` | 锁 `2-剧本` 主稿 -> 组界 -> quantizer -> 可选 reviewer -> 尾钩 -> validator | grouped script、执行报告与 quantizer 一致 |
| `full_chain` | 串行执行前三个 mode；中间子目录是处理边界，不是默认交互断点 | 三类产物均 pass 后进入 `stage_validation` |
| `stage_validation` | 汇总已发生产物 -> 写 verdict -> 下游 handoff | `validation-report.md` 不含伪造完成项 |
| `repair` | 定位 owner -> 修复引用/脚本/模板/报告 -> 重跑验证 | 失败码消失且迁移矩阵同步 |

## Failure Routing

| fail_code | symptom | rework_target |
| --- | --- | --- |
| `FAIL-PLAN-02` | mode 不唯一或误判 | `types/planning-type-map.md`、`SKILL.md` Mode Selection |
| `FAIL-PLAN-03` | 分集索引与正文漂移 | `references/episode-splitter-contract.md`、`templates/episode-split-plan.template.json` |
| `FAIL-PLAN-04` | `2-剧本` 策略或 validator 失败 | `references/script-format-contract.md`、`scripts/validate_script_output.py` |
| `FAIL-PLAN-05` | 分组量化、尾钩或报告不一致 | `references/grouping-contract.md`、`scripts/grouping_quantizer.py`、`scripts/validate_grouping_output.py` |
| `FAIL-PLAN-07` | 旧子技能入口或路径断链 | `references/legacy-migration-matrix.md`、`scripts/aigc_skill_audit.py` |

## Merge Rule

`validation-report.md` 只接收已执行模式返回的有效 patch。未命中的分集、格式或分组模式不得因为结构完整性被补空字段。
