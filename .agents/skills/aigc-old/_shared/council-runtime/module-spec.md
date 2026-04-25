# Council Runtime 共享运行时规范

## Module Identity

- `module_type`: `shared-runtime`
- `activation_signal`: 项目根存在 `projects/aigc/<项目名>/team.yaml` 且 `enabled == true`
- `primary_consumers`: `2-Global`、`3-Detail`、`4-Design`、`5-Image`、`6-Video` 及其可直达子技能

## Scope

本模块只负责跨阶段共享的顾问团运行时：

- 读取并解释项目根 `team.yaml`
- 保留 `0-Init` 写入的 `init_contract.*` 与 `planning.init_execution.*` 初始化 provenance
- 判断当前阶段是否启用智能顾问团模式
- 决定当前阶段先调用 `监制` 还是 `评审`
- 对 `2-Global / 3-Detail / 4-Design`，只定义 `监制` 的前置 advisory；首次落盘后的收尾归阶段审计/验收层，不在本模块内定义
- 规定 `评审` 只在 `5-Image / 6-Video` 的阶段级 `validation-report.md` 前后介入
- 约束 subagents 只是参谋，不夺取 canonical 写回权

本模块不负责：

- 重新定义 `2-Global / 3-Detail / 4-Design / 5-Image / 6-Video` 的阶段内容合同
- 直接产出阶段 canonical
- 取代 `0-Init` 生成 `team.yaml`

## Canonical Sources

- 项目级团队真源：`projects/aigc/<项目名>/team.yaml`
- 共享模板真源：`.agents/skills/aigc/_shared/council-runtime/team.template.yaml`

## Stage Role Routing

| 当前阶段 | 默认前置顾问角色 | 后置收口时机 | canonical 写回权 |
| --- | --- | --- | --- |
| `2-Global` | `监制` | 落盘后的收尾由阶段审计/验收层定义；本模块不再定义 `监制 refine` | 主代理 |
| `3-Detail` | `监制` | 落盘后的收尾由阶段审计/验收层定义；本模块不再定义 `监制 refine` | 主代理 |
| `4-Design` | `监制` | 落盘后的收尾由阶段审计/验收层定义；本模块不再定义 `监制 refine` | 主代理 |
| `5-Image` | `评审` | `projects/aigc/<项目名>/5-Image/validation-report.md` 前后 | 主代理 |
| `6-Video` | `评审` | `projects/aigc/<项目名>/6-Video/validation-report.md` 前后 | 主代理 |

## Runtime Decision Contract

1. 进入阶段根技能或其可直达子技能时，先读取 `projects/aigc/<项目名>/team.yaml`。
2. 若文件不存在、`enabled != true`、或所有角色成员都为空，走普通路径。
3. `init_contract.*` 与 `roles.planning.init_execution.*` 主要由 `0-Init` 消费；后续阶段只把它们视为 provenance，不重写其初始化裁决。
4. 若 `enabled == true` 但当前阶段默认角色成员为空，则跳过前置顾问，仅保留已配置的 `评审` 闸门。
5. 若启用且当前阶段默认角色成员非空：
   - `2-Global / 3-Detail / 4-Design` 先调用 `roles.supervision.members`
   - `5-Image / 6-Video` 先调用 `roles.review.members`
6. 对 `2-Global / 3-Detail / 4-Design`，主代理先整合前置顾问意见，再产出本轮阶段草案与 canonical 首次写回。
7. `2-Global / 3-Detail / 4-Design` 首次写回后的审计、验收与收尾 patch，回到各阶段自己的 `validation-report` / audit 合同；不得再由 `roles.supervision` 在本模块内发起 post-write refine。
8. `roles.supervision.source_skill_refs` 在 `2-Global / 3-Detail / 4-Design` 中只可作为领域提示，不得被升级为落盘后收尾 reviewer。
9. 在 `5-Image / 6-Video` 的阶段级 `validation-report.md` 写作前后，若 `roles.review.members` 非空，则调用 `评审` 给出 PASS/返工意见。
10. 无论顾问是否启用，主代理都保留最终 canonical 写回权。
11. `0-Init` 若读取到 `runtime_policy.require_subagents_for_init_execution == true`，则其 planning 固定题包直答不得使用本条普通降级路径；后续阶段才允许按本模块的普通 fallback 规则处理。

## Subagent Contract

### 阶段顾问

- `监制` 负责 `2-Global / 3-Detail / 4-Design` 的前置 advisory。
- `2-Global / 3-Detail / 4-Design` 首次落盘后的收尾 refine 不再属于 `监制`，而归阶段审计/验收层。
- `评审` 负责 `5-Image / 6-Video` 的收口与 validation gate。
- 他们不能直接落盘 canonical。
- 主代理必须把其建议整理为：
  - `共识`
  - `关键分歧`
  - `建议采用方案`
  - `少数派高价值提醒`

### 评审顾问

- `评审` 只对 `5-Image / 6-Video` 的阶段终稿与阶段级 `validation-report.md` 负责。
- `评审` 默认不参与前置发散创作。
- `评审` 产出应收敛为：
  - `PASS / FAIL`
  - `返工关注点`
  - `高风险遗漏`

## Verification Checklist

1. 当前阶段进入前，已读取项目根 `team.yaml`。
2. `enabled == false` 或无成员时，没有误触发顾问团。
3. `2-Global / 3-Detail / 4-Design` 命中的是 `监制`，`5-Image / 6-Video` 命中的是 `评审`。
4. `2-Global / 3-Detail / 4-Design` 的 output-related canonical 首次落盘后，不再由本模块触发 `roles.supervision` refine。
5. `roles.supervision.source_skill_refs` 若不是 team reviewer skill，只被当作领域提示，不会被升级为落盘后收尾 reviewer。
6. `评审` 只在 `5-Image / 6-Video` 的阶段级 `validation-report.md` 前后介入。
7. 主代理保留最终 canonical 写回权。
