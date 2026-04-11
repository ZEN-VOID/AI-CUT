# 2-格式 / Type Strategies

本文件是 `2-格式` 的 VSM 四件套真源。

## 复杂度声明

- complexity_level: `medium`
- reason: 存在 4 个关键变量、2 个互斥主变体、1 个双案对照回退分支

## 1. Variable Register

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| VAR-FMT-01 | 叙事 | 用户是否显式提到“解说剧 / 旁白主导 / 讲述者带路” | `explicit_explainer` / `no_explicit_explainer` | 读用户请求与项目说明 | P0 |
| VAR-FMT-02 | 结构 | 项目主通道更靠表演还是解释 | `performance_led` / `narration_led` / `mixed` | 读 `north_star`、`init_handoff`、分集摘要 | P1 |
| VAR-FMT-03 | 资源 | 下游是否需要高密度解释性文本 | `high_explainer_need` / `normal` | 看平台节奏、受众、项目定位 | P2 |
| VAR-FMT-04 | 技术 | 输入是否足够支持稳定判模 | `enough` / `insufficient` | 检查上游文件完整度 | P0 |

## 2. Scenario Table

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| CASE-FMT-STD | `VAR-FMT-01=no_explicit_explainer` 且 `VAR-FMT-04=enough` | 0.70 | 与 `CASE-FMT-EXP` 互斥 | 可与 `CASE-FMT-COMPARE` 做分析并发 |
| CASE-FMT-EXP | `VAR-FMT-01=explicit_explainer` 或 `VAR-FMT-02=narration_led` | 0.75 | 与 `CASE-FMT-STD` 互斥 | 可与 `CASE-FMT-COMPARE` 做分析并发 |
| CASE-FMT-COMPARE | 用户明确要求两套格式对照 | 0.90 | 不互斥主分析，但正式落盘仍需推荐主案 | 可并发生成两案 |
| CASE-FMT-BLOCKED | `VAR-FMT-04=insufficient` | 1.00 | 与所有正式落盘 case 互斥 | 无 |

## 3. Case -> Strategy Map

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| CASE-FMT-STD | STRAT-FMT-STD | 进入 `subtypes/标准剧`，生成标准剧合同/样例/局部验证 | 必须明确表演优先与旁白从严 | STRAT-FMT-REVIEW | 若子技能产物缺样例或边界不清 |
| CASE-FMT-EXP | STRAT-FMT-EXP | 进入 `subtypes/解说剧`，生成解说剧合同/样例/局部验证 | 必须明确旁白主导、对白保真 | STRAT-FMT-REVIEW | 若子技能产物缺主体统一或误吞对白 |
| CASE-FMT-COMPARE | STRAT-FMT-COMPARE | 并行生成两套合同，再由父级标推荐主案 | 不得只给对照不给主案 | STRAT-FMT-REVIEW | 若推荐主案缺理由 |
| CASE-FMT-BLOCKED | STRAT-FMT-STOP | 停止向下执行，回报缺失输入 | 不得伪造判模结论 | 无 | 用户补齐上游输入后重启 |

## 4. Routing Card

- 判定顺序:
  1. 先看输入是否足够
  2. 再看用户是否显式要求解说剧
  3. 再看项目主通道偏表演还是偏解释
  4. 最后处理是否需要双案对照
- 冲突解消规则:
  - 用户显式要求 > 项目默认节奏 > 仓库默认 `标准剧`
- unknown 默认路由:
  - 若信息不完整则暂停
  - 若信息完整但无明确解说信号，则默认 `标准剧`
- 失败重试上限: 1 次父级复核 + 1 次子技能返工
- 停止条件:
  - 输入缺失
  - 子技能无法给出合同或样例
  - 双案对照却无法指定推荐主案
