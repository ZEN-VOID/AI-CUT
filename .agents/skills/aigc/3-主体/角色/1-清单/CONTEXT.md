# Context: aigc 3-主体/角色/1-清单

本文件是 `角色/1-清单` 的经验层知识库，不是过程日志。它用于沉淀角色清单提取、归并、首次登场裁决和输出修复中的可复用经验。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 22000
hard_limit_chars: 44000
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-25
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 同一角色拆成多行 | 身份归并层 | 回查最早相关分镜组正文，确认姓名、称谓、代称是否指向同一主体 | 在归并前建立 `canonical_name -> observed_names` 草表，由 LLM 裁决 | 清单 `名称` 单元含主名与别名，不出现重复主体 |
| 不同角色被错误合并 | 证据边界层 | 拆回独立条目，并在报告记录冲突证据 | 不因同职业、同称谓、同群体身份直接合并 | 每个合并都有 source anchor 或项目上下文证据 |
| 首次登场偏晚 | 遍历顺序层 | 按 registry 顺序和 source anchors 重新扫描 `subjects.characters` | 首次登场只取 canonical 角色首次出现的 source anchor | 任一后续条目的首次登场不晚于候选证据表 |
| 描述变成设计正文 | 输出边界层 | 压回关键词式原文证据，删除外貌扩写和性格分析 | `原文描述（关键词式）` 只消费 registry 和 source anchor | 单元格为短语或关键词串，不是设定段落 |
| 从正文补出 registry 没有的角色 | 上游真源层 | 删除无 registry 依据的条目，或记录上游 registry 漏项风险 | 正文只用于 source anchor 证据回查，不是独立候选来源 | 每条候选都能指向 registry `subjects.characters` |
| 表格增加额外主体列 | 模板漂移层 | 恢复三列表格，把归并说明移入 `名称` 或执行报告 | 模板固定三列，review gate 检查列名 | 表头精确为 `名称`、`首次登场`、`原文描述（关键词式）` |
| 脚本生成归并结果 | LLM-first 层 | 停用生成逻辑，保留只读抽取或校验 | scripts README 固定机械辅助边界 | 脚本不输出 canonical markdown 清单正文 |
| 锚点替换伪角色差异 | 反模板伪差异层 | 废弃该批候选清单，回到 YAML 候选和 LLM 身份归并节点逐角色裁决 | `SKILL.md` 固定 `FAIL-CHAR-LIST-PSEUDO-DIFF`，字段完整不得放行 | 每条保留/合并/待核都有主体级裁决证据 |
| 状态变体被拆成多角色 | 变体归属层 | 把少年期、老年期、战斗态、战损态、受伤态、多套服装等合回同一 base character，并记录 `variant_state_map` | `SKILL.md` / review 固定 `FAIL-CHAR-LIST-VARIANT-SPLIT`；清单三列不新增变体列，必要时写 `变体：...` 或 manifest sidecar | 清单无重复主体；设计阶段可从描述或 `design-manifest.yaml.character_variants` 识别多状态资产 |
| 状态变体被吞掉 | 设计交接层 | 在 `原文描述（关键词式）` 补紧凑变体标签，或在 manifest sidecar 补 `character_variants` | 清单阶段审查 `variant_state_evidence -> variant_state_map -> description_keyword_evidence` | 显著服装/战斗/伤势/年龄阶段不会在设计阶段丢失 |
| runtime spine 缺业务画像或模块触发 | Skill 2.0 主脊柱层 | 把业务目标、类型路由、节点、模块触发、汇流和 review gate 写回 `SKILL.md` | `test-prompts.json` 覆盖 project_all、incremental_merge、repair/review | validator 能发现缺控制块，dry-run 能解释 source -> merge -> render -> review |

## Repair Playbook

1. 先锁定项目根、目标集号范围和所有可读 `8-分组/第N集.md`。
2. 按 registry 顺序建立候选证据表：`registry_id`、`canonical_name`、`source_anchors`、故事源证据摘记。
3. 对每个候选角色保留原始称呼，不急于改名；等全部候选收齐后再做归并。
4. 归并时优先采用项目已确认姓名；其次采用最具体、最早出现、可复查的称呼。
5. `老师`、`学生`、`路人` 等泛称默认不互相合并，除非 source anchor 或项目上下文明确指向同一人。
6. `他`、`她`、`那人` 等代称只能在同组上下文可明确回指时归入某角色；否则保留为风险，不写入强归并。
7. `名称` 单元可承载别名：`主名（别名：旧称、代称）`；不要新增独立别名列。
8. 首次登场总是取归并后 canonical 角色的最早分镜组 ID，而不是主名第一次出现的位置。
9. 描述关键词优先来自 registry 原词，其次来自 source anchor 中与识别身份直接相关的短语。
10. 多服装、战斗、战损、受伤、少年、老年等状态先判定是否同一叙事主体；默认作为同一角色变体，不拆行。
11. 完成后人工审查四件事：是否全来自 YAML、是否三列固定、是否有可疑错误合并、是否把状态变体误拆或吞掉。
12. 若发现清单像模板换角色名、关键词锚点替换、句式轮换或同义改写批量产物，不做表层润色；废弃候选稿并回到 LLM 身份归并裁决。

## Reusable Heuristics

- 角色清单服务资产一致性，不服务剧情百科；宁可短而可证，也不要提前写成角色设定。
- 名称归并的核心不是“文字相似”，而是“是否能证明同一叙事主体”。
- 一个群体称呼如果代表可设计的群像主体，可以保留为群体角色；如果只是背景人群，应在报告中说明未纳入。
- 最早分镜组 ID 是后续设计资产的锚点，优先级高于清单阅读美观。
- 关键词式描述要保留上游的辨识词，例如身份、关系、状态、动作钩子；不要补心理动机。
- 状态证据是资产变体，不是角色身份；“同一个人不同年龄/服装/战斗损伤”应被设计阶段消费为多版本设计稿，而不是清单阶段拆成多个角色。
- 当 YAML 与正文冲突时，不直接改写 YAML 结论；先在执行报告记录冲突，再由上游修复或人工裁决。
- 角色清单的新版 spine 应围绕 registry 证据和 LLM 身份归并构建；legacy workflow 可以保留为 reference，但不能重新成为执行节点真源。
