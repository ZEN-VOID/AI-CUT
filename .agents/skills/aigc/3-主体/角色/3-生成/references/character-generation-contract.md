# Character Generation Contract

本文件展开 `角色/3-生成` 的业务细则。入口、路由和最终输出路径仍以同目录 `SKILL.md` 为准。

## Upstream Consumption

- Canonical input: `projects/aigc/<项目名>/3-主体/角色/2-设计/<角色名>.md`。
- 必需区块：`4. 解构`。
- 必需主体 ID：优先读取 `## 4. 解构` 下方的 `主体ID号：<主体ID>`；缺失时从设计文件名前缀 `C###` 派生，并在 JSON 中记录 `subject_id_source`。
- 推荐读取区块：`名称 / 首次登场 / 原文描述`、`Visual Drivers`、`Detailed Character Design`、`Detailed Costume Design`、`Cinematography`。
- 本技能只消费设计文档，不改写设计文档，不新增 canonical 角色主体。

## LibTV Canvas Image Dependency

- 生成阶段必须按 `.agents/skills/cli/libTV/SKILL.md + CONTEXT.md` 的当前合同执行。
- 默认使用 libTV 画布 `image` 节点路径，除非用户明确选择 provider/API/model controls 或 libTV 合同另有要求。
- 若无法真实调用 libTV，允许进入 `prompt_only`，但必须报告阻断原因，并且不得声称图片已生成。
- 项目绑定产物必须持久化到工作区输出目录，不得只保留在临时生成目录。
- 普通新主体默认模型为 `Midjourney V8.1`；执行前必须解析画布 UUID 和 modelKey，并拼接角色图 `--ar 9:16 --hd --style raw` 后缀。
- 生成前必须扫描 `projects/aigc/<项目名>/3-主体`：同主体同状态已有图则跳过生成；本地已有图仅在当前画布缺同名节点时上传为画布同名节点；同主体新状态必须用 `Lib Image` 和既有参考图生成带状态后缀的变体。
- 第 N 集画布上生成或复用的角色主图/多视图节点必须用 `libtv download` 同步到 `projects/aigc/<项目名>/3-主体/角色/3-生成/`，或证明本地 canonical 文件已存在。

## Step Outputs

Step1 main image:

- Input: 单角色设计文档中的 `4. 解构`。
- Output image: `<主体ID>-<主体名称>-主图.<ext>`。
- Output JSON: `<主体ID>-<主体名称>-主图.json`。
- Purpose: 建立角色正向身份、脸、发型、体型、服装主轮廓和整体画风的 continuity anchor。

Step2 multi-view sheet:

- Input: Step1 主图作为 reference image，加上 `templates/character-multiview-prompt-template.json`。
- Output image: `<主体ID>-<主体名称>-多视图.<ext>`。
- Output JSON: `<主体ID>-<主体名称>-多视图.json`。
- Purpose: 生成同一角色的多视图主体设计图，服务后续资产、服装、镜头和制作审阅。
- libTV same-canvas image node gate: Step1 主图必须是当前 libTV 画布中的同名图片节点；若主图只在本地，先用 `libtv upload "<节点名>" -p <canvas_uuid> -f <local_path>` 上传。多视图 JSON 必须记录 `reference_node_name` 与 `reference_context_status: linked_in_libtv_canvas`。`prompt_only` 可记录 `pending_libtv_node_reference`，但不得声称已完成参考图生成。

## Prompt Authorship Boundary

- 主图 JSON 的 `prompt_text` 必须直接采用或轻量包装设计文档 `4. 解构`，但不得新增主体设定；不得继续使用旧 `提示词设计` 英文整合 prompt 作为 Midjourney V8.1 或 Lib Image 导入源。
- 多视图 JSON 的 `critical_requirements` 允许直接引用角色设计文档中的 `4. 解构`，并把该文本作为设计真源。
- 模板负责布局、模块和一致性，不负责创造角色身份、服装事实、时代设定或叙事压力。
- 脚本不得生成 prompt_text；脚本只允许复制、校验、汇总已有 prompt 字段，不得批量生成、批量插入、正则套句或映射投影创作提示词。

## Non-Goals

