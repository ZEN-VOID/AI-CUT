# Type Map: 漫画生成

本文件用于在执行前选择固定加载的类型包。`types/` 保存运行时必须固定加载的类型上下文，不替代 `steps/` 的执行拓扑，也不替代 `references/` 的细则。

## Package Index

| type_id | 命中信号 | 加载路径 | 可并用 | 默认 |
| --- | --- | --- | --- | --- |
| `built-in-imagegen-nine-page` | 用户要求生图、默认漫画 3 号执行、需要 `.agents/skills/cli/imagegen` | `types/type-map.md` + `references/imagegen-nine-page-generation.md` | `dry-run-plan`、`execute-built-in` | yes |
| `dry-run-plan` | 未明确执行、需要先看 prompt plan、工具执行不可用 | `templates/output-template.md` | `built-in-imagegen-nine-page` | yes |
| `execute-built-in` | 用户显式 `execute/render/generate images`、要求实际生成图片 | `review/review-contract.md` + `.agents/skills/cli/imagegen/references/mode-routing.md` + `.agents/skills/cli/imagegen/references/output-persistence.md` | `built-in-imagegen-nine-page` | no |
| `legacy-external` | 用户显式指定 CLI/API、`scripts/image_gen.py`、Seedream、Dreamina、AnyFast 或旧 API | legacy references + legacy scripts | no | no |

## Type Profiles

### `built-in-imagegen-nine-page`

- provider: `built-in-imagegen`
- runtime_mode: `built_in_image_gen`
- resolution_target: inherit upstream or `2k_default`
- resolution_value: inherit upstream or `2K`
- output_format: `png`
- execution_shape: 9 distinct built-in image_gen prompts, one page asset per prompt
- batch_execution: `subagents_parallel_default`, max concurrency 10; main-thread serial only by explicit user request
- prompt_policy: preserve upstream `pages[].positive_prompt`; append only execution constraints and project hard constraints
- forbidden: `scripts/image_gen.py`, `generate-batch`, API key prompts, hard model/size/quality controls, one master prompt containing all 9 pages, one prompt generating 9 variants

### `dry-run-plan`

- writes plan/report without calling built-in image_gen
- required artifacts: `imagegen_handoff_plan.json`, `imagegen_prompt_set.json`, `pageXX-imagegen_prompt.txt`, `comic_generation_report.json`
- gate: exactly 9 prompt specs; no image files required

### `execute-built-in`

- requires built-in `image_gen` availability through the agent/tool path, not an API key
- route: one built-in `image_gen` call per prompt, then parent gather/persist
- gate: 9 expected output PNG files exist under the project output directory
- failure handling: do not switch provider silently; report built-in tool blocker or persistence failure

### `legacy-external`

- trigger must be explicit, not inferred from old docs
- CLI path remains external legacy and requires explicit legacy acknowledgement
- Seedream path remains single-request sequential; Dreamina remains per-page queue style
- reports must mark provider as legacy

## Selection Rules

1. Start with `built-in-imagegen-nine-page`.
2. Add `dry-run-plan` unless the user or upstream command explicitly selects execute/render/generate images.
3. Replace `dry-run-plan` with `execute-built-in` only when execution is explicit.
4. Use `legacy-external` only when the user explicitly requests a non-built-in provider or CLI/API path.
