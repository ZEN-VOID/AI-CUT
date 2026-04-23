# 3-Detail Shared Creative Guidance Contract

## Purpose

本文件定义 `3-Detail` 根技能在当前单技能模式下的创作引导载体：

- `references/路由画像.yaml`
- `references/正反例.md`
- `references/创作评审标尺.md`
- `references/电影学院派知识接线.md`

它们不拥有写回权，只负责：

- 路由偏置
- 正反例校准
- 创作验收口径

## Canonical Scope

- canonical 路径固定为：`.agents/skills/aigc/3-Detail/_shared/creative-guidance-contract.md`
- 当前适用对象：
  - `.agents/skills/aigc/3-Detail/SKILL.md`
  - `.agents/skills/aigc/3-Detail/references/路由画像.yaml`
  - `.agents/skills/aigc/3-Detail/references/正反例.md`
  - `.agents/skills/aigc/3-Detail/references/创作评审标尺.md`
  - `.agents/skills/aigc/3-Detail/references/电影学院派知识接线.md`
  - `.agents/skills/aigc/3-Detail/references/编剧手册.md`
  - `.agents/skills/aigc/3-Detail/references/镜头语言.md`

## Artifact Ownership

### `路由画像.yaml`

- 回答：当前 group 该强调什么策略偏置
- 不替代固定主顺序

### `正反例.md`

- 回答：什么是好写法、坏写法、越权写法、空泛写法

### `创作评审标尺.md`

- 回答：怎么判断字段已达到可消费质量

### `电影学院派知识接线.md`

- 回答：本轮到底读了哪些知识域、为什么读、读完后该落到哪些字段
- 不替代字段写作，只负责 bundle 选择与转译边界

## Usage Rules

1. 先遵守根技能固定顺序，再用 `路由画像.yaml` 做局部偏置。
2. `正反例.md` 和 `创作评审标尺.md` 只能校准和验收，不能替代字段真源。
3. 若 `路由画像.yaml` 的偏置与固定顺序冲突，以固定顺序为准。
4. 两份 playbook 负责承接原 `水月 / 镜花` 的高密度创作方法，供 route、example、rubric 回链，不得自立第二主链。
5. 若本轮实际读取了学院派知识包，`validation-report.md` 必须写出 `knowledge_mode / knowledge_domain / selected_bundles / applied_passes / translation_targets`；若未实际采用，也必须写 `unused_with_reason`。

## Validation Gate

- 创作引导校验入口固定为：`.agents/skills/aigc/3-Detail/scripts/validate_creative_guidance.py`
