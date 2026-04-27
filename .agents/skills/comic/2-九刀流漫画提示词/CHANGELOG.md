# Changelog

## 2026-04-26 - Skill 2.0 full upgrade

- 将 `SKILL.md` 从长篇总汇重写为入口、路由、动态引用、质量门禁和 Output Contract。
- 新增 `steps/nine-blade-workflow.md`，承接原 `SKILL.md` 中的来源前奏、切组、九刀主流程、三支路漫画语法汇流和失败回路。
- 新增 `review/review-contract.md`，固定结构、schema、语义、版式、文字和 handoff 审计门禁。
- 新增 `types/` 类型包：`grouped-script`、`raw-source-fallback`、`multi-episode-continuity`、`poster-aware-handoff`。
- 新增 `knowledge-base/comic-prompt-heuristics.md`，沉淀风格、版式、提示词拼装和反模式经验。
- 新增 `templates/output-template.md`，对齐 Output Contract 五字段。
- 新增 `README.md`，说明目录树、入口和校验命令。

### Migration Matrix

| old source | target owner | operation | semantic risk |
| --- | --- | --- | --- |
| `SKILL.md` frontmatter / positioning / context loading | `SKILL.md` | keep and compress | low |
| `业务需求分析合同` | `SKILL.md` + `steps/nine-blade-workflow.md` | summarize + move execution details | medium |
| `总输入合同` / source priority | `SKILL.md` + `types/` | keep input boundary and split type-specific rules | medium |
| `剧本来源格式化前奏合同` | `steps/` + `types/raw-source-fallback/` | move | medium |
| `Page-Group 划分前奏合同` | `steps/` + `types/grouped-script/` | move | medium |
| `思行网络` / `思行节点表` | `steps/nine-blade-workflow.md` | move and normalize | low |
| `输出合同` / poster handoff | `SKILL.md` + `templates/output-template.md` + `types/poster-aware-handoff/` | keep and split | medium |
| `版式与文字硬规则` | `references/` + `knowledge-base/` + `review/` | keep existing reference and add review/heuristics | low |
| `字段映射` / `验证` / `Root-Cause 合同` | `SKILL.md` + `review/` | compress and keep gates | low |
| `CONTEXT.md` experience layer | `CONTEXT.md` | keep, with migration heuristic added | low |
| schema/template/validator | `templates/` + `scripts/` | keep | low |

## 2026-04-26 - Move comic genre type packs into this skill

- 将 `.agents/skills/comic/type-packs/漫画/` 迁移为 `.agents/skills/comic/2-九刀流漫画提示词/types/漫画/`。
- 更新 `types/type-map.md`，把 12 个漫画题材包纳入本技能类型包索引。
- 更新 `comic_type_pack_resolver.py`，题材知识根改为本技能 `types/漫画/`，`runtime.yaml` 仍保留在父级 `comic/type-packs/` 作为跨阶段默认栈配置。
- 同步更新父级 comic 合同、共享 type-pack loading contract、模板、自检样例与项目产物中的旧路径引用。
- 对旧项目产物中的 legacy 题材名做兼容映射：`热血战斗` -> `少年战斗冒险`；`悬疑惊悚` 中的推理文件 -> `推理悬疑`，恐惧空间 -> `恐怖怪谈`。
