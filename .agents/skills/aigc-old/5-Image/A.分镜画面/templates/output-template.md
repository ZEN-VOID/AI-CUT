# Output Template

## Output Contract Alignment

- Required output: 单帧 request JSON、可选参照绑定三件套、可选 provider handoff 包，以及用户可读闭环说明。
- Output format: Markdown 说明 + JSON/Markdown 业务文件；沿用 `第N集.json`、`_manifest.json`、`match-report.md`、`submit-plan.json`、`submit-brief.md`。
- Output path: `projects/aigc/<项目名>/5-Image/分镜帧/第N集/`、`projects/aigc/<项目名>/5-Image/2-参照引用/<mode>/<source_tranche>/第N集/`、`projects/aigc/<项目名>/5-Image/3-图像生成/<provider>/<source_tranche>/第N集/`。
- Naming convention: `第N集.json`、`_manifest.json`、`match-report.md`、`submit-plan.json`、`submit-brief.md`；`分镜ID` 使用四段式 `episode-scene-group-frame`。
- Completion gate: 命中 mode 的 Pass Table 通过；参照绑定和 handoff 分别通过对应 review gate；Skill 2.0 结构 validator 通过。

## Final Output

```yaml
mode: ""
project: ""
episode: ""
shot_id: ""
executed_nodes: []
skipped_nodes: []
outputs:
  request_json: ""
  reference_bound_json: ""
  reference_manifest: ""
  match_report: ""
  submit_plan: ""
  submit_brief: ""
next_entry: ""
verdict: ""
```

## Evidence

- source_request:
- prompt_gate:
- reference_gate:
- provider_gate:
- output_paths:

## Review Result

- verdict:
- findings:
- rework_entry:
