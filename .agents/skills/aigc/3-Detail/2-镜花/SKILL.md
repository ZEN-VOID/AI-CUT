---
name: aigc-detail-jinghua
description: Use when `3-Detail` needs a stage-local parent skill to orchestrate `分镜构图 / 摄影美学 / 运镜手法 / 转场特效` as independent branch skills, write their branch process sidecars, and assemble `projects/aigc/<项目名>/3-Detail/镜花/第N集.field-patch.json` without语义压缩式聚合.
governance_tier: full
---

# 3-Detail / 2-镜花

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 必须回读父层 `3-Detail/SKILL.md`、`_shared/branch-output-contract.md`、`_shared/branch-review-contract.md`。

## 概述

`2-镜花` 不再把多个镜头分支先挤成 `shot_patches[]` 的统一导演 prose。

新的 canonical 路线是：

1. `1-分镜构图` 先执行，锁定 `分镜构图`
2. `2-摄影美学 -> 3-运镜手法 -> 4-转场特效` 在已锁定的 `分镜构图` 上按当前序号继续串行
3. 四个 branch 各自输出：
   - `思维·执行 sidecar`
   - `branch-owned json patch`
4. `2-镜花` 父层只做：
   - 前置门检查
   - branch review gate
   - serial progressive commit
   - compatibility projection（可选）

## Parent Positioning

### `镜花` 父层拥有

- `分镜构图 -> 摄影美学 -> 运镜手法 -> 转场特效` 的顺序门
- branch sidecar 完整性校验
- owner bundle 写回
- branch review 汇总

### `镜花` 父层不拥有

- 在 bundle 阶段重新发明镜头语法
- 把 branch 结果压成一条统一 `分镜表现`
- 越权改动 `角色表现 / 运动表现 / 氛围表现 / 视觉强化`

## Governed Child Skills

1. `1-分镜构图`
2. `2-摄影美学`
3. `3-运镜手法`
4. `4-转场特效`

branch-owned canonical 字段：

- `分镜构图`
- `摄影美学`
- `运镜手法`
- `转场特效`

## Canonical Sources

