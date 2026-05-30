# CHANGELOG

## 2026-05-29

- 初始化 BYKJ `场景提取` 子技能。
- 固定默认输入为 `output/[项目名]/02-剧本处理/`。
- 增加场景标题优先、重复标题处理、缺标题回退和五段式 review gate。
- 增加提取后场景设计规格 JSON，参考 `aigc/7-设计/场景/2-设计` 的空镜、空间设计、摄影和英文提示词约束；canonical 输出改为 `scenes.json`、`scene-extraction-report.json`、`manifest.json`。
