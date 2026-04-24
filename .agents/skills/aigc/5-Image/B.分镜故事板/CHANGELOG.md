# CHANGELOG

## 2026-04-24

- 创建 `B.分镜故事板` Skill 2.0 融合包。
- 融合原 `1-提示词蒸馏/分镜故事板`、`2-参照引用`、`3-图像生成` 三段合同。
- 保留原三个技能包与既有 runtime 写位。
- 增加 `references/`、`steps/`、`types/`、`review/`、`knowledge-base/`、`templates/`、`scripts/` 与 `agents/openai.yaml`。
- 将旧 `1-提示词蒸馏/分镜故事板` 的完整版蒸馏方法消化进 `references/request-distillation.md` 与 `steps/storyboard-sheet-workflow.md`，补齐固定前缀、组级设计块、多镜融写列、字段覆盖、压缩层级、request gate 与 `_manifest.json` 口径。
- 修正 `types/type-map.md` 中 `from_detail + storyboard_group` 路由，避免从 `S1` 直接跳到 `S4` 而跳过 `S2/S3`。
