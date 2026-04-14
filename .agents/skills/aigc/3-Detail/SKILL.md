---
name: aigc-detail
description: Use when the `3-Detail` stage needs to route `水月` and `镜花`, inherit or repair the shared `projects/aigc/<项目名>/3-Detail/第N集.json`, merge child patch sidecars, fill `组间设计.出场角色及穿搭` plus `分镜明细[]`, and write the stage `validation-report.md`.
governance_tier: full
---

# aigc 3-Detail

## 概述

`3-Detail` 是 `aigc` 技能树承接 `2-Global`、连接 `4-Design / 5-Image / 6-Video` 的阶段父 skill。

当前阶段不再采用“`水月` 先扩一份 markdown、`镜花` 再扩同一目标”的双次扩写模式。新的 canonical 合同是：

1. `projects/aigc/<项目名>/3-Detail/第N集.json`
   - 唯一业务真源
   - 阶段主线固定先读取这一份，再在同一份上 merge 写回
   - `剧本正文` 继承上游，不在本阶段重写
   - 正常来源是 `2-Global` 阶段末段写入的 shared episode root
   - 仅当该 root 缺失或不可用时，才允许 `3-Detail` 走兼容 bootstrap / repair
2. `projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json`
   - 组级与 beat 级事实 patch sidecar
3. `projects/aigc/<项目名>/3-Detail/镜花/第N集.field-patch.json`
   - shot skeleton 与导演/摄影 patch sidecar

`水月` 与 `镜花` 的内部思考机制保留，但执行落点改成字段填充式：

- `水月`
  - 负责把固定 `剧本正文` 拆成可聚合的 beat-level factual evidence
- `镜花`
  - 负责消费 shared root 中已给出的 `分镜切换` 与 `水月` evidence，按既定镜数落真实切镜、构图、摄影、运镜、转场 patch
- 父层 `3-Detail`
  - 负责 stage gate、字段 ownership、sidecar merge、shared JSON writeback 与 validation

## Parent Positioning

`3-Detail` 是 stage-local parent skill。

当前 active 子技能：

1. `水月`
2. `镜花`

父层拥有：

- `2-Global -> 3-Detail` shared root 继承与缺口诊断
- `分镜切换 -> 水月 -> 镜花` 的顺序门与 selective dispatch
- patch sidecar 到 shared JSON 的聚合与冲突裁决
- `组间设计.出场角色及穿搭` 的阶段级回填
- `分镜明细[]` 的 patch-in-place
- `metadata.document_phase = detail_in_progress | ready` 的推进
- `projects/aigc/<项目名>/3-Detail/validation-report.md` 写回

父层不拥有：

- 重写 `1-Planning/3-分组` 的组界、组序、组 ID
- 改写 `第N集.json` 中既有 `剧本正文`
- 在无显式返工理由时重写 `2-Global` 已写入的 `组间设计.全局风格 / 类型元素`
- 把 shared JSON 写回责任外包给子技能
- 直接生成 `4-Design / 5-Image / 6-Video` 请求

## Internal Capability Fusion Contract (Mandatory)

`3-Detail` 的阶段总线统一分布在父 skill、两个子技能与 shared contracts：

| 能力面 | 当前 owner | 说明 |
| --- | --- | --- |
| 阶段入口判定与顺序 dispatch | `3-Detail/SKILL.md` | 决定本轮命中 `水月`、`镜花`、还是 patch-only，并锁 `分镜切换 -> 水月 -> 镜花` 的先后门 |
| beat-level factual evidence | `水月/SKILL.md` | 提供 `出场角色及穿搭`、角色/走位/道具事实和 `镜头消费提示` |
| 镜头层 patch | `镜花/SKILL.md` | 消费 `分镜切换 + 水月 evidence`，提供真实切镜、shot skeleton 与导演/摄影 patch |
| shared root 继承与结构化 merge | `3-Detail/SKILL.md` + shared schema/contracts | 把 sidecar 证据压回 `第N集.json`，并推进 `document_phase` |
| 阶段验收与 handoff | `3-Detail/SKILL.md` | 写 `projects/aigc/<项目名>/3-Detail/validation-report.md` |

硬规则：

1. `水月` 与 `镜花` 只产出 patch sidecar，不产第二份 episode 主文件。
2. `剧本正文` 默认继承上游，不得在 `3-Detail` 阶段重写。
3. `水月` 与 `镜花` 的目录去序号，不再用目录名暗示顺序；实际顺序必须由父层显式声明，不得凭目录观感推断。
4. 若将来新增 detail 子链，必须先说明它补的是哪组字段 ownership，不得与现有 owner 并行抢写。

