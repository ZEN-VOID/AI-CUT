---
name: aigc-detail
description: Use when the `3-Detail` stage needs to route `水月` and `镜花`, keep `projects/aigc/<项目名>/3-Detail/第N集.json` as the only business truth, assemble branch-owned patches, and close the stage with validation plus review gates.
governance_tier: full
---

# aigc 3-Detail

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 概述

`3-Detail` 是 `aigc` 技能树承接 `2-Global`、连接 `4-Design / 5-Image / 6-Video` 的阶段父 skill。

当前阶段的 canonical 目标不是“把 `水月 + 镜花` 再语义压缩成一段更顺的 prose”，而是：

1. 保持 `projects/aigc/<项目名>/3-Detail/第N集.json` 为唯一业务真源。
2. 让 `水月 / 镜花` 各自先在 branch 层完成创作、评审与 patch。
3. 父层只做：
   - root 继承与 scope lock
   - owner dispatch
   - branch review / coherence gate
   - serial progressive commit
   - compatibility projection
   - stage validation / report

换句话说：`3-Detail` 现在是 `orchestrator + serial commit gate`，不是创作性聚合器。

## Parent Positioning

### 父层拥有

- `2-Global -> 3-Detail` root 继承与缺口诊断
- `水月 -> 镜花` 的顺序门
- `watermoon / jinghua` owner bundle 读取与校验
- branch-owned 字段按 owner scope 串行写回 shared root
- branch-aware team review 与组级 coherence 审核
- legacy compatibility projection 的生成与阻塞
- `metadata.document_phase` 推进与 `validation-report.md` 写回

### 父层不拥有

- 重写 `剧本正文`
- 重新裁决 `分镜切换`
- 在 assembly 阶段把 branch 结论压成一条统一 prose
- 把旧兼容字段当作新的 canonical 真相
- 越权让父层直接代写 branch owner 字段

## Internal Capability Fusion Contract (Mandatory)

`3-Detail` 的阶段总线统一分布在父 skill、两个 owner parent、八个 branch child 与 shared contracts：

| 能力面 | 当前 owner | 说明 |
| --- | --- | --- |
| root lock / seed check / stage close | `3-Detail/SKILL.md` | 锁 root、裁决阶段门、写回 stage report |
| `角色表现 / 运动表现 / 氛围表现 / 视觉强化` | `1-水月/SKILL.md` | 负责 performer-facing 与 scene-facing 前置真相 |
| `分镜构图 / 摄影美学 / 运镜手法 / 转场特效` | `2-镜花/SKILL.md` | 负责 cinematic-facing 真相 |
| branch process sidecar 形状 | `_shared/branch-output-contract.md` + schema | 约束 branch 输出与 owner bundle |
| branch-aware review / coherence gate | `_shared/branch-review-contract.md` + `team.yaml` | 约束先审 branch 再审整体 |
| 下游消费优先级 | `4-Design` shared contract + `5-Image/6-Video` shared contracts | 约束 branch-owned first, legacy fallback |

硬规则：

1. `3-Detail` 不再把 `水月 + 镜花` 聚成统一导演 prose。
2. parent 只做 serial progressive commit，不替 branch 重写结论。
3. `1-水月 -> 2-镜花` 固定串行；每个 owner parent 内部也按当前序号串行。
4. 若共享结构需要更新，先改 shared contract / schema，再改 parent/child 载体。

## Governed Child Skills

### Stage-local parents

1. `1-水月`
2. `2-镜花`

### Branch-owned canonical 字段

| owner_parent | branch_skill | canonical_field | 作用 |
| --- | --- | --- | --- |
| `1-水月` | `1-角色表现` | `角色表现` | `动作戏 / 对话戏 / 内心戏` |
| `1-水月` | `2-运动表现` | `运动表现` | `逻辑性 / 位置和方向 / 一致性` |
| `1-水月` | `3-氛围表现` | `氛围表现` | `层次 / 空间诗学 / 意境` |
| `1-水月` | `4-视觉强化` | `视觉强化` | `冲击力 / 观赏性 / 品味` |
| `2-镜花` | `1-分镜构图` | `分镜构图` | `景别景深 / 镜头类型 / 构图形式` |
| `2-镜花` | `2-摄影美学` | `摄影美学` | `光影 / 色彩 / 质感` |
| `2-镜花` | `3-运镜手法` | `运镜手法` | `变化 / 速度 / 组合` |
| `2-镜花` | `4-转场特效` | `转场特效` | 仅在需要显式转场/特效时填写 |

