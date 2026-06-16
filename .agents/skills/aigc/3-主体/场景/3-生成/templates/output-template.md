# Scene Generation Output Template

## Execution Report

````markdown
# 场景生成执行报告

project_root: `projects/aigc/<项目名>`
output_root: `projects/aigc/<项目名>/3-主体/场景/3-生成`
imagegen_mode: `built_in_generate`
reference_context_status: `visible_in_conversation_context | pending_view_image`
review_status: `external_provider | local_checklist`

## Inputs

| subject_id | subject | source_design_document | mode |
| --- | --- | --- | --- |
| {{主体ID}} | {{主体名称}} | `{{source_design_document}}` | {{mode}} |

## Outputs

| subject_id | subject | main_image | main_json | multiview_image | multiview_json | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| {{主体ID}} | {{主体名称}} | `{{主体ID}}-{{主体名称}}-主图.{{ext}}` | `{{主体ID}}-{{主体名称}}-主图.json` | `{{主体ID}}-{{主体名称}}-多视图.{{ext}}` | `{{主体ID}}-{{主体名称}}-多视图.json` | {{verdict}} |

## Review

```yaml
verdict: pass
reviewer: scene-generation-review
review_status: local_checklist
local_checklist:
  findings: []
  repair_actions: []
findings: []
notes: ""
```
````

## Prompt Record Shape

```json
{
  "schema": "aigc.scene_generation.prompt_record/v1",
  "skill_id": "aigc-scene-generation",
  "stage": "3-主体/场景/3-生成",
  "source_design_document": "projects/aigc/<项目名>/3-主体/场景/2-设计/S###-<场景名>.md",
  "subject_id": "<主体ID>",
  "subject_id_source": "source_deconstruction_subject_id | source_filename_prefix",
  "subject_name": "<主体名称>",
  "image_role": "main_image | multiview_sheet",
  "imagegen_mode": "built_in_generate",
  "prompt": "",
  "negative_prompt": "",
  "reference_images": [],
  "reference_context_status": "pending_view_image | visible_in_conversation_context | not_applicable",
  "output_path": "projects/aigc/<项目名>/3-主体/场景/3-生成/<主体ID>-<主体名称>-主图.png",
  "review": {
    "verdict": "pending",
    "notes": ""
  },
  "created_at": "YYYY-MM-DD"
}
```

## LLM-First Authorship Gate

- 本模板只定义报告和 JSON record shape，不生成主图 prompt、多视图 prompt、panel 差异或 `generation_profile`。
- 禁止脚本批量生成、批量插入、正则套句或映射投影 prompt；每个 JSON prompt record 必须由 LLM 基于上游 `4. 解构` 逐条裁决。

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | Report and prompt record cover main image, multi-view image, same-name JSON, source document, imagegen mode, and review status. |
| Output format | Markdown report and JSON prompt records; bitmap image files are referenced by path. |
| Output path | All asset examples point to `projects/aigc/<项目名>/3-主体/场景/3-生成`. |
| Naming convention | Uses fixed `主体ID-主体名称-主图` and `主体ID-主体名称-多视图` stems. |
| Completion gate | Includes source, path, prompt, reference image, reference context status and review fields needed for final gate validation. |
