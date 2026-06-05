# Source Detail Incremental Fusion Contract

本文件定义 `8-摄影` 对上游 `7-分镜` 原文的保真和增量注入规则。

## Core Rule

`8-摄影` 只在原有 `分镜N（N-N秒）：原有内容` 后追加运镜手法描述，不替换原有内容，不删除分镜编号，不改秒数，不重排分镜，不改剧情事实。

普通输出格式：

```text
分镜1（0-2秒）：原有内容。镜头从具体机位和角度进入，说明景别/镜头类型、运动方式、运动路径、速度曲线、如何沿既有构图轴线或空间层次运动，以及景深与对焦行为。
```

空间边界：运镜句可以引用 `7-分镜` 中既有的主体位置、前中后景、画面方位、遮挡关系、空间纵深和构图层次，用来说明摄影机如何使用空间；不得新增或改写上游未定义的空间布局。

## Preservation Checks

| check | requirement |
| --- | --- |
| `line_identity` | 分镜编号和时间码原样保留 |
| `original_content` | 冒号后的原有分镜内容完整保留在运镜句之前 |
| `no_story_change` | 不新增剧情事实、角色关系、对白含义、动作结果 |
| `no_spatial_relayout` | 不新增或改写 `7-分镜` 未定义的主体方位、遮挡关系、前中后景或空间纵深，只描述摄影机如何沿既有空间运动 |
| `no_lens_motion_conflation` | 不把推/拉/横移/跟拍/升降写成变焦，不把广角/长焦透视效果写成机位路径 |
| `no_focus_plan_loss` | 不用“焦点接力”替代具体起止焦点、对焦模式、景深策略和必须保持可读的信息 |
| `no_aesthetic_copy` | 不把画面基调或大师参照原句硬贴进分镜正文 |
| `conflict_repair` | 若已有旧运镜与新规则矛盾，只微调运镜句，不动原分镜内容 |

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 原 `7-分镜` 行是否完整保留？ | `GATE-CAM-08-SOURCE-01` | `FAIL-CAM-SOURCE-LOSS` | `N7-CAM-INJECT` | source_line_diff |
| 运镜注入是否只增量追加，不改剧情和对白？ | `GATE-CAM-08-SOURCE-02` | `FAIL-CAM-STORY-OVERREACH` | `N7-CAM-INJECT` | story_fact_diff |
| 运镜注入是否没有重新定义 `7-分镜` 的空间布局？ | `GATE-CAM-08-SPATIAL-BOUNDARY` | `FAIL-CAM-SPATIAL-OVERREACH` | `N6-CAM-MOVEMENT-DESIGN` | source_spatial_boundary_check |
| 运镜注入是否没有混淆镜头运动、焦距变化和透视效果？ | `GATE-CAM-08-LENS-MOTION-BOUNDARY` | `FAIL-CAM-LENS-MOTION-CONFLATION` | `N6-CAM-MOVEMENT-DESIGN` | lens_or_camera_motion_boundary |
| 旧矛盾口径是否只做最小运镜修复？ | `GATE-CAM-08-SOURCE-03` | `FAIL-CAM-CONFLICT-REPAIR` | `R2-CAM-SYNC-REPAIR` | conflict_repair_log |
