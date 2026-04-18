---
name: aigc-detail-watermoon
description: Use when `3-Detail` needs a stage-local parent skill to orchestrate `角色表现 / 运动表现 / 氛围表现 / 视觉强化` as independent branch skills, write their branch process sidecars, and assemble `projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json` without语义压缩式聚合.
governance_tier: full
---

# 3-Detail / 1-水月

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 必须回读父层 `3-Detail/SKILL.md`、`_shared/branch-output-contract.md`、`_shared/branch-review-contract.md`。
- 冲突优先级：用户显式请求 > `AGENTS.md` / 根技能 > 本 `SKILL.md` > 本 `CONTEXT.md`。

## 概述

`1-水月` 不再把四条主链先压成 `beat_patches[]` 的语义合稿，再交给父层继续压缩。

新的 canonical 路线是：

1. 四个 branch skill 按当前序号串行创作：
   - `1-角色表现`
   - `2-运动表现`
   - `3-氛围表现`
   - `4-视觉强化`
2. 每个 branch 各自输出：
   - `思维·执行 sidecar`
   - `branch-owned json patch`
3. `1-水月` 父层只做：
   - scope lock
   - branch dispatch
   - branch review gate
   - serial progressive commit
   - compatibility projection（可选）

## Parent Positioning

### `水月` 父层拥有

- branch 串行调度与 progressive commit 裁决
- branch output 完整性校验
- `projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json` bundle 落盘
- branch review 汇总与回流
- legacy compatibility projection 的生成与阻塞

### `水月` 父层不拥有

- 替 `角色表现 / 运动表现 / 氛围表现 / 视觉强化` 重写创作结论
- 把 branch 结果压成一条短促 `品味` 才算完成
- 越权写 `分镜构图 / 摄影美学 / 运镜手法 / 转场特效`

## Governed Child Skills

1. `1-角色表现`
2. `2-运动表现`
3. `3-氛围表现`
4. `4-视觉强化`

branch-owned canonical 字段：

- `角色表现`
- `运动表现`
- `氛围表现`
- `视觉强化`

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
- `1-角色表现/SKILL.md`
- `2-运动表现/SKILL.md`
- `3-氛围表现/SKILL.md`
- `4-视觉强化/SKILL.md`

## Context Preload

1. 根 `AGENTS.md`
2. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
3. `.agents/skills/aigc/3-Detail/SKILL.md + CONTEXT.md`
4. 本 `SKILL.md + CONTEXT.md`
5. `_shared/branch-output-contract.md`
6. `_shared/branch-review-contract.md`
7. `.agents/skills/aigc/_shared/director_episode_output.schema.json`
8. `projects/aigc/<项目名>/3-Detail/第N集.json`
9. `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md`（若存在）
10. `module-index.md`
11. `route-profile.yaml`
12. `examples.md`
13. `creative-review-rubric.md`
14. `1-角色表现/SKILL.md + CONTEXT.md`
15. `2-运动表现/SKILL.md + CONTEXT.md`
16. `3-氛围表现/SKILL.md + CONTEXT.md`
17. `4-视觉强化/SKILL.md + CONTEXT.md`

## Input Contract

### 必需输入

- `projects/aigc/<项目名>/3-Detail/第N集.json`

### 可选输入

- `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md`
- 已存在的 branch process sidecar
- 已存在的 `水月/第N集.field-patch.json`

### 硬规则

1. `剧本正文` 只读继承。
2. 四个 branch 固定按当前序号 `1 -> 2 -> 3 -> 4` 串行执行。
3. 每个 branch 开始前，必须重新读取当前 `projects/aigc/<项目名>/3-Detail/第N集.json`，把前序已写回字段当作上下文。
4. branch process sidecar 缺失时，不得直接伪造 bundle。
5. progressive commit 只允许写 `水月` owner 字段，不做 prose 改写。

## Output Contract

### branch process sidecar

- `projects/aigc/<项目名>/3-Detail/水月/角色表现/第N集.branch-patch.json`
- `projects/aigc/<项目名>/3-Detail/水月/运动表现/第N集.branch-patch.json`
- `projects/aigc/<项目名>/3-Detail/水月/氛围表现/第N集.branch-patch.json`
- `projects/aigc/<项目名>/3-Detail/水月/视觉强化/第N集.branch-patch.json`

### owner bundle

- `projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json`

bundle 最低要求：

- `metadata.schema_version = aigc/detail-branch-bundle-sidecar/v1`
- `metadata.patch_owner = 水月`
- `metadata.bundle_mode = assembly_only`
- `branch_sidecars[]`
- `group_patches[].branch_patches`

### compatibility projection

允许保留：

- `group_design_patch.出场角色及穿搭`
- `compatibility_projection.角色背景面`
- `compatibility_projection.角色站位走位`
- `compatibility_projection.道具及状态`
- `compatibility_projection.分镜表现`

但它们是 projection，不是 canonical 真相。

## Review Contract

1. branch 按当前序号逐个 review。
2. review findings 先回流对应 branch。
3. 每个 branch review 通过后，先 progressive commit 到当前 root，再进入下一序号。
4. 只有四个 branch 都 `reviewed` 且都已 commit，bundle 才允许进入完整 `assembly_only` 收束。
5. 若 team 只看 owner bundle 而未读取 branch sidecar，视为评审输入降级。

