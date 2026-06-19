# Scope Package: Problem Discovery

## Selection Signals

- 用户只给出“不好看”“不对”“读不清”“AI 味”“人物怪”“伏笔断”“没钩子”“节奏塌”“爽点弱”“动作不精彩”“内心戏浅”“氛围淡”“科技感弱”“赛博味不足”等宽泛质量反馈。
- review finding 只给结论，没有定位到章节、对象、源层或坏点类型。
- 用户要求“先找问题”“评估哪里坏了”“看看该怎么修”，但未授权直接写回。
- 上述“动作不精彩 / 内心戏浅 / 氛围淡 / 科技感弱 / 赛博味不足 / 玄幻能力表现弱 / 言情拉扯弱”只是特定题材或特定场景可能出现的症状族，不是所有题材章节的默认问题方向。

## Fixed Context

- 问题发现只负责把症状转成诊断包和候选路由，不生成 canonical 小说正文、设定正文、规划正文或润色正文。
- 每个模糊症状必须先找到至少 1 个 `evidence_anchor`：章节路径、段落摘记、验收包字段、review finding、旧口径关键词或项目上下文条目。
- 没有证据锚点时，输出 `blocked_inputs` 和下一步取证要求；不得凭泛化读感进入整章重写。
- `problem_discovery_packet` 只能作为 `N1-INTAKE`、`N2-IMPACT-MAP` 或 owning stage repair brief 的输入，不替代 impact map 和 source owner 判定。
- 选择 `owning_stage_repair_packages` 前，必须先判断项目题材、场景功能、源章坏点或用户 finding 是否真的命中对应症状族；未命中的候选问题写入 N/A，不得反向要求章节补齐。
- 不得因为项目是小说、网文或类型文，就默认检查动作、内心戏、氛围、科技、赛博、玄幻、言情全部维度。

## Symptom Heuristic Matrix

