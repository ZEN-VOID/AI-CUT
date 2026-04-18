# CONTEXT.md

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
|---|---|---|---|---|
| 把 `4-Validation` 写成直接执行 checker | skill contract | 改回阶段调度器定位，收回 checker 判断权 | 在 `SKILL.md` 写死“只调度 `references/validation-team-contract.md` 白名单角色” | 运行时不再出现主流程内联审查结论 |
| 评估结果受上轮上下文污染 | orchestration | 每轮新建后台团队，不复用旧线程 | 在 `SKILL.md` 把“新上下文 + 新团队”设为硬规则 | 相邻两轮评估可独立复核，不依赖旧措辞 |
| `PASS` 结果没有进入 `5-Loopback` actualization，或非 PASS 结果误入 truth 写回 | handoff contract | 重新按 `validation_status` 分流 | 在 `SKILL.md` 固定 `PASS -> review + 5-Loopback`，非 PASS 禁止进入 actualization 主流程 | 通过验证的 episode 才会刷新 Cards / MAP / projection |
| validation 输入缺少承诺/章节板/卡片状态切片，导致 checker 只按旧大纲粗审 | fact pack contract | 把 `validation_fact_pack` 升级为最小输入硬门槛 | 在 `context-agent` 与 `4-Validation` 同时写死五类强制 slice | checker 报告可明确引用承诺、`chapter_board` 与 `current_state/history` 证据 |
| 反剧透/反刻意/反冷评只停留在文本要求，没有进入 validation 聚合字段 | aggregation contract | 新增正式 checker 与一等风险字段 | 把 `spoiler-checker`、`immersion-voice-checker` 和 `spoiler_risk / contrivance_risk / cold_commentary_risk` 写入聚合与持久化 schema | 风险不再只能藏在 `notes` 或口头提醒里 |
| 初始化已生成 `TEAM.toml`，但 `4-Validation` 执行时不读取 `评审` 布阵 | stage team governance | 在 `4-Validation/SKILL.md` 把 `TEAM.toml["评审"]` 升级为必读输入，并要求有指派 AGENTS 时创建评审专家组子通道 | 将“checker 白名单是基础框架，评审团队只做增量加层，不做覆盖替换”写成根技能硬规则 | 执行 `4-Validation` 时能明确区分 checker 证据层与评审专家组裁决层 |
| workflow 已写 `<run_id>` 级治理工件，但验证层合同不承认这些工件的 review-office 证据地位 | governance artifact contract | 在 `4-Validation` 合同中显式声明 task dir 中的 `validation_report / learning_record / root_cause_trace` | 让验证层、审查层和共享脚本对门下省证据层使用同一套路径语义 | 失败或通过后的 task dir 可以被审计脚本直接识别，而不需要猜路径 |

## Repair Playbook

1. 先判断问题出在调度层、checker 合同层，还是聚合/回流层。
2. 若出现判断失真，优先检查是否复用了旧上下文或把主流程意见注入 checker。
3. 若出现结果不可回流，优先检查聚合 schema 是否缺失 `issues / severity_counts / critical_issues`。
4. 只有在调度与合同层确认正常后，才处理章节内容本身。

## Reusable Heuristics

- `4-Validation` 的价值不是“再做一次 review”，而是用隔离上下文的后台团队提供更客观的第二视角。
- 只要目的是检验客观性，就应优先新建团队而不是复用旧 checker 线程。
- 阶段调度层可以薄，但不能虚；必须明确白名单 agent、聚合 schema 和回流方向。
- `TEAM.toml["评审"]` 对 `4-Validation` 来说是治理增量，不是框架替换；基础 checker 团队必须始终保留。
- `4-Validation` 也是 `5-Loopback` 的唯一写回闸门；只要 gate 松掉，下游 truth 就会被污染。
- 只要 validation 目标扩展到“反坏写法”，事实包就不能只给设定和大纲，还必须给承诺、静默区和表达门禁。
- `反剧透 / 反刻意 / 反冷评` 只有进入一等字段和趋势统计后，才算真正进入系统，而不是停留在审稿话术里。
- 当某个 validation 合同会被 `3-Drafting`、`4-Validation`、`review/` 和 checker 团队共同消费时，应提升为根级 shared reference，而不是散落在单一阶段文档里。
- task dir 里的 `validation_report.md` 是门下省证据层，不是新的 checker；判断权仍在 `4-Validation` 聚合本身。
