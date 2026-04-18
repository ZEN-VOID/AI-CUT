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

## Repair Playbook

1. 先判断问题出在输入装配、连续性、根文件真源、工序顺序，还是某个子技能的加工维度。
2. 若当前集看起来像“另起一稿”，优先检查是否绕开了 `第N集.md` 单一根文件。
3. 若从第 2 集开始人物/关系突然漂移，先回查上一集终稿是否真的被装进上下文。
4. 若文本只有事件流水，没有文学质感，优先确认 2-7 是否真的按顺序执行，而不是只做了 1。
5. 收尾固定核对：
   - `第N集.md`
   - `写作日志.yaml`
   - `Planning/全息地图.json`
   - `第N-1集.md`（当 `N>1`）

## Reusable Heuristics

- `story_map` 对 drafting 最重要的价值不是“给一点点梗概”，而是明确本集欠哪些功能债和线程债。
- 单集写作最稳的方式不是一次成稿，而是让同一份正文在不同加工维度下逐层变厚、变准、变活。
- 第 2 集之后的连续性，通常不是靠“总结上一集”解决，而是靠回读上一集终稿里的情绪、动作和信息停点。
- `写作日志.yaml` 的价值不只是断点恢复，它还能防止某一步被误以为“已经做过了”。