| symptom_family | common signals | suspected_root_layer | candidate_scope_packages | route_hint |
| --- | --- | --- | --- | --- |
| `continuity_or_clue_break` | 伏笔断、线索不接、前后说法冲突、读者看不懂真相链 | `2-卷章` / same-layer predecessor | `scope.clue-thread`, `scope.chapter-event`, `scope.structure-topology` | 先做 impact assessment，再决定是否修 planning 或回 owning stage |
| `character_false_note` | 人物不像自己、动机突然、对白同质、关系转折不成立 | `1-设定` / `2-卷章` / owning stage prose | `scope.character-state`, `scope.chapter-event`, `scope.tone-contract` | 先查角色卡和最近出场；源层正确时进 `3-初稿` 或 `4-润色` local repair |
| `mechanism_or_world_rule_break` | 道具/能力像外挂、规则解释矛盾、代价消失 | `1-设定` / `0-初始化` / `2-卷章` | `scope.mechanism`, `scope.chapter-event`, `scope.accepted-truth` | 先锁规则 owner，再同步后续使用点 |
| `time_place_readability` | 站位不清、路线混乱、时间穿帮、谁在哪里读不清 | scene cards / chapter event / owning stage prose | `scope.timeline-place`, `scope.chapter-event` | 源层错误走 impact map；纯读写可读性走 `4-润色` local repair |
| `action_choreography_weak` | 动作不精彩、打斗像流水账、招式/追逐无路径、受力无代价、余波不清 | owning stage prose / chapter event | `scope.chapter-event`, `scope.timeline-place`, `scope.tone-contract` | 源章事实正确时进入 `4-润色` `action_choreography_repair`；若要改胜负/伤亡/能力规则则先 impact assessment |
| `interiority_thin` | 内心戏浅、心理转折突兀、欲望压抑/创伤回声不足、第一人称内在节奏弱 | `1-设定` / owning stage prose / style contract | `scope.character-state`, `scope.tone-contract`, `scope.locality` | 源层正确时进入 `4-润色` `interiority_repair`；若新增动机/创伤则先查角色卡和 planning |
| `atmosphere_pressure_weak` | 氛围淡、压迫感弱、现场空、感官颗粒不服务冲突 | owning stage prose / scene context | `scope.timeline-place`, `scope.chapter-event`, `scope.tone-contract` | 进入 `4-润色` `atmosphere_pressure_repair`；不得新增无源天气、光源或装饰段 |
| `technology_texture_weak` | 科技感弱、技术像标签、缺边界/代价/反馈、机甲/AI/算法/星际技术太泛 | `1-设定` / `0-初始化` / owning stage prose | `scope.mechanism`, `scope.tone-contract`, `scope.chapter-event` | 源层已有技术时进入 `4-润色` `sci_fi_tech_repair`；若要新科技或改规则先 impact assessment |
| `cyberpunk_texture_weak` | 赛博味不足、只有霓虹标签、义体/监控/公司压迫/高科技低生活不成立 | `0-初始化` / `1-设定` / owning stage prose | `scope.tone-contract`, `scope.mechanism`, `scope.character-state` | 源层赛博方向成立时进入 `4-润色` `cyberpunk_texture_repair`；若要新增公司/义体规则先 impact assessment |
| `xuanhuan_power_weak` | 玄幻能力只有光效、修仙/异能/高武缺规则触发、资源代价和反馈 | `1-设定` / `0-初始化` / owning stage prose | `scope.mechanism`, `scope.chapter-event`, `scope.accepted-truth` | 源层规则正确时进入 `4-润色` `xuanhuan_power_repair`；若改能力体系先锁规则 owner |
| `romance_tension_weak` | 言情拉扯直白、暧昧模板化、脸红/占有奖励、欲望与回避不足 | `1-设定` / `2-卷章` / owning stage prose | `scope.character-state`, `scope.chapter-event`, `scope.tone-contract` | 源层关系结果不变时进入 `4-润色` `romance_tension_repair`；若改关系结果先 impact assessment |
| `prose_texture_or_ai_voice` | 太顺、AI 味、解释腔、总结句多、句群过度规整、场景空 | `4-润色` / style contract | `scope.tone-contract`, `scope.locality` | 进入 `4-润色` affected-span repair；不得扩大成整章洗稿 |
| `reader_pull_or_hook_weak` | 没钩子、爽点弱、节奏平、章末不牵引 | `2-卷章` / chapter event / owning stage prose | `scope.chapter-event`, `scope.structure-topology`, `scope.tone-contract` | 先查章规划任务和章末承接，再交 owning stage 修正文 |
| `accepted_truth_drift` | 已 PASS 后又要改事实、return 后上下文回流不一致 | stage acceptance / return / STATE | `scope.accepted-truth`, `scope.structure-topology` | 先失效或重验 acceptance/return，再决定正文或投影修复 |

## Required Output

```yaml
problem_discovery_packet:
  symptom_family: ""
  raw_symptom: ""
  evidence_anchor:
    path: ""
    excerpt_or_field: ""
    reason: ""
  suspected_root_layer: ""
  candidate_scope_packages: []
  owning_stage_repair_packages: []
  n_a_stage_repair_focus: []
  route_hint: impact_assessment | repair_plan | execute_repair | audit_only | owning_stage_local_repair | blocked
  confidence: high | medium | low
  blocked_inputs: []
```

## Review Gate

- 模糊症状必须有 `problem_discovery_packet`，不能直接进入正文改写或泛化润色。
- `candidate_scope_packages` 至少包含 1 个真实 `types/scope/*` 包；无法判定时必须说明 `blocked_inputs`。
- 当 `route_hint=owning_stage_local_repair` 时，`owning_stage_repair_packages` 应列出真实 owning stage package id，例如 `story-polishing:action_choreography_repair` 或 `story-polishing:sci_fi_tech_repair`。
- `owning_stage_repair_packages` 只列适用于当前题材/场景/源章坏点/finding 的 package；不适用的候选焦点必须写入 `n_a_stage_repair_focus`，不得作为缺陷或扣分项。
- `route_hint` 必须指向 `story-repair` 的模式或 owning stage repair 入口，不得指向未授权平行阶段。
- 诊断包不得把启发式结论写成 canonical creative truth。
