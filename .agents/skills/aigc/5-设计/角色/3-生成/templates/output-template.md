# 角色 3-生成执行报告

project: `projects/aigc/<项目名>/`
output_root: `projects/aigc/<项目名>/4-设计/角色/3-生成/`

## Targets

| 主体名称 | source_design_path | mode | verdict |
| --- | --- | --- | --- |
| {{主体名称}} | {{source_design_path}} | {{real_generation_or_prompt_only}} | {{verdict}} |

## Deliverables

| 主体名称 | 主图 | 主图 JSON | 多视图 | 多视图 JSON |
| --- | --- | --- | --- | --- |
| {{主体名称}} | {{main_image_path}} | {{main_prompt_json_path}} | {{multiview_image_path}} | {{multiview_prompt_json_path}} |

## Imagegen Notes

- imagegen mode: {{imagegen_mode}}
- reference image for multiview: {{reference_image_path}}
- blocked reason, if any: {{blocked_reason}}

## Review Verdict

```yaml
verdict: pending
findings: []
subagent_status: ""
notes: ""
```

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 本模板汇总每个角色的一张主图、一张多视图图和两份同名 JSON prompt 文件。 |
| Output format | 图片产物由 imagegen 生成；JSON prompt 使用 `character-main-image-prompt-template.json` 与 `character-multiview-prompt-template.json`；报告为 Markdown。 |
| Output path | Canonical 路径为 `projects/aigc/<项目名>/4-设计/角色/3-生成/`。 |
| Naming convention | 主图为 `<主体名称>-主图`，多视图为 `<主体名称>-多视图`，JSON 同名。 |
| Completion gate | source design 可回链；真实生成模式下图片存在；多视图引用对应主图；prompt-only 模式阻断原因清楚。 |
