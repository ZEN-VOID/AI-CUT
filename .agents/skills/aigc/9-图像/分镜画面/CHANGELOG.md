# Changelog

## 2026-06-15

- 同步 `.agents/skills/cli/imagegen` 更新口径：分镜画面生成阶段统一调用该技能的内置 `image_gen` 路线，`scripts/image_gen.py`、CLI/API/provider 专属控制不作为默认或 fallback 路径。
- 将组级多图拓扑从旧 provider 术语收束为“组级 imagegen 任务包 + 每个 `shot_id` 一个 task spec + `expected_image_count == shot_count`”。
- 批量多任务默认交由 imagegen subagents 并发执行，最大并发数为 `10`；只有用户显式要求时才主线程逐一执行；输出必须持久化到关联项目目录。

## 2026-06-04

- 将项目输出根从旧 `9-图像/A-分镜画面` 收敛为与叶子技能包名一致的 `9-图像/分镜画面`，并同步 `SKILL.md`、模板、README、CONTEXT、references、test prompt 与父级/registry/query 引用。
- 明确画面比例规则：默认 `16:9`；仅当用户显式要求时调整为 `9:16` 或其他比例，并同步 prompt、plan 与报告字段。
- 按新版 Skill 2.0 runtime-spine 规范升级 `A-分镜画面`：主 `SKILL.md` 补齐业务分析、类型路由、节点表、模块矩阵、触发矩阵、量化标准、汇流门、审查绑定、注意力协议、检查点和评估资产。
- 生图拓扑从旧的“完整 prompts 文档前置 + 按 `shot_id` 逐镜串行 imagegen”调整为“每个普通分镜组一次 GPT-IMAGE-2 multi-image task”。
- 组词逻辑改为直接引用 `8-分组` 对应 `## x-y-z` 的完整组稿；组内普通 `分镜N` 数量决定 `n/image_count`，并映射为四段式 `x-y-z-N` 图片。
- 新增任务执行词前缀：明确要求生成 N 张单独图片，禁止 storyboard sheet、collage、grid、multi-panel、contact sheet 或 variants。
- 参照逻辑改为援引组底 YAML 中对应角色、场景、道具主体图，多视图优先，生成前必须 `view_image`。
- 强化同组多图一致性：同一调用共享角色、服装、场景、光影、色调、材质、空间锚点和道具约束。
- 移除 `steps/frame-image-workflow.md` 第二节点真源，并补充 `test-prompts.json` 回归资产。

## 2026-05-22

- 吸收 AI 生图/视频提示词学习：英文 prompt 新增 `scene_frame_identity` 口径，要求先锁定场景/画面/镜头身份，再写主体动作。
- 同步 `SKILL.md`、`prompt-assembly-contract.md`、模板、review 与经验层：光线必须写来源相对位置、照亮对象和阴影/轮廓结果；方向参照必须相对镜头、画面边界或固定锚点。

## 2026-05-01

- 调整批量任务执行程序为两阶段：先为指定范围完整生成并落盘 `第N集-分镜画面-prompts.md`、reference manifest 与 imagegen plan，再按 prompts 文档逐镜串行执行 imagegen；禁止边生图边补写后续 prompt。
- 新增场景参照图视觉风格锁：prompt 组织前必须 `view_image` 场景参照图，额外用图像信息锁定画面风格、光影、色调和氛围，并固定写入“画面风格，光影，色调和氛围与场景参照图保持一致。”及英文等价约束。
- 收紧图片参照选择规则：同一主体如有多视图可选，prompt slot、reference manifest 与 imagegen plan 均优先使用多视图；只有缺少多视图时才退到主图。
- 强化 built-in `image_gen` 本地参照图语义：已绑定本地图片必须先 `view_image` 进入对话上下文，再执行参照图生成；结果记录 `reference_input_status: visible_in_conversation_context`，确无绑定图片时才使用 `no_reference_images_bound`。
- 新增同场景上一画面回看门禁：组织当前分镜 prompt 前，若上一分镜同场景且已有本地生成图，必须先 `view_image` 回看并把空间站位、走位、朝向、遮挡、关键道具相对位置和镜头轴线纳入当前 prompt 连续性约束。
- 收紧批量执行拓扑：整集或多分镜批量生成必须按 `shot_id` 严格串行逐镜执行，禁止并发、后台并行、分片并跑或跳过前镜结果。
- 新增三维空间一致性合同：空间参照不得退化为平面背景复用；同场景分镜必须建立 3D `space_model`，定位角色起点、终点、移动轨迹、视线、遮挡、正反打相对背景面和对话轴线。

## 2026-04-26

- 初始化 `A-分镜画面` Skill 2.0 配置。
- 固化 step1-step4：`8-分组` 镜级提取、英文 prompt 组装、主体图片参照绑定、`.agents/skills/cli/imagegen` 批量生成 handoff。
- 增加 Mermaid 流程图、状态图、输出模板、review gate 与产品侧 `agents/openai.yaml`。
- 明确 built-in `image_gen` 曾可按 `text_prompt_only` 生成并持久化；该口径已由 2026-05-01 的 `view_image` 前置门禁收紧。