## Thinking-Action Network

| node_id | 对应 Step | 聚焦字段 | objective | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `N1-INPUT-LOCK` | `S1` | `FIELD-WM-01` | 锁定唯一 episode/group scope | 读取 root 与选中 scope | `input_lock_note` | -> `N2` | scope 唯一 |
| `N2-BRANCH-DISPATCH` | `S2` | `FIELD-WM-02` | 锁定按序号串行的执行包 | 生成 `1 -> 2 -> 3 -> 4` run list | `dispatch_note` | -> `N3` | branch ownership 明确 |
| `N3-BRANCH-RUN` | `S3` | `FIELD-WM-03~06` | 按序号逐个获取 branch process sidecar | 每次先回读当前 root，再执行/复用 branch skill | `branch_sidecars` | -> `N4` | 每个 branch 只命中自己的 target path |
| `N4-BRANCH-REVIEW` | `S4` | `FIELD-WM-07` | 先在 branch 粒度完成 review | 汇总 findings，必要时回流 branch | `branch_review_note` | -> `N5` | 当前 branch 未过审不得进入下一序号 |
| `N5-SERIAL-COMMIT` | `S5` | `FIELD-WM-08` | 每个 branch 过审后先 progressive commit 到 root | 写当前批准字段并刷新 root，再更新 bundle | `bundle_note` | -> `N6` | root 已刷新后才可继续 |
| `N6-VALIDATE` | `S6` | `FIELD-WM-09` | 校验 bundle 与 branch sidecar | 执行 validator | `validation_verdict` | pass -> done | 校验通过 |

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| `FIELD-WM-01` | 输入锁定 | root 与 scope 唯一 | `S1` | 真源稳定性 | `FAIL-WM-01` |
| `FIELD-WM-02` | branch 调度 | 四个 branch 串行次序明确 | `S2` | 调度清晰度 | `FAIL-WM-02` |
| `FIELD-WM-03` | `角色表现` | 仅角色表现 owner 命中 | `S3` | ownership | `FAIL-WM-03` |
| `FIELD-WM-04` | `运动表现` | 仅运动表现 owner 命中 | `S3` | ownership | `FAIL-WM-04` |
| `FIELD-WM-05` | `氛围表现` | 仅氛围表现 owner 命中 | `S3` | ownership | `FAIL-WM-05` |
| `FIELD-WM-06` | `视觉强化` | 仅视觉强化 owner 命中 | `S3` | ownership | `FAIL-WM-06` |
| `FIELD-WM-07` | branch review | findings 已回流到各 branch | `S4` | review 完整度 | `FAIL-WM-07` |
| `FIELD-WM-08` | owner bundle + 当前 root | 只做 serial commit，不做语义压缩 | `S5` | 抗压缩性与连续性 | `FAIL-WM-08` |
| `FIELD-WM-09` | 最终 bundle | validator 通过 | `S6` | 可交付性 | `FAIL-WM-09` |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `S1` | `FIELD-WM-01` | 本轮到底补哪一集、哪几个 group | 锁定 root 与 scope | 输入混用 |
| `S2` | `FIELD-WM-02` | 四个 branch 按什么顺序跑 | 生成串行 dispatch | branch ownership 不清或顺序不明 |
| `S3` | `FIELD-WM-03~06` | 当前 branch 是否先读了最新 root 再写自己的字段 | 读取当前 root 并生成 branch sidecar | 仍按旧快照执行或发生越权 |
| `S4` | `FIELD-WM-07` | review 是否发生在未压缩前 | 做 branch review | 只审 bundle 不审 branch |
| `S5` | `FIELD-WM-08` | 当前 branch 过审后是否先 commit 到 root | 写当前字段并刷新 bundle/root | 又开始 prose 聚合或未刷新 root |
| `S6` | `FIELD-WM-09` | bundle 是否可交付 | 跑 validator | schema 或 ownership 失败 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| `FIELD-WM-01` | root 与 scope 唯一 | `FAIL-WM-01` | `S1` |
| `FIELD-WM-02` | branch 串行调度包清楚 | `FAIL-WM-02` | `S2` |
| `FIELD-WM-03~06` | branch 不越权 | `FAIL-WM-03/04/05/06` | `S3` |
| `FIELD-WM-07` | branch review 完成 | `FAIL-WM-07` | `S4` |
| `FIELD-WM-08` | progressive commit 顺序正确，且 bundle 为 `assembly_only` | `FAIL-WM-08` | `S5` |
| `FIELD-WM-09` | 校验通过 | `FAIL-WM-09` | `S6` |

## Root-Cause Execution Contract

出现以下任一情况，必须先修源层：

- bundle 开始替 branch 重写语义
- branch 被并发执行而非按当前序号串行
- 下一序号 branch 没有读取前序已写回的当前 root
- 评审只看 bundle，不看 branch sidecar
- compatibility projection 反向覆盖 canonical branch-owned field

## Completion Contract

只有同时满足以下条件，`1-水月` 才允许宣布完成：

1. 四个 branch process sidecar 已存在。
2. `水月/第N集.field-patch.json` 已写回。
3. `bundle_mode == assembly_only`。
4. validator 通过。
