# Context: fine-tuning

本文件是 `.agents/skills/aigc/fine-tuning` 的经验层知识库，不是第二份执行合同。调用 `$fine-tuning` 时，它必须与同目录 `SKILL.md` 一起加载，用于识别调优对象、常见失败模式、阶段方案选择和 owner handoff 风险。

## Context Health

```yaml
monitor_version: 2
soft_limit_chars: 30000
hard_limit_chars: 60000
status: ok
recommended_action: keep-stage-tuning-heuristics-focused
last_checked_at: 2026-06-16
```

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 系统预防修复 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `FT-TM-01` | 用户要求“调优”，但目标产物没有阶段归属 | object routing layer | 回到 `N1-INTAKE`，用路径、标题、字段、阶段关键词和 owning stage 合同建立 `target_stage_map` | 在报告模板中强制 `target_stage_map`，无归属不进入候选生成 | 每个对象都有 stage、owner、source path 或 chat-only 标记 |
| `FT-TM-02` | 调优变成泛泛润色，没有阶段专属方案 | scheme matching layer | 回到 `N2-SCHEME-MATCH`，按 `2-10` 方案表选择方向和验收焦点 | `references/stage-tuning-schemes.md` 保持每阶段独立 scheme id | `scheme_selection_matrix` 覆盖 100% 对象 |
| `FT-TM-03` | 外部资料质量很高，但候选背离原故事或阶段事实 | source/reference layer | 回到 `N3-SOURCE-REFERENCE-BUILD`，把外部资料降级为 reference principle，并补 source anchors | 报告中区分 `source truth`、`reference principle` 和 `provider constraint` | 每个 planned change 都有 source anchor |
| `FT-TM-04` | 多轮调优只有一次改写或同义替换 | iteration layer | 回到 `N4-ITERATE`，每轮先诊断再 patch，再记录 delta 和下一轮目标 | 默认 2 轮，最多 3 轮；无 delta 不算一轮 | `iteration_ledger` 有 round、diagnosis、patch、delta、verdict |
| `FT-TM-05` | 候选稿看似更好，但无法说明相对基线提升 | comparison layer | 回到 `N5-COMPARE`，建立基线-候选-方案三方矩阵 | `Comparison Acceptance Matrix` 是完成门，不是附属说明 | 每个目标方向评分和 fatal gate 可审计 |
| `FT-TM-06` | 调优报告准备直接覆盖阶段产物 | owner boundary layer | 回到 `N6-OWNER-CHECK`，改为 owner handoff patch | 根 AIGC 合同把 `fine-tuning` 明确为卫星入口 | final verdict 不声称本技能完成 canonical 写回 |
| `FT-TM-07` | 图像或画布调优只看 prompt，不看实际生成结果或 provider 形态 | production evidence layer | 对 `9-图像` / `10-画布` 补 actual result、imageList、node evidence 或明确 N/A | 阶段方案里把 provider result shape 和 run evidence 设为验收焦点 | 结果证据与 prompt / source 之间有对照 |

## Repair Playbook

1. 先锁定对象归属：阶段编号、路径、输出字段、叶子技能和 owning stage。
2. 再锁定调优方向：用户显式方向优先；没有时用对应阶段默认方向，不跨阶段套用。
3. 对每个改动先找 source anchor，再抽 reference principle；没有 source anchor 的“高级感”不得进入候选 patch。
4. 每轮调优必须留下 round delta；只改措辞、换同义词、套口号或扩大形容词密度不算有效轮次。
5. 比对验收先看硬门：上游保真、LLM 主创、owner 边界、provider 形态；硬门失败不得用平均分抵消。
6. 多阶段调优时，每个对象独立评分，再做跨阶段一致性审查；不要用总评覆盖单对象失败。
7. `9-图像` 与 `10-画布` 的调优要区分 prompt quality、asset binding、provider result shape 和实际运行证据。
8. 若发现 owning stage 缺少反脚本、上游应用或比对验收 gate，把问题回交 `learn` 或目标 stage 源层修复，不在本技能中偷渡阶段规则。

## Reusable Heuristics

- “迭代调优”在本仓库中更接近 `iterative refinement + comparison-gated optimization`，不是单次 polish。
- 阶段越靠后，越要把审美提升翻译成生产约束：`8-分组` 看组边界，`9-图像` 看结果形态，`10-画布` 看节点和运行证据。
- 高质量参考只提供原则，不提供可直接复制的镜头、文案或 prompt；最稳的写法是 `reference principle -> local adaptation -> boundary check`。
- 调优成功的最低证据不是“新稿更顺”，而是能回答：改了哪里、为什么改、源依据是什么、比基线好在哪、哪个 owner 能接收。
- 对 AIGC 产物，字段完整是底线，不是质量上限；调优必须显式评估差异化、可视化、可生产性和上下游继承。
