# Prop Generation Contract

本文件定义 `道具/3-生成` 的业务细则。根 `SKILL.md` 拥有入口、路由和输出合同；本文件只展开道具图像生成规则。

## Upstream Contract

必须消费：

- `projects/aigc/<项目名>/3-主体/道具/2-设计/<主体名称>.md`
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

Step2 使用 built-in `image_gen` 时，单主体图是本地图片路径，不是自动可见的视觉输入。执行多视图生成前必须先用 `view_image` 检视对应主图，并标注为 `prop main image / multiview reference`；多视图 JSON 必须记录 `reference_context_status: visible_in_conversation_context`。`prompt_only` 可记录 `pending_view_image`，但不得声称已完成参考图生成。

## Prompt Source Rules

- `critical_requirements` 必须忠实引用相应道具/主体设计文档中的 `4. 解构`。
- 导入给 gpt-image-2 的主图提示词和多视图提示词不得再以旧“提示词设计”英文整合 prompt 为主源。
- 允许将上游解构拆成 subject、style、materials、negative、composition 等字段，但不得改变主体身份、材质事实、尺度逻辑、叙事功能或识别点。

## Execution Engine Route

- 普通生成默认且唯一的执行入口是 `.agents/skills/cli/imagegen`，并由该 skill 自己决定内置 `image_gen`、显式 CLI fallback 或其他已确认路径。
- 未获得用户显式 provider / API / model 指令时，不得直接调用 `nano-banana`、Dreamina、AnyFast 子技能或其他图像执行器。
- 只有用户显式选择其他 provider / API / model 控制，才可离开 `.agents/skills/cli/imagegen` 入口；执行报告必须记录该显式指令与所用 provider。
- 项目绑定资产必须最终持久化到 `projects/aigc/<项目名>/3-主体/道具/3-生成/`。

## Non-Goals

- 不创建或修改 `道具/2-设计` 文档。
- 不重新抽取清单，不改父级 registry、routes、runbook。
- 不处理角色或场景生成资产。
- 不把多个不同道具合成一个产品线、合集海报或混合主体图，除非上游设计文档明确该主体本身就是一组套件。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否为每个目标道具锁定 canonical 上游 `2-设计/<主体名称>.md`，并读取到 `4. 解构` 下方的 `主体ID号` 或可解释的文件名前缀 / source row ID 派生来源？ | `REV-PROP-GEN-01` | `FAIL-PROP-GEN-SOURCE` | `N1-INTAKE` | 报告 `source_design_doc`、`subject_id`、`subject_id_source`、目标主体清单；缺失时写明应回到 `道具/2-设计` 或补充用户输入。 |
| 若上游设计文档缺少可用 `4. 解构`，是否停止生成并路由上游修复，而不是在 `3-生成` 临时主创研究、物语、解构或新设定？ | `REV-PROP-GEN-02` | `FAIL-PROP-GEN-PROMPT-DRIFT` | `N3-MAIN-PROMPT` | 报告缺失的 `source_deconstruction_section`、阻断原因、上游修复目标；不得出现临时补写的主体设定。 |
| 主图 JSON 的 `critical_requirements` / prompt 是否忠实引用 `4. 解构`，只做 imagegen 可执行字段拆分，没有改变主体身份、材质事实、尺度逻辑、叙事功能或识别点，也没有回退使用旧英文整合 prompt？ | `REV-PROP-GEN-02` | `FAIL-PROP-GEN-PROMPT-DRIFT` | `N3-MAIN-PROMPT` | 报告主图 JSON 路径、`source_deconstruction_section` 回指、旧英文 prompt 未使用结论、漂移 finding。 |
| 默认执行入口是否仍为 `.agents/skills/cli/imagegen`，只有在用户显式选择 provider / API / model 时才离开该入口？ | `REV-PROP-GEN-08` | `FAIL-PROP-GEN-EXECUTOR-DRIFT` | `N2-TYPE` | 报告 `imagegen_mode`、执行器名称、用户显式授权原文或 `default_executor: .agents/skills/cli/imagegen`。 |
| Step1 是否产出同 stem 的 `<主体ID>-<主体名称>-主图.<ext>` 与 `<主体ID>-<主体名称>-主图.json`，且资产最终持久化在项目 `3-主体/道具/3-生成/`？ | `REV-PROP-GEN-04` | `FAIL-PROP-GEN-NAMING` | `N4-MAIN-IMAGE` | 报告主图图片路径、主图 JSON 路径、basename 对照、canonical path 存在检查。 |
| 多视图 JSON 是否以对应 Step1 单主体图作为 `reference_image`，没有跨道具复用主图或把多个不同道具合成一个混合主体？ | `REV-PROP-GEN-03` | `FAIL-PROP-GEN-REFERENCE` | `N5-MULTIVIEW-PROMPT` | 报告 `reference_image`、对应 `main_image`、`subject_id` 配对结果、跨主体复用检查。 |
| 真实生成 Step2 前，作为本地路径的主图是否已先通过 `view_image` 检视并标注为 `prop main image / multiview reference`，且多视图 JSON 记录 `reference_context_status: visible_in_conversation_context`？ | `REV-PROP-GEN-07` | `FAIL-PROP-GEN-REFERENCE-CONTEXT` | `N5-MULTIVIEW-PROMPT` | 报告 `reference_context_status`、`view_image` 检视说明、多视图 JSON 路径；`prompt_only` 只能记录 `pending_view_image`。 |
| Step2 是否产出同 stem 的 `<主体ID>-<主体名称>-多视图.<ext>` 与 `<主体ID>-<主体名称>-多视图.json`，并套用当前道具多视图模板而不是重新设计主体？ | `REV-PROP-GEN-10` | `FAIL-PROP-GEN-MULTIVIEW` | `N6-MULTIVIEW-IMAGE` | 报告多视图图片路径、多视图 JSON 路径、模板引用、同一主体/材质/比例/识别点 continuity 复核。 |
| 主图与多视图 JSON 是否都能回指设计文档、`subject_id`、`subject_id_source`、输出图路径和必要参考图信息，保证图像可复跑、可审查？ | `REV-PROP-GEN-11` | `FAIL-PROP-GEN-JSON` | `N3-MAIN-PROMPT` | 报告两份 JSON 路径、必填字段检查、`source_design_doc -> prompt -> output_image` 证据链。 |
| 所有项目绑定资产是否最终持久化到 `projects/aigc/<项目名>/3-主体/道具/3-生成/`，没有只停留在临时目录、`$CODEX_HOME` 或 imagegen provider 输出区？ | `REV-PROP-GEN-05` | `FAIL-PROP-GEN-PERSISTENCE` | `N4-MAIN-IMAGE` | 报告最终 workspace 路径、临时源路径迁移说明、文件存在检查。 |
| `prompt_only` 模式是否只落盘 JSON 和 planned path，并明确 `pending_view_image` / 阻断原因，没有声称主图或多视图已经真实生成？ | `REV-PROP-GEN-09` | `FAIL-PROP-GEN-PROMPT-ONLY-CLAIM` | `N7-REVIEW` | 报告 `mode: prompt_only`、`blocked_reason`、已落盘 JSON、空图片路径或 planned output path。 |
| 本阶段是否没有创建或修改 `道具/2-设计`、父级 registry / routes / runbook、角色或场景生成资产、其他 worker 文件，也没有把不同道具合成合集海报或混合主体图？ | `REV-PROP-GEN-06` | `FAIL-PROP-GEN-WRITE-BOUNDARY` | `N7-REVIEW` | 报告 `changed_files`、输出目录范围、非目标目录无写入结论；若上游明确套件主体，报告对应 source evidence。 |
