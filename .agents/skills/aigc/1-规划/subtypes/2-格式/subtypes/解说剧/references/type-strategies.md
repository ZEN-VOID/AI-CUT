# 解说剧 / Type Strategies

本文件是 `解说剧` 的 VSM 四件套真源。

## 复杂度声明

- complexity_level: `medium`
- reason: 需要同时控制旁白主导强度、对白保真边界与内心独白开关

## 1. Variable Register

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| VAR-EXP-01 | 叙事 | 旁白是否必须成为非对白信息主通道 | `narration_primary` / `narration_support_only` | 看用户与项目节奏要求 | P0 |
| VAR-EXP-02 | 结构 | 对白是否需要严格逐字保留 | `dialogue_strict` / `dialogue_flexible` | 看项目是否强调对白戏剧支点 | P1 |
| VAR-EXP-03 | 风格 | 内心独白是否允许开启 | `inner_voice_on` / `inner_voice_off` | 看用户是否显式要求 | P2 |

## 2. Scenario Table

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| CASE-EXP-CORE | `VAR-EXP-01=narration_primary` 且 `VAR-EXP-02=dialogue_strict` | 0.80 | 与 `CASE-EXP-WEAK` 互斥 | 可与 `CASE-EXP-INNER` 并发分析 |
| CASE-EXP-WEAK | `VAR-EXP-01=narration_support_only` | 0.75 | 与 `CASE-EXP-CORE` 互斥 | 无 |
| CASE-EXP-INNER | `VAR-EXP-03=inner_voice_on` | 0.90 | 无 | 可并发 |

## 3. Case -> Strategy Map

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| CASE-EXP-CORE | STRAT-EXP-CORE | 保留旁白、旁白画面、动作画面、对白四件套 | 旁白主导但不吞对白 | STRAT-EXP-REVIEW | 样例里对白被解释化 |
| CASE-EXP-WEAK | STRAT-EXP-RECHECK | 回父级复核是否真应进入解说剧 | 不得把弱信号硬拉成主变体 | 无 | 父级改判为标准剧 |
| CASE-EXP-INNER | STRAT-EXP-INNER | 在合同中显式开启内心独白，并补对应画面 | 不得默认常开 | STRAT-EXP-CORE | 内心独白只是重复旁白 |

## 4. Routing Card

- 判定顺序:
  1. 先确认旁白是否真是主通道
  2. 再确认对白保真要求
  3. 最后决定是否打开内心独白扩展
- unknown 默认路由:
  - 不打开内心独白
  - 若旁白主导信号不足，则回父级复核
- 失败重试上限: 2 次
- 停止条件:
  - 对白被吞并
  - 旁白主体不统一
