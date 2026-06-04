# AI Video Light Handoff Contract

本文件定义 `9-光影` 如何为后续 AI 视频生成保留可执行光影信息，但不输出视频 prompt、provider 参数、灯位图或设备方案。

## Handoff Principles

- 写可见结果：主体哪里亮、哪里暗、什么材质反光、空气中是否有光束、色温如何变化。
- 写时间变化：光源是否摇曳、扫过、反射、闪烁、被遮挡或逐渐衰减。
- 写稳定边界：避免高频频闪、过密光效、过多实体光源和不可生成的抽象审美词。
- 写与摄影配合：推、拉、横移、跟拍、转焦时，光影如何随镜头变化或保持稳定。

## Forbidden

- 不输出完整视频 prompt。
- 不输出 provider 参数、负面词、采样参数、镜头 JSON、灯位图、灯具型号或摄影器材。
- 不把光影描述压缩成英文标签串。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 是否保留可被下游视频稳定理解的可见光影信息？ | `GATE-LIGHT-09-DYNAMIC` | `FAIL-LIGHT-DYNAMIC-EMPTY` | `N6-LIGHT-DESIGN` | `video_light_payload_table` |
| 是否没有越权输出 prompt、参数或灯位图？ | `GATE-LIGHT-09-BOUNDARY` | `FAIL-LIGHT-DOWNSTREAM-OVERREACH` | `N7-LIGHT-INJECT` | `overreach_scan` |
