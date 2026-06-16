# Prop Masterprompt Structured v2

## 输入锚点

- prop_id:
- source_row:
- project_style:
- prop_design_corpus: load `knowledge-base/prop-design-corpus.md` when designing aesthetics, cultural/identity/function symbols, craft/structure details, function structure, condition/use state, or prompt phrasing

## **物语**

- narrative_function:
- handling_logic:

## **解构**

- subject_id: must equal prop_id and appear directly under "## 4. 解构" as "主体ID号：<prop_id>"
- source_confidence:
- form:
- material:
- craft:
- design_detail_culture: visible design appeal, unique silhouette, material memory, craft/structure detail, conditional cultural/identity/function symbol or minimal function-led rationale, condition/use state, function structure, and signature detail
- condition_state_policy: decide pristine/new/sealed/clean/polished/maintained/display-grade/used/worn/repaired/oxidized/contaminated state from evidence; do not force scratches, dirt, patina, rust, damage, or aged distress
- prop_corpus_usage_trace: corpus seeds used, original transfer, symbol applicability, period/culture guardrail, and evidence in prompt
- function_logic:
- photography: full-view prop shot, 45-degree view, full prop in view, entire prop fully visible, uncropped full silhouette, prop only, solid color background only, no people, no background elements, no scene environment

## **prompt整合**

- subject_id_prefix: positive_prompt must start with the exact prop_id, formatted as "<prop_id>: ..."
- prompt_evidence_chain:
- deconstruction_coverage: record how every effective Photography and Prop Design slot is represented, compressed, merged, or explicitly omitted with reason.
- positive_prompt: must start with prop_id, integrate all effective information from "## 4. 解构", including design appeal, signature detail, conditional cultural/identity/function symbol or minimal function-led rationale, craft/structure detail, period context guardrail, full-view prop shot, 45-degree view, full prop in view, entire prop fully visible, uncropped full silhouette, prop only, solid color background, no people, no background elements, no scene environment; max 1300 characters; must use natural-language negative constraints and must not use Midjourney "--no".
- negative_constraints_natural_language: avoid people, hands, character, model, body parts, tabletop scene, room set, street, landscape, props cluster, background elements, cropped prop, partial prop, detail-only composition
