# Resume Review Gate

本文件定义 `$aigc-resume` 的交付前质量门禁、verdict 模型与 reviewer/provider 降级口径。

## Default Provider

- 默认辅助 provider：`code-reviewer`
- 用途：检查 Skill 2.0 结构、恢复证据链、安全边界、runtime 口径和输出模板。
- 若上层策略阻断真实 subagent 或外部 reviewer 调度，降级为本地 checklist；必须报告阻断来源、原计划 provider、实际路径和未启动的 reviewer。

## Gate Checklist

| dimension | pass condition |
| --- | --- |
| `project_root` | 唯一锁定 `projects/aigc/<项目名>/`，或已输出最小追问 |
| `evidence_chain` | 至少列明 `STATE.json` / `governance-state.yaml` / 初始化工件 / 阶段产物中的实际证据 |
| `runtime_profile` | 当前中文 runtime 与 legacy 输入兼容已区分 |
| `resume_mode` | 模式来自 `types/resume-type-map.md`，且与用户意图不冲突 |
| `risk_level` | 高风险和 destructive 请求已标注 |
| `governance_gate` | 需要 preflight / validation / review 时未跳过 |
| `unique_next_entry` | 输出一个唯一入口；无法唯一时输出 blocker |
| `forbidden_actions` | 未默认建议 Git hard reset、删除源文本或清空资产 |
| `truth_boundary` | 未替阶段技能生成 canonical 业务真稿 |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 恢复裁决可交付 |
| `pass_with_followups` | 可交付，但有非阻断后续补件 |
| `needs_rework` | 证据链、模式或下一入口有阻断问题 |
| `blocked` | 项目根、权限、用户意图或上层策略阻断 |

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: project_root | evidence | runtime | mode | gate | safety | output
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Mandatory Failures

- 无法唯一定位项目根却继续推断断点。
- 输出多个并列下一入口。
- 把空阶段目录当成阶段完成证据。
- 高风险续跑缺 gate 仍建议直接执行。
- 将旧英文 runtime 输出为新版默认下一入口。
- 默认建议 destructive Git 或资产删除动作。
- 把 rebootstrap 明确请求判为普通 resume。

## Local Checklist Fallback

当无法真实启动默认 reviewer 时，主 agent 本地执行以下 checklist：

1. 运行结构 validator。
2. 检查 `SKILL.md` 是否只保留入口、路由和输出合同。
3. 检查 `references/`、`steps/`、`types/`、`review/` 是否各有单一 owner。
4. 检查输出模板是否包含 Output Contract Alignment。
5. 检查 legacy runtime 是否只作为兼容输入出现。