- `3-Detail/SKILL.md`
- `3-Detail/_shared/branch-output-contract.md`
- `3-Detail/_shared/branch-review-contract.md`
- `.agents/skills/aigc/3-Detail/_shared/node-pack-contract.md`
- `.agents/skills/aigc/3-Detail/_shared/creative-guidance-contract.md`
- `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- `module-index.md`
- `route-profile.yaml`
- `examples.md`
- `creative-review-rubric.md`
- `1-分镜构图/SKILL.md`
- `2-摄影美学/SKILL.md`
- `3-运镜手法/SKILL.md`
- `4-转场特效/SKILL.md`

## Context Preload

1. 根 `AGENTS.md`
2. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
3. `.agents/skills/aigc/3-Detail/SKILL.md + CONTEXT.md`
4. 本 `SKILL.md + CONTEXT.md`
5. `_shared/branch-output-contract.md`
6. `_shared/branch-review-contract.md`
7. `.agents/skills/aigc/_shared/director_episode_output.schema.json`
8. `projects/aigc/<项目名>/3-Detail/第N集.json`
9. `projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json`
10. `module-index.md`
11. `route-profile.yaml`
12. `examples.md`
13. `creative-review-rubric.md`
14. `1-分镜构图/SKILL.md + CONTEXT.md`
15. `2-摄影美学/SKILL.md + CONTEXT.md`
16. `3-运镜手法/SKILL.md + CONTEXT.md`
17. `4-转场特效/SKILL.md + CONTEXT.md`

## Input Contract

### 必需输入

- `projects/aigc/<项目名>/3-Detail/第N集.json`
- `projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json`

### 硬规则

1. 四个 branch 固定按当前序号 `1 -> 2 -> 3 -> 4` 串行执行。
2. 每个 branch 开始前，必须重新读取当前 `projects/aigc/<项目名>/3-Detail/第N集.json`，把前序已写回字段当作上下文。
3. 后三支必须依附当前 root 中已存在的 `分镜构图`，不得反向改镜数或重判事实。
4. progressive commit 只允许写 `镜花` owner 字段，不做统一导演 prose。

## Output Contract

### branch process sidecar

- `projects/aigc/<项目名>/3-Detail/镜花/分镜构图/第N集.branch-patch.json`
- `projects/aigc/<项目名>/3-Detail/镜花/摄影美学/第N集.branch-patch.json`
- `projects/aigc/<项目名>/3-Detail/镜花/运镜手法/第N集.branch-patch.json`
- `projects/aigc/<项目名>/3-Detail/镜花/转场特效/第N集.branch-patch.json`

### owner bundle

- `projects/aigc/<项目名>/3-Detail/镜花/第N集.field-patch.json`

bundle 最低要求：

- `metadata.schema_version = aigc/detail-branch-bundle-sidecar/v1`
- `metadata.patch_owner = 镜花`
- `metadata.bundle_mode = assembly_only`
- `branch_sidecars[]`
- `group_patches[].branch_patches`

### compatibility projection

允许保留：

- `shot_patches[]`

但它是 projection，不是 canonical 真相。

## Review Contract

1. `分镜构图` 先 review 并先写回当前 root。
2. `2-摄影美学 -> 3-运镜手法 -> 4-转场特效` 只能在读取了当前 root 的 `分镜构图` 后继续。
3. 每个 branch review 通过后，先 progressive commit 到 root，再进入下一序号。
4. team review 默认先看 branch sidecar，再看 owner bundle。
5. 若 stage 只看 `shot_patches[]` 而不看 branch-owned field，视为评审输入降级。

## Thinking-Action Network

| node_id | 对应 Step | 聚焦字段 | objective | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `N1-INPUT-LOCK` | `S1` | `FIELD-JH-01` | 锁定 root 与 factual 前置 | 读取 root 与 `水月` bundle | `input_lock_note` | -> `N2` | 前置存在 |
| `N2-COMPOSITION-FIRST` | `S2` | `FIELD-JH-02` | 先完成 `分镜构图` branch | 回读当前 root，执行/复用 `1-分镜构图` | `composition_branch` | -> `N3` | 构图稳定 |
| `N3-SERIAL-BRANCHES` | `S3` | `FIELD-JH-03~05` | 在构图稳定后按序号逐个执行后三支 | 每次先回读当前 root，再执行/复用 `摄影 -> 运镜 -> 转场` | `branch_sidecars` | -> `N4` | 不得越权 |
| `N4-BRANCH-REVIEW` | `S4` | `FIELD-JH-06` | branch 粒度 review | 汇总 findings 并回流 | `branch_review_note` | -> `N5` | 当前 branch 未过审不得进入下一序号 |
| `N5-SERIAL-COMMIT` | `S5` | `FIELD-JH-07` | 每个 branch 过审后先 progressive commit 到 root | 写当前批准字段并刷新 root，再更新 bundle | `bundle_note` | -> `N6` | root 已刷新后才可继续 |
| `N6-VALIDATE` | `S6` | `FIELD-JH-08` | 校验 bundle 与 branch sidecar | 执行 validator | `validation_verdict` | pass -> done | 校验通过 |

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| `FIELD-JH-01` | 输入锁定 | root 与 `水月` 前置稳定 | `S1` | 前置完整性 | `FAIL-JH-01` |
| `FIELD-JH-02` | `分镜构图` | 构图 branch 先行 | `S2` | 顺序门 | `FAIL-JH-02` |
| `FIELD-JH-03` | `摄影美学` | 仅摄影 branch 命中 | `S3` | ownership | `FAIL-JH-03` |
| `FIELD-JH-04` | `运镜手法` | 仅运镜 branch 命中 | `S3` | ownership | `FAIL-JH-04` |
| `FIELD-JH-05` | `转场特效` | 仅转场 branch 命中 | `S3` | ownership | `FAIL-JH-05` |
| `FIELD-JH-06` | branch review | findings 已回流 | `S4` | review 完整度 | `FAIL-JH-06` |
| `FIELD-JH-07` | owner bundle + 当前 root | 只做 serial commit | `S5` | 抗压缩性与连续性 | `FAIL-JH-07` |
| `FIELD-JH-08` | 最终 bundle | validator 通过 | `S6` | 可交付性 | `FAIL-JH-08` |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `S1` | `FIELD-JH-01` | 当前 root 与 factual 前置是否可用 | 锁定输入 | 没有 `水月` 前置 |
| `S2` | `FIELD-JH-02` | `分镜构图` 是否先锁稳并已写回当前 root | 运行构图 branch | 先跑后三支或未刷新 root |
| `S3` | `FIELD-JH-03~05` | 后三支是否先读了当前 root 再做增量 patch | 读取/生成 branch sidecar | 越权改骨架或仍按旧快照执行 |
| `S4` | `FIELD-JH-06` | review 是否发生在未压缩前 | 做 branch review | 只审 bundle |
| `S5` | `FIELD-JH-07` | owner bundle 与当前 root 是否只是 serial commit | 写 bundle / root | 再次 prose 聚合或未刷新 root |
| `S6` | `FIELD-JH-08` | 是否可交付 | 跑 validator | schema 失败 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| `FIELD-JH-01` | 输入稳定 | `FAIL-JH-01` | `S1` |
| `FIELD-JH-02` | 构图 branch 先行且已写回当前 root | `FAIL-JH-02` | `S2` |
| `FIELD-JH-03~05` | 后三支不越权，且已读取当前 root | `FAIL-JH-03/04/05` | `S3` |
| `FIELD-JH-06` | branch review 完成 | `FAIL-JH-06` | `S4` |
| `FIELD-JH-07` | bundle 为 `assembly_only` | `FAIL-JH-07` | `S5` |
| `FIELD-JH-08` | 校验通过 | `FAIL-JH-08` | `S6` |

## Root-Cause Execution Contract

出现以下任一情况，必须先修源层：

- 后三支跳过 `分镜构图`
- 按当前序号应串行的 branch 仍被并发处理
- 下一序号 branch 没有读取前序已写回的当前 root
- bundle 开始替 branch 写统一镜头语言
- compatibility projection 反向盖过 `分镜构图 / 摄影美学 / 运镜手法 / 转场特效`

## Completion Contract

只有同时满足以下条件，`2-镜花` 才允许宣布完成：

1. 四个 branch process sidecar 已存在。
2. `镜花/第N集.field-patch.json` 已写回。
3. `bundle_mode == assembly_only`。
4. validator 通过。
