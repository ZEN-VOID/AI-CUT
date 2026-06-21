# Context: wjs-auditing-project

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2534
current_lines: 44
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-auditing-project` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

| symptom | root_cause_layer | immediate_fix | systemic_prevention | verification |
| --- | --- | --- | --- | --- |
| 用户说“make it right”后直接修代码、合 PR 或推送，跳过审计清单 | phase boundary | 退回 Phase 1，只做只读调查并输出 grouped checklist | 固定 Investigate -> Confirm -> Fix 两阶段门禁 | 最终输出先出现待确认 checklist，未出现 commit / merge / push |
| 只看 `git status`，漏掉 PR、CI、未发布版本、计划漂移或日志错误 | audit coverage | 补跑 Phase 1 A-G 的只读检查 | 把检查面按工作树、PR、CI、发布、计划、日志、反馈链分组 | 每个异常项都有编号、日期、路径或命令证据 |
| in-app feedback 已被 `app/claude` PR 合并，却误判为功能没做 | feedback release chain | 比较反馈 PR merge 时间与 TestFlight/App Store build 时间 | 把“反馈入主干”和“用户拿到新 build”分成两个状态 | 结论明确是代码未合、已合未构建、还是已构建未提交 |
| PR 看起来干净就自行 merge，或对 stash / branch 做破坏性整理 | confirmation boundary | 停止写操作，逐项征求用户确认 | Fix 阶段按用户确认的 item 执行，不做隐含授权 | 每个 merge、drop、tag、push 都能对应用户确认文本 |
| TODO / ROADMAP 过期项被当作废弃内容删除 | plan drift governance | 只把过期项列为 plan drift，询问 descoped 还是 forgotten | 计划文件是审计证据，不是自动清理对象 | 过期项仍保留，除非用户明确要求修改 |
| 尝试代用户提交 TestFlight / App Store | human-action boundary | 输出以 `!` 开头的用户执行命令并停止 | 把签名、上传、App Store 后台操作列为 requires-human | 回复中没有代执行上传，只给明确命令与前置状态 |
| CI 失败后直接 rerun | root-cause discipline | 先读失败日志，确认根因或疑似 flaky 证据 | rerun 只能发生在诊断之后，不能作为默认修复 | checklist 或修复摘要包含失败 job、日志片段和处理依据 |

## Repair Playbook

1. 先读取同目录 `SKILL.md`，确认本轮必须走 read-only investigation，再进入用户确认后的 fix。
2. Phase 1 并行收集工作树、stash、branch、PR、CI、release/build、plan drift、logs、feedback PR 链路；失败或不可用的检查要列为 verification gap。
3. 输出按 Blocking / Open work / Plan drift / Logs / Looks fine 分组的 checklist；每项包含问题、证据和可让用户 yes/no 的建议动作。
4. checklist 之后等待用户确认；用户说“全部修”也视为确认，但不能省略 checklist。
5. Phase 2 只处理用户确认的 item，顺序优先 failing CI -> branch/PR -> tag/version/release notes -> build prompt。
6. 每修完一项，重跑对应 Phase 1 检查验证，不用全仓重跑来替代局部证据。

## Reusable Heuristics

- “没有问题”的检查不一定进入 checklist，但阻塞工具或缺权限必须进入 verification gaps。
- 证据优先用 PR 号、run id、branch 名、tag/build 号、文件路径和日期；不要只写“看起来没有发布”。
- 对 Cathier 反馈链路，先判断 `app/claude` PR 是否创建、是否合并、是否晚于最新 TestFlight build。
- App Store / TestFlight 相关结论要区分“代码状态”“构建状态”“提交状态”，避免把发布问题误修成代码问题。
- Stash、force push、branch 删除、tag push、App Store 上传都属于高风险动作；即便在 Fix 阶段也需要明确授权。
- 计划漂移是决策输入，不是自动修复对象；过期 deadline 应呈现给用户裁决。

## Promotion Backlog

- 抽取 Phase 1 只读检查为 dry-run 审计脚本，输出结构化 JSON 供 checklist 生成。
- 增加 Cathier release comparator：自动比较 `app/claude` merge 时间、最新 tag、TestFlight build 时间。
- 增加 checklist 模板，强制每项包含 `evidence` 与 `proposed_action`。

## Case Log

暂无案例。后续只追加可复用、可验证、可晋升的案例。
