# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc-bykj/02-剧本处理` 的经验层知识库，不是执行日志。
- 调用同目录 `SKILL.md` 时必须同时加载本文件。
- 本文件不改写 `SKILL.md` 的输入、输出、节点、门禁或路径合同；只提供可复用失效模式、修复顺序和执行启发。

## Context Health

- soft_limit_chars: 12000
- hard_limit_chars: 24000
- status: ok
- last_checked_at: 2026-05-28

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `02` 又被拆成 `2-编剧/3-导演/4-表演` 三套输出 | 单阶段真源层 | 收回 `output/[项目名]/02-剧本处理/`，只保留 `剧本处理稿.json` 为正文真源 | 在 `SKILL.md` 固定 source skills 只作为能力来源 | 输出目录无分阶段 canonical 写回 |
| 剧本处理稿像剧情摘要 | 编剧保真层 | 回到 source truth lock，按原顺序恢复事实、对白和场景信息 | `PASS-02-03` 阻断摘要、删减和重排 | 抽样段落可回指输入原文 |
| 导演和表演能力只在报告里出现，正文没有变强 | 汇流投影层 | 把导演/表演证据拆回对应 beat，不保留总结块 | `N4/N5` 输出必须进入正文正式字段 | 正文能看到戏剧压力、声音、空间、身体和台词交付 |
| 来源技能只做引用索引，未内化细则精华 | 源能力整合层 | 在 `SKILL.md` 建立 `Integrated Source Essence Bank`，把原细则压成可执行判据、证据键和阻断失败 | 追溯表只能作为争议复核入口，不能替代主文档内化能力 | 不翻原 references 也能执行编剧、导演、表演核心判断 |
| 超长小说或剧本被强行单稿处理 | 输入容量层 | 默认按 `50000` 字上限阻断单稿处理，转入章节/集/幕/场/sequence 分段 | `SKILL.md` 固定 `processing_limit` 与 `FAIL-02-LENGTH-LIMIT` | 超限输入有 `segmentation_plan`，不丢上下文也不硬塞 |
| 原文 `第N章` / `第N集` 标题被改写或吞掉 | 结构保真层 | 恢复原始划分标题，建立 `section_title_map` | `SKILL.md` 固定 `ESS-SCRIPT-SECTION-TITLE` 和 `FAIL-02-SECTION-TITLE` | 输出标题与输入划分标题逐字一致 |
| 导演层抽象化 | 具像导演语言层 | 把“电影感/高级感/宿命感/氛围感”改成可见物、可听声、空间方向、动作余波 | `FAIL-02-DIRECTOR` 回到 `N4-DIRECTOR` | 离开抽象词仍可拍 |
| 表演层过度写心理解释 | 可演性层 | 改为眉眼嘴、呼吸、声线、手、重心、距离、道具互动或沉默反应 | `FAIL-02-PERFORMANCE` 回到 `N5-PERFORMANCE` | 观众能从声画 GET 到心理 |
| 受控增强变成新增剧情 | 增强边界层 | 删除新增事件、对白、规则、线索、因果和人物动机，只保留有锚点的承托 | `controlled_enrichment_ledger` 必填 risk_check | 删掉增强项后剧情事实完全不变 |
| 输出路径漂移到项目 runtime | BYKJ 路由层 | 移回 `output/[项目名]/02-剧本处理/` | 父级和阶段合同都固定 BYKJ output 路径 | manifest 中 output_root 正确 |

## Repair Playbook

1. 先判断失败属于输入取证、保真投影、导演具像、表演可演、汇流复审还是输出路径。
2. 若事实或对白漂移，优先修 `N3-SCRIPT`；不要让导演或表演层继续叠加。
3. 若正文正确但“不好看”，先查 `director_substance_plan`、`episode_visual_spine`、`atmosphere_mood_evidence`，再修局部文字。
4. 若人物“有情绪但不能演”，先查触发点、压制动机、微表情、身体联动、声线和对手反应。
5. 若报告证据齐全但正文没有承接，把 evidence 当作 planning draft，拆回对应剧本 beat。
6. 若发生路径或多真源问题，先修输出目录和 manifest，再处理内容细节。

## Reusable Heuristics

- `02-剧本处理` 的关键不是把三个旧阶段拼接，而是让同一份稿依次具备“可拍、可导、可演”。
- 对整合型 skill，来源技能的 references 不能只列成“需要时读取”；用户要的是原复杂细则的核心精华进入当前 `SKILL.md`，追溯入口只能作为争议复核。
- `02-剧本处理` 默认单次处理上限是 `50000` 字小说原文或剧本正文；超限时先做分段计划，不要让单稿处理承担过长上下文风险。
- 原文自带 `第N章`、`第N集` 等划分标题时，这些标题属于结构真源；剧本处理可以在其下新增场景标题，但不能改写或替换原划分标题。
- 编剧层是地基：事实和对白漂移后，导演与表演越强，错误越难修。
- 导演层最容易失败在抽象审美词；凡不能被画面、声音、空间或动作执行的词，都要回炉。
- 表演层最容易失败在心理解释；凡演员不能用身体、声音、停顿、距离或对手反应演出来的句子，都要回炉。
- 受控增强的安全判断很简单：它能增强观看体验，但删掉后剧情事实必须完全不变。
- BYKJ 阶段输出目录优先于原 AIGC runtime；本阶段只产出 `output/[项目名]/02-剧本处理/`。
