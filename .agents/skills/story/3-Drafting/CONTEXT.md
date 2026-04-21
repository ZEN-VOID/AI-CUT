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
| 当前集 scope 已锁定，但仍无法从 `story_map` 命中唯一 chapter board | board locating contract | 先按 `episode_num / episode_id` 回查 `chapter_boards[].episode_ref`，必要时再用 `episode_sequence_axis -> node_id` 回指 | 在 `3-Drafting/_shared/chapter-board-locating-contract.md` 固化定位顺序，并禁止用数组顺序猜本集 board | 当前 step 的 `process_log_entry` 能写出唯一 `chapter_board.node_id` |
| 子技能各自写一份完整稿，父层没有统一收束 | composite output governance | 改为 child 只返回 `manuscript_patch + process_log_entry` | 在 `_shared/drafting-child-output-contract.md` 固化输出协议 | `写作日志.yaml` 能回放 1-8 的 progressive rewrite |
| 把 `2-Planning/全息地图.json` 当摘要参考，而不是规划法律 | planning truth drift | 回到 `chapter_boards / story_spine / threads / navigation_rules` 逐项吸收 | 在父技能 Overview 固定 story_map 语义与禁飞区 | 当前正文能对照 board 功能与 thread 债务 |
| 只有剧情起盘，没有后续层层加工 | process under-spec | 回到 1-8 固定顺序补工序 | 在父技能 Dispatch Order Contract 固定串行 8 步 | 当前集日志可显示所有已完成工序 |
| 某一步明明已经暴露早期结构/逻辑问题，却继续往后写到最后才返工 | inline validation gap | 在当前 step 写回后立即跑 registry 声明的即时审计 hook | 把即时审计合同固化进 `drafting-instant-validation-contract.md` 与 process log | 更早的问题不会无声滚到 Step 8 |
| 运行时把 1-8 当成“连续大改稿”，没有严格执行“一步写回一步 hook” | serial gate ambiguity | 回到真正串行版：当前 step 单独写回，立刻跑当前 step hook，通过后才准进入下一步 | 在父 `SKILL.md` 与 `_shared` 合同中明确“一 step 一提交一 gate”，并禁止多步合批正式写回 | `写作日志.yaml` 能逐步对齐 `Step 1 -> hook -> Step 2 -> hook ... -> Step 8` |
| `8-润色` 被误当成最终通过成品 | stage boundary drift | 把 `8-润色` 收回到 `candidate_final_draft` 边界 | 在父技能与终修子技能写死“最终 PASS 只归 4-Validation” | drafting 不再自我盖章放行 |
| 已写了 inline hook 合同，但 `workflow_manager.py` 没有真实触发与阻断逻辑 | runtime landing gap | 把 registry 接到 `complete-step / start-step / record-inline-validation` 运行时链路 | 以后遇到“合同化新机制”时，同时检查 `story.py / workflow_manager.py / tests` 是否已落地 | step 完成后会自动生成 inline validation batch，并真实阻断下一步 |
| inline validation 已触发，但仍完全依赖人工逐条回填结果 | validator runner gap | 增加 `validation_runner.py`，让 `complete-step` 先尝试自动批跑当前 validators | 新增 validator 维度时，同时补 registry、runner handler、workflow 挂接与 tests | manuscript 存在时，Step 完成后可直接自动写回当前 batch |
| 人物心理活动长期被分散在角色刻画、对白和润色边缘，导致内心描写不是太像摘要，就是太像作者评论 | inner-life ownership gap | 在 `3-Drafting` 增设 `6-心理活动描写`，固定它专门负责 POV 锚定、身体化知觉、半显性自辩与心理波动的戏内化 | 以后碰到“内心写不自然”时，优先先查 Step 6 合同、validator checkpoint 与 step-specific hook，而不是把问题丢给终修兜底 | 心理活动问题能直接回流到专属 step，而不是在 Step 4/5/8 之间漂移 |
| 追读力分类真源被压缩成几条摘要，Step 7 只能靠局部经验 improvisation | shared taxonomy under-spec | 把 hook / cool-point / micro-payoff taxonomy 恢复到根级 `_shared/reading-power-taxonomy.md`，Step 7 只保留执行映射 | 固定“共享 taxonomy 在根级 `_shared/`，Step 7 只消费不复写”的治理边界 | Step 7、context builder 与 query 读取的是同一份 taxonomy |
| 爽点设计只剩零散题材材料与失效跳转，没有 active shared guide | shared cool-point guide missing | 在根级 `_shared/` 补 `cool-points-guide.md`，把强度梯度、组合技、疲劳防控和虐爽转换收束成共享工程指南 | 固定“taxonomy 管分类、guide 管编排”，Step 7 只消费共享 guide，不再在本地散写第二份爽点手册 | Step 7、review redirect 与共享 `_shared/` 指向同一份 guide |
| 主角已启用成长系统，但 drafting 只有正文变化，没有结构化成长证据链 | growth evidence chain gap | 回到 `Step 4 + Step 6 + Step 7` 三步产证：前者留行为证据，`Step 6` 留心路/情感证据，`Step 7` 留压力/牵引证据 | 在父技能与 child output contract 写死 `growth_axis_evidence` 的责任边界 | `写作日志.yaml.step_history[]` 能回读三轴证据，而不是只看正文猜测 |
| 任务层已把句子改顺，但类似“卷次/阶段/规划术语直写进正文”的破次元句还会反复冒出 | diegetic boundary drift | 立刻把外部术语翻译成人物可感知的压力、代价、预感或局势变化 | 固定“planning / validation / workflow 语言不得直接落入正文，只能投影成戏内经验” | 正文不再出现“第一卷/阶段/时间压力落锁”这类作者层术语 |
| 同一画面信息被连续两句重复命名，读起来像 prompt 展开而不是小说 | local repetition in scene landing | 第一处交代身份，第二处只推进构图、动作或空间关系 | 在 drafting 经验层固定“同一意象近距离只保留一次命名，其余句子负责推进” | 类似“抱着鱼篓药包的平民”不会在两句里重复出现 |
| 章末为了做 hook 直接抛提纲式问句，续读感有了但小说感变差 | hook phrasing drift | 把问句式铺垫改成“危险逼近 / 余波未平 / 新债将至”的场面化收束 | 在 Step 7 / Step 8 经验层明确：先让麻烦走近，再决定是否发问 | 章末牵引更像故事自己继续，而不是作者点题 |
| 续作项目的 drafting 只读当前 board，不读 `story-source-manifest.yaml` 与 relevant 旧作来源，导致前情回响退化成空泛背景说明 | sequel continuity load gap | 在父层装配时显式注入 `story_source_manifest` 摘要与 relevant source refs，并把它们只用于影响当前动作/关系的局部场面 | 固定“续作 continuity 只在影响当前局面时进场”的治理边界；不再让模型靠模糊记忆补前作 | 旧事余波会落成护短、迟疑、回避、旧伤触发等戏内证据 |
| drafting 正文残留“画面骤碎 / 蒙太奇 / 人物名单独报幕”等影视分镜句法，导致文本像脚本而不是小说 | screenplay residue | 在 Step 1 阻断最粗残留，在 Step 8 做总清扫 | 把“分镜残留”提升为 drafting 独立故障类型，合同、validator、终修模块一起承认它 | 章节读起来不再像把分镜说明直接展开成 prose |
| chapter board 明明承诺了三拍或多拍结构，但 Step 1 只落了前半段，后续却被当作“已完成起盘”继续加工 | beat coverage false positive | 在起盘阶段显式检查 `chapter_goal / turning_point / emotion_beat` 的最低 beat 覆盖 | 把“完整起盘”从主观感觉改成 beat 覆盖合同，并让 validator 读取 `beat_checkpoints` | 第001集这类“楔子 -> 反切 -> 恶压落地”不会再只写到前两拍 |

