# Changelog

## 2026-05-10

- 将 D 主板混合参照视频时长从固定 15 秒改为组级估算投影：读取 `4-分组` 当前组 `时长估算`，按 4-15 秒范围 clamp 后写入 LibTV submit plan 和远端提交。

## 2026-05-05

- 将默认视频基础规格收束为 720P、15 秒、16:9；用户显式指定时才覆盖。

## 2026-04-30

- 将 LibTV 视频生成默认路由改为以 `.agents/skills/cli/libTV` 后端默认路由为中心，并把默认分辨率收束为 LibTV 当前可用的视频输出设置。

## 2026-04-27

- 初始化 `.agents/skills/aigc/7-视频-backup/D-主板混合参照/` Skill 2.0 包。
- 明确 D 路线含义：在同一个分镜组提示词中合并故事板总参照与主体后缀参照。
- 补齐 `references/`、`steps/`、`review/`、`types/`、`templates/`、`scripts/`、`knowledge-base/` 与 `agents/openai.yaml`。
