# 3-Detail Shared Creative Guidance Contract

## Purpose

本文件是 `aigc/3-Detail` 阶段共享创作引导包的真源合同。

它统一约束 `水月` 与 `镜花` 如何使用 package-local `route-profile.yaml`、`examples.md` 与 `creative-review-rubric.md` 这些创作指导载体，避免每个子技能各自发明第二套创作引导规则。

## Canonical Scope

- canonical 路径固定为：`.agents/skills/aigc/3-Detail/_shared/creative-guidance-contract.md`
- 适用对象：
  - `.agents/skills/aigc/3-Detail/1-水月/{route-profile.yaml,examples.md,creative-review-rubric.md}`
  - `.agents/skills/aigc/3-Detail/2-镜花/{route-profile.yaml,examples.md,creative-review-rubric.md}`
- 子技能自己的 `module-index.md`、`SKILL.md` 只能回指本合同，不得再回指已删除的 `.agents/skills/aigc/3-Detail/references/creative-guidance-contract.md`

## Artifact Ownership

### `route-profile.yaml`

- 是创作路由真源
- 负责定义：
  - `profile_goal`
  - `default_strategy`
  - `route_profiles`
  - `signal_id`
- 只回答“哪类组型该优先打哪条链/阶段”，不替代节点 schema

### `examples.md`

- 是正反例与风格边界载体
- 负责展示：
  - 什么叫有效 patch
  - 什么叫空泛 prose
  - 什么叫越权写法

### `creative-review-rubric.md`

- 是创作验收载体
- 负责定义：
  - 评审维度
  - 通过/不通过信号
  - 常见返工原因

## Usage Rules

1. 先用 `route-profile.yaml` 决定主链或阶段偏置，再进入具体节点包。
2. `examples.md` 与 `creative-review-rubric.md` 只能辅助校准和验收，不得替代 `module-spec.yaml` 的执行合同。
3. 创作引导层不拥有 shared root 写回权；它只影响子技能内部如何生成更稳定的 patch。
4. 若父层或子层拓扑调整，创作引导层必须同步检查是否仍与实际拓扑一致。

## Validation Gate

- 创作引导校验入口固定为：`.agents/skills/aigc/3-Detail/scripts/validate_creative_guidance.py`
- validator 至少应覆盖：
  - `_shared/creative-guidance-contract.md` 存在
  - 子技能 `SKILL.md` 与 `module-index.md` 已回指本真源
  - `module-index.md` 仍包含 `作用 / 汇流顺序 / 配置真源规则`
  - `route-profile.yaml` 声明必要键和值
  - 父层 `3-Detail/SKILL.md` 未回指已删除叶子，且与 `镜花` 当前 `分镜构图` 先行拓扑一致

## Conflict Policy

- 用户显式请求 > 根 `AGENTS.md` / `aigc/3-Detail/SKILL.md` > 本合同 > 子技能 `route-profile.yaml` / `examples.md` / `creative-review-rubric.md`
