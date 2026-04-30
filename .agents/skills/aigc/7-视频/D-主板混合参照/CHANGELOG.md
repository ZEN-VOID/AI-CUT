# Changelog

## 2026-04-30

- 将 Dreamina 视频生成默认模型从 `seedance2.0` 调整为 `seedance2.0_vip`，并把默认分辨率收束为 Seedance 2.0 family 当前 CLI 可用的 `720p`；未显式指定模型时不得静默降级到普通或 fast 队列。

## 2026-04-27

- 初始化 `.agents/skills/aigc/7-视频/D-主板混合参照/` Skill 2.0 包。
- 明确 D 路线含义：在同一个分镜组提示词中合并故事板总参照与主体后缀参照。
- 补齐 `references/`、`steps/`、`review/`、`types/`、`templates/`、`scripts/`、`knowledge-base/` 与 `agents/openai.yaml`。
