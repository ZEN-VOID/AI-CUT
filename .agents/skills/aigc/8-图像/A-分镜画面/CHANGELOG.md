# Changelog

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
- 固化 step1-step4：`6-分组` 镜级提取、英文 prompt 组装、主体图片参照绑定、`.agents/skills/cli/imagegen` 批量生成 handoff。
- 增加 Mermaid 流程图、状态图、输出模板、review gate 与产品侧 `agents/openai.yaml`。
- 明确 built-in `image_gen` 曾可按 `text_prompt_only` 生成并持久化；该口径已由 2026-05-01 的 `view_image` 前置门禁收紧。
