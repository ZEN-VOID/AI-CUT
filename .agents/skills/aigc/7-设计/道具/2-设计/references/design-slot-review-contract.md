# 道具 Design Slot Review Contract

slot_bundles:
- id: PROP-BUNDLE-01
  owner: prop-design-review
  required_slots:
  - prop_id
  - deconstruction_subject_id
  - source_confidence
  - material_logic
  - function_logic
  - prompt_evidence_chain
  - deconstruction_coverage

Resolver runtime: `scripts/resolve_design_slot_bundles.py`

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| `PROP-BUNDLE-01` 是否被解析为非空 slot bundle，而不是只保留旧审计器兼容标记或空数组？ | `GATE-PROP-DESIGN-SLOT-01` | `FAIL-PROP-DESIGN-SLOT-01` | `N7-REVIEW` | `slot_bundle_review`、bundle id、resolver 输出摘要 |
| `prop_id` 与 `deconstruction_subject_id` 是否都有证据位置，且能与文件名前缀、`## 4. 解构` 主体 ID、提示词主体 ID、英文 prompt 前缀对齐？ | `GATE-PROP-DESIGN-SLOT-01` / `GATE-PROP-DESIGN-06` | `FAIL-PROP-DESIGN-SLOT-01` / `FAIL-PROP-DESIGN-05` | `N7-REVIEW` / `N6-DESIGN` | required slot evidence map、主体 ID 对照表 |
| `source_confidence` 是否记录来源置信度和不确定性，而不是把清单外推断、网络线索或灵感写成确定事实？ | `GATE-PROP-DESIGN-SLOT-01` / `GATE-PROP-DESIGN-09` | `FAIL-PROP-DESIGN-SLOT-01` / `FAIL-PROP-DESIGN-08` | `N7-REVIEW` / `N5-RESEARCH-CHAIN` | `source_confidence` 证据位置、置信度/不确定性标注 |
| `material_logic` 与 `function_logic` 是否分别有证据位置，并能回指研究转译或 Prop Design 字段？ | `GATE-PROP-DESIGN-SLOT-01` / `GATE-PROP-DESIGN-09` | `FAIL-PROP-DESIGN-SLOT-01` / `FAIL-PROP-DESIGN-08` | `N7-REVIEW` / `N5-RESEARCH-CHAIN` | 材料逻辑、功能逻辑证据位置、研究转译链 |
| `prompt_evidence_chain` 与 `deconstruction_coverage` 是否都有证据位置；缺槽是否形成 blocking finding 并回到研究或设计节点？ | `GATE-PROP-DESIGN-SLOT-01` / `GATE-PROP-DESIGN-10` | `FAIL-PROP-DESIGN-SLOT-01` / `FAIL-PROP-DESIGN-09` | `N7-REVIEW` / `N5-RESEARCH-CHAIN` / `N6-DESIGN` | `prompt_evidence_chain`、`deconstruction_coverage`、缺槽 finding 与返工入口 |
| `scripts/resolve_design_slot_bundles.py` 是否只做机械解析和缺槽定位，没有替代 LLM 设计判断或补写创作正文？ | `GATE-PROP-DESIGN-05` / `GATE-PROP-DESIGN-SLOT-01` | `FAIL-SCRIPT-AUTHORSHIP` / `FAIL-PROP-DESIGN-SLOT-01` | `N7-REVIEW` / `N6-DESIGN` | resolver 职责说明、脚本输出范围、LLM 主创声明 |
