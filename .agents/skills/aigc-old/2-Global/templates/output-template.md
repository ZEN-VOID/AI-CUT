# Output Template Index

This file exists only to satisfy the Skill 2.0 structural validator. It is not a creative business output template and must not be copied into project runtime.

## Output Contract Alignment

### Required output

- Creative business output: `projects/aigc/<项目名>/2-Global/第N集.json`
- Governance sidecar: `projects/aigc/<项目名>/2-Global/validation-report.md`

### Output format

- Creative business output format: JSON
- The JSON must follow `templates/episode-root.template.json`
- The sidecar format is Markdown

### Output path

- `projects/aigc/<项目名>/2-Global/第N集.json`
- `projects/aigc/<项目名>/2-Global/validation-report.md`

### Naming convention

- `第N集.json` uses the same `N` as the current episode planning input.
- Runtime output must not be named `episode_root.json`.

### Completion gate

- The stage is complete only after `第N集.json` is written or patched against `templates/episode-root.template.json` and passes the field gate.
