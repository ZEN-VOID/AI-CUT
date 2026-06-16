# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `$aigc-scene-list` 的经验层知识库，不是过程日志。
- 调用本目录 `SKILL.md` 时必须同时加载本文件。
- 本文件不改写 `SKILL.md` 的输入、输出和门禁；只沉淀可复用判断经验、失败模式和修复打法。

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
| 正文新增未在 registry 出现的场景 | 来源真源层 | 删除该主体，除非回查到 registry `subjects.scenes` 条目 | 在取证表中固定 `registry_id` 与 `canonical_name` | 每个主体都有 registry 来源 |
| 别名重复成多行 | 归并层 | 合并为 canonical 名称，关键词保留别名证据 | 执行别名、代称、缩写、全称四类扫描 | 同一空间不重复占行 |
| 不同空间被误合 | 空间边界层 | 拆分为独立场景，首次登场分别取最早组 | 对“楼/层/房间/门口/走廊/内外”保守处理 | 后续设计能单独制作空间 |
| 同一空间日夜被机械拆分 | 状态层 | 合并到同一 canonical 场景，关键词保留日/夜或状态 | 仅当时段造成资产差异或用户指定时拆分 | 没有无意义重复行 |
| 子空间边界丢失 | 制作粒度层 | 对需要独立美术资产的子空间拆行 | 评估取景范围、布景差异、叙事功能 | 子空间不被大场景吞掉 |
| 首次登场错误 | 排序层 | 回到所有输入集按集号和分镜组 ID 重新取最早项 | 记录每个候选出现序列再归并 | `首次登场` 指向最早组 |
| 关键词扩写成设计稿 | 输出边界层 | 改为短关键词，删除新增设定和视觉方案 | 模板固定 `原文描述（关键词式）` 不承载设计正文 | 描述可回指原文，不含新设定 |
| 脚本替代归并判断 | LLM-first 层 | 停用自动归并逻辑，脚本只做字段/格式校验 | scripts README 固定机械辅助边界 | 没有脚本生成 canonical 名称 |
| 锚点替换伪场景差异 | 反模板伪差异层 | 废弃该批候选清单，回到 YAML 候选和 LLM 归并节点逐主体裁决 | `SKILL.md` 固定 `FAIL-SCENE-LIST-PSEUDO-DIFF`，字段完整不得放行 | 每条保留/合并/拆分都有主体级裁决证据 |
| 2.0 目录完整但缺可视拓扑 | Skill 2.0 表达层 | 在 `SKILL.md`、`SKILL.md` runtime spine、`types/`、`review/` 补 Mermaid 图与返工路由 | 后续新增或升级分区时同步检查关键拓扑图是否覆盖入口、执行、类型和验收 | `rg "mermaid" <skill-dir>` 能命中关键分区 |
| 旧 workflow 节点与 runtime-spine 节点并存 | Skill 2.0 主真源层 | 以 `SKILL.md` 的 `Thinking-Action Node Map` 为执行主表，旧 workflow 只作兼容参考 | 升级时先补主入口必需控制块，不无限整包重写 | `rg "Thinking-Action Node Map|Module Trigger Matrix|Review Gate Binding" SKILL.md` 命中 |

## Repair Playbook

1. 先列出所有输入 `8-分组/第N集.md`，按集号与文件顺序建立候选扫描顺序。
2. 对每个分镜组只抽取底部 YAML 的 `场景` 字段；正文标题只做证据回查。
3. 为每个候选保留 `source_episode`、`group_id`、`yaml_scene_value` 和必要正文关键词。
4. 先做精确同名归并，再做别名、代称、简称、全称和错别字近似归并。
5. 遇到“同一地点 + 不同时段/状态”时，默认合并；只有制作资产明显不同、叙事空间不同或用户指定时拆分。
6. 遇到“同一建筑 + 不同房间/走廊/门口/天台/地下室”时，默认保守拆分，除非原文明确只是同一镜头内的泛称。
7. 跨场景或移动路线不要压成一个场景；如果 YAML 写成组合地点，按可制作空间拆分并在关键词中保留组合证据。
8. `首次登场` 取归并后所有候选中最早的分镜组 ID，不取命名最完整的一次。
9. `原文描述（关键词式）` 只写原文关键词、别名证据、时段/区域提示，不写美术设计建议。
10. 最后用 review gate 检查三列字段、registry 来源、重复项、误合风险和脚本边界。
11. 若发现清单像模板换名、关键词锚点替换、句式轮换或同义改写批量产物，不做表层润色；废弃候选稿并回到 LLM 归并/拆分裁决。

## Reusable Heuristics

- 场景清单是后续设计任务的入口索引，不是场景设定稿。
- registry 场景名越短，越要回查 source anchor 和风格协议做消歧；但回查不能新增主体。
- “教室”“本班教室”“高三一班教室”通常是别名候选；“教室门口”“教室内”“走廊”通常需要保守区分。
- 同一地点的昼夜、正常/异化、过去/现在，只有影响独立资产制作时才拆成多行。
- 跨越路线如“走廊到楼梯间”要警惕，它可能不是一个场景，而是两个需要分别设计的空间。
- 关键词越贴近原文越稳；清单阶段不追求文学表达。
- 最危险的错误不是漏掉背景，而是把不同空间误合，导致后续设计阶段无法发现缺资产。
- 结构校验通过不等于工作车间质量达标；对批量生成的 Skill 2.0 包，必须额外检查是否有入口拓扑、执行节点图、类型决策图和 review 回路图。
- 清单 skill 升级时优先保证来源真源、LLM 归并和三列表格 gate 可执行；旧说明可保留，但不得高于 `SKILL.md` 主节点表。
