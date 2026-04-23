# 3-Detail Shared Node-Pack Contract

## Purpose

本文件是 `3-Detail` 根技能 references 模块的结构真源。

当前不再校验 `1-水月 / 2-镜花` 子技能节点包，而是校验：

- 根技能是否显式回指 references 模块
- `references/能力通道图谱.yaml` 是否定义了固定顺序与字段边界
- `references/思行网络.md` 是否定义了主链和回退门
- `references/模板字段填写指南.md` 是否定义了字段填写规则

## Canonical Scope

- canonical 路径固定为：`.agents/skills/aigc/3-Detail/_shared/node-pack-contract.md`
- 当前适用对象：
  - `.agents/skills/aigc/3-Detail/SKILL.md`
  - `.agents/skills/aigc/3-Detail/references/思行网络.md`
  - `.agents/skills/aigc/3-Detail/references/能力通道图谱.yaml`
  - `.agents/skills/aigc/3-Detail/references/模板字段填写指南.md`
  - `.agents/skills/aigc/3-Detail/references/编剧手册.md`
  - `.agents/skills/aigc/3-Detail/references/镜头语言.md`

## Structural Rules

1. `思行网络.md` 必须给出固定顺序，且明确 `1-分镜构图` 先行。
2. `能力通道图谱.yaml` 必须至少声明：
   - `ordered_passes`
   - `pass_writes`
   - `required_before_projection`
   - `forbidden_overlap`
3. `模板字段填写指南.md` 必须同时覆盖组级字段与镜级字段。
4. `编剧手册.md` 必须吸收原 `1-水月` 的字段级细则，而不是只保留抽象摘要。
5. `镜头语言.md` 必须吸收原 `2-镜花` 的镜头级细则，而不是只保留抽象摘要。
6. 根 `SKILL.md` 只能引用本合同与 references 模块，不得把旧子技能包当成当前主链真源。

## Validation Gate

- 结构校验入口固定为：`.agents/skills/aigc/3-Detail/scripts/validate_node_packs.py`

## Conflict Policy

- 用户显式请求 > 根 `AGENTS.md` / `aigc/3-Detail/SKILL.md` > 本合同 > `references/*.md|*.yaml` > `CONTEXT.md`
