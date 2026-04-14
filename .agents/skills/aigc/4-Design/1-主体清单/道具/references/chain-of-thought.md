# Chain Of Thought

共享合同回指：

- 输入消费：`../../_shared/detail-output-consumption-contract.md`
- 对象归一：`../../_shared/object-normalization-contract.md`

## 字段主表

| field_id | 输出位置 | 内容要求 | 默认责任脚本 | 失败码 |
| --- | --- | --- | --- | --- |
| FIELD-PROP-LIST-01 | `道具清单.json.group_prop_map[]` | 必须保留 `group_id + shot_id + raw_prop_text + prop_mentions` | `extract_episode_props.py` | FAIL-PROP-EXTRACT |
| FIELD-PROP-LIST-02 | `道具清单.json.props[]` | 必须形成稳定 canonical prop、状态变体与 display 摘要 | `extract_episode_props.py` | FAIL-PROP-AGGREGATE |
| FIELD-PROP-LIST-03 | `道具研究.json.props[]` | 必须形成 evidence、material/function/craft 研究结论、`narrative_significance` 与 chronicle | `build_prop_research.py` | FAIL-PROP-RESEARCH |
| FIELD-PROP-LIST-04 | `prop_design_bridge.json.props[]` | 必须形成 structure、material、wear、shot_route、physical_character、`narrative_significance` | `build_prop_research.py` | FAIL-PROP-BRIDGE |
| FIELD-PROP-LIST-05 | 三份 JSON 主产物 | 必须同轮落盘到 `4-Design/道具/1-清单/第N集/` | `run_prop_list_pipeline.py` | FAIL-PROP-OUTPUT |

## 情况判定表

| case_id | 触发谓词 | 处理策略 | fallback |
| --- | --- | --- | --- |
| C-PROP-PATH-DRIFT | 输入路径不存在但 `3-Detail <-> 编导` 可互转 | 自动回退同集路径 | 若仍失败则 hard fail |
| C-PROP-NO-PROP | `道具及状态` 为空或命中 no-prop token | 保留空 `prop_mentions` 并继续 | 仅把组记入 `groups_without_props` |
| C-PROP-STATE-MERGED | clause 同时包含器物名与状态词 | 拆成 `prop_name + state` | 若无法稳定命中器物名，则保留空 mention，不把整句回退成 prop |
| C-PROP-NARRATIVE-SPECIAL | 道具承担身份确认、记忆回收或关键动作触发 | 输出 `narrative_significance` 并下沉 `visual_obligation / continuity_guard` | 若证据不足则保守标记为 `background` |
| C-PROP-BRIDGE-FLAT | 研究层缺少设计桥接字段 | 强制补齐 bridge profile | 若仍缺失则 FAIL-PROP-BRIDGE |

## Pass Table

| pass_id | 对应字段 | 验收问题 | 通过条件 | 失败回流 |
| --- | --- | --- | --- | --- |
| PASS-01 | FIELD-PROP-LIST-01 | 是否完成镜头级抽取 | `group_prop_map[]` 可回链到 `group_id + shot_id` | FAIL-PROP-EXTRACT |
| PASS-02 | FIELD-PROP-LIST-02 | 是否形成稳定 prop 聚合 | `props[].canonical_name` 非空，且有 shot/group 锚点，并且不是状态残句 | FAIL-PROP-AGGREGATE |
| PASS-03 | FIELD-PROP-LIST-03 | 是否形成可读研究结论 | 每个 prop 有 `evidence_ledger + attribute_profile + narrative_significance + chronicle` | FAIL-PROP-RESEARCH |
| PASS-04 | FIELD-PROP-LIST-04 | 是否能直接给下游设计消费 | 每个 prop 有 `structure_modules + shot_route + physical_character + narrative_significance` | FAIL-PROP-BRIDGE |
| PASS-05 | FIELD-PROP-LIST-05 | 输出目录是否正确 | 三份 JSON 同轮落盘 | FAIL-PROP-OUTPUT |
