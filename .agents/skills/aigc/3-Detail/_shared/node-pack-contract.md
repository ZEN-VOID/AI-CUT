# 3-Detail Shared Node-Pack Contract

## Purpose

本文件是 `aigc/3-Detail` 阶段共享节点包的真源合同。

它统一约束 `水月` 与 `镜花` 两个子技能在各自 package 内如何组织可执行节点包，避免各自再长出第二套节点包规则。

## Canonical Scope

- canonical 路径固定为：`.agents/skills/aigc/3-Detail/_shared/node-pack-contract.md`
- 适用对象：
  - `.agents/skills/aigc/3-Detail/1-水月/**`
  - `.agents/skills/aigc/3-Detail/2-镜花/**`
- 子技能自己的 `module-index.md`、`SKILL.md` 只能回指本合同，不得再回指已删除的 `.agents/skills/aigc/3-Detail/references/node-pack-contract.md`

## Layer Split

### `module-spec.yaml`

- 是 branch / leaf 节点的执行配置真源
- 至少声明：
  - `module_id`
  - `module_level`
  - `purpose`
  - `triggers`
  - `must_answer`
  - `patch_contract`
  - `merge_policy`
  - `quality_gates`

### `module-guide.md`

- 是节点解释层，不是第二真源
- 负责说明：
  - why
  - anti-pattern
  - 审美尺度
  - 常见误用与回退

### `module-index.md`

- 是子技能内部总索引
- 负责声明：
  - 顶层主链/阶段顺序
  - 汇流顺序
  - ownership 分工
  - 共享真源回链
- 不得替代各节点自己的 `module-spec.yaml`

### `CONTEXT.md`

- 是经验层
- 记录失败模式、修复顺序和可复用 heuristics
- 不得回写节点 schema

## Structural Rules

1. 每个 branch / leaf 目录都必须同时存在 `module-spec.yaml` 与 `module-guide.md`。
2. package-local 模块不得再用 `README.md` 充当唯一规范真源。
3. branch 节点若声明 child modules，必须显式列出 `child_modules.path`，且路径必须以 package root 为基准可解析。
4. 子技能只能在自己的 package 内维护节点包；跨子技能共享规则必须上收 `_shared/`。

## Validation Gate

- 结构校验入口固定为：`.agents/skills/aigc/3-Detail/scripts/validate_node_packs.py`
- validator 至少应覆盖：
  - `_shared/node-pack-contract.md` 存在
  - 子技能 `SKILL.md` 与 `module-index.md` 已回指本真源
  - branch / leaf 的 `module-spec.yaml` / `module-guide.md` 配对完整
  - branch 的 child spec 引用可解析

## Conflict Policy

- 用户显式请求 > 根 `AGENTS.md` / `aigc/3-Detail/SKILL.md` > 本合同 > 子技能 `module-index.md` / `module-spec.yaml` > 子技能 `CONTEXT.md`
