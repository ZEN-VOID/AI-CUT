# Planning Review Contract

本文件定义 `aigc/1-Planning` 单包融合后的质量门禁。review 只拥有审计与返工建议权，不拥有业务主真源改写权。

## Review Scope

| dimension | checks |
| --- | --- |
| structure | `1-Planning` 是否是单一 Skill 2.0 包，旧三子包是否已迁入分区 |
| dynamic_reference | 根 `SKILL.md` 是否只做入口、路由、动态引用、门禁和输出合同 |
| legacy_preservation | 原 `1-分集 / 2-格式 / 3-分组` 细则是否可在 `references/` 追溯 |
| runtime_boundary | 项目 runtime 子目录是否保留业务输出边界，不与技能包入口混淆 |
| script_boundary | `scripts/` 是否只做校验、量化、渲染、postprocess，不替代 LLM 主创 |
| validation | validator、quantizer、审计脚本是否可运行 |
| references | 全仓是否仍有旧子技能路径断链 |

## Required Gates

1. Skill 2.0 结构校验：
   `python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/aigc/1-规划`
2. sibling context 校验：
   `python3 scripts/skill_context_audit.py --root .agents/skills/aigc/1-规划 --strict`
3. AIGC 技能树审计：
   `python3 scripts/aigc_skill_audit.py --strict`
4. 引用同步检查：
   `rg -n "\\.agents/skills/aigc/1-规划/(1-分集|2-格式|3-分组)|aigc-planning-(episode-splitter|script|grouping)"`

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可作为融合后的 Skill 2.0 包交付 |
| `pass_with_todo` | 可交付，但存在非阻断 TODO 或历史报告残留引用 |
| `needs_rework` | 有结构、断链或门禁失败，必须返工 |
| `blocked` | 缺失关键输入、权限或上层策略阻断 |

## Reviewer / Subagent Policy

- 仓库层允许 reviewer gate，但真实 subagent/provider 调度必须服从当前会话更高优先级策略。
- 若上层策略阻断真实 subagent 或外部 reviewer，降级为本地 checklist，并在最终报告中说明：
  - 阻断来源层级
  - 原计划路径
  - 实际降级路径
  - 未真实启动的 reviewer

## Pass Conditions

- `find .agents/skills/aigc/1-规划 -name SKILL.md` 只返回父级 `SKILL.md`。
- `references/legacy-migration-matrix.md` 覆盖旧三包所有根文件、脚本、模板、metadata 和 shared I/O。
- `agents/openai.yaml` 的默认提示只推荐 `$aigc-planning`。
- `scripts/`、`templates/`、`skill_manifest.json` 不再指向旧子包路径。
- 若审计保留历史 CHANGELOG 或 reports 中的旧路径，只能作为历史证据存在，不得作为当前运行入口。
