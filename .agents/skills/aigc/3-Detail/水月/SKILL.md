---
name: aigc-detail-watermoon
description: Use when `3-Detail` needs a stage-local child skill to keep `剧本正文` unchanged, read the existing shared root `3-Detail/第N集.json` as the primary source, use planning/global evidence only as support, and emit a factual field-patch sidecar under `projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json`.
governance_tier: full
---

# 3-Detail / 水月

## 概述

`水月` 是 `3-Detail` 下的 stage-local child skill。

它不再把 grouped script 扩写成第二份 markdown 成稿，而是保持 `剧本正文` 不动，围绕已有 shared root 拆出 **可聚合的 factual patch**：

- 主输入：`projects/aigc/<项目名>/3-Detail/第N集.json`
- 辅助证据：`projects/aigc/<项目名>/1-Planning/3-分组/第N集.md`
- canonical 输出：`projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json`

内部思考主链保持不变，仍由四条并发树形维度链驱动：

1. `角色表现`
2. `运动表现`
3. `氛围表现`
4. `视觉强化`

但最终落盘从“单段 prose 扩写”改成：

- `组间设计.出场角色及穿搭`
- `beat_patches[].角色背景面`
- `beat_patches[].角色站位走位`
- `beat_patches[].道具及状态`
- `beat_patches[].镜头消费提示`

## Child-Skill Positioning

### `水月` 拥有

- 从固定 `剧本正文` 中提炼组级角色 / 动作 / 空间 / 氛围事实
- 生成 `出场角色及穿搭` 的组级回填建议
- 把组内事实拆成可被父层 merge 的 `beat_patches[]`
- 写回 `projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json`

### `水月` 不拥有

- 改写 `1-Planning/3-分组` 的组界、组序、组 ID
- 改写 shared root 的 `剧本正文`
- 生成 `分镜ID / 时间段 / 景别 / 运镜手法 / 摄影美学`
- 直接写 `projects/aigc/<项目名>/3-Detail/第N集.json`

## When to Use

- 上游已经存在 `projects/aigc/<项目名>/3-Detail/第N集.json`
- 需要先生成人物、动作、空间与道具状态的 factual patch
- 需要回填 `组间设计.出场角色及穿搭`
- 需要一个可被父层和 `镜花` 切镜阶段消费的 group/beat sidecar

## When Not to Use

- 还没有稳定的 `projects/aigc/<项目名>/3-Detail/第N集.json`
- 当前目标只涉及 shot skeleton / 摄影 / 运镜字段
- 用户要求直接修改 `剧本正文`

## Canonical Source Contract (Mandatory)

- 第一输入真源固定为：`projects/aigc/<项目名>/3-Detail/第N集.json`
- `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md` 只作为组界复核、beat 锚点补证与兼容 repair 证据
- `0-Init` 只提供项目目标、题材、人物关系、语气与禁写项
- `2-Global` 只提供风格、类型、设计元素与已写入 shared root 的 `分镜切换`
- `.agents/skills/aigc/_shared/director_episode_output.schema.json#/$defs/detail_patch_sidecar`
  - 持有 patch sidecar 的唯一结构真源
- 最终真源只允许落在：
  - `projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json`

硬规则：

1. 不得改组 ID、组序、组边界。
2. 不得改写 `剧本正文`。
3. 不得产出 `分镜ID / 时间段 / 景别 / 运镜手法 / 摄影美学`。
4. 不得把思考过程直接写进最终 sidecar。
5. `beat_id` 必须使用 `<group_id>-bNN` 规则。

## Context Preload (Mandatory)

固定加载顺序：

1. 根 `AGENTS.md`
2. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
3. `.agents/skills/aigc/3-Detail/SKILL.md + CONTEXT.md`
4. 本 `SKILL.md + CONTEXT.md`
5. `.agents/skills/aigc/_shared/director_episode_output.schema.json#/$defs/detail_patch_sidecar`
6. `projects/aigc/<项目名>/0-Init/north_star.yaml`
7. `projects/aigc/<项目名>/0-Init/init_handoff.yaml`
8. `projects/aigc/<项目名>/0-Init/story-source-manifest.yaml`（若存在）
9. `projects/aigc/<项目名>/3-Detail/第N集.json`
10. `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md`（若存在）
11. `projects/aigc/<项目名>/2-Global/全局风格.md`（若存在）
12. `projects/aigc/<项目名>/2-Global/全集类型元素.md`（若存在）
13. `projects/aigc/<项目名>/2-Global/分组类型元素.md`（若存在）
14. `projects/aigc/<项目名>/2-Global/导演意图.md`（若存在）
15. `references/module-index.md`
16. `.agents/skills/aigc/3-Detail/_shared/node-pack-contract.md`
17. `.agents/skills/aigc/3-Detail/_shared/creative-guidance-contract.md`
18. `references/route-profile.yaml`
19. 按需读取各分类 `module-spec.yaml` 与命中叶子 `module-spec.yaml`
20. `references/examples.md`
21. `references/creative-review-rubric.md`
22. `templates/field-patch.template.json`

