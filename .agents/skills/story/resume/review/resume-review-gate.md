# Resume Review Gate

本文件定义 `$story-resume` 的交付前质量门禁、verdict 模型与 reviewer/provider 降级口径。

## Default Provider

- 默认辅助 provider：`code-reviewer`
- 用途：检查 Skill 2.0 结构、恢复证据链、安全边界、runtime 口径和输出模板。
- 若上层策略阻断真实 subagent 或外部 reviewer 调度，降级为本地 checklist；必须报告阻断来源、原计划 provider、实际路径和未启动的 reviewer。

## Gate Checklist

| dimension | pass condition |
| --- | --- |
| `project_root` | 唯一锁定包含 `STATE.json` 的真实项目根，或已输出最小追问 |
| `preflight` | 已执行或消费 `story.py preflight` / `where` 结果 |
| `detect_evidence` | 已执行或消费 `workflow detect`；无 tracked 中断时已检查 fallback |
| `runtime_profile` | 当前中文 runtime 与 legacy fallback 已区分 |
| `resume_mode` | 模式来自 `types/resume-type-map.md`，且与用户意图不冲突 |
| `risk_level` | cleanup、clear、fail-task、继续执行等风险已标注 |
| `user_confirmation` | 风险动作已等待用户确认；未确认时只输出方案 |
| `unique_next_entry` | 输出一个唯一入口；无法唯一时输出 blocker |
| `forbidden_actions` | 未默认建议 Git hard reset、未备份删除正文、伪造 workflow state |
| `truth_boundary` | 未替 `3-初稿`、`review/` 或 `context-return` 写 canonical 业务真源 |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 恢复裁决可交付 |
| `pass_with_followups` | 可交付，但有非阻断后续补件 |
| `needs_rework` | 证据链、风险标注或下一入口有阻断问题 |
| `blocked` | 项目根、权限、用户意图、证据冲突或上层策略阻断 |

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: project_root | evidence | runtime | mode | confirmation | safety | output | truth_boundary
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Mandatory Failures

- 无法唯一定位项目根却继续推断断点。
- 没有执行或消费 `workflow detect` 却声称当前中断位置。
- 没有 tracked 中断时跳过 artifact fallback。
- 输出多个并列下一入口。
- 把 `story-query` 套进章节 cleanup。
- `story-review` Step 7 自动替用户裁决。
- cleanup 未 preview 或未确认即执行。
- 默认建议 `git reset --hard`、假定章节 tag、未备份删除正文。
- 把 `resume/` 冒充 `context-return` actualization。

## Local Checklist Fallback

当无法真实启动默认 reviewer 时，主 agent 本地执行以下 checklist：

1. 运行结构 validator。
2. 检查 `SKILL.md` 是否只保留入口、路由、门禁和输出合同。
3. 检查 `references/`、`steps/`、`types/`、`review/` 是否各有单一 owner。
4. 检查输出模板是否包含 Output Contract Alignment。
5. 检查危险动作是否被过滤。
6. 检查 legacy runtime 是否只作为兼容说明出现。
