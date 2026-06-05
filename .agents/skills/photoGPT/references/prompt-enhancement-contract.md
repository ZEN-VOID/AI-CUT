# Prompt Enhancement Contract

本文件定义 `photoGPT` 从用户自然语言到 `gpt-image-2` 可执行提示词的强化规则。

## Canonical Prompt Plan

每次强化都先产出以下结构，再决定是否调用 imagegen：

```yaml
photoGPT_prompt_plan:
  type_profile:
    edit_family: ""
    edit_subtype: ""
    template_path: ""
    image_role_schema: ""
    output_mode: prompt_only | imagegen_execute
  image_roles:
    edit_target: ""
    reference_images: []
  preserve_scope: []
  change_scope: []
  final_prompt: ""
  negative_constraints: []
  imagegen_handoff:
    skill: ".agents/skills/cli/imagegen"
    model: gpt-image-2
    mode: gpt_image_2_generate | gpt_image_2_edit | prompt_only
```

## Prompt Strengthening Rules

1. 先锁定图片角色，再写提示词。多图任务必须明确“图一/图二/图三”的语义。
2. 用 `change_scope` 表示允许变化的区域；用 `preserve_scope` 表示严禁漂移的身份、姿态、构图、服装、背景或材质。
3. 每个模板都必须包含至少一条负面约束，避免模型把编辑任务误解成全面重绘。
4. 用户没有要求风格化时，默认追求自然、真实、保留原图叙事。
5. 多视图设计页必须固定 layout grammar，不得只写“多角度展示”。
6. 多图融合必须采用“逐图角色分配”，不得把多张参考图平均混合成含糊风格池。
7. 多镜头必须锁定参照图画面风格、构图元素、主体信息、场景事实和叙事瞬间，只允许变化景别、机位、镜头视角、裁切范围和前中后景强调。
8. 风格化必须声明风格作用范围：`风格迁移` 可改变视觉语言，`滤镜` 只改变色彩、影调和后期质感。
9. 角色多视图默认使用“面部放大版”：顶部为面部高清放大特写，底部为全身正面、侧面、背面三视图；只有用户显式要求多细节、细节界面、UI 面板或表情/手势/配饰模块时，才进入“多细节界面版”。
10. 角色多视图、换装、换角色、换脸等涉及保留角色形象不变的任务，必须明确写入“保留原角色形象和妆容不变”，不能只写身份不变。
11. 服装多视图、换装等涉及服装保留或替换的任务，必须明确写入“服装样式和版型”，不能只写服装或衣服不变。
12. 提示词正文由 LLM 直接创作；脚本只允许保存、校验或转发 prompt plan。
13. 不能用脚本做批量生成、批量插入、正则套句或映射投影；必须由 LLM 从上到下逐条理解目标对象，并只把 LLM 判断后的结果写入 prompt plan。

## Image Role Rules

| role | meaning | common families |
| --- | --- | --- |
| `edit_target` | 待编辑主图，通常提供构图、主体和镜头关系 | 修图、风格化、元素替换 |
| `background_reference` | 背景环境来源 | 元素替换/换背景 |
| `character_reference` | 新角色身份来源，必须锁定原角色形象和妆容 | 元素替换/换角色 |
| `identity_reference` | 面貌/脸部身份来源，必须锁定原角色形象和妆容 | 元素替换/换脸 |
| `costume_reference` | 服装来源，必须锁定服装样式和版型 | 元素替换/换装 |
| `product_reference` | 商品身份、包装、材质、logo 来源 | 多图融合/电商广告 |
| `subject_reference` | 角色、主体或物体身份来源 | 多图融合/分镜构图 |
| `scene_reference` | 场景空间、环境、台面、背景来源 | 多图融合、多视图/场景 |
| `storyboard_composition_reference` | 分镜机位、景别、画面重心和动作方向来源 | 多图融合/分镜构图 |
| `style_reference` | 风格语言、材质语言、色彩体系来源 | 风格化/风格迁移、多图融合 |
| `filter_direction` | 影调、滤镜、调色方向 | 风格化/滤镜 |
| `main_subject_reference` | 多视图主体参考图；角色多视图必须锁定原角色形象和妆容 | 多视图/场景、道具、服装、角色 |
| `shot_grid_reference` | 多镜头主参照图；锁定画面风格、构图元素、主体信息、场景事实和叙事瞬间 | 多镜头/九宫格 |
| `supporting_reference` | 辅助材质、局部、姿态、表情、配饰或细节参照 | all |

