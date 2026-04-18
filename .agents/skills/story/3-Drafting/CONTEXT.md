# CONTEXT.md

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| drafting 仍回退到 `Drafting/chNNNN/chapter-root.md` | stage canonical runtime | 改回 `projects/story/<项目名>/3-Drafting/第N集.md` | 在父技能与 `_shared` 合同中固定单一正文根文件 | 任何子技能都只回写 `第N集.md` |
| 第 2 集之后直接开写，没读上一集终稿 | continuity contract | 阻塞当前集，先补上一集终稿读取 | 在父技能 Total Input Contract 写死 `N>1` 必需连续性输入 | 当前集日志能记录 `previous_episode_ref` |
| 子技能各自写一份完整稿，父层没有统一收束 | composite output governance | 改为 child 只返回 `manuscript_patch + process_log_entry` | 在 `_shared/drafting-child-output-contract.md` 固化输出协议 | `写作日志.yaml` 能回放 1-7 的 progressive rewrite |
| 把 `Planning/全息地图.json` 当摘要参考，而不是规划法律 | planning truth drift | 回到 `chapter_boards / story_spine / threads / navigation_rules` 逐项吸收 | 在父技能 Overview 固定 story_map 语义与禁飞区 | 当前正文能对照 board 功能与 thread 债务 |
| 只有剧情起盘，没有后续层层加工 | process under-spec | 回到 1-7 固定顺序补工序 | 在父技能 Dispatch Order Contract 固定串行 7 步 | 当前集日志可显示所有已完成工序 |
| 某一步明明已经暴露早期结构/逻辑问题，却继续往后写到最后才返工 | inline validation gap | 在当前 step 写回后立即跑 registry 声明的即时审计 hook | 把即时审计合同固化进 `drafting-instant-validation-contract.md` 与 process log | 更早的问题不会无声滚到 Step 7 |
| `7-润色` 被误当成最终通过成品 | stage boundary drift | 把 `7-润色` 收回到 `candidate_final_draft` 边界 | 在父技能与终修子技能写死“最终 PASS 只归 4-Validation” | drafting 不再自我盖章放行 |
| 已写了 inline hook 合同，但 `workflow_manager.py` 没有真实触发与阻断逻辑 | runtime landing gap | 把 registry 接到 `complete-step / start-step / record-inline-validation` 运行时链路 | 以后遇到“合同化新机制”时，同时检查 `story.py / workflow_manager.py / tests` 是否已落地 | step 完成后会自动生成 inline validation batch，并真实阻断下一步 |
| inline validation 已触发，但仍完全依赖人工逐条回填结果 | validator runner gap | 增加 `validation_runner.py`，让 `complete-step` 先尝试自动批跑当前 validators | 新增 validator 维度时，同时补 registry、runner handler、workflow 挂接与 tests | manuscript 存在时，Step 完成后可直接自动写回当前 batch |
| 追读力分类真源被压缩成几条摘要，Step 6 只能靠局部经验 improvisation | shared taxonomy under-spec | 把 hook / cool-point / micro-payoff taxonomy 恢复到根级 `_shared/reading-power-taxonomy.md`，Step 6 只保留执行映射 | 固定“共享 taxonomy 在根级 `_shared/`，Step 6 只消费不复写”的治理边界 | Step 6、context builder 与 query 读取的是同一份 taxonomy |
| 爽点设计只剩零散题材材料与失效跳转，没有 active shared guide | shared cool-point guide missing | 在根级 `_shared/` 补 `cool-points-guide.md`，把强度梯度、组合技、疲劳防控和虐爽转换收束成共享工程指南 | 固定“taxonomy 管分类、guide 管编排”，Step 6 只消费共享 guide，不再在本地散写第二份爽点手册 | Step 6、review redirect 与共享 `_shared/` 指向同一份 guide |

## Repair Playbook

1. 先判断问题出在输入装配、连续性、根文件真源、工序顺序，还是某个子技能的加工维度。
2. 若当前集看起来像“另起一稿”，优先检查是否绕开了 `第N集.md` 单一根文件。
3. 若从第 2 集开始人物/关系突然漂移，先回查上一集终稿是否真的被装进上下文。
4. 若文本只有事件流水，没有文学质感，优先确认 2-7 是否真的按顺序执行，而不是只做了 1。
5. 若问题在 Step 5/6 才暴露，但 `rework_target_step` 指向更早节点，必须回退到最早受影响 step，而不是只修当前步。
6. 收尾固定核对：
   - `第N集.md`
   - `写作日志.yaml`
   - `Planning/全息地图.json`
   - `第N-1集.md`（当 `N>1`）

## Reusable Heuristics

- `story_map` 对 drafting 最重要的价值不是“给一点点梗概”，而是明确本集欠哪些功能债和线程债。
- 单集写作最稳的方式不是一次成稿，而是让同一份正文在不同加工维度下逐层变厚、变准、变活。
- 第 2 集之后的连续性，通常不是靠“总结上一集”解决，而是靠回读上一集终稿里的情绪、动作和信息停点。
- `写作日志.yaml` 的价值不只是断点恢复，它还能防止某一步被误以为“已经做过了”。
- 即时审计 hook 的价值，不是提前做最终验收，而是在当前步刚写完时立刻拦截会污染后续步骤的早期错误。
- `7-润色` 之后最合理的状态是“高置信候选终稿”，不是“自判最终 PASS”。
- `6-追读力强化` 最稳的做法不是把“张力”写得更大声，而是把共享 taxonomy 投影为当前章的主钩、微兑现和章末单一主牵引。
- 爽点设计最容易漂移的不是“名字”，而是“强度、频率、组合和防疲劳规则”；这些更适合独立成共享 guide，而不是混进 taxonomy 表。
