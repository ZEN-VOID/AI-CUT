# 场景清单思维链细则

## 字段主表

| field_id | 输出位置 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-SCENE-LIST-01 | `metadata / summary` | 输入源、episode、统计信息完整可追溯 | S1-S2 | 输入真源清晰度 | FAIL-SCENE-LIST-01 |
| FIELD-SCENE-LIST-02 | `group_scene_map[]` | 每个镜头都有 `scene_raw -> scene_name -> scene_variant` 映射 | S3-S4 | 镜级提取稳定性 | FAIL-SCENE-LIST-02 |
| FIELD-SCENE-LIST-03 | `scenes[]` | 同一主场景稳定聚合，首次出现与覆盖范围完整 | S5 | 场景聚合稳定性 | FAIL-SCENE-LIST-03 |
| FIELD-SCENE-LIST-04 | `scenes[].variants[]` | 方位/边界变体可追溯到 group / shot | S5 | 变体表达清晰度 | FAIL-SCENE-LIST-04 |
| FIELD-SCENE-LIST-05 | `第N集.json / _manifest.json` | episode 级输出完整可 handoff | S6 | 输出可消费性 | FAIL-SCENE-LIST-05 |

## Think-Think Design Snapshot

1. 先问：上游 episode JSON 壳是否成立。
2. 再问：当前镜头的 `场景及方位` 能否直接作为场景锚点。
3. 再问：是否能稳定拆出 `scene_name`，否则就保守留 raw。
4. 再问：同名主场景是否应聚到同一场景条目。
5. 最后问：当前 episode JSON 是否已经足够给 `2-设计` 继续消费。

## Thought Pass Table

| step_id | field_id | intent | action | failure_signal |
| --- | --- | --- | --- | --- |
| S1 | FIELD-SCENE-LIST-01 | 锁定输入真源 | 校验上游 root file 与 episode_id | shared schema 壳不成立 |
| S2 | FIELD-SCENE-LIST-01 | 建立本轮统计基线 | 统计 group / shot 总数 | 统计与上游分镜数不一致 |
| S3 | FIELD-SCENE-LIST-02 | 抽镜级场景串 | 读取 `场景及方位` 并清洗 | 原句为空或全是噪声 |
| S4 | FIELD-SCENE-LIST-02 | 保守拆主场景与变体 | earliest-marker 拆分或 keep raw | 主场景为空或异常裂变 |
| S5 | FIELD-SCENE-LIST-03 / FIELD-SCENE-LIST-04 | 聚合 episode 级场景表 | 以 `scene_key` 合并，并整理 variants | 同一主场景被分成多个 scene_id |
| S6 | FIELD-SCENE-LIST-05 | 写出可 handoff carrier | 写 `第N集.json`，按需写 `_manifest.json` | 缺 summary / scenes / group_scene_map |

## Pass Table

| field_id | through_standard | fail_code | rework_entry |
| --- | --- | --- | --- |
| FIELD-SCENE-LIST-01 | 输入源路径、episode_id、统计字段完整 | FAIL-SCENE-LIST-01 | 回到 S1-S2 重新校验根文件 |
| FIELD-SCENE-LIST-02 | 每个镜头至少有 1 条场景映射记录 | FAIL-SCENE-LIST-02 | 回到 S3-S4 重新抽取或回退 unknown |
| FIELD-SCENE-LIST-03 | 同一主场景不出现重复 scene_id | FAIL-SCENE-LIST-03 | 回到 S5 调整 scene_key 归一规则 |
| FIELD-SCENE-LIST-04 | 每个变体都能回链到原镜头 | FAIL-SCENE-LIST-04 | 回到 S5 重建 variants 聚合 |
| FIELD-SCENE-LIST-05 | `第N集.json` 可直接交给下游读取 | FAIL-SCENE-LIST-05 | 回到 S6 修补输出壳 |
