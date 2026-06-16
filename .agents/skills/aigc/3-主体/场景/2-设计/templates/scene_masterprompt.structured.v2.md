# Scene Masterprompt Structured v2

## 输入锚点

- scene_id:
- source_row:
- project_style:
- period_region_anchor:
- space_style_anchor:

## **物语**

- narrative_pressure:
- spatial_story:

## **解构**

- subject_id: must equal scene_id and appear directly under "## 4. 解构" as "主体ID号：<scene_id>"
- research_brief:
- source_posture:
- uncertainty_register:
- visual_translation:
- scene_design:
- cinematography:

## **prompt整合**

- subject_id_prefix: positive_prompt must start with the exact scene_id, formatted as "<scene_id>: ..."
- integration_scope: positive_prompt must integrate all effective information from the full "解构" section, including scene_design and cinematography; it is incomplete if it only adds prefix/suffix tokens such as scene_id, style, period, region, or no-people constraints.
- deconstruction_coverage: record how each effective scene_design/cinematography slot is represented, compressed, merged, or explicitly omitted with reason.
- prompt_evidence_chain:
- prompt_evidence_chain.space_style_token:
- positive_prompt:
- negative_prompt:
