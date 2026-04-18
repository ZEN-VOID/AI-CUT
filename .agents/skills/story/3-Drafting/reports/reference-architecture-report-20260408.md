# 3-Drafting References 升级报告

## 模式与对象

- 当前模式：`reference-promotion`
- 目标技能：[`3-Drafting/SKILL.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/3-Drafting/SKILL.md)
- 本轮范围：把扁平 `references/` 重构为“step 模块 + craft 模块 + appendix”三级结构

## 根因链路

- Symptom：`3-Drafting/references` 同时混着 step 单文件、craft leaf docs 与 deprecated 入口，根 `SKILL.md` 只能逐文件直连，层级关系不清
- Direct Technical Cause：旧 references 以“单文档直连”扩张，缺少统一模块路由与二级 craft 入口
- Rule Source：`3-Drafting/SKILL.md` 的旧 `References（逐文件引用清单）`
- Meta Rule Source：仓库 `AGENTS.md` 的 canonical source / references governance 合同，以及 `references-update` 的 `reference-promotion` 规范
- Fix Landing Points：
  - 新增 `references/<module>/module-spec.md + CONTEXT.md`
  - 回写根 `SKILL.md` 的 `Reference Loading Guide`
  - 新增 `references/README.md`
  - 将旧 step 单文件降级为 appendix / 迁移入口

## 新层级

### Tier 1：Step Modules

- `step-1-context-contract`
- `step-2-style-pass`
- `step-3-review-gate`
- `step-4-polish-gate`
- `step-5-data-writeback`

### Tier 2：Craft Module

- `writing-craft-catalog`

### Tier 3：Leaf Appendices

- 顶层旧 step 文件：只作为 appendix / migration stub
- `references/writing-craft-catalog/leaf-notes/*.md`：只作为 craft leaf notes，由 `writing-craft-catalog` 统一调度

## 为什么这样分

1. `step-1` 到 `step-5` 的 reference 负责的是“工作流阶段合同”，天然属于 step modules。
2. `writing/*.md` 负责的是“症状型 craft 工法”，天然应该从 step 模块二级路由，而不是在根 `SKILL.md` 逐个直连。
3. 旧单文件还需要保留历史兼容入口，但不能继续作为真源，因此降级为 appendix / migration stub。

## 验收

- [x] 根 `SKILL.md` 已改为模块路由
- [x] `references/README.md` 已给出统一视图
- [x] 每个模块都有 `module-spec.md + CONTEXT.md`
- [x] `writing-craft-catalog` 已接管 craft leaf docs 的统一入口
- [x] 旧 step 单文件已标记为非 canonical appendix / migration stub
