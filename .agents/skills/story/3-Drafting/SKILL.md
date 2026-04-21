---
name: story-drafting
governance_tier: full
description: |
  Use when story2026 needs volume-by-volume manuscript drafting through a volume batch orchestrator that dispatches one episode worker per chapter and converges into ten governed episode manuscripts plus one volume batch log.
tools: [Read, Write, Edit, Grep, Bash]
color: rose
---

# 3-Drafting

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 本阶段的父单元已经从“单集串行父流程”升级为“卷级 orchestrator + 卷内每集 worker”。
- `第N集.md` 仍然是每一集的单一正文真源，但父层调度、恢复、监制、审计与收束的 canonical 单元改为卷。
- 正式执行默认要求命中 `team.yaml` 中已锁定的监制/生产团队，并以真实 subagents/worker 方式执行“一集一个线程”的卷内并发；若上层权限阻断真实 subagent dispatch，必须显式报告降级，而不是把本地顺序模拟伪装成正常并发。

## Overview

`3-Drafting` 现在负责把 `2-Planning` 已经定好的卷地图，翻译成卷内 10 集的成套正文。

新的父层模型固定为：

1. 先锁定当前卷、卷分片、卷内章节范围与 `team.yaml` 监制/生产配置。
2. 父层为卷内每一集组装 `episode_worker_pack`：
   - 当前集 `chapter_board`
   - 卷级 continuity pack
   - 当前卷开放线程 / 伏笔窗口 / 任务债务
   - `Cards / Init / type-pack` 必需真源
3. 父层默认并发启动 10 个 episode workers，每个 worker 只拥有自己那一集的 `第N集.md` 写权。
4. 每个 episode worker 内部仍严格执行 `1 -> 8` 八道工序，且单 worker 内部必须保持“一 step 一写回一 gate”的串行纪律。
5. 父层只做卷级调度、监制、批次日志、候选终稿汇总与 volume-ready 判定，不再把“上一集正文是否存在”当作卷内所有 worker 的硬阻塞门。
6. 当卷内 10 集都达到 `candidate_final_draft` 后，父层再把整卷交给 `4-Validation` 做卷级终验。

一句话裁决：

- `3-Drafting` 的业务正文真源仍然是一组 `第N集.md`。
- `3-Drafting` 的执行治理真源已经改成卷级批次。

## Parent Positioning

### 父层拥有

- `volume scope` 锁定与章节范围裁定
- `team.yaml` 监制/生产团队读取与并发 dispatch 裁定
- 卷级 `continuity pack` 装配
- 卷内每集 worker 的启动、阻断、重试与批次日志
- `第V卷.写作日志.yaml` 的唯一写回
- 卷级 `candidate_volume_draft` 判定
- 失败时回流到当前集 worker、最早受影响 step、或 upstream source fix 的总裁定

### 父层不拥有

- 越权改写 `2-Planning/全息地图.json` 或卷分片规划真源
- 用“卷级大生成”覆盖每个 episode worker 的正式写回
- 把 10 集并成一份总正文文件冒充 canonical manuscript
- 在没有明确阻断说明时，把本地顺序执行说成“后台多线程并发”

## Governed Child Skills

卷内每个 episode worker 仍固定使用以下 8 个受治理子技能：

| order | child skill | worker 内职责 |
| --- | --- | --- |
| 1 | `1-单集叙事起盘` | 建立本集叙事骨架与首轮可读正文 |
| 2 | `2-节奏优化` | 校准本集推进脉冲与段落呼吸 |
| 3 | `3-场景和氛围渲染` | 强化空间、感官与情景气压 |
| 4 | `4-角色形象刻画` | 强化动作、人物偏移、关系受压与行为选择 |
| 5 | `5-对白个性化` | 让对白回到角色、关系与局面 |
| 6 | `6-心理活动描写` | 写稳 POV、内心运动与身体化知觉 |
| 7 | `7-追读力强化` | 拉高钩子、微兑现与章末牵引 |
| 8 | `8-润色` | 统一自然感并清扫 AI 味 / meta 腔 |

硬规则：

- 卷内可以多 worker 并发。
- 单个 worker 内的 `1 -> 8` 永远禁止并发。

## Shared Canonical Sources

- `./_shared/episode-root-contract.md`
- `./_shared/episode-root.template.md`
- `./_shared/process-log.template.yaml`
- `./_shared/drafting-child-output-contract.md`
- `./_shared/drafting-instant-validation-contract.md`
- `./_shared/sequel-continuity-contract.md`
- `./_shared/chapter-board-locating-contract.md`
- `../4-Validation/_shared/validation-dimension-registry.yaml`
- `../_shared/context-loading-contract.md`
- `../_shared/core-constraints.md`

## Canonical Runtime

### 正文真源

- `projects/story/<项目名>/3-Drafting/第N集.md`

### 卷级批次真源

- `projects/story/<项目名>/3-Drafting/第V卷.写作日志.yaml`

### 业务语义

- 每一集正文只有一份 `第N集.md`
- 每一卷只有一份卷级批次日志
- 卷级日志记录 worker 状态、step history、inline validation 摘要、监制回指与恢复指针

## Volume Continuity Contract

本阶段不再把“上一集终稿”设为卷内并发的硬启动门。

新的连续性规则固定为：

