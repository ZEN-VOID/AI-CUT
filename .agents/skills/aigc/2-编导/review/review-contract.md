# Review Contract

## Review Purpose

`2-编导` 的 review gate 验证逐集编导稿是否忠实承接 `1-分集`，并能被下游分组、摄影、设计与视频链路稳定消费。

## Default Provider

- 默认辅助 provider：`code-reviewer`
- 用途：检查 Skill 2.0 包结构、脚本边界、输出合同和剧本字段门禁。
- 若本轮启动 subagents 模式，review 还必须检查 `../../_shared/team-advisor-consultation-contract.md` 与 `../SKILL.md#Subagents Execution Mechanism`：是否从项目 `team.yaml` 解析监制组相关智能顾问团、是否要求顾问代入专业视角和个人风格提出编导阶段具体参谋问题、是否形成 `advisor_consultation_packet`，以及顾问指导是否沉淀为后续任务上下文而未改写上游真源。
- 若上层策略阻断真实 subagent 或 provider 调度，允许降级为本地 review checklist，并在报告中说明阻断来源、原计划 provider、实际路径和未启动 reviewer。

## Stage-End Review-Repair Rule

- 除 `review_only` 外，review gate 是写回前的阻断门，不是交付后的附带报告。
- `needs_rework` 必须回到 `steps/directing-workflow.md` 的 `N6R-DIRECT-REPAIR`，由 `2-编导` 本阶段直接做最小修复并复审；复审未通过不得写入 canonical `2-编导/第N集.md`。
- 允许直接修复的范围：字段投影、声画配对、slugline 去重、画面具像化、声音本体、高潮承托、frontmatter/report 证据和格式。
- 禁止直接修复的范围：新增或删减剧情事实、改写对白、改变事件顺序、替上游 `1-分集` 修剧情。遇到这类问题必须输出 source owner 和阻断报告。
- `pass_with_followups` 只允许非阻断质量建议；任何保真、对白、声画、slugline、字段纯度或 LLM-first 问题不得降级为 followup。

## Blocking Gates

| gate_id | check | fail_code |
| --- | --- | --- |
| `GATE-DIRECT-01` | 输出路径为 `projects/aigc/<项目名>/2-编导/第N集.md` | `FAIL-PATH` |
| `GATE-DIRECT-02` | frontmatter 含 `source_episode_path` 且可回指上游 | `FAIL-SOURCE` |
| `GATE-DIRECT-03` | 上游事实信息量与顺序完整承接 | `FAIL-FAITHFULNESS` |
| `GATE-DIRECT-04` | 对白逐字保真，中文双引号，引号内无动作 | `FAIL-DIALOGUE` |
| `GATE-DIRECT-05` | 声音字段就近配对对应 `*画面` 字段 | `FAIL-PAIRING` |
| `GATE-DIRECT-06` | 每个场景至少一条正式画面字段 | `FAIL-SCENE-VISUAL` |
| `GATE-DIRECT-07` | 场景标题是阿拉伯编号 + slugline，同 slugline 不重复开场 | `FAIL-SLUGLINE` |
| `GATE-DIRECT-08` | `动作画面` 不含心理解释、抽象判断或小说章节名 | `FAIL-ACTION-PURITY` |
| `GATE-DIRECT-09` | 脚本没有替代 LLM 生成核心创作正文 | `FAIL-LLM-FIRST` |
| `GATE-DIRECT-10` | 所有 `*画面`、`环境描写`、`道具特写`、`表演提示` 均具像化、画面化、反抽象、反概念、反比喻 | `FAIL-CONCRETE-VISUAL` |
| `GATE-DIRECT-11` | `音效` 字段只写声音本体，不写时间说明、事件概括或描述性句子 | `FAIL-SOUND-LITERAL` |
| `GATE-DIRECT-12` | 上游存在高潮/爽点/高光成分时，输出完成 `peak_visual_pass`，高点有可回指证据、可拍承托、状态差或余波，且没有新增事实、对白或因果 | `FAIL-PEAK-VISUAL` |
| `GATE-DIRECT-13` | 启动 subagents 模式时，已完成 `team.yaml` 监制顾问请教并沉淀为后续上下文，或记录上层阻断降级 | `FAIL-ADVISOR-CONSULT` |

## Recommended Mechanical Check

```bash
python3 .agents/skills/aigc/2-编导/scripts/validate_script_projection.py projects/aigc/<项目名>/2-编导/第N集.md
```

该脚本只检查结构、字段和基础配对，不能证明剧情事实完整承接；事实完整性和对白逐字保真仍需 LLM/人工对读上游。

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可交付给下游阶段 |
| `pass_with_followups` | 可交付，但存在非阻断质量优化 |
| `needs_rework` | 存在保真、对白、声画或场景标题阻断项 |
| `blocked` | 上游缺失、路径不可读、权限或策略阻断 |

## Report Shape

```yaml
review:
  verdict: pass | pass_with_followups | needs_rework | blocked
  source_episode_path: projects/aigc/<项目名>/1-分集/第N集.md
  output_path: projects/aigc/<项目名>/2-编导/第N集.md
  checks:
    faithfulness: pass
    dialogue_lock: pass
    audio_visual_pairing: pass
    slugline_stability: pass
    field_purity: pass
    concrete_visuals: pass
    sound_literal: pass
    peak_visual_treatment: pass
    advisor_consultation: pass
    hollywood_quality: pass
    repair_loop: pass
  repair_actions: []
  re_review_verdict: pass
  findings: []
```
