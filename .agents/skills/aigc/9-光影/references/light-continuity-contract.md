# Light Continuity Contract

本文件定义 `9-光影` 的光影连续性规则。逐分镜光影注入不是给每条分镜套独立漂亮光效，而是在整集、场景、画面点和分镜行之间建立可延续的光色状态。

## Continuity Checks

- 日夜、室内/室外、天气、火源、屏幕、窗光、门缝、烟雾、雨幕等状态是否前后连贯。
- 主光方向、明暗强度、色温倾向是否在同一空间内突然跳变。
- 角色移动、摄影运动和焦点转移是否能解释光影变化。
- 光影变化是否能承接上一分镜的情绪和空间关系。
- 场景切换时，是否有明确光色差异或过渡理由。

## Repair Rule

连续性失败时，优先最小修复当前分镜光影句，不重写上游摄影稿；如果失败来自 source 自身矛盾，在报告中标记 `source_conflict`，并只做保守光影处理。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 相邻分镜和场景内光色状态是否连续？ | `GATE-LIGHT-09-CONTINUITY` | `FAIL-LIGHT-CONTINUITY-BREAK` | `N4-LIGHT-CONTINUITY` | `light_state_timeline` |
