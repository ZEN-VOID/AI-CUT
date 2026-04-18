# Menxia Review Protocol

## Purpose

定义 `aigc/review` 在本仓库中的专业审查协议。

本协议吸收 `code-reviewer` 的核心方法，但按本项目属性做了收束：审查对象不只是代码，还包括 `SKILL.md`、`CONTEXT.md`、shared contracts、registry / routes、runtime mapping、audit scripts 与项目级治理工件。

## Review Dimensions

默认按以下维度组织 review：

| dimension | 关注点 | 典型证据 |
| --- | --- | --- |
| `contract_integrity` | 技能合同、template、runbook、schema 是否自洽 | `SKILL.md`、shared contract、template |
| `canonical_source_consistency` | 是否存在第二真源、旧口径或 sibling 漂移 | `project-runtime-layout.md`、registry、root skill |
| `runtime_mapping_alignment` | 技能树执行层与项目 runtime 落盘层是否对齐 | `projects/aigc/<项目名>/`、shared runtime mapping |
| `audit_coverage` | 审计脚本是否真的覆盖当前 active 合同，而不是只给假绿结论 | `scripts/aigc_skill_audit.py`、validator output |
| `doc_runner_parity` | 文档合同与脚本/validator/runner 是否同步消费同一规则 | `SKILL.md`、脚本、审计器 |
| `governance_carrier_sync` | `preflight / validation / learning / governance-state` 是否同步 | runtime carriers、review outputs |
| `regression_risk` | 当前改动是否会在下一轮迁移中继续回归 | CHANGELOG、CONTEXT、audit guardrail |

## Evidence Pack

门下省默认需要最小证据包：

1. `carrier evidence`
   - 当前 canonical carrier 路径
   - 现有 verdict / report / learning 载体
2. `runtime evidence`
   - `project_state.yaml`
   - `governance-state.yaml`
   - `project-runtime-layout.md`
3. `rule evidence`
   - `SKILL.md`
   - shared contract
   - registry / routes
4. `execution evidence`
   - audit / validator 输出
   - 脚本、目录、落盘产物或 diff

无最小证据包时，门下省不得给高置信度放行结论。

## Findings Schema

每条 finding 至少应包含：

- `severity`: `P0 | P1 | P2 | P3`
- `dimension`
- `summary`
- `evidence_path`
- `impact`
- `recommended_action`
- `confidence`

建议写法：

`[P1][audit_coverage][confidence=0.92] strict audit 在 bootstrap_compat 下只审 parent，导致 active leaf 可能假绿。 evidence: scripts/aigc_skill_audit.py:978-980`

## Severity Ladder

| severity | meaning | default review consequence |
| --- | --- | --- |
| `P0` | 会导致错误放行、错误结案、真源破坏、安全/合规/高风险任务绕门禁 | 默认 `reject` |
| `P1` | 会导致错误路由、错误 carrier、假绿审计、关键阶段失真 | 默认 `revise` |
| `P2` | 当前不一定立即失败，但会持续制造噪音、回归或维护成本 | 可 `revise` 或带条件 `pass` |
| `P3` | 低风险清晰度或维护性改进 | 可 `pass` 并记录改进项 |

## Verdict Mapping

- `reject`
  - 任一未缓释 `P0`
  - 或证据包严重不足，无法判断是否可执行
- `revise`
  - 无 `P0`，但存在未缓释 `P1`
  - 或关键 carrier / runtime / audit 三者仍不一致
- `pass`
  - 无 `P0/P1`
  - 且关键证据完整
  - 且下一入口明确

## Project-Specific Hard Guards

- 不把阶段业务真源修改权拿给 `review/`
- 不把 shared layout、registry、审计脚本三者的分歧当成“只是文档问题”
- 不把 audit 全绿当作唯一放行证据
- 不把 `governance-state.yaml` 当成 verdict 本体

## Output Ordering

门下省默认输出顺序：

1. findings
2. verdict / blocker / approved scope
3. layered trace
4. closure triad
5. next entry
