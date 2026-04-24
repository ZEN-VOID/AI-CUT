# 3-Detail Shared Node-Pack Contract

## Purpose

本文件是 `3-Detail` 根技能节点包与兼容 references 模块的结构合同。

当前不再校验 `1-水月 / 2-镜花` 子技能节点包，而是校验：

- 根技能是否显式回指 Skill 2.0 `steps/` 节点真源与兼容 references 模块
- `references/能力通道图谱.yaml` 是否定义了固定顺序与字段边界
- `steps/detail-thinking-action-workflow.md` 是否定义了主链、回退门与汇流点
- `references/思行网络.md` 是否继续作为旧校验器和既有引用的兼容入口
- `references/模板字段填写指南.md` 是否定义了字段填写规则
- `references/incremental-patch-playbook.md` 是否定义了局部 patch scope 与返工入口

## Canonical Scope

- canonical 路径固定为：`.agents/skills/aigc/3-Detail/_shared/node-pack-contract.md`
- 当前适用对象：
  - `.agents/skills/aigc/3-Detail/SKILL.md`
  - `.agents/skills/aigc/3-Detail/steps/detail-thinking-action-workflow.md`
  - `.agents/skills/aigc/3-Detail/references/思行网络.md`
  - `.agents/skills/aigc/3-Detail/references/能力通道图谱.yaml`
  - `.agents/skills/aigc/3-Detail/references/模板字段填写指南.md`
  - `.agents/skills/aigc/3-Detail/references/编剧手册.md`
  - `.agents/skills/aigc/3-Detail/references/镜头语言.md`
  - `.agents/skills/aigc/3-Detail/references/incremental-patch-playbook.md`

## Structural Rules

1. `steps/detail-thinking-action-workflow.md` 必须给出固定顺序、节点证据、返工入口和唯一汇流点。
2. `references/思行网络.md` 必须保留 `1-分镜构图` 先行规则，作为兼容 reference 入口。
3. `能力通道图谱.yaml` 必须至少声明：
   - `ordered_passes`
   - `pass_writes`
   - `required_before_projection`
   - `forbidden_overlap`
4. `模板字段填写指南.md` 必须同时覆盖组级字段与镜级字段。
5. `编剧手册.md` 必须吸收旧字段级细则，而不是只保留抽象摘要。
6. `镜头语言.md` 必须吸收旧镜头级细则，而不是只保留抽象摘要。
7. `incremental-patch-playbook.md` 必须把 `group_scope / shot_scope / field_scope / closure_scope` 与返工入口对应起来。
8. 根 `SKILL.md` 只能引用本合同、`steps/` 与 references 模块，不得把旧子技能包当成当前主链真源。

## Validation Gate

- 结构校验入口固定为：`.agents/skills/aigc/3-Detail/scripts/validate_node_packs.py`

## Conflict Policy

- 用户显式请求 > 根 `AGENTS.md` / `aigc/3-Detail/SKILL.md` > 本合同 > `references/*.md|*.yaml` > `CONTEXT.md`