## Shared Canonical Sources (Mandatory)

- `.agents/skills/aigc/_shared/project-runtime-layout.md`
- `.agents/skills/aigc/_shared/group_design_seed_contract.md`
- `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- `.agents/skills/aigc/_shared/director_episode_bootstrap.template.json`
- `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
- `.agents/skills/aigc/4-Design/1-主体清单/_shared/detail-output-consumption-contract.md`
- `.agents/skills/aigc/3-Detail/_shared/node-pack-contract.md`
- `.agents/skills/aigc/3-Detail/_shared/creative-guidance-contract.md`
- `.agents/skills/aigc/_shared/director_episode_output.schema.json#/$defs/detail_patch_sidecar`
- `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
- `.agents/skills/aigc/2-Global/SKILL.md`
- `水月/SKILL.md`
- `镜花/SKILL.md`

真源分工：

- 本 `SKILL.md`
  - 父层路由、shared root 继承/修复、阶段聚合、phase 推进、validation
- `水月/SKILL.md`
  - factual patch sidecar 真源
- `镜花/SKILL.md`
  - cinematic patch sidecar 真源
- `director_episode_output.schema.json`
  - `3-Detail/第N集.json` 的最终结构化字段真源
  - 同时持有 `#/$defs/detail_patch_sidecar` 等 sidecar projection 定义
- `4-Design/1-主体清单/_shared/detail-output-consumption-contract.md`
  - 定义 `角色 / 服装 / 道具 / 场景` 四类下游清单如何消费 `3-Detail` 的 canonical 字段
  - `3-Detail` 不拥有下游 design-source artifact，但拥有它们的 upstream field contract

## Downstream Handoff Contract (Mandatory)

`3-Detail` 的完成态不只等于 “父层 merge 成功”，还等于“下游 `1-主体清单` 能按共享消费合同直接读取”。

因此 handoff 最低要求固定为：

1. `角色` 可直接消费：
   - `分镜明细[].角色站位走位`
   - `分镜明细[].角色背景面`
   - `组间设计.出场角色及穿搭`
2. `场景` 可直接消费：
   - `分镜明细[].角色背景面`
3. `道具` 可直接消费：
   - `分镜明细[].道具及状态`
   - `分镜明细[].角色背景面`
   - `分镜明细[].角色站位走位`
   - `分镜明细[].分镜表现`
4. 若命中 legacy 兼容字段，它们只能作为 fallback 被读取，不得回写成新的 canonical 输出。

## Business Requirement Analysis Contract (Mandatory)

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 在同一份 `projects/aigc/<项目名>/3-Detail/第N集.json` 上继承 `2-Global` 已写入的分镜组壳、`组间设计` 与固定 `分镜切换`，再把 `水月` beat-level evidence 与 `镜花` cinematic sidecar 收束成 `组间设计.出场角色及穿搭 + 分镜明细[]`，使其进入可供下游消费的阶段状态。 |
| `business_object` | `projects/aigc/<项目名>/3-Detail/第N集.json`、`projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json`、`projects/aigc/<项目名>/3-Detail/镜花/第N集.field-patch.json`、`projects/aigc/<项目名>/3-Detail/validation-report.md`。 |
| `constraint_profile` | shared episode root 是唯一结构化真源；`剧本正文` 保持不动；`组间设计` 与 `分镜切换` 默认继承不重写；`水月` 只写 beat-level factual evidence；`镜花` 只写 cinematic patch；`分镜明细[]` 只在 `3-Detail` 阶段扩展；若 shared root 缺失，只能走显式兼容 bootstrap。 |
| `success_criteria` | 本轮 scope 内的分镜组都能在 shared root 中看到稳定的 `分镜明细[]` patch、必要的 `出场角色及穿搭` 回填、正确的 `document_phase` 推进，以及阶段级 `validation-report.md`。 |
| `non_goals` | 不再生成两轮 markdown 扩写稿；不重写 `剧本正文`；不越权重写 `2-Global` 的项目级设计真源；不直接生成 design/image/video 请求。 |
| `complexity_source` | 当前阶段要同时维护 shared JSON、既定 `分镜切换`、两个字段 patch sidecar，以及 beat-level factual evidence 与 shot-level cinematic patch 的 merge 对齐。 |
| `topology_fit` | 固定为“输入锁定 -> council gate -> root seed 检查/兼容回退 -> 顺序 dispatch (`分镜切换 -> 水月 -> 镜花`) -> child patch 产出/复用 -> parent merge -> shared JSON patch -> phase 推进 -> stage validation”。 |
| `step_strategy` | 父 `SKILL.md` 保留阶段门、字段边界、merge 规则与验收；子技能细则留在各自目录，不在父层重复展开。 |

