# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `review/` 的经验层知识库，不是过程日志。
- 每次调用 `review/` 时，应自动预加载本文件，用于预审 / 验收 / 学习桥接的模式判断与常见故障闭环。
- 冲突优先级固定为：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 高风险执行没有 `preflight-verdict.yaml` 就要往下跑 | review gate | 先进入 `preflight-review` | 把 preflight 写成 review 的显式 mode | 高风险执行前存在 verdict 文件 |
| 阶段产物存在就被当作“已通过验收” | acceptance contract | 同时更新对应 `validation-report.md` | 在 review mode 中固定 acceptance carrier | 验收结论能回到 canonical report |
| `2-Global` 仍被误映射到 `3-Detail/validation-report.md` | acceptance carrier sync | 立即把 `2-Global` 独立映射回 `2-Global/validation-report.md` | 将 scope-carrier mapping、council-runtime 与 `team.yaml` gate artifact 收束到同一真源 | `review/`、shared runtime、项目样本都对 `2-Global` 使用同一路径 |
| `review/` 越权修改 stage 业务真源 | satellite boundary | 只写 verdict 与下一入口 | 在 skill 中固定“不代替阶段执行” | review 输出不再改写业务内容 |
| project / stage report 路径写旧 runtime | runtime mapping | 回查 `project-runtime-layout.md` 后改正 carrier | 把 runtime mapping 当 review 的必读真源 | `validation-report.md` 落点与当前 runtime 一致 |
| learning 只停在聊天说明，没有落 `learning-record.md` | learning bridge | 进入 `learning-bridge` mode | 把 learning record 固定为 canonical carrier | 学习沉淀能在项目目录读回 |
| review 只写 report，不同步断点治理摘要 | governance snapshot sync | 同步更新 `governance-state.yaml.review_bridge` 与 `resume_contract` | 在 review contract 固定“carrier 本体 + governance-state 摘要”双写位 | review 结束后 `resume/query` 能读到最新 gate 状态 |
| 父级 `review/` 同时承载 preflight / acceptance / learning 细则，导致边界再次混层 | subtype governance | 将三种 mode 下沉到 `subtypes/` | 父级只保留 mode router，局部合同放到 subtype | review 根合同不再平行复制三套细则 |
| 门下省只给笼统结论，没有 severity、证据包与 findings 次序 | review protocol layer | 引入 `menxia-review-protocol.md`，固定 `severity + dimension + evidence_path + impact + recommended_action + confidence` | 让 `review/` 与各 subtype 的输出顺序统一为 findings -> verdict -> layered trace -> closure | 高风险 verdict 可回链到明确 finding，而不是主观语气 |

## Repair Playbook

1. 先判定是 `preflight-review`、`acceptance-review` 还是 `learning-bridge`。
2. 再锁定 scope 对应的 canonical carrier。
3. 若问题涉及高风险执行，先查 `mission-brief / route-plan / preflight-verdict`。
4. 若问题涉及阶段验收，先查该 scope 的 `validation-report.md`。
5. 先列 findings，再给 verdict；高风险问题不能藏在概述后面。
6. 只有 carrier 锁定后，才给出 verdict 与下一入口。

## Reusable Heuristics

- `review/` 最重要的不是“评价得多漂亮”，而是“把 gate 写回 canonical carrier”。
- 对 `aigc` 来说，review 是门下省桥接层，不是阶段执行层。
- 只要 scope 是阶段级，就应该先写该阶段 runtime 下的 `validation-report.md`，而不是默认写项目根报告。
- `2-Global` 和 `3-Detail` 虽然共享 episode root handoff，但验收 carrier 不应继续共用；前者写 `2-Global/validation-report.md`，后者写 `3-Detail/validation-report.md`。
- 若 review 发现的是治理链缺口，最稳的下一入口通常不是阶段 skill，而是根 `aigc` 或 `resume/`。
- `governance-state.yaml` 只记录 review 摘要和下一入口投影，真正 verdict 仍应回到 `preflight-verdict.yaml`、`validation-report.md`、`learning-record.md`。
- 当 `review` 同时拥有 3 种长期模式时，最稳的演化方向不是继续给父技能加段落，而是提升为 `subtypes/preflight-review / acceptance-review / learning-bridge`。
- 对这个仓库，最有价值的 review 维度通常不是“代码风格”，而是 `canonical source consistency / runtime mapping alignment / audit coverage / doc-runner parity`。
- `python3 scripts/aigc_skill_audit.py --strict` 可以作为证据的一部分，但不能单独替代门下省 verdict；若审计覆盖范围本身存疑，门下省必须先质疑审计器。
