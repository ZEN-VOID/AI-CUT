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
  "mode": "dry-run-or-execute",
  "input_json": "projects/comic/<project>/2-九刀流漫画提示词/page-group-01-nine_blade_comic_prompts.json",
  "page_group": {},
  "group_slug": "page-group-01",
  "provider": "cli-imagegen",
  "runtime": {
    "skill_path": ".agents/skills/cli/imagegen",
    "script": ".agents/skills/cli/imagegen/scripts/image_gen.py",
    "subcommand": "generate-batch",
    "model": "gpt-image-2",
    "size": "1152x2048",
    "quality": "medium",
    "output_format": "png",
    "concurrency": 3
  },
  "output_dir": "projects/comic/<project>/3-漫画生成/page-group-01/imagegen-cli",
  "paths": {
    "generation_plan": "imagegen_generation_plan.json",
    "jobs_jsonl": "imagegen_jobs.jsonl"
  },
  "filename_scheme": "page01.png .. page09.png",
  "expected_result_count": 9,
  "saved_files": [],
  "validation": {
    "json_validator": "pass",
    "job_count": 9,
    "cli_exit_code": null
  },
  "review": {
    "verdict": "pass_with_todo",
    "notes": []
  }
}
```
