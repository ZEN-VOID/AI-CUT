# Conflict Verification Contract

本文件定义当学习对象与模型固有认知、仓库合同或外部事实冲突时的核查规则。

## Verification Triggers

必须核查后再落盘的情况：

- 用户学习对象提出的事实与已知常识、仓库合同或目标 skill 规则冲突。
- 来源可能过期，例如 API、模型能力、平台规则、法律政策、价格、接口参数或工具可用性。
- 材料来自二手总结、营销页面、论坛、视频口播、未署名文档或来源不明文件。
- 建议会改变安全、权限、版权、隐私、医疗、法律、金融或合规边界。
- 建议会大规模改写 AIGC 阶段链、项目 runtime 或审计脚本。

## Source Priority

| priority | source type |
| --- | --- |
| P1 | 官方文档、标准、论文原文、项目仓库真源、本地 `AGENTS.md` / `SKILL.md` |
| P2 | 权威媒体、作者本人说明、可信课程材料、版本化 release note |
| P3 | 高质量技术博客、社区讨论、视频讲解、二手笔记 |
| P4 | 无来源摘录、营销文案、模型记忆、单一评论 |

## Decision Labels

| label | meaning |
| --- | --- |
| `adopt` | 证据充分，与仓库合同兼容，可转为规则或经验 |
| `adapt` | 原理可用，但需按 AIGC 技能树改写后吸收 |
| `reject` | 证据不足、冲突不可调和、违反安全或版权边界 |
| `hold` | 需要更多来源或用户授权，暂不落盘 |

## Web Verification Rule

当需要联网时，优先查官方和一手来源；只有缺少一手来源时才使用二手资料。最终报告必须列出核查结论、采用标签和未解决风险。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 学习对象与常识、仓库合同、目标 skill 规则或外部事实冲突时，是否先触发核查而非直接落盘？ | `GATE-LEARN-VERIFY-01` | `FAIL-AIGC-LEARN-VERIFY` | `N4-VERIFY` / `Verification Triggers` | conflict trigger、冲突对象、被影响文件或规则 |
| API、模型能力、平台规则、法律政策、价格、接口参数或工具可用性等易变信息是否按当前可靠来源核实？ | `GATE-LEARN-VERIFY-01` | `FAIL-AIGC-LEARN-VERIFY` | `N4-VERIFY` / `Verification Triggers` | verified date、official/reliable source URLs or local source paths |
| 二手总结、营销页面、论坛、视频口播、未署名文档或来源不明文件是否被降级处理并寻找更高优先级来源？ | `GATE-LEARN-VERIFY-01` | `FAIL-AIGC-LEARN-VERIFY` | `N4-VERIFY` / `Source Priority` | source priority label、fallback search notes、confidence level |
| 涉及安全、权限、版权、隐私、医疗、法律、金融或合规边界的建议是否经过高风险核查？ | `GATE-LEARN-VERIFY-01` | `FAIL-AIGC-LEARN-VERIFY` | `N4-VERIFY` / `Verification Triggers` | risk category、verification notes、blocked/adapted scope |
| 会大规模改写 AIGC 阶段链、项目 runtime 或审计脚本的建议是否先完成 owner 与 sync scope 裁决？ | `GATE-LEARN-MAP-01` | `FAIL-AIGC-LEARN-MAP` | `N5-MAP` / `Verification Triggers` | affected stages、primary owner、sync scope、not_owned |
| 核查来源是否优先使用官方文档、标准、论文原文、项目仓库真源或本地 `AGENTS.md` / `SKILL.md`？ | `GATE-LEARN-VERIFY-01` | `FAIL-AIGC-LEARN-VERIFY` | `N4-VERIFY` / `Source Priority` | P1/P2/P3/P4 source list、why lower-priority source was used |
| 最终是否给出 `adopt` / `adapt` / `reject` / `hold` 标签，而不是只写“已核查”？ | `GATE-LEARN-VERIFY-02` | `FAIL-AIGC-LEARN-VERIFY` | `N4-VERIFY` / `Decision Labels` | decision label、reason、unresolved risks |
| `hold` 或 `reject` 的内容是否没有被写成强制规则或经验层确定结论？ | `GATE-LEARN-VERIFY-02` | `FAIL-AIGC-LEARN-VERIFY` | `N4-VERIFY` / `Decision Labels` | changed_files scan、held/rejected item list、no writeback note |
| 需要联网时，最终证据是否列出核查结论、采用标签和未解决风险？ | `GATE-LEARN-VERIFY-02` | `FAIL-AIGC-LEARN-VERIFY` | `N4-VERIFY` / `Web Verification Rule` | verification summary、decision label、residual risks |
