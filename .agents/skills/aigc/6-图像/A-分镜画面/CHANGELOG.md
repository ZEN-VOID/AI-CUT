# Changelog

## 2026-04-26

- 初始化 `A-分镜画面` Skill 2.0 配置。
- 固化 step1-step4：`4-分组` 镜级提取、英文 prompt 组装、主体图片参照绑定、`.agents/skills/cli/imagegen` 批量生成 handoff。
- 增加 Mermaid 流程图、状态图、输出模板、review gate 与产品侧 `agents/openai.yaml`。
- 明确 built-in `image_gen` 可按 `text_prompt_only` 生成并持久化；本地 reference path 默认只记录，不等于已作为视觉输入传入模型，需在 results/report 中写明。
