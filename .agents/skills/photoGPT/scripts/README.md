# Scripts

`photoGPT` 当前不提供会生成核心创作提示词的脚本。

允许脚本职责：

- 校验 prompt plan 字段是否齐全。
- 校验 `edit_family/edit_subtype/template_path` 是否落在五大类十四子类。
- 校验 `templates/<类型>/<子类型>/TEMPLATE.json` 是否存在。
- 将 LLM 已创作的 prompt plan 保存为 JSON。
- 批量检查本技能目录结构。

禁止脚本职责：

- 根据模板自动拼接、扩写或生成最终创作提示词。
- 替代 LLM 进行编辑类型裁决、审美判断或图像叙事判断。
