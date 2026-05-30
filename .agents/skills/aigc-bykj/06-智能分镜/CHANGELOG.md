# CHANGELOG

## 2026-05-29

- 初始化 `06-智能分镜` 为 BYKJ JSON-first 分镜阶段。
- 整合原 AIGC `5-摄影` 的视觉单元、节拍、镜头时值、摄影语法、AI 视频稳定 payload、连续性、道具准入、对白和高点分镜能力。
- 整合原 AIGC `6-分组` 的约 15 秒生产组、18 秒硬上限、atomic unit、定场镜头、构图分区、画面属性、组间连接件和统计能力。
- 固定输出到 `output/[项目名]/06-智能分镜/`，不写回旧 AIGC runtime。
- 增加 `storyboard.json`、`shot-list.json`、`group-index.json`、`bridge-connectors.json`、`分镜报告.json`、`manifest.json` 输出合同。

## 2026-05-29 补充

- 明确 `06-智能分镜` 同步原 AIGC `6-分组` 的输出规则，而不是同步旧输出路径。
- 扩展 group JSON schema，使其完整承载原 `6-分组` 的场景标题行、定场镜头、画面构图、六分区、画面属性、三项风格行、正文保真、五项 YAML 等价统计和计数边界。
- 扩展 bridge JSON schema，使其完整承载原 `6-分组` 的组间首尾帧连接件字段、禁止字段和计数边界。
- 增加 `AIGC 6-分组 Rule Synchronization Contract` 与对应 review gates。