1. **硬输入**是 `2-Planning` 已声明的卷级 continuity pack：
   - 当前卷 `volume_board`
   - 每集 `chapter_board`
   - 卷内开放线程 / 任务债务 / 伏笔静默窗口
   - 当前集 `entry_state / carryover_threads / expected_exit_delta`
2. **可选增强输入**才是上一集终稿：
   - 若前序集已完成，允许当前集 worker 读取它做二次校准
   - 若前序集尚未完成，不得因此阻塞当前集开工
3. 当前集 worker 必须优先服从卷地图 continuity pack，而不是临场猜测上一集会怎么写。
4. 若卷内前序集后续实际写成与 planning continuity pack 明显冲突，应在当前卷批次内触发 targeted re-sync，而不是恢复旧的“全卷串行等上一集”模型。

## Team / Subagent Contract

默认执行模式固定为：

- `dispatch_mode = team-supervised-parallel-workers`
- `worker_granularity = one-episode-per-worker`
- `worker_count = 当前卷章节数，默认 10`

父层必须：

1. 优先读取 `projects/story/<项目名>/team.yaml`
2. 锁定本卷使用的监制 / 评审 / 生产角色
3. 以监制视角监督 worker 进度、质量门与回退
4. 在卷级日志中记录：
   - `worker_ref`
   - `chapter_ref`
   - `monitor_ref`
   - `status`
   - `latest_completed_step`
   - `block_reason`

若真实 subagents 不可用，必须显式报告：

- 阻断层级
- 原本应采用的并发路径
- 实际降级成的本地串行或半并发路径
- 哪些监制/worker 没有真实启动

## Total Input Contract

### 必需输入

- `0-Init/north_star.yaml`
- `0-Init/init_handoff.yaml`
- `0-Init/story-source-manifest.yaml`
- `1-Cards/0-全局卡/**/*.json`
- `1-Cards/**/*.json`
- `2-Planning/全息地图.json`
- 当前卷命中的 `2-Planning/卷分片/*.json`
- `volume_ref / volume_num`
- 当前卷的 `chapter_refs`
- `team.yaml`

### 可选增强输入

- 卷内已完成前序集的 `第N集.md`
- 既有 `第V卷.写作日志.yaml`
- 历史批次或 crash 后残留的 batch artifact

### 硬规则

1. `2-Planning/卷分片/*.json` 在本阶段语义上等同于卷分片；固定 `10 章 = 1 卷` 时，卷分片就是卷地图 carrier。
2. 父层必须先锁 `volume_board + chapter_refs + continuity pack`，再允许任何 worker 开始。
3. 当前卷 worker 默认并发，但单 worker 内仍必须严格串行执行 `1 -> 8`。
4. `第N集.md` 是 worker 级单一正文真源；不得生成 `第N集-pass2.md` 等 sibling manuscript。
5. `第V卷.写作日志.yaml` 是父层批次日志真源；不得再并行维护第二份卷级 batch ledger。
6. “上一集终稿”从阻塞门降为可选增强门；卷内并发不得因为等待上一集全文而停摆。
7. 若某 worker inline validation 失败，只阻断该 worker 或显式波及的受影响 workers，不得把整卷静默拖死。
8. 当卷内全部章节达到 `candidate_final_draft` 前，不得把整卷宣布为 ready-for-validation。

## Dispatch Order Contract

### 卷级主干

1. `N1-VOLUME-LOCK`
2. `N2-CONTEXT-ASSEMBLY`
3. `N3-WORKER-DISPATCH`
4. `N4-WORKER-PROGRESSIVE-REWRITE`
5. `N5-VOLUME-READY-GATE`
6. `handoff to 4-Validation`

### Worker 内部固定顺序

`1-单集叙事起盘 -> hook -> 2-节奏优化 -> hook -> 3-场景和氛围渲染 -> hook -> 4-角色形象刻画 -> hook -> 5-对白个性化 -> hook -> 6-心理活动描写 -> hook -> 7-追读力强化 -> hook -> 8-润色 -> hook -> candidate_final_draft`

### 并发规则

- 允许并发：
  - 卷内不同 episode workers
  - 同一 worker 内部的候选比较 / reviewer 会诊 / 句式实验
- 禁止并发：
  - 单个 worker 的正式 step 写回
  - 同一 `第N集.md` 上的多 worker 写入
  - 同一卷级日志的无锁并发覆写

## Output Contract

### Canonical outputs

- `projects/story/<项目名>/3-Drafting/第N集.md`
- `projects/story/<项目名>/3-Drafting/第V卷.写作日志.yaml`

### 卷级完成定义

父层只有在以下条件同时成立时，才能产出 `candidate_volume_draft`：

- 当前卷全部 `chapter_refs` 都已有 `第N集.md`
- 每个 worker 都已完成 `Step 8`
- 每个 worker 的 inline hooks 均为 `pass`
- 卷级日志中不存在未处理的 `block_reason`

## Failure Routing Contract

- 单 worker 质量问题：
  - 回到该 worker 的最早受影响 step
- 卷内 continuity pack 失真：
  - 回到 `2-Planning`
- `Cards / Init / type-pack` 真源冲突：
  - 回到相应 source owner
- 因上层权限无法真实并发：
  - 显式报告并进入降级执行

## Completion Contract

- 当前卷的章节范围、卷分片与 team 监制配置已锁定
- 卷内每个 worker 的 step 进度与 block 状态可追踪
- 全部章节已形成 `candidate_final_draft` 后，才把整卷交给 `4-Validation`