## Beat Patch Contract (Mandatory)

`水月` 输出的是 **group patch + beat patch**，不是 prose。

其中 `beat_patches[].镜头消费提示` 是 pre-shot evidence，不是 shared root 最终 shot-level `分镜表现`；最终镜级字段由父层按 `beat_refs[]` 投影生成。

### group patch 最低要求

- `group_id`
- `target_fields[]`
- `group_design_patch.出场角色及穿搭`（若有证据）

`target_fields[]` 只允许声明：

- `组间设计.出场角色及穿搭`
- `分镜明细[].角色背景面`
- `分镜明细[].角色站位走位`
- `分镜明细[].道具及状态`
- `beat_patches[].镜头消费提示`

### beat patch 最低要求

- `beat_id`
- `anchor_summary`
- `角色背景面`
- `角色站位走位`
- `道具及状态`
- `镜头消费提示`

### beat 切分规则

1. 只围绕固定 `剧本正文` 的组内锚点切分，不发明新剧情。
2. `beat_id` 使用 `<group_id>-b01 / b02 / ...`。
3. 切分基准优先级：
   - 主动作切换
   - 主视线或主关系切换
   - 空间朝向或走位切换
   - 明确道具状态切换

## Thinking-Action Network (Mandatory)

| node_id | 对应 Step | 聚焦字段 | objective | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `N1-INPUT-LOCK` | `S1` | `FIELD-WM-01` | 锁定唯一 shared root 与 group scope | 读取 `第N集.json`，必要时辅读 `第N集.md` 复核组序与固定 `剧本正文` | `input_lock_note` | -> `N2` | shared root 唯一后才可继续 |
| `N2-CONTEXT-SEED` | `S2` | `FIELD-WM-02` | 回收 `Init / Global` 中与当前集相关的事实约束 | 提炼题材语气、角色气质、风格和设计元素 | `seed_context_note` | -> `N3` | 证据成形后再拆组 |
| `N3-GROUP-ANCHOR` | `S3` | `FIELD-WM-03` | 为每组抽取 factual 锚点 | 提炼 `场景 / 冲突 / 角色 / 主行动 / 道具状态` | `group_anchor_table` | -> `N4A~N4D` | 每组锚点必须可引用 |
| `N4A-CHARACTER-BRANCH` | `S4` | `FIELD-WM-04` | 让角色行为和关系可落字段 | 运行 `角色表现` 叶子链，生成角色事实 patch | `character_patch` | -> `N5` | 只产 factual patch |
| `N4B-MOTION-BRANCH` | `S4` | `FIELD-WM-05` | 让走位与连续性可落字段 | 运行 `运动表现` 叶子链，生成走位事实 patch | `motion_patch` | -> `N5` | 不得重写组界 |
| `N4C-ATMOSPHERE-BRANCH` | `S4` | `FIELD-WM-06` | 让空间与道具状态可落字段 | 运行 `氛围表现` 叶子链，生成环境事实 patch | `atmosphere_patch` | -> `N5` | 只补可见事实 |
| `N4D-VISUAL-BRANCH` | `S4` | `FIELD-WM-07` | 让 `镜头消费提示` 有可被切镜消费的抓手 | 运行 `视觉强化` 叶子链，生成表现事实 patch | `visual_patch` | -> `N5` | 不得写成空泛辞藻 |
| `N5-CONVERGE` | `S5` | `FIELD-WM-08` | 把四条支路收束成 beat factual patch | 组装 `beat_patches[]` 与 `group_design_patch` | `beat_patch_summary` | -> `N6` | 不得回写 prose |
| `N6-WRITEBACK` | `S6` | `FIELD-WM-09` | 按模板一次性写回 sidecar | 落盘 `projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json` | `writeback_note` | -> `N7` | 只写一个 canonical 文件 |
| `N7-VALIDATE` | `S7` | `FIELD-WM-09` | 验证 sidecar 结构与 ownership | 执行 `scripts/validate_watermoon_output.py` | `validation_verdict` | pass -> `done`；fail -> 回 `S5/S6` | 通过前不得结案 |

## Output Contract (Mandatory)

### 输出路径

- `projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json`

### 输出格式

- 顶层必须符合 `.agents/skills/aigc/_shared/director_episode_output.schema.json#/$defs/detail_patch_sidecar`
- `target_fields[]` 只允许声明：
  - `组间设计.出场角色及穿搭`
  - `分镜明细[].角色背景面`
  - `分镜明细[].角色站位走位`
  - `分镜明细[].道具及状态`
  - `beat_patches[].镜头消费提示`
- 只允许出现：
  - `group_design_patch.出场角色及穿搭`
  - `beat_patches[].角色背景面`
  - `beat_patches[].角色站位走位`
  - `beat_patches[].道具及状态`
  - `beat_patches[].镜头消费提示`