## Shared Canonical Sources (Mandatory)

- `.agents/skills/aigc/_shared/project-runtime-layout.md`
- `.agents/skills/aigc/_shared/group_design_seed_contract.md`
- `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- `.agents/skills/aigc/_shared/director_episode_bootstrap.template.json`
- `.agents/skills/aigc/3-Detail/_shared/branch-output-contract.md`
- `.agents/skills/aigc/3-Detail/_shared/branch-review-contract.md`
- `.agents/skills/aigc/3-Detail/_shared/node-pack-contract.md`
- `.agents/skills/aigc/3-Detail/_shared/creative-guidance-contract.md`
- `.agents/skills/aigc/4-Design/1-清单/_shared/detail-output-consumption-contract.md`
- `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md`
- `.agents/skills/aigc/6-Video/_shared/image-to-video-prompt-principles.md`
- `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
- `.agents/skills/aigc/2-Global/SKILL.md`
- `.codex/commands/master-check-team.md`
- `.codex/commands/master-check.md`
- `1-水月/SKILL.md`
- `2-镜花/SKILL.md`

真源分工：

- 本 `SKILL.md`
  - 父层路由、assembly、compatibility projection、stage review、validation
- `1-水月/SKILL.md`
  - `角色表现 / 运动表现 / 氛围表现 / 视觉强化` owner bundle 真源
- `2-镜花/SKILL.md`
  - `分镜构图 / 摄影美学 / 运镜手法 / 转场特效` owner bundle 真源
- `.agents/skills/aigc/_shared/director_episode_output.schema.json`
  - `第N集.json` 的最终字段真源
  - 同时持有 branch process sidecar、owner bundle 与兼容投影定义
- `.agents/skills/aigc/4-Design/1-清单/_shared/detail-output-consumption-contract.md`
  - 下游 design 清单如何优先消费 branch-owned 字段
- `.agents/skills/aigc/6-Video/_shared/image-to-video-prompt-principles.md`
  - 视频 prompt 如何优先消费 branch-owned 字段并在必要时回退到兼容投影

## Business Requirement Analysis Contract (Mandatory)

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 在同一份 `projects/aigc/<项目名>/3-Detail/第N集.json` 上继承 `2-Global` 已写入的 episode root，再把 `水月 / 镜花` branch-owned 结果稳定写回与 child skill 同名的镜级八字段，并只在需要下游兼容时派生旧字段投影。 |
| `business_object` | `projects/aigc/<项目名>/3-Detail/第N集.json`、`projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json`、`projects/aigc/<项目名>/3-Detail/镜花/第N集.field-patch.json`、`projects/aigc/<项目名>/3-Detail/validation-report.md`。 |
| `constraint_profile` | shared episode root 是唯一业务真源；`剧本正文` 保持不动；`分镜切换` 只继承不重判；本阶段必须补出 `正文切分参考[] + 分镜明细[].正文回指` 作为 `剧本正文 -> 分镜明细[]` 的唯一桥接层；branch 只写自己字段；compatibility projection 只能派生不能反向盖 canonical。 |
| `success_criteria` | 命中 scope 的镜头都具备可消费的 `角色表现 / 运动表现 / 氛围表现 / 视觉强化 / 分镜构图 / 摄影美学 / 运镜手法 / 转场特效`；owner bundle 与 branch process sidecar 可追踪；legacy 投影若存在也不反向压扁 canonical；阶段 validator 与 review gate 通过。 |
| `non_goals` | 不生成第二份 episode 主文件；不把 branch 结果压成统一 prose；不直接生成 design/image/video 请求；不重写上游分镜数与剧情事实。 |
| `complexity_source` | 复杂度来自 owner dispatch、branch review、compatibility projection 和下游 handoff，而不是再做一次创作性 merge。 |
| `topology_fit` | 固定为“root lock -> seed check -> owner dispatch -> branch review -> assembly -> compatibility projection -> stage validation -> supervision -> close”。 |
| `step_strategy` | 父层只保留阶段门、owner 边界、assembly 规则与验收；branch 细则留在各自 skill，不在父层重复展开。 |

