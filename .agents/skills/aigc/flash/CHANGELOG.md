# CHANGELOG

## 2026-06-09

- 增加台词/对白/旁白承接机制：`dialogue_manifest`、`dialogue_policy`、`dialogue_timing_map`。
- 将台词作为 `dialogue_overlay` 接入 `F1/F3/F5/F6/F9/F10`，明确用户给出的引号、角色冒号发言或“必须说/原样保留”默认 `hard_frozen`。
- 补齐 `GATE-FLASH-11`、`FAIL-FLASH-DIALOGUE`、输出模板中的 `台词策略`、声音生成边界和 `test-prompts.json` 回归用例。

## 2026-06-05

- 初始化 `aigc-flash` 为 `.agents/skills/aigc` 的聊天窗口 mini prompt 技能。
- 按 `skill-2.0` runtime-spine 规范补齐 `SKILL.md`：Context Loading、Runtime Spine、Business Requirement Analysis、Input、Mode Selection、Type Routing、Thinking-Action Node Map、Module Loading / Trigger、Convergence、Review Gate、Quantifiable Criteria、Attention、Checkpoint、Evaluation Prompt、Output 与 Learning Writeback。
- 明确 `flash` 压缩串联 `2-编剧`、`3-美学`、`4-导演`、`5-表演`、`6-氛围`、`7-分镜`、`8-摄影`、`9-光影`、`10-分组`，但只输出聊天窗口 prompt pack，不保存文档。
- 增加图生视频、首尾帧生视频、参考视频、多模态混合输入和 prompt repair 对策。
