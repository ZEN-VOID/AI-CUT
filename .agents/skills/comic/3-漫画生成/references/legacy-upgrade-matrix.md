# Legacy Upgrade Matrix: 漫画生成

| source_path | source_section | content_class | target_path | operation | semantic_risk | reference_updates | validation_gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SKILL.md` | frontmatter / Context Loading | entry contract | `SKILL.md` | rewrite | low | none | skill audit |
| `SKILL.md` | 定位 / 默认模型口径 | runtime policy | `SKILL.md`, `references/imagegen-nine-page-generation.md` | rewrite to CLI imagegen | medium | registry, parent comic skill | self-test + audit |
| `SKILL.md` | 输入合同 / Group Execution Rule | input/output contract | `SKILL.md` | keep and compress | low | none | skill audit |
| `SKILL.md` | 思行网络 / 节点表 | steps | `steps/execution-workflow.md` | move and rewrite | low | SKILL reference table | manual review |
| `SKILL.md` | 单页 Prompt 强约束 | reference detail | `references/imagegen-nine-page-generation.md` | move and adapt | medium | runner prompt compiler | self-test |
| `SKILL.md` | 字段映射 | field mapping | `SKILL.md`, `review/review-contract.md` | split | low | none | skill audit |
| `CONTEXT.md` | built-in image_gen experience | context heuristic | `CONTEXT.md` | rewrite to CLI experience | medium | none | manual review |
| `references/seedream-nine-page-generation.md` | Seedream default note | legacy reference | `references/seedream-nine-page-generation.md` | demote to legacy | low | registry | grep |
| `scripts/run_seedream_comic_generation.py` | legacy runner | script | same path | keep as legacy | low | docstrings to update | self-test unaffected |
| `agents/openai.yaml` | default prompt | metadata | `agents/openai.yaml` | rewrite | low | none | skill audit |