## Family Prompt Rules

| edit_family | prompt focus |
| --- | --- |
| `多视图` | 固定对象类型、设计页 layout、身份徽章、跨面板一致性和非目标护栏；角色多视图默认顶部面部高清放大特写、底部全身正/侧/背三视图，并必须保留原角色形象和妆容不变；旧式细节模块布局称为多细节界面版；服装多视图必须锁定服装样式和版型 |
| `多镜头` | 固定 3x3 电影镜头九宫格；保留参照图风格、构图元素、主体信息和场景事实；九个 panel 使用电影常用景别与机位组合 |
| `多图融合` | 逐图职责、主视觉优先级、透视/光线/阴影统一、无关元素排除 |
| `风格化` | 风格作用范围、主体和叙事事实保真、风格参考不复制无关主体 |
| `修图` | 自然保真、画质或人物修整目标、禁止重绘和身份漂移 |
| `元素替换` | 图序、替换来源、保留范围、接触光影/边缘融合和漂移禁止项；换装、换角色、换脸必须明确保留原角色形象和妆容不变；换装必须锁定服装样式和版型 |

## Handoff To Imagegen

- 调用前必须读取 `.agents/skills/cli/imagegen/SKILL.md + CONTEXT.md`。
- `photoGPT` 只允许把任务交给 `gpt-image-2`；`imagegen_handoff.model` 必须显式写为 `gpt-image-2`。
- 不得把 prompt plan 交给 nano-banana、AnyFast Gemini image、InsightFace、inswapper、Roop、DeepFace、Photoshop generative edit 或其他非 `gpt-image-2` provider。
- 若 `gpt-image-2` 不能执行，`photoGPT` 仍可交付 prompt plan，但必须写清 `blocked_provider_not_gpt_image_2` 或其他具体阻断原因。
- 项目资产落盘、命名、2K 默认和透明背景规则均由 imagegen 合同裁决。

## Review Gate Mapping

| review_question | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| prompt plan 是否先锁定图片角色再写提示词？ | 每张输入图必须有明确 role，且图序与子类一致 | `FAIL-PGPT-ROLES` | `SKILL.md N3-ROLES` | `image_roles` |
| prompt 是否包含保留项、变化项和负面约束？ | 三组字段各至少 1 条，且与用户目标一致 | `FAIL-PGPT-PROMPT` | `SKILL.md N5-PROMPT` | `preserve_scope/change_scope/negative_constraints` |
| 角色多视图是否默认使用面部放大版？ | 未显式请求多细节界面版时，顶部必须是面部高清放大特写，底部必须是正/侧/背全身三视图 | `FAIL-PGPT-CHARACTER-MULTIVIEW-MODE` | `templates/多视图/角色/TEMPLATE.json` | character branch audit |
| 多镜头是否只变化镜头语言而不改参照图事实？ | 九宫格每格景别/机位不同，参照图风格、构图元素、主体信息和场景事实不变 | `FAIL-PGPT-MULTI-SHOT` | `templates/多镜头/九宫格/TEMPLATE.json` | shot plan audit |
| prompt 是否由 LLM 直接创作？ | 发现脚本拼接、正则套句或映射投影即失败 | `FAIL-CREATIVE-AUTHORSHIP-SCRIPT` | `SKILL.md LLM-First Creative Authorship Contract` | anti-scripted audit |
| provider handoff 是否只指向 `gpt-image-2`？ | `imagegen_handoff.model != gpt-image-2` 或建议其他 provider 即失败 | `FAIL-PGPT-PROVIDER` | `SKILL.md Provider Boundary` | `imagegen_handoff` |
