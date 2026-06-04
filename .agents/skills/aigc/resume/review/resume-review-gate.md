# Resume Review Gate

本文件定义 `$aigc-resume` 的交付前质量门禁、verdict 模型与 reviewer/provider / 本地 checklist 口径。

## Default Provider

- 默认辅助 provider：`code-reviewer`
- 用途：检查 Skill 2.0 结构、恢复证据链、安全边界、runtime 口径和输出模板。
- 若外部 reviewer provider 不可用，直接使用本地 checklist。

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

## Review Gates

| review_gate | pass condition | fail_code | default_rework_target |
| --- | --- | --- | --- |
| `GATE-RESUME-PROJECT-ROOT` | 项目根按 canonical 顺序唯一锁定，未把仓库根、`projects/` 或多候选目录当作项目根 | `FAIL-RESUME-PROJECT-ROOT` | `N1-INTAKE` |
| `GATE-RESUME-EVIDENCE-CHAIN` | 恢复裁决至少由状态真源与真实工件交叉验证，未用空目录、mtime 或聊天记忆单独判定断点 | `FAIL-RESUME-EVIDENCE` | `N2-TRUTH-LOCK` |
| `GATE-RESUME-RUNTIME-PROFILE` | 当前中文 runtime、transition 路径与 legacy 英文路径已明确分层，输出不把 legacy 路径当新版默认入口 | `FAIL-RESUME-RUNTIME` | `N2-TRUTH-LOCK` |
| `GATE-RESUME-MODE-INTENT` | `resume_mode` 来自类型矩阵并与用户意图一致，rebootstrap/query/review/stage 请求未被误并入普通 resume | `FAIL-RESUME-MODE` | `N3-TYPE` |
| `GATE-RESUME-GOVERNANCE-GATE` | 高风险续跑、validation failure、review bridge 或 required repairs 均回到正确 gate owner，未跳过 preflight/review/repair | `FAIL-RESUME-GOVERNANCE-GATE` | `N5-GATE` |
| `GATE-RESUME-UNIQUE-NEXT` | 输出一个唯一下一入口；无法唯一时输出 blocker 与最小补充信息 | `FAIL-RESUME-MULTI-ENTRY` | `N4-PLAN` |
| `GATE-RESUME-FORBIDDEN-ACTIONS` | 未默认建议或执行 destructive Git、源文本删除、资产清空或未授权覆盖 | `FAIL-RESUME-FORBIDDEN-ACTION` | `N5-GATE` |
| `GATE-RESUME-TRUTH-BOUNDARY` | resume 只做恢复裁决和回接，不生成阶段业务真稿，不替 query/review/0-初始化拥有真源 | `FAIL-RESUME-TRUTH-BOUNDARY` | `N4-PLAN` |
| `GATE-RESUME-MIGRATION-COVERAGE` | 旧 resume 包的入口、加载、边界、证据链、类型、review、metadata 与搁浅阶段语义均有迁移落点、风险和验证项 | `FAIL-RESUME-MIGRATION-COVERAGE` | `N2-TRUTH-LOCK` |
| `GATE-RESUME-MIGRATION-NONLOSS` | 旧包“不伪造状态”“rebootstrap 不属于 resume”“legacy 只作输入”等意图未在新版中丢失或反向覆盖当前真源 | `FAIL-RESUME-MIGRATION-LOSS` | `N3-TYPE` |
| `GATE-RESUME-LEGACY-SHELVED` | `7-Cut`、旧英文阶段和 transition `4-设计` 只进入 reroute/block/迁移确认，不被直接续跑 | `FAIL-RESUME-LEGACY-STAGE` | `N4-PLAN` |
| `GATE-RESUME-REPORT-EVIDENCE` | closeout 报告包含项目根、证据、模式、风险、blockers/repairs、唯一入口与 gate verdict，可复核本次裁决 | `FAIL-RESUME-REPORT` | `N6-CLOSE` |

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

当无法外部执行默认 reviewer 时，主 agent 本地执行以下 checklist：

1. 运行结构 validator。
2. 检查 `SKILL.md` 是否只保留入口、路由和输出合同。
3. 检查 `SKILL.md` 主节点、`references/`、`types/`、`review/` 是否各有单一 owner。
4. 检查输出模板是否包含 Output Contract Alignment。
5. 检查 legacy runtime 是否只作为兼容输入出现。
