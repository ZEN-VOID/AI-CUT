# Review Contract

## Review Purpose

`2-编导` 的 review gate 验证逐集编导稿是否忠实承接 `1-分集`，并能被下游分组、摄影、设计与视频链路稳定消费。

## Default Provider

- 默认辅助 provider：`code-reviewer`
- 用途：检查 Skill 2.0 包结构、脚本边界、输出合同和剧本字段门禁。
- 若上层策略阻断真实 subagent 或 provider 调度，允许降级为本地 review checklist，并在报告中说明阻断来源、原计划 provider、实际路径和未启动 reviewer。

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
    hollywood_quality: pass
  findings: []
```
