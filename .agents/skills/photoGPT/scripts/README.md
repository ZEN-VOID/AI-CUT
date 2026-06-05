# Scripts

`photoGPT` 当前不提供会生成核心创作提示词的脚本。

允许脚本职责：

- 校验 prompt plan 字段是否齐全。
- 校验 `edit_family/edit_subtype/template_path` 是否落在六大类十五子类。
- 校验 `templates/<类型>/<子类型>/TEMPLATE.json` 是否存在。
- 将 LLM 已创作的 prompt plan 保存为 JSON。
- 批量检查本技能目录结构。
- 校验 `test-prompts.json` 是否至少包含 3 条 `id/prompt/expected`。
- 扫描是否残留 `steps/` 第二节点真源引用。

禁止脚本职责：

- 根据模板自动拼接、扩写或生成最终创作提示词。
- 批量生成、批量插入、正则套句或映射投影创作正文。
- 替代 LLM 进行编辑类型裁决、审美判断或图像叙事判断。
- 自动修复、改写或裁决 `preserve_scope`、`change_scope`、`negative_constraints`、`final_prompt`。

任何脚本若生成了看似可用的创作提示词，该产物不得进入 canonical prompt plan；必须回到 `SKILL.md` 的 `N5-PROMPT`，由 LLM 从上到下逐条理解目标对象后重新生成。