## Repair Playbook

1. 先判断问题出在输入装配、连续性、根文件真源、工序顺序，还是某个子技能的加工维度。
2. 若当前集看起来像“另起一稿”，优先检查是否绕开了 `第N集.md` 单一根文件。
3. 若从第 2 集开始人物/关系突然漂移，先回查上一集终稿是否真的被装进上下文。
4. 若文本只有事件流水，没有文学质感，优先确认 2-8 是否真的按顺序执行，而不是只做了 1。
5. 若问题在 Step 5/6 才暴露，但 `rework_target_step` 指向更早节点，必须回退到最早受影响 step，而不是只修当前步。
6. 收尾固定核对：
   - `第N集.md`
   - `写作日志.yaml`
   - `2-Planning/全息地图.json`
   - `第N-1集.md`（当 `N>1`）
7. 若项目主角启用了成长系统，再核对 `Step 4 / Step 6 / Step 7` 的 `process_log_entry` 是否都留下了 `growth_axis_evidence`；缺一侧时，优先补最早缺失的 step。

## Reusable Heuristics

- `story_map` 对 drafting 最重要的价值不是“给一点点梗概”，而是明确本集欠哪些功能债和线程债。
- 单集写作最稳的方式不是一次成稿，而是让同一份正文在不同加工维度下逐层变厚、变准、变活。
- 对续作项目来说，最稳的 continuity 不是把前作设定再讲一遍，而是让旧债在当前场面里逼出新的动作偏差。
- 第 2 集之后的连续性，通常不是靠“总结上一集”解决，而是靠回读上一集终稿里的情绪、动作和信息停点。
- `写作日志.yaml` 的价值不只是断点恢复，它还能防止某一步被误以为“已经做过了”。
- 即时审计 hook 的价值，不是提前做最终验收，而是在当前步刚写完时立刻拦截会污染后续步骤的早期错误。
- `3-Drafting` 的“串行”不是口头顺序，而是严格 gate：上一 step 没写回且没过 hook，下一 step 就还不存在正式执行资格。
- `8-润色` 之后最合理的状态是“高置信候选终稿”，不是“自判最终 PASS”。
- 起盘是否完整，不能只看“有没有一篇稿”，还要看本集承诺的 beat 有没有真正写到终端碰撞。
- `6-心理活动描写` 最稳的做法不是解释“人物此刻很复杂”，而是把复杂感落进知觉、身体、小动作、欲言又止和半显性自辩。
- `7-追读力强化` 最稳的做法不是把“张力”写得更大声，而是把共享 taxonomy 投影为当前章的主钩、微兑现和章末单一主牵引。
- 爽点设计最容易漂移的不是“名字”，而是“强度、频率、组合和防疲劳规则”；这些更适合独立成共享 guide，而不是混进 taxonomy 表。
- 十集分片模式下，当前集真正要读的是“global index + active slice”；只读 `全息地图.json` 而不解 slice，会让 `chapter_board`、静默窗口和本集线程债务全部失真。
- 主角成长系统在 drafting 最稳的落点不是某一句“他成长了”，而是 `Step 4` 提供行为证据、`Step 6` 提供心路证据、`Step 7` 提供压力与牵引证据，三侧一起为 validation / loopback 供料。
- 当任务层已经把一处句子改到“更像小说”，源层回收时不要只记“改了什么词”，而要记“原来哪一层越过了戏内边界”，例如：作者层术语直落、提纲式问句直落、画面信息重复命名。
- 同一画面里，第一句负责“谁在场”，第二句更适合负责“他们怎么被摆进空间里”；两句都重复身份名词，会立刻长出 prompt 感。
- 对已有 IP / 前作的回响，最稳的落点是人物记忆、自嘲或情绪反弹，而不是作者出来解释“这是前作互文”。
- “画面骤碎 / 蒙太奇 / 某某。” 这一类句子，通常不是文笔还差一点，而是叙事语法还停留在分镜中间态；它们值得被当作独立故障，而不是普通润句问题。
