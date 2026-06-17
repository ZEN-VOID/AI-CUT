# Character Masterprompt Structured v2

## 输入锚点

- character_id:
- base_subject_id:
- asset_id: default uses base_subject_id; variant uses variant_id
- variant_id: default | C###-V##
- variant_label:
- variant_type: default | costume_variant | combat_state | battle_damage_state | injury_state | age_stage | disguise_state | time_jump_state
- source_row:
- project_style:

## **物语**

- identity_pressure:
- narrative_function:

## **解构**

- subject_id: must equal asset_id and appear directly under "## 4. 解构" as "主体ID号：<asset_id>"; default asset_id equals base_subject_id, variant asset_id equals variant_id
- base_subject_id: records the stable character identity for all variants
- variant_state:
  - variant_id:
  - variant_label:
  - variant_type:
  - source_anchor:
  - identity_invariants: face/bone structure, eyes, body proportion, core temperament, signature colors/costume motifs or identity pressure that must remain recognizable
  - state_delta: costume set, combat condition, battle damage, injury, age-stage changes, disguise changes, posture or maintenance changes allowed for this variant
  - forbidden_delta: do not replace the base character identity, do not change into a new canonical character
- identity_evidence:
- visual_drivers:
- aesthetic_appeal:
  - source_fit_aesthetic_target:
  - lead_beauty_handsomeness_floor:
  - lead_presence_temperament_floor:
  - charisma_floor:
  - face_bone_aesthetic:
  - costume_appeal_strategy:
  - celebrity_face_inspiration: default none/generic_only; use real-person inspiration only when explicitly allowed and originalized, no exact real-person replica
- corpus_usage_trace:
  - corpus_loaded: knowledge-base/character-design-corpus.md
  - trigger_reason:
  - selected_corpus_lenses:
  - originalized_transfer:
  - costume_period_guardrail:
  - rejected_corpus_items:
- physical_styling:
  - height_scale: explicit height range or scale category; use inferred when evidence is thin
  - body_build: skeleton, shoulders, neck/back, waistline, limb proportion, weight/mass impression and center of gravity
  - hair_design: length, volume, silhouette, hairline/temple hair, styling or headwear logic, era/occupation fit
  - costume_color_palette: main color, secondary color, accent color, value/saturation, warm/cool contrast, cultural/class/identity meaning
- face_readability_lighting:
  - readable_facial_features: brows, eyes, nose bridge, mouth, bone structure, skin tone and expression remain clear
  - lighting_plan: key light, fill light, rim light or controlled side light; dramatic mood must not hide the face
  - forbidden_shadow: no heavy shadows over eyes or face, no dark face, no low-key silhouette as the main character-design prompt
- detailed_character_design:
- detailed_costume_design:
- cinematography:

## **prompt整合**

- subject_id_prefix: positive_prompt must start with the exact asset_id, formatted as "<asset_id>: ..."; default uses base_subject_id, variant uses variant_id
- prompt_evidence_chain:
- deconstruction_coverage: record how every effective identity_pressure, variant_state, identity_invariants, variant_state_delta, visual_drivers, aesthetic_appeal, lead_beauty_handsomeness_floor, lead_presence_temperament_floor, charisma_floor, corpus_usage_trace, physical_styling, face_readability_lighting, detailed_character_design, detailed_costume_design and cinematography slot is represented, compressed, merged, or explicitly omitted with reason.
- positive_prompt: must integrate all effective information from "## 4. 解构", not just attach prefix/suffix style phrases; max 1300 characters; must use natural-language negative constraints and must not use Midjourney "--no".
- negative_constraints_natural_language: avoid scene environment, architecture, street, interior set, props cluster, extra characters, crowds, cropped body, sexualized framing
