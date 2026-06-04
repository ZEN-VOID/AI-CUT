# 角色 Design Slot Review Contract

slot_bundles:
- id: ROLE-BUNDLE-01
  owner: character-design-review
  required_slots:
  - character_id
  - deconstruction_subject_id
  - identity_evidence
  - visual_drivers
  - aesthetic_appeal
  - corpus_usage_trace
  - costume_design
  - prompt_evidence_chain
  - deconstruction_coverage

Resolver runtime: `scripts/resolve_design_slot_bundles.py`

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| `ROLE-BUNDLE-01` 是否被解析为非空 `slot_bundles` 记录，而不是只保留空数组或跳过 slot bundle review？ | `GATE-CHAR-DESIGN-15` | `FAIL-SLOT-BUNDLE-MISSING` | `N8-REVIEW-GATE` | `slot_bundle_review`、bundle id、解析结果 |
| `character_id` 与 `deconstruction_subject_id` 是否都有证据位置，并能对应文件名前缀、`## 4. 解构`、`## 5. 提示词设计` 与英文 prompt 前缀？ | `GATE-CHAR-DESIGN-11` | `FAIL-CHAR-DESIGN-ID-CONSISTENCY` | `N7-MERGE-DRAFT` / `N9-WRITE-OUTPUT` | ID slot evidence map、四处主体 ID 对照 |
| `identity_evidence / visual_drivers / costume_design` 是否都有证据位置，并能回到研究镜头和解构字段，而非空槽或泛化审美词？ | `GATE-CHAR-DESIGN-06` | `FAIL-RESEARCH-FLAT` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | required slot evidence map、缺槽 finding |
| `aesthetic_appeal` 是否有证据位置，并覆盖容貌、妆发、骨相、身形、服装吸引力、主角强化和明星脸原创转译边界？ | `GATE-CHAR-DESIGN-19` | `FAIL-CHAR-DESIGN-AESTHETIC-APPEAL` | `N7-MERGE-DRAFT` | `aesthetic_appeal` slot evidence map、缺槽 finding |
| `corpus_usage_trace` 是否有证据位置，并说明语料库触发原因、选用 lens、原创转译、服装时代语境和被剔除语料？ | `GATE-CHAR-DESIGN-20` | `FAIL-CHAR-DESIGN-CORPUS-MISSING` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | `corpus_usage_trace` slot evidence map、缺槽 finding |
| `prompt_evidence_chain` 与 `deconstruction_coverage` 是否都有证据位置，并能说明 prompt 关键短语如何从研究和解构压缩而来？ | `GATE-CHAR-DESIGN-08` | `FAIL-CHAR-DESIGN-PROMPT-EVIDENCE` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | `Prompt Evidence Chain`、`deconstruction_coverage`、缺槽 finding |
| `scripts/resolve_design_slot_bundles.py` 是否只做机械解析和校验，没有替代 LLM 生成设计正文或 slot 解释？ | `GATE-CHAR-DESIGN-05` | `FAIL-SCRIPT-AUTHORSHIP` | `N7-MERGE-DRAFT` | resolver 职责说明、脚本输出边界、LLM 汇流声明 |
