# Scripts

本目录只承载机械辅助脚本或说明，不承担 `$aigc-scene-design` 的核心创作。

允许的脚本职责：

- 检查 canonical 目录与必需文件是否存在。
- 检查输出 Markdown 是否包含固定标题。
- 检查英文 prompt 字符数是否不超过 2000 characters。
- 检查设计稿是否存在 `research_brief`、`source_posture`、`uncertainty_register`、`visual_translation` 和 `prompt_evidence_chain` 标题或字段。
- 解析 `references/design-slot-review-contract.md` 的 `SCENE-BUNDLE-01`，输出 required slots 供 review gate 逐项验收。
- 检查文件名非法字符替换。
- 统计已生成设计稿与上游清单行的覆盖关系。

禁止的脚本职责：

- 生成研究考据、物语、Scene Design、Cinematography 或英文提示词。
- 自动决定建筑/空间风格、摄影风格或冷门信息结论；脚本不得把自然、超现实、交通或抽象空间强行归入建筑流派。
- 自动填写 `research_brief`、来源姿态、不确定性、视觉翻译或 prompt 证据链。
- 自动新增上游清单不存在的场景主体。
- 写入 registry、父级 skill 或其他 worker 的技能包。

当前包只提供机械 resolver / validator 类脚本；需要新增执行脚本时只能采用 dry-run 或校验用途，并保持 LLM-first 边界。
