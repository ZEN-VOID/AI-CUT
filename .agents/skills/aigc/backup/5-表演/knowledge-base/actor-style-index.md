# Actor Style Index

本索引用于登记已整理的演员、表演流派或作品级表演风格资料。它是外部资料索引，不是经验层，也不替代 `SKILL.md` 的运行合同。

## Current Entries

当前未登记本地演员风格资料。执行时若用户指名演员或表演流派，应按 `SKILL.md` 的 Context Loading Contract 先记录 `knowledge_base_match=false`，再使用模型已有知识或必要网络检索，并在执行报告中记录来源边界。

## Entry Schema

```yaml
- id: actor_or_style_slug
  display_name: ""
  source_files: []
  usable_dimensions:
    - body_baseline
    - vocal_baseline
    - micro_expression
    - rhythm
    - mask_vs_authentic
  forbidden_misreadings: []
  notes: ""
```