## Context Preload (Mandatory)

加载顺序固定为：

1. 根 `AGENTS.md`
2. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
3. 本 `SKILL.md + CONTEXT.md`
4. `.agents/skills/aigc/_shared/project-runtime-layout.md`
5. `.agents/skills/aigc/_shared/group_design_seed_contract.md`
6. `.agents/skills/aigc/_shared/director_episode_output.schema.json`
7. `.agents/skills/aigc/_shared/director_episode_bootstrap.template.json`
8. `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
9. `.agents/skills/aigc/3-Detail/_shared/node-pack-contract.md`
10. `.agents/skills/aigc/3-Detail/_shared/creative-guidance-contract.md`
11. `.agents/skills/aigc/_shared/director_episode_output.schema.json#/$defs/detail_patch_sidecar`
12. `.agents/skills/aigc/1-Planning/3-分组/SKILL.md`
13. `.agents/skills/aigc/2-Global/SKILL.md`
14. `水月/SKILL.md`
15. `镜花/SKILL.md`
16. `projects/aigc/<项目名>/team.yaml`（若存在）
17. `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md`
18. `projects/aigc/<项目名>/3-Detail/第N集.json`（若存在）
19. `projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json`（若存在）
20. `projects/aigc/<项目名>/3-Detail/镜花/第N集.field-patch.json`（若存在）
21. `projects/aigc/<项目名>/2-Global/全局风格/全局风格设计.md`（若存在）
22. `projects/aigc/<项目名>/2-Global/类型元素/全集设计.md`（若存在）
23. `projects/aigc/<项目名>/2-Global/类型元素/分组设计.md`（若存在）
24. `projects/aigc/<项目名>/2-Global/设计元素/设计元素.md`（若存在）

## Total Input Contract (Mandatory)

### 必需输入

- `projects/aigc/<项目名>/3-Detail/第N集.json`

### 强烈建议输入

- `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md`
- `projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json`
- `projects/aigc/<项目名>/3-Detail/镜花/第N集.field-patch.json`

### 可选输入

- `projects/aigc/<项目名>/team.yaml`
- `projects/aigc/<项目名>/0-Init/north_star.yaml`
- `projects/aigc/<项目名>/0-Init/init_handoff.yaml`
- `projects/aigc/<项目名>/0-Init/story-source-manifest.yaml`
- 现有 `projects/aigc/<项目名>/3-Detail/validation-report.md`
- 用户显式指定的 `selected_groups[] / selected_fields[] / selected_chains[]`

### 硬规则

1. shared root 存在时，`3-Detail` 必须优先继承它，而不是重新从 Markdown 长文抽结构。
2. `剧本正文` 在 `3-Detail` 默认保持不动。
3. `组间设计.全局风格 / 类型元素` 与 `分镜切换` 默认继承 `2-Global`，不得因 detail 补写而漂移。
4. `组间设计.出场角色及穿搭` 可由 `3-Detail` 在镜级事实稳定后回填。
5. `分镜明细[]` 只能在 `3-Detail` 阶段扩展。
6. 若 shared root 缺失或仍是 `bootstrapped` 空壳，必须先报告 seed 缺口，再决定是否进入兼容 bootstrap / backfill；不得把兼容路径误当默认主线。
7. 若用户只要求局部组或局部字段，本轮只 patch 命中 scope，不默认全量重跑所有 group。

## Dispatch Order Contract (Mandatory)

`3-Detail` 的默认顺序不是“`水月 / 镜花` 可自由并发”，而是：

