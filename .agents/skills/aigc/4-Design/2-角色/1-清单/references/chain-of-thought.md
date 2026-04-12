# Chain Of Thought

## Field Master

| field_id | 输出位置 | 内容要求 | 来源 | fail_code |
| --- | --- | --- | --- | --- |
| FIELD-ROLE-LIST-01 | `roles[]` | 角色 canonical identity、首次出现、出现统计、角色层级 | `分镜明细[].角色及站位和穿搭` | FAIL-ROLE-LIST-01 |
| FIELD-ROLE-LIST-02 | `group_role_map[]` | 每镜角色证据、原始角色文本、场景文本、穿搭片段、`group_id + shot_id` | `分镜组列表[].分镜明细[]` | FAIL-ROLE-LIST-02 |
| FIELD-ROLE-LIST-03 | `roles[].costume_profile` | 角色穿搭主线索和常见变体 | 命中服装关键词的角色子句 | FAIL-ROLE-LIST-03 |
| FIELD-ROLE-LIST-04 | `_manifest.json` | 输入输出路径、统计、告警与产物摘要 | 提取脚本运行结果 | FAIL-ROLE-LIST-04 |

## Thought Pass Map

| step_id | 目标 | 关联字段 | 通过标准 |
| --- | --- | --- | --- |
| S1 | 校验输入 JSON 是否符合 shared director schema 基本结构 | FIELD-ROLE-LIST-02 | 能读取 `分镜组列表[] / 分镜明细[]` |
| S2 | 逐镜提取角色名、穿搭片段和场景证据 | FIELD-ROLE-LIST-02, FIELD-ROLE-LIST-03 | 每镜都有可解释的 `roles` 或 `unknown` |
| S3 | 聚合角色 canonical list 与首次出现信息 | FIELD-ROLE-LIST-01 | `roles[]` 非空且证据可回链 |
| S4 | 生成清单与 manifest 并做统计收口 | FIELD-ROLE-LIST-04 | 输出文件完整且统计一致 |

## Pass Table

| pass_id | 检查项 | 失败码 | rework_entry |
| --- | --- | --- | --- |
| P1 | 输入缺少 `final_output.main_content.分镜组列表` | FAIL-ROLE-LIST-02 | 回到 S1 修输入读取 |
| P2 | `group_role_map[]` 缺 `group_id` 或 `shot_id` | FAIL-ROLE-LIST-02 | 回到 S2 修镜级证据构造 |
| P3 | `roles[]` 为空或全为 `unknown` | FAIL-ROLE-LIST-01 | 回到 S2-S3 修角色抽取与聚合 |
| P4 | `costume_profile` 全部失真或明显串场 | FAIL-ROLE-LIST-03 | 回到 S2 修服装子句绑定 |
| P5 | `_manifest.json` 统计与主清单不一致 | FAIL-ROLE-LIST-04 | 回到 S4 重新收口统计 |
