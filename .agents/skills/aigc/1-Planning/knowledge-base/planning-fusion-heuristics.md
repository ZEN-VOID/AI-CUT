# Planning Fusion Heuristics

本文件承载 `1-Planning` 三包融合为单包后的可复用经验。

## Heuristics

- “单包融合”不等于把项目 runtime 输出目录也合并；业务产物边界和技能入口边界要分开治理。
- 旧子包的 `SKILL.md` 最适合作为 `references/*-contract.md`，旧子包的 `CONTEXT.md` 最适合作为 `knowledge-base/*-heuristics.md`。
- 如果根 `SKILL.md` 开始复制 `episode_split/script_format/grouping` 的完整细则，说明动态引用失败，应立即抽回 references。
- 迁移脚本与模板时，优先保持文件名不变，只改变父路径；这样 validator 调用和历史经验更容易追踪。
- 旧 `agents/openai.yaml` 可以作为 legacy metadata 归档，但产品侧入口必须收敛到一个 `$aigc-planning`。

## Common Repairs

| symptom | repair |
| --- | --- |
| 旧子包路径还在脚本中出现 | 更新到父级 `scripts/` 或 `templates/` |
| 旧子包 skill name 还在 backfill mapping 中出现 | 将 path-specific mapping 指回 `aigc-planning` |
| comic 或其他技能仍链接旧 `2-格式/SKILL.md` | 改链到 `references/script-format-contract.md` |
| Skill 2.0 validator 报缺分区 | 补最小说明文件，而不是创建空目录 |
