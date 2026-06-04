# Source Detail Incremental Fusion Contract

本文件定义 `8-摄影` 对上游 `7-分镜` 原文的保真和增量注入规则。

## Core Rule

`8-摄影` 只在原有 `分镜N（N-N秒）：原有内容` 后追加运镜手法描述，不替换原有内容，不删除分镜编号，不改秒数，不重排分镜，不改剧情事实。

普通输出格式：

```text
分镜1（0-2秒）：原有内容。镜头角度（如何变化），镜头类型，镜头速度，焦点（静止或变化）的综合运镜手法。
```

## Preservation Checks

| check | requirement |
| --- | --- |
| `line_identity` | 分镜编号和时间码原样保留 |
| `original_content` | 冒号后的原有分镜内容完整保留在运镜句之前 |
| `no_story_change` | 不新增剧情事实、角色关系、对白含义、动作结果 |
| `no_aesthetic_copy` | 不把画面基调或大师参照原句硬贴进分镜正文 |
| `conflict_repair` | 若已有旧运镜与新规则矛盾，只微调运镜句，不动原分镜内容 |

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 原 `7-分镜` 行是否完整保留？ | `GATE-CAM-08-SOURCE-01` | `FAIL-CAM-SOURCE-LOSS` | `N7-CAM-INJECT` | source_line_diff |
| 运镜注入是否只增量追加，不改剧情和对白？ | `GATE-CAM-08-SOURCE-02` | `FAIL-CAM-STORY-OVERREACH` | `N7-CAM-INJECT` | story_fact_diff |
| 旧矛盾口径是否只做最小运镜修复？ | `GATE-CAM-08-SOURCE-03` | `FAIL-CAM-CONFLICT-REPAIR` | `R2-CAM-SYNC-REPAIR` | conflict_repair_log |
