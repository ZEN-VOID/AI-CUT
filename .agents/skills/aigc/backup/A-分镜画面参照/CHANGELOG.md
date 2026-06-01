# Changelog

## 2026-05-10

- 将 A 分镜画面参照视频时长从固定 15 秒改为组级估算投影：读取 `5-分组` 当前组 `时长估算`，按 4-15 秒范围 clamp 后写入 LibTV batch 和远端提交。

## 2026-05-05

- 将默认视频基础规格收束为 720P、15 秒、16:9；用户显式指定时才覆盖。

## 2026-04-30

- 将 LibTV 视频生成默认路由改为以 `.agents/skills/cli/libTV` 后端默认路由为中心。

## 2026-04-25

- 初始化 `.agents/skills/aigc/8-视频-backup/A-分镜画面参照/` Skill 2.0 配置。
- 固定三步主流程：`5-分组` 完整组内容与四段式 `分镜ID` 映射、`7-图像/A-分镜画面` 镜级图片绑定、LibTV 组级多图参照视频生成。
- 补齐 `SKILL.md`、`CONTEXT.md`、`references/`、`steps/`、`types/`、`review/`、`templates/`、`scripts/`、`knowledge-base/`、`agents/openai.yaml`、`README.md`。
