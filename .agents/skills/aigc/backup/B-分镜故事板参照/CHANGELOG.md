# Changelog

## 2026-05-10

- 将 B 分镜故事板参照视频时长从固定 15 秒改为组级估算投影：读取 `4-分组` 当前组 `时长估算`，按 4-15 秒范围 clamp 后写入 LibTV batch 和远端提交。

## 2026-05-05

- 将默认视频基础规格收束为 720P、15 秒、16:9；用户显式指定时才覆盖。

## 2026-04-30

- 将 LibTV 视频生成默认路由改为以 `.agents/skills/cli/libTV` 后端默认路由为中心。

## 2026-04-25

- 初始化 `.agents/skills/aigc/7-视频-backup/B-分镜故事板参照/` Skill 2.0 包。
- 将新版主流程固定为：
  - step1：读取 `projects/aigc/<项目名>/4-分组`，直接使用现有分镜组内容作为视频 prompt 主体。
  - step2：检查 `projects/aigc/<项目名>/6-图像/B-分镜故事板` 中对应 `group_id` 的故事板图，有图写入 YAML 参照路径，无图保持空引用。
  - step3：按 `.agents/skills/cli/libTV` 规范投影 `libtv_session_with_uploaded_references` / `libtv_session_text_only` 命令，并以分镜组为单位默认后台多线程批量并发执行。
- 添加 Mermaid 拓扑、LibTV batch YAML 模板、review gate、types 分流和经验层上下文。
