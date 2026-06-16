# Source Incremental Light Injection Contract

本文件定义 `9-光影` 对上游 `7-摄影` 或用户指定文稿的保真和增量注入规则。

`9-光影` 只在原有 `分镜N（N-N秒）：原有内容` 后追加光影美学描述，不替换原有内容，不删除分镜编号，不改秒数，不重排分镜，不改剧情事实、对白、景别、构图或摄影运镜。

## Allowed

- 在句末追加当前分镜专属光影描述。
- 修复已有候选 `9-光影` 稿中明显越权、泛化或缺失的光影句。
- 对 source 中已有矛盾光影描述做最小修复，并在报告中记录。

## Forbidden

- 把原分镜改写成新的剧情句。
- 删除或重写摄影·运镜内容。
- 为了光影效果新增不存在的火源、窗户、屏幕、车灯、雨雪、烟雾或爆炸。
- 输出灯位图、器材参数、图像 prompt 或视频 prompt。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 原分镜编号、秒数、原文和摄影内容是否完整保留？ | `GATE-LIGHT-09-SOURCE` | `FAIL-LIGHT-SOURCE-LOSS` | `N7-LIGHT-INJECT` | `source_preservation_diff` |
| 注入是否只增加光影句而不改剧情？ | `GATE-LIGHT-09-BOUNDARY` | `FAIL-LIGHT-DOWNSTREAM-OVERREACH` | `N7-LIGHT-INJECT` | `overreach_scan` |
