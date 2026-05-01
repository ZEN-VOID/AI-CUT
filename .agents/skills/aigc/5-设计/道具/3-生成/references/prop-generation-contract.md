# Prop Generation Contract

本文件定义 `道具/3-生成` 的业务细则。根 `SKILL.md` 拥有入口、路由和输出合同；本文件只展开道具图像生成规则。

## Upstream Contract

必须消费：

- `projects/aigc/<项目名>/5-设计/道具/2-设计/<主体名称>.md`
- `$imagegen` 的 `SKILL.md + CONTEXT.md`
- 上游设计文档 `## 4. 解构` 下方的 `主体ID号：<主体ID>`；缺失时从文件名前缀或 source row ID 派生，并写入 JSON 的 `subject_id_source`。

可按需消费：

- `projects/aigc/<项目名>/MEMORY.md`
- `projects/aigc/<项目名>/CONTEXT/`
- 用户提供的额外参考图，仅作为风格或形态辅助，不替代上游设计文档。

## Scope Boundary

- 上游 `2-设计` 已经为所有目标道具细目式创建设计文档。
- 本技能只消费相关设计文档，不重新设计主体，不补写研究、物语、解构或新设定。
- 若设计文档缺少可用的 `4. 解构`，必须回到 `2-设计` 修复；不得在本阶段临时主创主体设计。

## Step Requirements

| step | required action | required evidence |
| --- | --- | --- |
| Step1 单主体图 | 用每份设计文档生成单主体图 | `主体ID-主体名称-主图.<ext>` 与 `主体ID-主体名称-主图.json` |
| Step2 多视图 | 套用道具多视图模板，以单主体图为参照图生成多视图主体设计图 | `主体ID-主体名称-多视图.<ext>` 与 `主体ID-主体名称-多视图.json` |

## Prompt Source Rules

- `critical_requirements` 必须忠实引用相应道具/主体设计文档中的 `4. 解构`。
- 导入给 gpt-image-2 的主图提示词和多视图提示词不得再以旧“提示词设计”英文整合 prompt 为主源。
- 允许将上游解构拆成 subject、style、materials、negative、composition 等字段，但不得改变主体身份、材质事实、尺度逻辑、叙事功能或识别点。

## Execution Engine Route

- 普通生成默认且唯一的执行入口是 `.agents/skills/cli/imagegen`，并由该 skill 自己决定内置 `image_gen`、显式 CLI fallback 或其他已确认路径。
- 未获得用户显式 provider / API / model 指令时，不得直接调用 `nano-banana`、Dreamina、AnyFast 子技能或其他图像执行器。
- 只有用户显式选择其他 provider / API / model 控制，才可离开 `.agents/skills/cli/imagegen` 入口；执行报告必须记录该显式指令与所用 provider。
- 项目绑定资产必须最终持久化到 `projects/aigc/<项目名>/5-设计/道具/3-生成/`。

## Non-Goals

- 不创建或修改 `道具/2-设计` 文档。
- 不重新抽取清单，不改父级 registry、routes、runbook。
- 不处理角色或场景生成资产。
- 不把多个不同道具合成一个产品线、合集海报或混合主体图，除非上游设计文档明确该主体本身就是一组套件。
