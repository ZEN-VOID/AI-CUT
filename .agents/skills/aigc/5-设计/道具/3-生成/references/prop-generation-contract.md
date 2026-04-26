# Prop Generation Contract

本文件定义 `道具/3-生成` 的业务细则。根 `SKILL.md` 拥有入口、路由和输出合同；本文件只展开道具图像生成规则。

## Upstream Contract

必须消费：

- `projects/aigc/<项目名>/4-设计/道具/2-设计/<主体名称>.md`
- `$imagegen` 的 `SKILL.md + CONTEXT.md`

可按需消费：

- `projects/aigc/<项目名>/MEMORY.md`
- `projects/aigc/<项目名>/CONTEXT/`
- 用户提供的额外参考图，仅作为风格或形态辅助，不替代上游设计文档。

## Scope Boundary

- 上游 `2-设计` 已经为所有目标道具细目式创建设计文档。
- 本技能只消费相关设计文档，不重新设计主体，不补写研究、物语、解构或新设定。
- 若设计文档缺少可用的“提示词设计”，必须回到 `2-设计` 修复；不得在本阶段临时主创主体设计。

## Step Requirements

| step | required action | required evidence |
| --- | --- | --- |
| Step1 单主体图 | 用每份设计文档生成单主体图 | `主体名称-主图.<ext>` 与 `主体名称-主图.json` |
| Step2 多视图 | 套用道具多视图模板，以单主体图为参照图生成多视图主体设计图 | `主体名称-多视图.<ext>` 与 `主体名称-多视图.json` |

## Prompt Source Rules

- `critical_requirements` 必须忠实引用相应道具/主体设计文档中的“提示词设计”。
- 用户原始口径允许直接引用“相应角色设计文档中的提示词设计”；本技能应用到道具生成时，统一解释为“相应道具/主体设计文档中的提示词设计”。
- 允许将上游提示词拆成 subject、style、materials、negative、composition 等字段，但不得改变主体身份、材质事实、尺度逻辑、叙事功能或识别点。

## Imagegen Route

- 普通生成默认使用 `$imagegen` 的内置 `image_gen` 路由。
- 只有用户显式选择 CLI/API/model 控制、真实透明背景或其他 `$imagegen` 合同允许的场景，才可进入 CLI fallback。
- 项目绑定资产必须最终持久化到 `projects/aigc/<项目名>/4-设计/道具/3-生成/`。

## Non-Goals

- 不创建或修改 `道具/2-设计` 文档。
- 不重新抽取清单，不改父级 registry、routes、runbook。
- 不处理角色或场景生成资产。
- 不把多个不同道具合成一个产品线、合集海报或混合主体图，除非上游设计文档明确该主体本身就是一组套件。
