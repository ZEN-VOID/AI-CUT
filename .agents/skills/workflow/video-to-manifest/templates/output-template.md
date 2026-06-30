# Video Manifest Execution Report

## Output Contract Alignment

- Required output: canonical `视频说明.yaml`, unless this was validate-only or audit-only.
- Output format: YAML `schema_version: 2` plus JSON validation report and Markdown sidecar report.
- Output path: `<target_video_dir>/视频说明.yaml` or the user-provided `manifest_path`.
- Naming convention: manifest file `视频说明.yaml`; evidence under `<work_dir>/`; backups as `视频说明.backup.<YYYYMMDD-HHMMSS>.yaml`.
- Completion gate: fatal validation errors are zero, every written video has media evidence and at least one segment, and consumer handoff notes are present.

## Scope

- target:
- manifest_path:
- work_dir:
- mode:
- videos_processed:
- existing_manifest:
- backup_path:

## Evidence

- material_evidence_json:
- analysis_slice_map:
- frame_dir:
- ffprobe_count:
- frame_count:
- analysis_slice_count:
- evidence_status:

## LLM Authorship Summary

- videos_authored:
- long_videos_pre_sliced:
- diversity_tag_depth_status:
- uncertain_fields:
- needs_review:
- script_authorship_boundary:

## Manifest Writeback

- schema_version:
- retained_video_ids:
- new_video_ids:
- retained_segment_ids:
- new_segment_ids:
- renames_registered:

## Validation

- validation_report:
- fatal_count:
- warning_count:
- verdict:

## Consumer Handoff

- read_phase: N1-INTAKE
- apply_phase: N5-VISUAL-PLAN
- verify_phase: N7-VERIFY
- workflow_ingestion_policy: optional_input_to_asset_evidence
- workflow_batch_diversity_handoff:
  - asset_usage_ledger_expected:
  - fields_for_diversity: semantic_vector / trigger_profile / visual_signature / variation_profile / reuse_profile
  - long_material_policy: analysis_slices are evidence-only; final segments still use original file + start/end
- handoff_notes:
- residual_risks:

## Source Sync Check

- source_trigger:
- synchronized_files:
- validation_result:
