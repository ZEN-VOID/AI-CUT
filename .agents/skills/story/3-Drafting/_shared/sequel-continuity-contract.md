# Sequel Continuity Contract

## Positioning

本合同服务 `3-Drafting` 在卷级并发模式下对“续作 / 前作 / 已有 IP 余波”的统一装配与落地。

- 它不把 drafting 变成考据 stage。
- 它只回答一件事：当卷内某一集需要借前作事实、旧人物底色或旧事件余波进场时，什么能进、怎么进、进到哪里为止。

## Canonical Inputs

1. `0-Init/story-source-manifest.yaml`
2. `0-Init/init_handoff.yaml`
3. `1-Cards/**/*.json`
4. 当前卷命中的 `2-Planning/第V卷/卷规划.md`
5. 当前章 worker 的 `2-Planning/第V卷/第N章.md`
6. 若卷内前序集已完成：可选读取上一章最终正文 `projects/story/<项目名>/3-Drafting/第N-1集.md`

## Trigger Conditions

命中以下任一信号时，视为当前章必须装配续作 continuity：

- `story-source-manifest.yaml` 存在可供 `3-Drafting` 消费的 `auxiliary_sources / development_briefs`
- 当前 `chapter_goal / emotion_execution / style_execution` 明确要求“旧事余波 / 前作回响 / 既有 IP 关系底色”
- `1-Cards` 角色卡明确写有 `source_refs / inherited_axes / old_character_policy / mirror_axis`

## Hard Rules

1. 旧作回响只能通过戏内载体进入：人物记忆、旧伤、旧物、旧称呼、旧动作习惯、旧羞耻或旧债务。
2. 禁止把“这是前作互文 / 前情提要 / 原著设定如此”直接写成作者说明句。
3. 若前作事实会直接改变本章行为逻辑，必须在 `Step 1` 起盘时就显影，不得把关键因果拖到终修兜底。
4. 在卷级并发模式下，前序集终稿只作为 continuity 增强输入，不作为开工硬门槛；当前章必须先服从当前卷 `卷规划.md / 第N章.md` 里已经声明的 continuity pack。
5. `story-source-manifest.yaml` 里的 source refs 不是自动真源；只有当它们已被当前项目 `Cards / Planning / init_handoff` 接住，才能进入正式正文判断。
6. 若 source refs 与当前 `Cards / Planning` 冲突，以当前项目已落地真源为准；不得为了“像前作”越权覆盖当前项目规划。

## Minimal Landing Forms

前作 continuity 在正文中的最小合格落点，至少满足其一：

- 一句被旧事刺到的即时反应
- 一件旧物或旧伤触发的动作偏差
- 一个只有老关系里才会出现的称呼/回避/护短方式
- 一个能解释当前选择的旧债影子

## Drafting Routing

- `Step 1`：负责决定旧事从哪里进场，以及为什么此刻必须被想起。
- `Step 4`：负责把旧关系写进动作、习惯、保护姿态和失手方式。
- `Step 6`：负责把旧伤、旧羞耻、旧债写进心理运动。
- `Step 8`：只负责清掉作者说明腔，不负责代替前面补 continuity。
