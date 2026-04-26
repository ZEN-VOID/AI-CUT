# Character Generation Contract

本文件展开 `角色/3-生成` 的业务细则。入口、路由和最终输出路径仍以同目录 `SKILL.md` 为准。

## Upstream Consumption

- Canonical input: `projects/aigc/<项目名>/4-设计/角色/2-设计/<角色名>.md`。
- 必需区块：`提示词设计`。
- 推荐读取区块：`名称 / 首次登场 / 原文描述`、`Visual Drivers`、`Detailed Character Design`、`Detailed Costume Design`、`Cinematography`。
- 本技能只消费设计文档，不改写设计文档，不新增 canonical 角色主体。

## Imagegen Dependency

- 生成阶段必须按 `.agents/skills/cli/imagegen/SKILL.md + CONTEXT.md` 的当前合同执行。
- 默认使用 imagegen 的 built-in 生成路径，除非用户明确选择 CLI/API/model controls 或 imagegen 合同另有要求。
- 若无法真实调用 imagegen，允许进入 `prompt_only`，但必须报告阻断原因，并且不得声称图片已生成。
- 项目绑定产物必须持久化到工作区输出目录，不得只保留在临时生成目录。

## Step Outputs

Step1 main image:

- Input: 单角色设计文档中的 `提示词设计`。
- Output image: `<主体名称>-主图.<ext>`。
- Output JSON: `<主体名称>-主图.json`。
- Purpose: 建立角色正向身份、脸、发型、体型、服装主轮廓和整体画风的 continuity anchor。

Step2 multi-view sheet:

- Input: Step1 主图作为 reference image，加上 `templates/character-multiview-prompt-template.json`。
- Output image: `<主体名称>-多视图.<ext>`。
- Output JSON: `<主体名称>-多视图.json`。
- Purpose: 生成同一角色的多视图主体设计图，服务后续资产、服装、镜头和制作审阅。

## Prompt Authorship Boundary

- 主图 JSON 的 `prompt_text` 可以直接采用或轻量包装设计文档 `提示词设计`，但不得新增主体设定。
- 多视图 JSON 的 `critical_requirements` 允许直接引用角色设计文档中的 `提示词设计`，并把该文本作为设计真源。
- 模板负责布局、模块和一致性，不负责创造角色身份、服装事实、时代设定或叙事压力。
- 脚本不得生成 prompt_text；脚本只允许复制、校验、汇总或投影已有 prompt 字段。

## Non-Goals

- 不生成场景、道具、视频、分镜或故事正文。
- 不修复上游 `角色/2-设计` 的创作内容；缺字段时报告上游修复需求。
- 不修改 registry、父级 skill、其他角色/场景/道具技能包。
- 不把多视图设计图做成 3x3 分镜、战斗动作集或泛化海报。
