# Legacy Upgrade Matrix: 漫画生成

| source_path | source_section | content_class | target_path | operation | semantic_risk | reference_updates | validation_gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SKILL.md` | 定位 / 默认模型口径 | runtime policy | `SKILL.md`, `references/imagegen-nine-page-generation.md` | rewrite from CLI imagegen to built-in image_gen | high | parent comic skill, stage-2 schema/validator | grep + planner self-test |
| `CONTEXT.md` | CLI imagegen experience | context heuristic | `CONTEXT.md` | rewrite to built-in handoff experience | medium | parent context | manual review |
| `types/type-map.md` | `cli-imagegen-nine-page` | type routing | `types/type-map.md` | replace with `built-in-imagegen-nine-page` | high | `steps/`, `review/` | grep |
| `steps/execution-workflow.md` | `N6/N7` CLI plan/execute | node network | `steps/execution-workflow.md` | replace JSONL/CLI nodes with handoff plan + built-in fan-out + persist nodes | high | `SKILL.md`, planner script | self-test |
| `references/imagegen-nine-page-generation.md` | CLI execution细则 | reference detail | same path | rewrite to built-in image_gen 九页细则 | high | README, template, review | grep |
| `templates/output-template.md` | report runtime | output schema | same path | replace provider/runtime/paths fields | medium | planner script | self-test output shape |
| `review/review-contract.md` | runtime gates | review gate | same path | replace CLI exit/API key gate with built-in route + persistence gate | medium | `SKILL.md` completion gate | manual review |
| former active CLI runner | active CLI runner | script | `scripts/run_legacy_imagegen_cli_comic_generation.py` | demote/rename to explicit legacy external runner | high | README, references, rg refs | grep |
| new planner | active mechanical planner | script | `scripts/prepare_builtin_imagegen_comic_generation.py` | add built-in handoff plan generator | medium | README, references | `--self-test` |
| `agents/openai.yaml` | default prompt | metadata | `agents/openai.yaml` | rewrite to built-in image_gen default | low | none | grep |
| `../2-九刀流漫画提示词/*` | `generation_contract.provider` | upstream schema | stage-2 schema/template/validator/docs | rewrite from `cli-imagegen` to `built-in-imagegen` | high | parent comic skill | validator self-test |
| `../SKILL.md`, `../CONTEXT.md` | stage 3 index | parent route | parent comic files | rewrite stage 3 output/runtime summary | medium | child stage docs | grep |
