# Character Masterprompt Structured v2

## 输入锚点

- character_id:
- source_row:
- project_style:

## **物语**

- identity_pressure:
- narrative_function:

## **解构**

- subject_id: must equal character_id and appear directly under "## 4. 解构" as "主体ID号：<character_id>"
- identity_evidence:
- visual_drivers:
- aesthetic_appeal:
  - beauty_handsomeness_target:
  - face_bone_aesthetic:
  - costume_appeal_strategy:
  - celebrity_face_inspiration: optional, originalized only, no exact real-person replica
- corpus_usage_trace:
  - corpus_loaded: knowledge-base/character-design-corpus.md
  - trigger_reason:
  - selected_corpus_lenses:
  - originalized_transfer:
  - costume_period_guardrail:
  - rejected_corpus_items:
- detailed_character_design:
- detailed_costume_design:
- cinematography:

## **prompt整合**

- subject_id_prefix: positive_prompt must start with the exact character_id, formatted as "<character_id>: ..."
- prompt_evidence_chain:
- deconstruction_coverage: record how every effective identity_pressure, visual_drivers, aesthetic_appeal, corpus_usage_trace, detailed_character_design, detailed_costume_design and cinematography slot is represented, compressed, merged, or explicitly omitted with reason.
- positive_prompt: must integrate all effective information from "## 4. 解构", not just attach prefix/suffix style phrases; max 1300 characters; must use natural-language negative constraints and must not use Midjourney "--no".
- negative_constraints_natural_language: avoid scene environment, architecture, street, interior set, props cluster, extra characters, crowds, cropped body, sexualized framing
