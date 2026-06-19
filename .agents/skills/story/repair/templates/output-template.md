# Story Repair Report

## Output Contract Alignment

| Output Contract field | Template section |
| --- | --- |
| Required output | `Repair Packet` |
| Output format | Markdown sections with YAML-like lists where useful |
| Output path | `Report Metadata.output_path` |
| Naming convention | `Report Metadata.naming` |
| Completion gate | `Completion Gate` |

## Report Metadata

- `project_root`:
- `output_path`:
- `naming`: `story-repair-YYYYMMDD.md`
- `mode`: `problem_discovery | impact_assessment | repair_plan | execute_repair | audit_only`
- `eval_mode`: `full_test | dry_run | n/a`

## Repair Packet

- `problem_discovery_packet`:
- `target_locality`:
- `change_intent`:
- `canonical_owner`:
- `owning_stage`:
- `owning_stage_repair_packages`:
- `n_a_stage_repair_focus`:
- `creative_engine_note`:
- `writeback_order`:
- `scope_packages_loaded`:
- `loaded_context_manifest`:
- `permission_boundary_check`:

## Impact Map

- `upstream_truth`:
- `same_layer_predecessors`:
- `current_locality`:
- `downstream_existing`:
- `future_constraints`:
- `acceptance_actualization`:
- `project_specific_extensions`:

## Execution Decision Trace

- `business_profile`:
- `type_profile`:
- `attention_anchor`:
- `symptom_to_scope_decision`:
- `symptom_to_stage_package_decision`:
- `stage_package_applicability_decision`:
- `source_owner_decision`:
- `authorship_boundary_decision`:
- `fallback_or_degradation`:

## Module And Gate Evidence

- `module_trigger_manifest`:
- `checkpoint_evidence`:
- `review_gate_findings`:
- `rule_evidence_map`:
- `n_a_justification`:
- `repair_log`:

## Stage Routes

- `source_stage`:
- `drafting_or_polishing_stage`:
- `review_route`:
- `return_route`:

## Audit Result

- `verdict`:
- `findings`:
- `code_reviewer_gate`:

## Changed Files

- `changed_files`:
- `not_changed_by_design`:

## Residual Risks

- `residual_risks`:
- `next_generation_constraints`:

## Completion Gate

- Problem discovery completed or N/A:
- Impact map completed:
- Source owner locked:
- Creative authorship preserved:
- LLM-first authorship checked:
- Review/return handled:
- Residual risks reported:
- Next generation constraints recorded:
