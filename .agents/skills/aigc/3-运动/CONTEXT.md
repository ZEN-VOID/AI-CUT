# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/3-运动` 的经验层知识库，不是第二份主合同。
- 调用同目录 `SKILL.md` 时必须同时加载本文件。
- 本文件只沉淀可复用判断经验、失败模式和修复打法；不改写 `SKILL.md` 的输入、输出和门禁。

## Context Health

- soft_limit_chars: 18000
- hard_limit_chars: 36000
- status: ok
- last_checked_at: 2026-05-31

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 运动强化只写“走过去/跑过去” | 五要素层 | 补主体、参照系、起点、路径和终点 | review 固定 `GATE-MOTION-03` | 任取一条 `运动强化：` 能回答从哪里、沿哪里、到哪里、相对什么 |
| 当前画面起点与上一画面终点冲突 | 时间轴连续层 | 回到 `motion_state_ledger`，先写上一画面 final_state，再推当前 start | steps 固定先 ledger 后扩写 | report 中每个 unit 有 `previous_final_state` 和 `current_start_inference` |
| 把静态环境描写当动作强化 | 候选识别层 | 删除或降级该 unit，除非环境变化影响角色可达路径 | type 包限定角色动作和状态迁移 | motion unit index 不含纯静态环境 |
| 扩写变成新剧情或新调度 | source 保真层 | 只补空间关系和运动路径，删除新增事件或动机 | `source-preservation-contract.md` 固定不可改字段 | 原剧情事实、对白和顺序可回对 source |
| 写成分镜/运镜而不是角色运动 | 阶段边界层 | 删除机位、景别、运镜、焦点、分镜编号和 prompt | Output Contract 禁止摄影字段 | 下游 `4-摄影` 仍拥有镜头语言 |
| 参照系泛化成“旁边/前方” | 空间参照层 | 改成场景内稳定物、人物、门窗、桌椅、墙面、地面线、台阶或角色身体部位 | `motion-five-elements-contract.md` 要求可复查参照 | 读者能在同一场景复原方向和位置 |
| 同一分镜组参照系漂移 | 组级参照层 | 先建 `group_reference_profile`，选一个组内主参照；局部切换补 `reference_switch_reason` | review 固定 `GATE-MOTION-04A` 与 `GATE-MOTION-04B` | 同组 motion units 能回指同一 `primary_reference_frame`，或每次切换都有源内理由 |

## Repair Playbook

1. 先锁定 source path 和目标输出路径；项目模式默认 source 为 `2-编导/第N集.md`。
2. 扫描每个角色动作句：移动、靠近、后退、转身、伸手、抬头、坐下、起身、跌倒、抓握、避让、进入、离开都应进入候选。
3. 对每个候选先写上一画面最终位置或状态，再推导当前起点；缺证时标注模糊，不直接编造。
4. 若 source 有分镜组或连续动作段，先选 `primary_reference_frame`；同组 motion units 默认沿用，只有参照不可见、动作重心转移或身体微动作时才切换。
5. 检查五要素：运动主体、起点、路径、终点、参照系；缺一个就回到扩写节点。
6. 对多人画面先分清主动运动者和被动反应者；不要让所有角色同时移动到同一强度。
7. 对动作链只补空间连续，不新增剧情目标、心理解释或镜头方案。
8. 删除机位、景别、运镜、分镜编号和视频 prompt；这些交给 `4-摄影`。
9. 报告必须留下 `motion_state_ledger` 和 `group_reference_profile`，否则后续阶段无法复查连续性与参照一致性。

## Reusable Heuristics

- 最稳的运动句不是更长，而是更可定位：相对什么、从哪里、沿哪里、到哪里、停成什么状态。
- “参考系”优先选稳定空间物或当前互动对象；不要只写抽象方向词。
- 同一分镜组最好像共用一张小地图：先选门、桌、墙、台阶、车门、床沿等主锚点，再让局部手部或眼神动作挂到这个主锚点上。
- 最佳参照系不是最近的名词，而是最稳定、最可见、最能承接上一状态并交给下一动作的锚点。
- 起点通常来自上一画面 final_state；如果从 source 看不到起点，先推导可达范围，再写保守句。
- 终点不只位置，也包括身体状态、朝向、手里物、接触关系和注意力落点。
- 运动路径应服务角色动作的因果和可达性，不要为了好看加入绕行、跨越、翻滚等新事件。
- 多人动作先锁主运动者，再写其他人维持、让开、追随或反应；这样下游分镜不会失焦。
