# 场景 Design Slot Review Contract

slot_bundles:
- id: SCENE-BUNDLE-01
  owner: scene-design-review
  required_slots:
  - scene_id
  - deconstruction_subject_id
  - period_region_anchor
  - research_brief
  - source_posture
  - visual_translation
  - prompt_evidence_chain
  - deconstruction_coverage

Resolver runtime: `scripts/resolve_design_slot_bundles.py`

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| `SCENE-BUNDLE-01` 是否被解析为非空 slot bundle 记录，而不是停留在 reference 文本或空 bundle 兼容标记？ | `GATE-SCENE-DESIGN-SLOT-01` | `FAIL-SCENE-DESIGN-SLOT-01` | `N7-REVIEW` | 报告记录 resolver 或本地解析结果、bundle id、owner 和非空 slot 列表。 |
| `scene_id`、`deconstruction_subject_id`、`period_region_anchor` 是否分别能回指上游场景主体、解构主体 ID、时间/地域锚点，且 ID 不发生漂移？ | `GATE-SCENE-DESIGN-SLOT-01` | `FAIL-SCENE-DESIGN-SLOT-01` | `N6-DESIGN` | 留下 slot evidence 表，包含场景 ID、解构 ID、prompt 前缀、时间 token、地域 token 的位置。 |
| `research_brief`、`source_posture`、`visual_translation` 是否都有非空证据位置，并能说明研究如何转成可见空间、材质、光线、陈设、构图或 prompt token？ | `GATE-SCENE-DESIGN-SLOT-01` | `FAIL-SCENE-DESIGN-SLOT-01` | `N5-RESEARCH` | 报告列出三个研究槽位的段落位置、缺槽 finding 和需要回写的研究项。 |
| `prompt_evidence_chain` 是否覆盖关键 prompt token，且 `deconstruction_coverage` 明确说明 Scene Design 与 Cinematography 槽位如何进入、合并或被剔除？ | `GATE-SCENE-DESIGN-10` | `FAIL-SCENE-DESIGN-10` | `N6-DESIGN` | 留下 token evidence、`deconstruction_coverage` 摘要、未覆盖 token 或未说明剔除项。 |
| 任一 required slot 缺证据时，review 是否形成 blocking finding，并给出可执行返工入口，而不是直接 `pass_with_followups` 或忽略？ | `GATE-SCENE-DESIGN-SLOT-01` | `FAIL-SCENE-DESIGN-SLOT-01` | `N7-REVIEW` | 报告写明缺槽名、severity、source contract、返工节点和复核结果。 |
