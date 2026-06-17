# 角色 Design Slot Review Contract

slot_bundles:
- id: ROLE-BUNDLE-01
  owner: character-design-review
  required_slots:
  - character_id
  - base_subject_id
  - asset_id
  - variant_id
  - variant_label
  - variant_type
  - identity_invariants
  - variant_state_delta
  - deconstruction_subject_id
  - identity_evidence
  - visual_drivers
  - aesthetic_appeal
  - lead_beauty_handsomeness_floor
  - lead_presence_temperament_floor
  - charisma_floor
  - height_scale
  - body_build
  - hair_design
  - costume_color_palette
  - face_readability_lighting
  - corpus_usage_trace
  - costume_design
  - prompt_evidence_chain
  - deconstruction_coverage

Resolver runtime: `scripts/resolve_design_slot_bundles.py`

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| `ROLE-BUNDLE-01` 是否被解析为非空 `slot_bundles` 记录，而不是只保留空数组或跳过 slot bundle review？ | `GATE-CHAR-DESIGN-15` | `FAIL-SLOT-BUNDLE-MISSING` | `N8-REVIEW-GATE` | `slot_bundle_review`、bundle id、解析结果 |
| `character_id`、`base_subject_id`、`asset_id`、`variant_id` 与 `deconstruction_subject_id` 是否都有证据位置，并能对应文件名前缀、`## 4. 解构`、`## 5. 提示词设计` 与英文 prompt 前缀？默认稿是否用 `base_subject_id`，变体稿是否用 `variant_id`？ | `GATE-CHAR-DESIGN-11` / `GATE-CHAR-DESIGN-23` | `FAIL-CHAR-DESIGN-ID-CONSISTENCY` / `FAIL-CHAR-DESIGN-VARIANT-INVARIANT` | `N7-MERGE-DRAFT` / `N9-WRITE-OUTPUT` | ID slot evidence map、base/variant/asset ID 四处对照 |
| `base_subject_id / asset_id / variant_id / variant_label / variant_type` 是否都有证据位置；默认稿是否 `asset_id=base_subject_id`，变体稿是否 `asset_id=variant_id` 并能回指同一 base character？ | `GATE-CHAR-DESIGN-23` | `FAIL-CHAR-DESIGN-VARIANT-INVARIANT` | `N3-CHARACTER-LIST` / `N7-MERGE-DRAFT` | variant slot evidence map、base/variant/asset ID 对照 |
| `identity_invariants / variant_state_delta` 是否说明同一角色跨变体保留什么、此变体只改变什么；是否避免把服装、战损、受伤或年龄阶段写成新人物？ | `GATE-CHAR-DESIGN-23` | `FAIL-CHAR-DESIGN-VARIANT-INVARIANT` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | identity invariant evidence、variant delta evidence、缺槽 finding |
| `identity_evidence / visual_drivers / costume_design` 是否都有证据位置，并能回到研究镜头和解构字段，而非空槽或泛化审美词？ | `GATE-CHAR-DESIGN-06` | `FAIL-RESEARCH-FLAT` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | required slot evidence map、缺槽 finding |
| `aesthetic_appeal / lead_beauty_handsomeness_floor / lead_presence_temperament_floor / charisma_floor` 是否有证据位置，并覆盖来源匹配审美路线、容貌、妆发、骨相、身形、服装吸引力、主角帅/美下限、主角整体气质下限、主角/大反派高魅力下限、真实人物灵感许可与原创转译边界？ | `GATE-CHAR-DESIGN-19` | `FAIL-CHAR-DESIGN-AESTHETIC-APPEAL` | `N7-MERGE-DRAFT` | `aesthetic_appeal`、`lead_beauty_handsomeness_floor`、`lead_presence_temperament_floor`、`charisma_floor` slot evidence map、缺槽 finding |
| `height_scale / body_build / hair_design / costume_color_palette` 是否有证据位置，并覆盖身高档位/安全范围、身形结构、比例重心、发型长度/体量/轮廓/时代职业适配、服装主色/辅色/点缀色和明度/饱和度/冷暖/反差关系？ | `GATE-CHAR-DESIGN-21` | `FAIL-CHAR-DESIGN-PHYSICAL-STYLING` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | `physical_styling` slot evidence map、`Height / Scale Signature`、`Hair Signature`、`Costume Color Signature`、缺槽 finding |
| `face_readability_lighting` 是否有证据位置，并说明面部骨相、眉眼、鼻梁、嘴部、肤色层次和表情意图如何在光线中保持可读，而不是被重阴影、遮眼阴影、半脸阴影或低调剪影吞掉？ | `GATE-CHAR-DESIGN-22` | `FAIL-CHAR-DESIGN-FACE-READABILITY` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | `face_readability_lighting` slot evidence map、`Cinematography / Face Readability Lighting`、prompt 光线短语、缺槽 finding |
| `corpus_usage_trace` 是否有证据位置，并说明语料库触发原因、选用 lens、原创转译、服装时代语境和被剔除语料？ | `GATE-CHAR-DESIGN-20` | `FAIL-CHAR-DESIGN-CORPUS-MISSING` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | `corpus_usage_trace` slot evidence map、缺槽 finding |
| `prompt_evidence_chain` 与 `deconstruction_coverage` 是否都有证据位置，并能说明 prompt 关键短语如何从研究和解构压缩而来？ | `GATE-CHAR-DESIGN-08` | `FAIL-CHAR-DESIGN-PROMPT-EVIDENCE` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | `Prompt Evidence Chain`、`deconstruction_coverage`、缺槽 finding |
| `scripts/resolve_design_slot_bundles.py` 是否只做机械解析和校验，没有替代 LLM 生成设计正文或 slot 解释？ | `GATE-CHAR-DESIGN-05` | `FAIL-SCRIPT-AUTHORSHIP` | `N7-MERGE-DRAFT` | resolver 职责说明、脚本输出边界、LLM 汇流声明 |
