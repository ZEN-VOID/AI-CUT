# Type Map: 漫画生成

本文件用于在执行前选择固定加载的类型包。`types/` 保存运行时必须固定加载的类型上下文，不替代 `steps/` 的执行拓扑，也不替代 `references/` 的细则。

## Package Index

| type_id | 命中信号 | 加载路径 | 可并用 | 默认 |
| --- | --- | --- | --- | --- |
| `cli-imagegen-nine-page` | 用户要求生图、默认漫画 3 号执行、需要 `.agents/skills/cli/imagegen` | `types/type-map.md` + `references/imagegen-nine-page-generation.md` | `dry-run-plan`、`execute-cli` | yes |
| `dry-run-plan` | 未明确执行、需要先看 prompt plan、缺少 API key | `templates/output-template.md` | `cli-imagegen-nine-page` | yes |
| `execute-cli` | 用户显式 `--execute`、要求实际生成图片 | `review/review-contract.md` + `.agents/skills/cli/imagegen/references/cli.md` | `cli-imagegen-nine-page` | no |
| `legacy-provider` | 用户显式指定 Seedream、Dreamina、AnyFast 或旧 API | `references/seedream-nine-page-generation.md` + legacy scripts | no | no |

## Type Profiles

### `cli-imagegen-nine-page`

- provider: `cli-imagegen`
- model: `gpt-image-2`
- size: `1152x2048`
- output_format: `png`
- command_shape: one `generate-batch` call with 9 distinct JSONL jobs
- prompt_policy: preserve upstream `pages[].positive_prompt`; append only execution constraints and project hard constraints
- forbidden: `--n 9` for one prompt, one master prompt containing all 9 pages, built-in `image_gen` as default

### `dry-run-plan`

- writes plan/report without network or API key
- required artifacts: `imagegen_generation_plan.json`, `imagegen_jobs.jsonl`, `pageXX-imagegen_prompt.txt`, `comic_generation_report.json`
- gate: exactly 9 jobs; no image files required

### `execute-cli`

- requires `OPENAI_API_KEY`
- command: `.agents/skills/cli/imagegen/scripts/image_gen.py generate-batch`
- gate: CLI exit code 0 and 9 expected output PNG files exist
- failure handling: do not switch provider silently; report missing key or CLI failure

### `legacy-provider`

- trigger must be explicit, not inferred from old docs
- Seedream path remains single-request sequential; Dreamina remains per-page queue style
- reports must mark provider as legacy

## Selection Rules

1. Start with `cli-imagegen-nine-page`.
2. Add `dry-run-plan` unless the user or upstream command explicitly selects execute.
3. Replace `dry-run-plan` with `execute-cli` only when execution is explicit.
4. Use `legacy-provider` only when the user explicitly requests a non-CLI provider.