## Context Preload (Mandatory)

加载顺序固定为：

1. 根 `AGENTS.md`
2. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
3. 本 `SKILL.md + CONTEXT.md`
4. `.agents/skills/aigc/_shared/project-runtime-layout.md`
5. `.agents/skills/aigc/_shared/group_design_seed_contract.md`
6. `.agents/skills/aigc/_shared/director_episode_output.schema.json`
7. `.agents/skills/aigc/_shared/director_episode_bootstrap.template.json`
8. `.agents/skills/aigc/3-Detail/_shared/branch-output-contract.md`
9. `.agents/skills/aigc/3-Detail/_shared/branch-review-contract.md`
10. `.agents/skills/aigc/3-Detail/_shared/node-pack-contract.md`
11. `.agents/skills/aigc/3-Detail/_shared/creative-guidance-contract.md`
12. `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
13. `.agents/skills/aigc/2-Global/SKILL.md`
14. `1-水月/SKILL.md + CONTEXT.md`
15. `2-镜花/SKILL.md + CONTEXT.md`
16. `projects/aigc/<项目名>/team.yaml`（若存在）
17. `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md`（若存在）
18. `projects/aigc/<项目名>/3-Detail/第N集.json`（若存在）
19. `projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json`（若存在）
20. `projects/aigc/<项目名>/3-Detail/镜花/第N集.field-patch.json`（若存在）

## Total Input Contract (Mandatory)

### 必需输入

- `projects/aigc/<项目名>/3-Detail/第N集.json`

### 推荐输入

- `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md`
- `projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json`
- `projects/aigc/<项目名>/3-Detail/镜花/第N集.field-patch.json`
- `projects/aigc/<项目名>/team.yaml`

### 硬规则

1. shared root 存在时，必须优先继承它，而不是重新从 Markdown 长文抽结构。
2. `剧本正文` 在 `3-Detail` 阶段只读继承。
3. `分镜切换` 只继承检查，不由本阶段重判。
4. `正文切分参考[]` 与 `分镜明细[].正文回指` 是 `剧本正文 -> 分镜明细[]` 的唯一桥接层；镜头不得复制整段正文作为平行真源。
5. 若用户只要求局部组或局部字段，本轮只 patch 命中 scope，不默认全量重跑所有 group。
6. compatibility projection 允许为空；branch-owned canonical 字段不允许被省略成只有旧字段。
7. 整个 `3-Detail/第N集.json` 默认执行“反抽象、具像化、细致化”写法：canonical 与 compatibility 字段都必须优先给出可见动作、位置关系、物件状态、空间承载、光气条件和构图抓手，不得用抽象总结句冒充 detail。

## Root Input Gate (Mandatory)

父层在调度前必须确认：

1. `metadata.document_phase in {detail_in_progress, ready}`
2. `final_output.main_content.分镜组列表[]` 存在
3. 命中组具备：
   - `分镜组ID`
   - `剧本正文`
   - `正文切分参考[]`（缺槽时本阶段必须补齐）
   - `组间设计.全局风格`
   - `组间设计.类型元素`
   - `组间设计.导演意图`
   - `组间设计.出场角色及穿搭`（允许为空，但不可缺槽）
   - `分镜切换`
   - `分镜明细[]`

若 root 缺失、损坏或仍是 bootstrap 空壳，必须先报告 `2-Global` seed 缺口，再决定是否进入兼容 repair。

## Dispatch Order Contract (Mandatory)

### 阶段级顺序

`2-Global` 已写入的 root -> `1-水月` -> `2-镜花` -> parent assembly

### Owner 内部顺序

- `1-水月`
  - 固定为：`1-角色表现 -> 2-运动表现 -> 3-氛围表现 -> 4-视觉强化`
- `2-镜花`
  - 固定为：`1-分镜构图 -> 2-摄影美学 -> 3-运镜手法 -> 4-转场特效`

### 当前 root 回读规则

1. 每一序号 branch 开始前，必须重新读取当前 `projects/aigc/<项目名>/3-Detail/第N集.json`。
2. 该 root 必须已经包含前一序号 branch 经 review 批准并写回的 canonical 字段。
3. 后一序号 branch 可以把当前 root 中已存在的前序字段当作一致性上下文，但不得越权改写它们。

### 默认调度规则

1. 若 `水月` 与 `镜花` owner bundle 都缺失，本轮先跑 `水月`，再跑 `镜花`。
2. 若只缺 `水月` canonical 字段，本轮只跑 `水月`。
3. 若 `水月` 已稳且只缺 `镜花` canonical 字段，本轮只跑 `镜花`。
4. 若 `镜花` 需要重跑而 `水月` factual 前置已过期，仍必须先重跑 `水月`。
5. shared root 的最终写回不再只发生在最后一轮；允许父层在 owner scope 内按序号逐步 commit。
6. progressive commit 只能发生在通过 review 的 branch patch 上。

## Patch Ownership And Assembly Contract (Mandatory)

### Root-level ownership

| owner | 允许写入 root canonical | 禁止写入 |
| --- | --- | --- |
| `水月 bundle` | `分镜明细[].角色表现`、`运动表现`、`氛围表现`、`视觉强化` | `分镜构图`、`摄影美学`、`运镜手法`、`转场特效` |
| `镜花 bundle` | `分镜明细[].分镜构图`、`摄影美学`、`运镜手法`、`转场特效` | `角色表现`、`运动表现`、`氛围表现`、`视觉强化` |
| 父层 `3-Detail` | shared root 最终写回、compatibility projection、`document_phase`、`validation-report.md` | 代写 branch 结论、重写剧情事实、重判镜数 |

### Owner bundle contract

1. `水月/镜花` 都必须优先写 owner bundle，而不是平行 master draft。
2. owner bundle 必须满足：
   - `metadata.schema_version = aigc/detail-branch-bundle-sidecar/v1`
   - `metadata.bundle_mode = assembly_only`
   - `branch_sidecars[]`
   - `group_patches[].branch_patches`
3. branch process sidecar 缺失时，不得伪造 owner bundle。
4. 每个 branch review 通过后，允许先把该 branch canonical 字段 progressive commit 到 root，再继续下一序号 branch。

### Assembly rules

1. 父层按当前序号逐步写 canonical object：
   - `角色表现 / 运动表现 / 氛围表现 / 视觉强化 / 分镜构图 / 摄影美学 / 运镜手法 / 转场特效`
2. 每次 progressive commit 后，当前 root 即成为下一序号 branch 的上下文真源。
3. 父层不得在 assembly 阶段做语义重写，只允许结构装配与 reviewer findings 吸收后的确定性写回。
4. 若保留 `角色背景面 / 角色站位走位 / 道具及状态 / 分镜表现 / 运镜手法 / 摄影美学` 等 compatibility 字段，它们也必须是具像摘要而非抽象总评；其中 `分镜表现` 视为 deprecated alias，语义上应向“分镜构图式兼容摘要”靠拢。
4. 若 branch findings 仍未解决，当前镜头或当前组应标记 `blocked`，不得为了完整性补空洞 prose。

### Compatibility projection rules

1. 旧字段只允许作为 projection：
   - `角色背景面`
   - `角色站位走位`
   - `道具及状态`
   - `分镜表现`
   - `摄影美学`
   - `运镜手法`
   - `转场特效`
2. projection 必须从 canonical 字段派生，不得成为新的真源。
3. projection 若会造成“多路结果再压成一句总结”，宁可留空或保守摘要，也不得重新走旧式语义压缩。
4. 任一 projection 不得反向覆盖 branch-owned canonical 字段。

## Downstream Handoff Contract (Mandatory)

`3-Detail` 的完成态不只等于“owner bundle 校验通过”，还等于“下游知道先读哪一层”。

### `4-Design`

优先消费：

- `角色表现`
- `动作路径`
- `空间氛围`
- `视觉抓手`
- `构图骨架`
- `摄影美学`
- `运镜手法`
- `转场特效`

旧字段只作 fallback，不得回写成新的 canonical 设计真源。

### `5-Image`

- prompt distillation 默认先读 branch-owned canonical 字段
- 需要做正文到镜头的精确桥接时，先读 `正文切分参考[]` 与 `分镜明细[].正文回指`，再回退整组 `剧本正文`
- 若某个叶子仍依赖旧字段，可短期读 compatibility projection，但不得反向要求 `3-Detail` 只输出旧字段

### `6-Video`

- 视频 prompt 总原则应优先消费 `角色表现 / 运动表现 / 氛围表现 / 视觉强化 / 分镜构图 / 摄影美学 / 运镜手法 / 转场特效`
- 需要做正文到镜头的精确桥接时，先读 `正文切分参考[]` 与 `分镜明细[].正文回指`，再回退整组 `剧本正文`
- `分镜表现 / 摄影美学 / 运镜手法 / 转场特效` 只作为压缩句法或 provider 兼容的 fallback

## Review Contract (Mandatory)

### Review layers

1. branch review
   - 先审 branch process sidecar 与 branch-owned patch
2. coherence review
   - 再审 owner bundle 与 root-level 跨字段一致性

### Branch-aware 默认 reviewer 偏好

| branch | 默认 reviewer 偏好 |
| --- | --- |
| `角色表现` | 编剧 / 演员 / 导演 |
| `运动表现` | 导演 / 动作 / 摄影 |
| `氛围表现` | 作品维度 / 摄影 / 设计 |
| `视觉强化` | 美学 / 摄影 / 导演 |
| `分镜构图` | 导演 / 摄影 |
| `摄影美学` | 摄影 / 导演 |
| `运镜手法` | 导演 / 摄影 / 动作 |
| `转场特效` | 导演 / 剪辑向审看 |

### Stage review hard rules

1. 不得只审 legacy projection 而跳过 branch-owned canonical 字段。
2. 若 reviewer findings 命中 branch owner，必须回流到对应 branch，不得由父层静默越权代写。
3. reviewer 可以检查“后一序号 branch 是否充分读取前序已写回 root”，并将其作为一致性信号。
4. 只有 branch review 与 coherence review 都完成，本阶段才允许进入 `ready`。

## Thinking-Action Network (Mandatory)

| node_id | 对应 Step | 聚焦字段 | objective | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `N1-INPUT-LOCK` | `S1` | `FIELD-DETAIL-01` | 锁定 episode / group / field scope | 读取 root 与 scope | `input_lock_note` | -> `N2` | scope 唯一 |
| `N2-SEED-CHECK` | `S2` | `FIELD-DETAIL-02` | 检查 root 是否可继承 | 校验 `剧本正文 / 组间设计 / 分镜切换 / document_phase`，并确认本轮需要补齐 `正文切分参考[] / 分镜明细[].正文回指` | `seed_check_note` | -> `N3` | root 可用 |
| `N3-WM-DISPATCH` | `S3` | `FIELD-DETAIL-03` | 决定是否运行或复用 `水月` | 读取/执行 `1-水月` | `watermoon_dispatch_note` | -> `N4` | `水月` owner 完整 |
| `N4-JH-DISPATCH` | `S4` | `FIELD-DETAIL-04` | 决定是否运行或复用 `镜花` | 读取/执行 `2-镜花` | `jinghua_dispatch_note` | -> `N5` | `分镜构图` 先稳 |
| `N5-BRANCH-REVIEW` | `S5` | `FIELD-DETAIL-05` | 完成 branch-aware review | 收 findings，必要时回流 branch | `branch_review_packet` | -> `N6` | findings 已闭环 |
| `N6-SERIAL-COMMIT` | `S6` | `FIELD-DETAIL-06` | 把 owner bundle 按序号逐步写回 root canonical | 写本轮批准的 branch-owned 字段，并刷新当前 root | `assembly_summary` | -> `N7` | 无语义压缩，且已刷新 root |
| `N7-COMPAT-PROJECT` | `S7` | `FIELD-DETAIL-07` | 只在需要时生成兼容投影 | 写 `compatibility_projection` 与 root fallback 字段 | `projection_note` | -> `N8` | 不反盖 canonical |
| `N8-STAGE-VALIDATE` | `S8` | `FIELD-DETAIL-08` | 形成可审看的 stage 输出包 | 写 `document_phase`、`validation-report.md`、跑 validator | `pre_review_validation_verdict` | -> `N9` | validator 过关 |
| `N9-SUPERVISION` | `S9` | `FIELD-DETAIL-09` | 做 branch-aware team review / coherence review | 解析 `team.yaml`、启动 reviewer、回收 findings | `supervision_runtime_note` | -> `N10` | reviewer 可追踪 |
| `N10-FINAL-CLOSE` | `S10` | `FIELD-DETAIL-10` | 完成终验闭环 | 重跑 validator，补写 closure | `final_close_verdict` | -> `done` | stage 完整闭环 |

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| `FIELD-DETAIL-01` | root scope lock | 输入唯一且 scope 清晰 | `S1` | 真源稳定性 | `FAIL-DETAIL-01` |
| `FIELD-DETAIL-02` | seed readiness | root 可继承 | `S2` | 上游完整性 | `FAIL-DETAIL-02` |
| `FIELD-DETAIL-03` | `水月` owner bundle | 四个 `水月` canonical 字段稳定 | `S3` | owner 完整度 | `FAIL-DETAIL-03` |
| `FIELD-DETAIL-04` | `镜花` owner bundle | 四个 `镜花` canonical 字段稳定 | `S4` | owner 完整度 | `FAIL-DETAIL-04` |
| `FIELD-DETAIL-05` | branch review packet | branch findings 与 apply decision 可追踪 | `S5` | 评审颗粒度 | `FAIL-DETAIL-05` |
| `FIELD-DETAIL-06` | `分镜明细[]` 八字段 canonical | 只做 serial progressive commit | `S6` | 抗压缩性 | `FAIL-DETAIL-06` |
| `FIELD-DETAIL-07` | legacy compatibility projection | 仅投影，不反盖 canonical | `S7` | 兼容治理 | `FAIL-DETAIL-07` |
| `FIELD-DETAIL-08` | `document_phase + validation-report.md` 初稿 | 输出包可审看 | `S8` | 预审可读性 | `FAIL-DETAIL-08` |
| `FIELD-DETAIL-09` | supervision runtime | branch-aware reviewer 与模式可追踪 | `S9` | review runtime 正确性 | `FAIL-DETAIL-09` |
| `FIELD-DETAIL-10` | final close | 终验、closure、patched targets 一致 | `S10` | 闭环完整性 | `FAIL-DETAIL-10` |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `S1` | `FIELD-DETAIL-01` | 这轮到底补哪一集、哪几个 group、哪几个 owner 字段 | 锁定 root 与 scope | scope 漂移、输入混用 |
| `S2` | `FIELD-DETAIL-02` | root 是否已具备可继承 seed | 做 seed readiness 检查 | 上游壳不完整却继续下游 |
| `S3` | `FIELD-DETAIL-03` | `水月` owner bundle 是否需要重跑或复用 | 读取/执行 `1-水月` | owner 缺失或 branch 不全 |
| `S4` | `FIELD-DETAIL-04` | `镜花` owner bundle 是否需要重跑或复用 | 读取/执行 `2-镜花` | `分镜构图` 未先稳就提前展开 |
| `S5` | `FIELD-DETAIL-05` | review 是否先发生在 branch 粒度 | 汇总 findings 并回流 owner | 只审 bundle 不审 branch |
| `S6` | `FIELD-DETAIL-06` | root canonical 是否按序号逐步 commit 且被后续 branch 回读 | 逐步写回八个 branch-owned 字段 | 未刷新 root 或后续 branch 仍按旧快照执行 |
| `S7` | `FIELD-DETAIL-07` | compatibility projection 是否仍受 canonical 约束 | 按需派生旧字段 | projection 反盖 canonical |
| `S8` | `FIELD-DETAIL-08` | stage 输出包是否已可审看和可交付 | 写 phase、report 初稿并跑 validator | validator 未过却继续 |
| `S9` | `FIELD-DETAIL-09` | team review 是否 branch-aware 且可追踪 | 解析 reviewer、执行 review | reviewer 来源不清或静默跳过 |
| `S10` | `FIELD-DETAIL-10` | 终验是否真正闭环 | 重跑校验、补写 closure triad | patched targets 与 closure 不一致 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| `FIELD-DETAIL-01` | shared root 与 selected scope 唯一 | `FAIL-DETAIL-01` | `S1` |
| `FIELD-DETAIL-02` | `剧本正文 + 组间设计 + 分镜切换` 可直接继承，且 `正文切分参考[] / 分镜明细[].正文回指` 已纳入本阶段待补结构槽位 | `FAIL-DETAIL-02` | `S2` |
| `FIELD-DETAIL-03` | `水月` owner bundle 为 `assembly_only` 且 branch sidecars 完整 | `FAIL-DETAIL-03` | `S3` |
| `FIELD-DETAIL-04` | `镜花` owner bundle 为 `assembly_only` 且 `分镜构图` 已先稳 | `FAIL-DETAIL-04` | `S4` |
| `FIELD-DETAIL-05` | branch review findings 已回流对应 owner | `FAIL-DETAIL-05` | `S5` |
| `FIELD-DETAIL-06` | `分镜明细[]` 八字段 canonical 满足 schema，且 progressive commit 顺序正确 | `FAIL-DETAIL-06` | `S6` |
| `FIELD-DETAIL-07` | compatibility projection 未回流到旧式语义压缩 | `FAIL-DETAIL-07` | `S7` |
| `FIELD-DETAIL-08` | stage validator 通过 | `FAIL-DETAIL-08` | `S8` |
| `FIELD-DETAIL-09` | supervision runtime 按 `team.yaml` / `master-check-team` 规则可追踪 | `FAIL-DETAIL-09` | `S9` |
| `FIELD-DETAIL-10` | 重跑校验、closure triad、patched targets 一致 | `FAIL-DETAIL-10` | `S10` |

## Root-Cause Execution Contract (Mandatory)

出现以下任一情况时，必须先修源层再继续下游：

- 父层仍把 branch 结果压成 `分镜表现` 之类统一 prose
- owner bundle 不是 `assembly_only`
- 按序号应串行的 branch 仍被并发处理
- 后一序号 branch 没有读取前序已写回的当前 root
- branch sidecar 缺失却仍伪造 bundle
- compatibility projection 反向盖过 canonical
- 下游继续把旧字段当成唯一真源
- review 只审旧投影、不审 branch-owned 字段

强制追因链：

`Symptom/Failure -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