- 不生成场景、道具、视频、分镜或故事正文。
- 不修复上游 `角色/2-设计` 的创作内容；缺字段时报告上游修复需求。
- 不修改 registry、父级 skill、其他角色/场景/道具技能包。
- 不把多视图设计图做成 3x3 分镜、战斗动作集或泛化海报。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否为每个目标角色锁定 canonical 上游 `2-设计/<角色名>.md`，并读取到 `4. 解构` 与可追溯 `主体ID号` 或 `C###` 派生来源？ | `GATE-CHAR-GEN-01` | `FAIL-SOURCE-LINK` | `N2-DESIGN` | 报告 `source_design_path`、`source_deconstruction_section`、`subject_id`、`subject_id_source`；缺失时写明上游 `角色/2-设计` 修复目标。 |
| 主图 JSON 的 `prompt_text` 是否只直接采用或轻量包装 `4. 解构`，没有新增身份、服装、时代、气质或叙事事实，也没有回退使用旧 `提示词设计` 英文整合 prompt？ | `GATE-CHAR-GEN-02` | `FAIL-PROMPT-DRIFT` | `N3-MAIN-JSON` | 报告主图 JSON 路径、`prompt_source: source_deconstruction_section`、旧英文 prompt 未使用结论和漂移 finding。 |
| 默认执行器是否仍锁定 `.agents/skills/cli/libTV`，未获用户本轮显式授权时没有切到 nano-banana、seedream、AnyFast 或其他图像 API？ | `GATE-CHAR-GEN-10` | `FAIL-EXECUTOR-DRIFT` | `N1-INTAKE` | 报告 `libtv_canvas_mode`、执行器名称、用户授权原文或 `default_executor: .agents/skills/cli/libTV`。 |
| 是否在生成前扫描 `projects/aigc/<项目名>/3-主体` 并保护同主体同状态资产？ | `GATE-CHAR-GEN-12` | `FAIL-ASSET-REUSE` | `N9-RECONCILE` | 报告 `asset_reuse_decision`、`existing_asset_path`、`generation_skipped`、`canvas_action`；仅当当前画布缺同名节点且发生上传时记录上传节点名。 |
| 角色主体图是否已确保存在于项目 `角色/3-生成/`？ | `GATE-CHAR-GEN-14` | `FAIL-CHAR-GEN-LOCAL-SYNC` | `N4-MAIN-IMAGE` / `N6-MULTIVIEW-IMAGE` | 报告 `local_sync_required`、`local_sync_action`、`local_sync_status`、`local_asset_path`、下载分支的 `download_command` / `download_stdout_path`，并检查本地文件 stem 与 libTV 节点名一致；本地 canonical 已有时允许 `already_present`。 |
| 同主体新状态是否使用 `Lib Image`、既有参考图和状态后缀命名？ | `GATE-CHAR-GEN-13` | `FAIL-STATE-VARIANT` | `N9-RECONCILE` / `N4-MAIN-IMAGE` | 报告 `generation_model_policy: lib_image_state_variant`、`variant_model_key`、`state_variant_suffix`、`base_reference_node_name`。 |
| 若 libTV 无法真实生成，是否进入 `prompt_only` 并清楚报告阻断原因，而不是声称图片已生成？ | `GATE-CHAR-GEN-07` | `FAIL-PROMPT-ONLY-CLAIM` | `N7-REVIEW` | 报告 `mode: prompt_only`、`blocked_reason`、空图片路径或 planned path，并列出已落盘 JSON。 |
| 真实生成模式下，主图是否以 `<主体ID>-<主体名称>-主图.<ext>` 存在于 `projects/aigc/<项目名>/3-主体/角色/3-生成/`，并可作为 continuity anchor？ | `GATE-CHAR-GEN-03` | `FAIL-MAIN-IMAGE` | `N4-MAIN-IMAGE` | 报告 `main_image_path`、文件存在检查、主图 JSON 的 `output_image_path`。 |
| 主图与多视图 JSON / 图片命名是否都遵守 `<主体ID>-<主体名称>-主图/多视图`，且 JSON 中 `subject_id` 与文件名前缀一致？ | `GATE-CHAR-GEN-06` | `FAIL-NAMING` | `N7-REVIEW` | 报告四类产物路径、basename 对照、`subject_id` 一致性检查。 |
| 多视图 JSON 是否以 Step1 主图作为 `reference_image_path`，且没有跨角色复用参照图？ | `GATE-CHAR-GEN-04` | `FAIL-REFERENCE` | `N5-MULTIVIEW-JSON` | 报告 `reference_image_path`、对应 `main_image_path`、角色名/subject_id 配对结果。 |
| 真实生成多视图前，对应主图是否已是同一 libTV 画布中的图片节点，且 JSON / 报告记录 `reference_context_status: linked_in_libtv_canvas`？ | `GATE-CHAR-GEN-09` | `FAIL-REFERENCE-CONTEXT` | `N5-MULTIVIEW-JSON` | 报告 `reference_node_name`、`reference_context_status`、多视图 JSON 路径。 |
| 真实生成模式下，多视图图片是否以 `<主体ID>-<主体名称>-多视图.<ext>` 存在于 canonical 输出目录？ | `GATE-CHAR-GEN-05` | `FAIL-MULTIVIEW-IMAGE` | `N6-MULTIVIEW-IMAGE` | 报告 `multiview_image_path`、文件存在检查、多视图 JSON 的 `output_image_path`。 |
| 多视图模板是否只负责布局、模块和一致性，没有创造或覆盖角色身份、服装事实、时代设定或叙事压力？ | `GATE-CHAR-GEN-02` | `FAIL-PROMPT-DRIFT` | `N5-MULTIVIEW-JSON` | 报告多视图 JSON 的 `critical_requirements` 来源、`4. 解构` 回指和模板边界 finding。 |
| 本阶段是否没有修改上游 `2-设计`、registry、父级 skill、场景/道具/视频/分镜目录，也没有把多视图做成 3x3 分镜、战斗动作集或泛化海报？ | `GATE-CHAR-GEN-08` | `FAIL-WRITE-BOUNDARY` | `N7-REVIEW` | 报告 `changed_files`，并确认全部位于 `projects/aigc/<项目名>/3-主体/角色/3-生成/` 或允许的执行报告路径。 |
| 脚本是否只承担复制、校验或汇总已有字段，没有生成、改写、批量插入、正则套句或映射投影 `prompt_text` 创作正文？ | `GATE-CHAR-GEN-11` | `FAIL-SCRIPT-AUTHORSHIP` | `N3-MAIN-JSON` | 报告脚本使用范围、生成 prompt 的 LLM/source owner、无脚本主创结论。 |
