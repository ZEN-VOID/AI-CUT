# Changelog

## 2026-04-30

- 将 Dreamina 视频生成默认模型从 `seedance2.0fast` 调整为 `seedance2.0_vip`；未显式指定模型时不得静默降级到普通或 fast 队列。

## 2026-04-25

- 初始化 `.agents/skills/aigc/7-视频/B-分镜故事板参照/` Skill 2.0 包。
- 将新版主流程固定为：
  - step1：读取 `projects/aigc/<项目名>/4-分组`，直接使用现有分镜组内容作为视频 prompt 主体。
  - step2：检查 `projects/aigc/<项目名>/6-图像/B-分镜故事板` 中对应 `group_id` 的故事板图，有图写入 YAML 参照路径，无图保持空引用。
  - step3：按 `.agents/skills/cli/dreamina-cli` 规范投影 `multimodal2video` / `text2video` 命令，并以分镜组为单位默认后台多线程批量并发执行。
- 添加 Mermaid 拓扑、Dreamina batch YAML 模板、review gate、types 分流和经验层上下文。
