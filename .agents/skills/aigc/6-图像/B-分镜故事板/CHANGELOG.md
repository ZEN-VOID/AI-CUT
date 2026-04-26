# Changelog

## 2026-04-25

- 初始化 `B-分镜故事板` Skill 2.0 配置。
- 将主信息源固定为 `projects/aigc/<项目名>/4-分组`。
- 固化用户指定的 multi-panel storyboard 固定英文开头。
- 固化组底 YAML 主体参照绑定规则：角色、场景、道具，多视图优先，主图次之，缺图移除槽位。
- 接入 `.agents/skills/cli/imagegen` 作为默认生图执行技能，并声明按分镜组批量计划、顺序或受控批量生成与项目内持久化门禁。
- 明确 built-in `image_gen` 可按 `text_prompt_only` 生成并持久化；本地 reference path 默认只记录，不等于已作为视觉输入传入模型，需在 results/report 中写明。