本阶段常见 landing points：

- `.agents/skills/aigc/3-Detail/SKILL.md`
- `.agents/skills/aigc/3-Detail/_shared/branch-output-contract.md`
- `.agents/skills/aigc/3-Detail/_shared/branch-review-contract.md`
- `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- `.agents/skills/aigc/4-Design/1-清单/_shared/detail-output-consumption-contract.md`
- `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md`
- `.agents/skills/aigc/6-Video/_shared/image-to-video-prompt-principles.md`
- `1-水月/SKILL.md`
- `2-镜花/SKILL.md`

## Completion Contract (Mandatory)

只有同时满足以下条件，`3-Detail` 才允许宣布完成：

1. `projects/aigc/<项目名>/3-Detail/第N集.json` 仍是唯一业务真源。
2. 本轮命中 group 的 `剧本正文` 未被改写。
3. 命中 group 已具备 `正文切分参考[]`，且每条命中镜头都具备 `正文回指`。
4. 命中镜头已具备八个 branch-owned canonical 字段，或显式标记 `blocked` 并给出原因。
5. owner bundle 与 branch process sidecar 可追踪。
6. `document_phase` 与实际完成度一致。
7. `projects/aigc/<项目名>/3-Detail/validation-report.md` 已写回。
8. 若 `projects/aigc/<项目名>/team.yaml` 启用 `roles.supervision` 且当前阶段命中 `3-Detail`，已完成一次 branch-aware review 或显式降级说明。
9. `scripts/validate_stage_output.py projects/aigc/<项目名>/3-Detail/第N集.json` 返回通过；若启用监制强化校验，再追加 `--team-yaml projects/aigc/<项目名>/team.yaml`。