`2-Global` 已写入的 `分镜切换` -> `水月` beat-level factual evidence -> `镜花` 真实切镜与后续镜头语言`

默认调度规则：

1. 若 shared root 缺 `分镜切换`，父层必须先报告 `2-Global` seed 缺口；不得让 `镜花` 默认代替 `2-Global` 决定组级镜数。
2. 若 `水月` 与 `镜花` sidecar 都缺失，本轮先跑 `水月`，再跑 `镜花`。
3. 若 `水月` 稳定、仅 `镜花` 缺失或需补 cinematic 字段，本轮只跑 `镜花`。
4. 若仅需 factual 字段或 `出场角色及穿搭`，本轮只跑 `水月`。
5. 若 `水月` evidence 已过期且 `镜花` 也需重跑，顺序仍必须是先 `水月`，后 `镜花`。
6. `镜花` 内部仍必须先经 `分镜构图` 消费 shared root 的 `分镜切换`，按既定镜数落成 shot skeleton，后续 `摄影 / 运镜 / 转场` 才能展开。
7. shared JSON 的最终写回始终只允许父层在 merge 后一次性落盘。

## Patch Ownership And Merge Contract (Mandatory)

### 固定字段 ownership

| owner | 允许写入 | 禁止写入 |
| --- | --- | --- |
| `水月` | `组间设计.出场角色及穿搭`、`beat_patches[].角色背景面`、`beat_patches[].角色站位走位`、`beat_patches[].道具及状态`、`beat_patches[].镜头消费提示` | `剧本正文`、`分镜切换`、`分镜ID`、`时间段`、`景别`、`运镜手法`、`摄影美学` |
| `镜花` | `shot_patches[].分镜ID`、`时间段`、`景别`、`镜头属性`、`镜头框架`、`镜头类型`、`镜头视角`、`运镜手法`、`镜头速度`、`摄影美学`、`转场特效`、`beat_refs[]` | `剧本正文`、`组间设计.*`、`分镜切换`、`角色背景面`、`角色站位走位`、`道具及状态`、`镜头消费提示` |
| 父层 `3-Detail` | shared root 的最终 `组间设计.出场角色及穿搭`、`分镜切换` 继承检查、`分镜明细[]` | 把 child sidecar 原样塞进 shared JSON |

### beat / shot 对齐规则

1. `水月` 与 `镜花` 都必须使用共享 `beat_id` 规则：
   - `beat_id = <group_id>-bNN`
   - `NN` 按固定 `剧本正文` 中的组内锚点顺序生成
2. `镜花` 在生成 `shot_patches[].beat_refs[]` 之前，必须先继承 shared root 中的 `分镜切换`
3. `镜花.shot_patches[].beat_refs[]` 必须显式回指一个或多个 `beat_id`
4. 父层 merge 顺序固定为：
   - 先确认 shared root 仍保留 `分镜切换`
   - 再读取 `水月.beat_patches[]`
   - 再用 `镜花.shot_patches[].beat_refs[]` 映射 factual evidence
   - 将 `镜头消费提示` 投影成 shared root `分镜明细[].分镜表现`
   - 若 `beat_refs[]` 缺失但 shot 数量与 beat 数量一致，则按组内顺序对齐
   - 若仍无法对齐，当前 group 进入 `blocked`，写入 `validation-report.md`

### shared root 写回规则

1. `剧本正文` 仅继承，不重写。
2. `组间设计` 默认只允许回填 `出场角色及穿搭`。
3. `分镜切换` 默认只做继承检查，不在 `3-Detail` 内重判。
4. `分镜明细[]` 由父层将 `水月` factual evidence 与 `镜花` cinematic patch 合成后写回。
5. 未命中 owner 的字段不得补空洞默认值。

## Shared Root Inheritance And Compatibility (Mandatory)

### 阶段主线真源

- `3-Detail` 的阶段主线固定为：先读取同一份 `projects/aigc/<项目名>/3-Detail/第N集.json`，再把 `水月/镜花` sidecar merge 回这一份。
- `水月` 与 `镜花` 都不是第二内容终稿出口，而是围绕既有 `第N集.json` 做字段写入准备。
- 因此本阶段的 read/write 主线只有一个根：`projects/aigc/<项目名>/3-Detail/第N集.json`。

### `第N集.json` 的来源

优先级固定为：

1. `2-Global` 在阶段末段基于 shared schema 写入完整分镜组壳：
   - `分镜组ID`
   - `总时长`
   - `剧本正文`
   - `组间设计`
   - `分镜切换`
   - `分镜明细=[]`
2. 若上游 root 缺失、损坏或仍不可用，`3-Detail` 才允许基于：
   - `.agents/skills/aigc/_shared/director_episode_bootstrap.template.json`
   - `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md`
   走保守兼容 bootstrap / repair

换句话说：正常情况不是 `3-Detail` 现造一份 `第N集.json`，而是继承 `2-Global` 已经放在 `projects/aigc/<项目名>/3-Detail/` 下的那一份。

### 正常路径

- 读取 `projects/aigc/<项目名>/3-Detail/第N集.json`
- 校验其是否符合 shared schema
- 优先继承：
  - `分镜组ID`
  - `总时长`
  - `剧本正文`
  - `组间设计`
  - `分镜切换`
- 在同一 root 上补：
  - `组间设计.出场角色及穿搭`
  - `分镜明细[]`
  - `metadata.document_phase`
  - `final_output.acceptance_notes`

### 兼容回退路径

仅当以下条件成立时，允许 `3-Detail` 创建或修复 shared root：

1. 用户明确要求继续 `3-Detail`
2. `1-Planning/3-分组/第N集.md` 存在
3. shared root 缺失或不可用
4. 已显式报告 `2-Global` seed 缺口

## Thinking-Action Network (Mandatory)

| node_id | 对应 Step | 聚焦字段 | objective | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `N1-INPUT-LOCK` | `S1` | `FIELD-DETAIL-01` | 锁定唯一 episode scope 与 shared root | 读取 `第N集.json`、`第N集.md` 与 selected scope | `input_lock_note` | 成功 -> `N2`；失败 -> 回 `S1` | scope 唯一后才可继续 |
| `N2-SEED-CHECK` | `S2` | `FIELD-DETAIL-02` | 检查 `2-Global` seed 是否完整 | 校验 `剧本正文 / 组间设计 / 分镜切换 / document_phase` | `seed_check_note` | 正常 -> `N3`；缺口 -> compat/blocked | shared root 可用且含 `分镜切换` 后再调子技能 |
| `N3-DISPATCH` | `S3` | `FIELD-DETAIL-03` | 决定本轮命中哪些 child owner 与先后门 | 判断 `水月 / 镜花` 缺口、复用与串行策略 | `dispatch_plan` | -> `N4` / `N5` | 只调度命中 owner，且 `镜花` 不得跳过前置 |
| `N4-WATERMOON-PATCH` | `S4` | `FIELD-DETAIL-04` | 获取 beat-level factual evidence sidecar | 复用或执行 `水月`，读取 `group_design_patch + beat_patches[]` | `watermoon_patch_note` | -> `N5/N6` | 不得越权写 cinematic 字段 |
| `N5-JINGHUA-PATCH` | `S5` | `FIELD-DETAIL-05` | 在既定 `分镜切换 + 水月 evidence` 基础上获取 cinematic patch sidecar | 复用或执行 `镜花`，读取 `shot_patches[]` | `jinghua_patch_note` | -> `N6` | 不得越权写 factual 字段，且不得重判 seed |
| `N6-MERGE` | `S6` | `FIELD-DETAIL-06` `FIELD-DETAIL-07` | 合并 child patch 并写回 shared root | 先回填 `出场角色及穿搭`，再按 `beat_refs[]` 合成 `分镜明细[]` | `merge_summary` | pass -> `N7`；drift -> 回 `S3~S6` | `剧本正文` 不得变化 |
| `N7-PHASE-VALIDATE` | `S7` | `FIELD-DETAIL-08` | 推进 phase 并写阶段验收 | 更新 `document_phase`、写 `validation-report.md` | `validation_verdict` | pass -> `done`；fail -> 回 `S4~S6` | `ready` 前必须存在可消费 `分镜明细[]` |

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| `FIELD-DETAIL-01` | episode scope / shared root lock | 输入唯一且 scope 清晰 | `S1` | 真源稳定性 | `FAIL-DETAIL-01` |
| `FIELD-DETAIL-02` | seed readiness | `剧本正文 + 组间设计 + 分镜切换` 已可继承 | `S2` | 上游完整性 | `FAIL-DETAIL-02` |
| `FIELD-DETAIL-03` | dispatch plan | owner、scope、顺序门明确 | `S3` | 调度准确度 | `FAIL-DETAIL-03` |
| `FIELD-DETAIL-04` | `水月` factual evidence | `出场角色及穿搭 + beat factual fields + 镜头消费提示` 稳定 | `S4` | 事实可聚合性 | `FAIL-DETAIL-04` |
| `FIELD-DETAIL-05` | `镜花` cinematic patch | shot skeleton 与 cinematic fields 稳定 | `S5` | 镜头可聚合性 | `FAIL-DETAIL-05` |
| `FIELD-DETAIL-06` | `组间设计.出场角色及穿搭` | 只回填有证据的服装摘要 | `S6` | 组级回填准确度 | `FAIL-DETAIL-06` |
| `FIELD-DETAIL-07` | `分镜明细[]` | factual + cinematic merge 后满足 schema | `S6` | shot patch 完整度 | `FAIL-DETAIL-07` |
| `FIELD-DETAIL-08` | `document_phase + validation-report.md` | 完成度表达真实且可验收 | `S7` | 闭环完整性 | `FAIL-DETAIL-08` |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `S1` | `FIELD-DETAIL-01` | 这轮到底补哪一集、哪几个 group、哪几个字段 owner | 锁 episode、group scope 与 shared root | scope 漂移、输入混用 |
| `S2` | `FIELD-DETAIL-02` | shared root 是否已经具备可继承 `剧本正文 + 组间设计 + 分镜切换` | 做 seed readiness 检查 | 上游壳不完整却继续下游 |
| `S3` | `FIELD-DETAIL-03` | 哪些 sidecar 需要重跑，哪些可以复用，`镜花` 的前置是否齐全 | 生成 dispatch plan | 跳过顺序门或 owner 混写 |
| `S4` | `FIELD-DETAIL-04` | `水月` 是否提供了可聚合 factual evidence | 读取/生成 group_design_patch 与 beat_patches | 只有抽象 prose，无结构化事实 |
| `S5` | `FIELD-DETAIL-05` | `镜花` 是否在 seed + factual evidence 基础上提供了可聚合 cinematic patch | 读取/生成 shot_patches | 只有镜头感，没有字段落点 |
| `S6` | `FIELD-DETAIL-06/07` | 如何在不改 `剧本正文` 的前提下写回 root | merge factual + cinematic patch | 字段 owner 漂移、对齐失败 |
| `S7` | `FIELD-DETAIL-08` | 当前是否只能 `detail_in_progress`，还是可以 `ready` | 写 phase 与 validation | `ready` 与真实完成度不符 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| `FIELD-DETAIL-01` | shared root、planning script 与 selected scope 唯一 | `FAIL-DETAIL-01` | `S1` |
| `FIELD-DETAIL-02` | `剧本正文 + 组间设计 + 分镜切换` 可直接继承 | `FAIL-DETAIL-02` | `S2` |
| `FIELD-DETAIL-03` | dispatch 只命中必要 owner，且顺序门正确 | `FAIL-DETAIL-03` | `S3` |
| `FIELD-DETAIL-04` | factual patch 可回链且不越权 | `FAIL-DETAIL-04` | `S4` |
| `FIELD-DETAIL-05` | cinematic patch 可回链且不越权 | `FAIL-DETAIL-05` | `S5` |
| `FIELD-DETAIL-06` | `出场角色及穿搭` 回填准确且克制 | `FAIL-DETAIL-06` | `S6` |
| `FIELD-DETAIL-07` | `分镜明细[]` 满足 schema 且 merge 无冲突 | `FAIL-DETAIL-07` | `S6` |
| `FIELD-DETAIL-08` | `document_phase` 与 `validation-report.md` 一致 | `FAIL-DETAIL-08` | `S7` |

## Root-Cause Execution Contract (Mandatory)

出现以下任一情况时，必须先修源层再继续下游：

- shared root 缺失、seed 不完整、`剧本正文` 被误改
- `水月` 或 `镜花` sidecar 越权写字段
- `beat_id / beat_refs[]` 无法对齐
- `分镜明细[]` 合成后不满足 shared schema
- `document_phase` 与真实完成度不一致

强制追因链：

`Symptom/Failure -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

本阶段常见 landing points：

- `.agents/skills/aigc/3-Detail/SKILL.md`
- `.agents/skills/aigc/_shared/director_episode_output.schema.json#/$defs/detail_patch_sidecar`
- `水月/SKILL.md`
- `镜花/SKILL.md`
- `.agents/skills/aigc/_shared/group_design_seed_contract.md`

## Completion Contract (Mandatory)

只有同时满足以下条件，`3-Detail` 才允许宣布本轮完成：

1. `projects/aigc/<项目名>/3-Detail/第N集.json` 仍是唯一业务真源。
2. 本轮命中 group 的 `剧本正文` 未被改写。
3. `组间设计.出场角色及穿搭` 若此前为空，已完成有依据回填或显式说明为何仍缺证据。
4. 命中 group 已写入合法 `分镜明细[]`。
5. `document_phase` 与实际完成度一致。
6. `projects/aigc/<项目名>/3-Detail/validation-report.md` 已写回。
