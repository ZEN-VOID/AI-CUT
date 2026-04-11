# 标准剧 / Type Strategies

本文件是 `标准剧` 的 VSM 四件套真源。

## 复杂度声明

- complexity_level: `medium`
- reason: 需要同时处理旁白开关、内心独白开关与样例简洁度

## 1. Variable Register

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| VAR-STD-01 | 风格 | 当前信息是否必须靠旁白补解释 | `need_narration` / `no_narration_needed` | 看剧情信息能否由动作+对白承载 | P0 |
| VAR-STD-02 | 叙事 | 是否需要内心独白辅助心理信息 | `inner_voice_needed` / `inner_voice_optional` / `inner_voice_off` | 看人物内压是否难以外化 | P1 |
| VAR-STD-03 | 结构 | 样例是否需要更复杂的字段组合 | `minimal` / `extended` | 看下游是否首次接触该格式 | P2 |
| VAR-STD-04 | 来源 | 当前是否命中 `storyboard_script / hybrid_story_text` | `preset_driven / narrative_only` | 读取 `source_profile` | P0 |
| VAR-STD-05 | 证据 | 上游是否明确写出运镜/镜头提示 | `camera_explicit / camera_absent` | 扫描分镜源中的镜头语言 | P0 |

## 2. Scenario Table

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| CASE-STD-LEAN | `VAR-STD-01=no_narration_needed` | 0.80 | 与 `CASE-STD-NARRATION` 互斥 | 可与 `CASE-STD-INNER` 并发分析 |
| CASE-STD-NARRATION | `VAR-STD-01=need_narration` | 0.75 | 与 `CASE-STD-LEAN` 互斥 | 无 |
| CASE-STD-INNER | `VAR-STD-02=inner_voice_needed` | 0.70 | 无 | 可与主 case 并发 |
| CASE-STD-STORYBOARD | `VAR-STD-04=preset_driven` | 1.00 | 无 | 可并发主 case |

## 3. Case -> Strategy Map

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| CASE-STD-LEAN | STRAT-STD-LEAN | 只保留动作画面、对白、对白画面为主骨架 | 样例允许零旁白 | STRAT-STD-REVIEW | 样例仍出现解释性旁白堆积 |
| CASE-STD-NARRATION | STRAT-STD-NARRATION | 旁白按需启用，但必须写明非默认常开 | 旁白不能替代表演主通道 | STRAT-STD-REVIEW | 旁白变成默认层 |
| CASE-STD-INNER | STRAT-STD-INNER | 内心独白按需加入，并补对应画面 | 不能缺 `内心独白画面` | STRAT-STD-LEAN | 独白只是重复对白 |
| CASE-STD-STORYBOARD | STRAT-STD-STORYBOARD | 优先保留镜头语言、规范化整理既有分镜结构、优先复用原场景标题 | 镜头语言保留率 100%，不脑补新增 | STRAT-STD-REVIEW | 场景标题被重概括，或镜头语言挂错位置 |

## 4. Routing Card

- 判定顺序:
  1. 先看信息能否由动作与对白承载
  2. 再判断是否需要内心独白
  3. 若命中分镜源，优先锁定原场景结构与镜头语言保留规则
  4. 最后决定样例用最简骨架还是扩展骨架
- unknown 默认路由:
  - 保持最简骨架，不默认开旁白
- 失败重试上限: 2 次
- 停止条件:
  - 样例仍依赖旁白解释核心信息
  - 分镜源的镜头语言被误删、误改写或脑补新增
