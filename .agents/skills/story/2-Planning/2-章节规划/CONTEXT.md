# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `2-章节规划` 子技能包的局部经验层，只服务 `2-Planning` Step 2。
- 加载顺序固定为：先读同目录 `SKILL.md`，再按需读取本文件。
- 跨 child 的挂章与 holomap 收束经验仍回写到 `2-Planning/CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 章节规划只有数量没有功能槽 | child contract | 补齐 chapter / volume blocks 与 function slots | 在子技能合同固化章节容器优先级 | Step 3-7 能稳定挂入章节容器 |
| 体量与对象密度失衡 | density contract | 回修 density contract 的区间带 | 在 Step 2 统一裁决密度，不让后序重发明 | holomap 能回指各类对象负荷 |
| 只有卷数和章数，没有整书波形 | macro rhythm scaffold | 回到 `Save the Cat` 拍点走廊，补 `macro_rhythm_scaffold` | 固定“Step 2 先锁整书节奏骨架，再让 Step 3 挂主干” | Step 3 能回答整书何处转向、何处见底、何处冲刺 |
| 中段发虚，所有卷都像同一档位推进 | midpoint / pressure corridor | 强制标出 `midpoint_shift`、`bad_guys_close_in` 与 `all_is_lost_corridor` | 在 Step 2 固化“中段必须改向、后段必须压缩” | 中盘不再只有事件累加而无波形变化 |
| B Story 和主题线没有被规划承载 | theme carrier planning | 指定 `theme_carrier / b_story_carrier`，把其写进节奏骨架 | 把主题与副线承载写成 Step 2 必填项，不再等 Step 3 临时补 | 后续冲突、任务、关系线都能回指谁在承担主题压力 |
| 卷尾或集尾总是平收 | entry/exit hook design | 在 volume wave 和 episode rhythm role 中补 `entry_promise / exit_hook` 摘要 | Step 2 固定给每卷/关键集分配“卷内 promise 与卷尾牵引” | 下游 drafting 能明确知道本卷/本集要用什么钩子离场 |
| 总风格只停在 `0-Init`，卷与卷写法没拉开 | volume planning contract | 回到 Step 2 补 `volume_board` 的卷级表现合同与 `slice_style_contract` | 在 Step 2 固化“卷级规划是一等输出，不是摘要附注” | downstream 能回答每卷的视觉气候、动作语法、悬疑密度与禁忌写法 |
| 集节奏只有抽象 role，没有具体可执行骨架 | episode rhythm under-spec | 回到 `episode-rhythm-rules.md`，补齐统一七步骨架与本集投影 | 固定 `episode_rhythm_roles` 至少写 `pack + mode + seven-step projection` | drafting 能直接知道本集怎么起、怎么升、怎么收 |
| 连续几集都落在同一种节奏音色，整段读感发闷 | polarity monotony | 为相邻集补 `yin_yang_polarity / polarity_sequence_note`，重新安排势能式与动能式切换 | 把“阴阳交替或成段切换”写成 Step 2 的显式检查项 | 集与集之间出现清晰转调，而不是一路同温 |
| 动静结合被误用成“静集写回忆，动集写打斗” | pack flattening | 回到七步骨架重写，强调它是推进策略，不是题材表面元素 | 在 pack 合同中固定 `fit_signals / misuse_signals` | 势能式也有不可逆高潮，动能式也不等于全程吵闹 |
| drafting 无法挂章 | handoff contract | 回到本 child 修章节容器，而非直接补 holomap | 固化“挂章失败先回 Step 2” | 下游不再出现临时拼章板 |
| 章节板直接复制角色卡正文 | cross-stage bridge | 只保留 `bundled_elements.characters + planned_state.character_focus` | 通过共享桥合同固定 board 只写角色/关系 refs | board 可引用角色，但不膨胀成第二份角色卡 |

## Repair Playbook

1. 先估算整书体量与卷数，再定章节容器。
2. 再用 `Save the Cat` 扩展框架锁 `catalyst / break_into_2 / midpoint / all_is_lost / finale` 等拍点走廊。
3. 把角色、线索、伏笔与爽点压力翻译成 density contract 和 volume wave。
4. 把总风格和题材 promises 下沉为每卷的表现合同，并在当前 slice 镜像为 `slice_style_contract`。
5. 检查关键节奏窗口、卷尾牵引与 `episode_rhythm_roles` 是否显式存在，并确认已写出 `pack + mode + seven-step projection`。
6. 收尾用 Step 3 与 downstream drafting 反查容器、卷级合同与节奏骨架是否可消费。

## Reusable Heuristics

- 章节规划最怕“平均主义”，真正稳定的是功能槽而不是均分章数。
- `Save the Cat` 在长篇/连载里最有价值的不是 15 个标签本身，而是帮你提前知道：哪一段该承诺、哪一段该转向、哪一段绝不能再拖。
- 当长线负荷上升时，应优先增加稳定挂点，而不是只增加章节总量。
- `Midpoint` 如果不能改变整部书的玩法，后半部通常就会显得像前半部的加长版。
- `All Is Lost` 不一定是单一章节，但一定要是一个读者能明显感觉“局势真的塌了”的走廊。
- Step 2 如果没站稳，后面的故事大纲和 holomap 通常都会看起来“像对的”，但用起来发虚。
- 章节板对角色最好的写法不是复制人物设定，而是锁 `谁在场 + 此章承受哪段角色/关系推进`。
- 卷级节奏最稳的写法，不是把每卷都写成同一种模板，而是让每卷都承担不同的 `wave duty`：给 promise、做扩张、强改向、压缩到底、收束兑现。
- 最稳的 Step 2 不是只有 `volume_boards` 这个名字，而是让 `volume_boards` 真正承担卷级 planning contract；否则执行时很容易退化成“卷名 + 一句剧情摘要”。
- 当项目已经有强风格基调时，Step 2 必须把它拆成每卷各自的 `visual_climate / action_grammar / mystery_mode / emotional_temperature / taboo_writeups`，否则后续 child 只会继承剧情，不会继承表现。
- 十集分片模式下，Step 2 既拥有 manifest/薄 axis，也拥有 slice `chapter_boards`；若这两层不同步，后续所有 episode 定位都会漂。
- `slice_style_contract` 的价值不在重复卷摘要，而在把当前十集必须 obey 的卷级写法送到 episode-local 层，防止 drafting 只看到 chapter goal 看不到卷的表现语法。
- 集节奏最怕“只有 role 没有写法”。真正能落地的集节奏，必须同时回答：这集选了什么包、什么 mode、七步各自怎么跑。
- `动静结合` 的价值不是把集分成“静集”和“动集”两类，而是给整部书提供两种互补音符：一种蓄压，一种爆发。
- 势能式最稳的关键不在“慢”，而在“平静外观下的持续加压”；若没有第 5-6 步的陷深与不可逆，势能式很容易写空。
- 动能式最稳的关键不在“猛”，而在“迷阵 + 反转 + 再升级”的节奏接力；若只有开场激突，后面却没有翻面，动能式也会很快失速。
