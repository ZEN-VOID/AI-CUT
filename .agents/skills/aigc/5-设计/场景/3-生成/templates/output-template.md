# Scene Generation Output Template

## Execution Report

````markdown
# 场景生成执行报告

project_root: `projects/aigc/<项目名>`
output_root: `projects/aigc/<项目名>/4-设计/场景/3-生成`
imagegen_mode: `built_in_generate`
subagent_status: `real_dispatch | downgraded_local_checklist`

## Inputs

| subject | source_design_document | mode |
| --- | --- | --- |
| {{主体名称}} | `{{source_design_document}}` | {{mode}} |

## Outputs

| subject | main_image | main_json | multiview_image | multiview_json | verdict |
| --- | --- | --- | --- | --- | --- |
| {{主体名称}} | `{{主体名称}}-主图.{{ext}}` | `{{主体名称}}-主图.json` | `{{主体名称}}-多视图.{{ext}}` | `{{主体名称}}-多视图.json` | {{verdict}} |

## Review

```yaml
verdict: pass
reviewer: scene-generation-review
subagent_status: downgraded_local_checklist
downgrade:
  blocked_by: developer
  planned_path: "source-contract-reviewer + continuity-reviewer + json-record-reviewer + persistence-reviewer"
  actual_path: "local checklist in review/review-contract.md"
  reviewers_not_started: []
findings: []
notes: ""
```
````

## Prompt Record Shape

```json
{
  "schema": "aigc.scene_generation.prompt_record/v1",
  "skill_id": "aigc-scene-generation",
  "stage": "5-设计/场景/3-生成",
  "source_design_document": "projects/aigc/<项目名>/4-设计/场景/2-设计/S###-<场景名>.md",
  "subject_name": "<主体名称>",
  "image_role": "main_image | multiview_sheet",
  "imagegen_mode": "built_in_generate",
  "prompt": "",
  "negative_prompt": "",
  "reference_images": [],
  "output_path": "projects/aigc/<项目名>/4-设计/场景/3-生成/<主体名称>-主图.png",
  "review": {
    "verdict": "pending",
    "notes": ""
  },
  "created_at": "YYYY-MM-DD"
}
```

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | Report and prompt record cover main image, multi-view image, same-name JSON, source document, imagegen mode, and review status. |
| Output format | Markdown report and JSON prompt records; bitmap image files are referenced by path. |
| Output path | All asset examples point to `projects/aigc/<项目名>/4-设计/场景/3-生成`. |
| Naming convention | Uses fixed `主体名称-主图` and `主体名称-多视图` stems. |
| Completion gate | Includes source, path, prompt, reference image and review fields needed for final gate validation. |
