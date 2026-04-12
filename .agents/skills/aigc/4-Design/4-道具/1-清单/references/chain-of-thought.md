# Chain Of Thought

## 字段主表

| field_id | 输出位置 | 内容要求 | 默认责任脚本 | 失败码 |
| --- | --- | --- | --- | --- |
| FIELD-PROP-LIST-01 | `道具清单.json.group_prop_map[]` | 必须保留 `group_id + shot_id + raw_prop_text + prop_mentions` | `extract_episode_props.py` | FAIL-PROP-EXTRACT |
| FIELD-PROP-LIST-02 | `道具清单.json.props[]` | 必须形成稳定 canonical prop、状态变体与 display 摘要 | `extract_episode_props.py` | FAIL-PROP-AGGREGATE |
| FIELD-PROP-LIST-03 | `道具研究.json.props[]` | 必须形成 evidence、material/function/craft 研究结论与 chronicle | `build_prop_research.py` | FAIL-PROP-RESEARCH |
| FIELD-PROP-LIST-04 | `prop_design_bridge.json.props[]` | 必须形成 structure、material、wear、shot_route、physical_character | `build_prop_research.py` | FAIL-PROP-BRIDGE |
| FIELD-PROP-LIST-05 | 三份 JSON 主产物 | 必须同轮落盘到 `4-Design/4-道具/1-清单/第N集/` | `run_prop_list_pipeline.py` | FAIL-PROP-OUTPUT |

## 情况判定表

| case_id | 触发谓词 | 处理策略 | fallback |
| --- | --- | --- | --- |
| C-PROP-PATH-DRIFT | 输入路径不存在但 `3-Detail <-> 编导` 可互转 | 自动回退同集路径 | 若仍失败则 hard fail |
| C-PROP-NO-PROP | `道具及状态` 为空或命中 no-prop token | 保留空 `prop_mentions` 并继续 | 仅把组记入 `groups_without_props` |
| C-PROP-STATE-MERGED | clause 同时包含器物名与状态词 | 拆成 `prop_name + state` | 若无法拆分则保留 raw clause |
| C-PROP-BRIDGE-FLAT | 研究层缺少设计桥接字段 | 强制补齐 bridge profile | 若仍缺失则 FAIL-PROP-BRIDGE |

## Pass Table

| pass_id | 对应字段 | 验收问题 | 通过条件 | 失败回流 |
| --- | --- | --- | --- | --- |
| PASS-01 | FIELD-PROP-LIST-01 | 是否完成镜头级抽取 | `group_prop_map[]` 可回链到 `group_id + shot_id` | FAIL-PROP-EXTRACT |
| PASS-02 | FIELD-PROP-LIST-02 | 是否形成稳定 prop 聚合 | `props[].canonical_name` 非空，且有 shot/group 锚点 | FAIL-PROP-AGGREGATE |
| PASS-03 | FIELD-PROP-LIST-03 | 是否形成可读研究结论 | 每个 prop 有 `evidence_ledger + attribute_profile + chronicle` | FAIL-PROP-RESEARCH |
| PASS-04 | FIELD-PROP-LIST-04 | 是否能直接给下游设计消费 | 每个 prop 有 `structure_modules + shot_route + physical_character` | FAIL-PROP-BRIDGE |
| PASS-05 | FIELD-PROP-LIST-05 | 输出目录是否正确 | 三份 JSON 同轮落盘 | FAIL-PROP-OUTPUT |