- 不得包含 `剧本正文`
- 不得包含 `分镜ID / 时间段 / 景别 / 运镜手法 / 摄影美学`

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| `FIELD-WM-01` | 输入锁定 | shared root 与 group scope 唯一 | `S1` | 真源稳定性 | `FAIL-WM-01` |
| `FIELD-WM-02` | 附加上下文种子 | `Init / Global` 的事实约束已可消费 | `S2` | 上下文利用率 | `FAIL-WM-02` |
| `FIELD-WM-03` | 组锚点 | 每组有清楚的主动作、主冲突和道具状态 | `S3` | 锚点清晰度 | `FAIL-WM-03` |
| `FIELD-WM-04` | 角色事实 patch | 人物心理、动作与关系可映射 | `S4` | 人物成立度 | `FAIL-WM-04` |
| `FIELD-WM-05` | 走位事实 patch | 动作路径、朝向与连续性清楚 | `S4` | 动作可视化 | `FAIL-WM-05` |
| `FIELD-WM-06` | 环境事实 patch | 空间、气候与道具状态清楚 | `S4` | 场感可落地性 | `FAIL-WM-06` |
| `FIELD-WM-07` | 表现事实 patch | `镜头消费提示` 可被镜头消费 | `S4` | 表现可消费性 | `FAIL-WM-07` |
| `FIELD-WM-08` | beat patch 汇流 | factual patch 被收束成合法 `beat_patches[]` | `S5` | 收束能力 | `FAIL-WM-08` |
| `FIELD-WM-09` | 最终 sidecar | 结构、ownership 与 validator 全通过 | `S6/S7` | 落盘可消费性 | `FAIL-WM-09` |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `S1` | `FIELD-WM-01` | 这轮到底抽哪一集、哪几个 group | 锁 episode、group scope 与 shared root | 用错输入、group scope 飘移 |
| `S2` | `FIELD-WM-02` | 哪些 `Init / Global` 约束必须进入 factual patch | 提炼约束种子 | 附加上下文只被罗列，不被消费 |
| `S3` | `FIELD-WM-03` | 每个分镜组真正需要哪些事实锚点 | 提炼组锚点表 | 后续 patch 散乱无主轴 |
| `S4` | `FIELD-WM-04~07` | 四条维度链分别应该补哪些 factual 字段 | 生成四类 patch | 分支开始写 cinematic 字段 |
| `S5` | `FIELD-WM-08` | 如何把四类 patch 收束成 `beat_patches[]` | 汇流 sidecar | 输出像分析表单，不像 patch |
| `S6` | `FIELD-WM-09` | 如何按模板一次性写回 | 落盘 sidecar | 结构不稳、字段越权 |
| `S7` | `FIELD-WM-09` | sidecar 是否真能交付父层 merge | 跑 validator | ownership 或结构未过 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| `FIELD-WM-01` | 只命中一个 shared root 与 group scope | `FAIL-WM-01` | `S1` |
| `FIELD-WM-02` | `Init / Global` 被压成 factual 约束 | `FAIL-WM-02` | `S2` |
| `FIELD-WM-03` | 每组锚点足以支撑 beat 切分 | `FAIL-WM-03` | `S3` |
| `FIELD-WM-04` | 人物关系可落镜级 factual 字段 | `FAIL-WM-04` | `S4` |
| `FIELD-WM-05` | 走位与连续性不打架 | `FAIL-WM-05` | `S4` |
| `FIELD-WM-06` | 空间与道具状态具体可见 | `FAIL-WM-06` | `S4` |
| `FIELD-WM-07` | `镜头消费提示` 能给镜头抓手 | `FAIL-WM-07` | `S4` |
| `FIELD-WM-08` | factual patch 被收束成合法 `beat_patches[]` | `FAIL-WM-08` | `S5` |
| `FIELD-WM-09` | 模板结构与 validator 同时通过 | `FAIL-WM-09` | `S6/S7` |

## Root-Cause Execution Contract (Mandatory)

出现以下任一情况时，必须先修源层再继续下游：

- `水月` sidecar 越权写 cinematic 字段
- 只剩抽象 prose，没有可 merge factual patch
- `beat_id` 不稳定，导致父层无法对齐
- `出场角色及穿搭` 没有证据却硬填

强制追因链：

`Symptom/Failure -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

## Completion Contract (Mandatory)

只有同时满足以下条件，`水月` 才允许宣布完成：

1. `projects/aigc/<项目名>/3-Detail/水月/第N集.field-patch.json` 已写回。
2. sidecar 不包含 `剧本正文`。
3. sidecar 不包含 cinematic 字段。
4. `group_design_patch.出场角色及穿搭` 与 `beat_patches[]` 至少对命中 group 完整成形。
5. `validate_watermoon_output.py` 返回通过。
