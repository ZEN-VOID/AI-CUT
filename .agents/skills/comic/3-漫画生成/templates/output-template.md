# Output Template: 漫画生成

## Output Contract Alignment

| Output Contract field | Template field |
| --- | --- |
| `Required output` | `artifacts`, `saved_files`, `report_path` |
| `Output format` | `formats`, `runtime.output_format` |
| `Output path` | `output_dir`, `paths` |
| `Naming convention` | `filename_scheme`, `saved_files` |
| `Completion gate` | `review.verdict`, `validation` |

## `comic_generation_report.json`

```json
{
  "ok": true,
  "status": "planned-or-generated",
  "mode": "built-in-plan-or-execute",
  "input_json": "projects/comic/<project>/2-九刀流漫画提示词/page-group-01-nine_blade_comic_prompts.json",
  "page_group": {},
  "group_slug": "page-group-01",
  "provider": "built-in-imagegen",
  "runtime": {
    "skill_path": ".agents/skills/cli/imagegen",
    "mode": "built_in_image_gen",
    "batch_execution": "subagents_parallel_default",
    "max_concurrency": 9,
    "resolution_target": "2k_default",
    "resolution_value": "2K",
    "output_format": "png",
    "script_invokes_imagegen": false
  },
  "output_dir": "projects/comic/<project>/3-漫画生成/page-group-01/built-in-imagegen",
  "paths": {
    "handoff_plan": "imagegen_handoff_plan.json",
    "prompt_set": "imagegen_prompt_set.json"
  },
  "filename_scheme": "page01.png .. page09.png",
  "expected_result_count": 9,
  "saved_files": [],
  "validation": {
    "json_validator": "pass",
    "prompt_count": 9,
    "built_in_tool_invoked_by_script": false
  },
  "review": {
    "verdict": "pass_with_todo",
    "notes": []
  }
}
```
