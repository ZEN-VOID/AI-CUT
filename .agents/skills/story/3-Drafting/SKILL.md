---
name: story-drafting
governance_tier: full
description: |
  Use when story2026 needs volume-by-volume manuscript drafting through a volume batch orchestrator that dispatches one chapter worker per chapter and converges into ten governed chapter manuscripts plus one volume batch log.
tools: [Read, Write, Edit, Grep, Bash]
color: rose
---

# 3-Drafting

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 本阶段的父单元已经从“单章串行父流程”升级为“卷级 orchestrator + 卷内每章 worker”。
- `Step 2 / 2-节奏优化` 继续保留为正式 runtime 工序，但不再维护独立子技能目录；其执行真源统一回收到 `./_shared/chapter-rhythm-execution-contract.md`。
- `projects/story/<项目名>/3-Drafting/第N卷/第N章.md` 仍然是每一章的单一正文真源，但父层调度、恢复、监制、审计与收束的 canonical 单元改为卷。
- 新增 `正文/` chapter-native 直写 child：当用户明确要求“按章写正文 / 写到 `第N卷/第N章.md` / 命中 `正文`”时，必须进入该 child，并额外加载 `全局卡 + 风格卡 + north_star + 项目 CONTEXT + 上一章正文`；其 actual creative step 固定走 AnyFast `doubao-seed-2.0-pro`，不得默认回退成本地 GPT 直写。
- 正式执行默认要求命中 `team.yaml` 中已锁定的监制/生产团队，并以真实 subagents/worker 方式执行“一章一个线程”的卷内并发；若上层权限阻断真实 subagent dispatch，必须显式报告降级，而不是把本地顺序模拟伪装成正常并发。

## Overview

`3-Drafting` 现在负责把 `2-Planning` 已经定好的整书规划、当前卷规划和当前章规划，翻译成当前卷 `chapter_refs` 对应的一组成套正文。

新的父层模型固定为：

1. 先锁定当前卷、当前卷规划目录、卷内章节范围与 `team.yaml` 监制/生产配置。
2. 父层为卷内每一章组装 `chapter_worker_pack`：
   - 当前章 `3-Drafting/第N卷/第N章.md`
   - 当前卷 `卷规划.md`
   - 整书 `整体规划.md`
   - 当前卷开放线程 / 伏笔窗口 / 任务债务
   - `Cards / Init` 中与当前题材相关的必需真源
3. 父层默认按当前卷 `chapter_refs` 并发启动 chapter workers，每个 worker 只拥有自己那一章的 `第N章.md` 写权；默认卷长是 `10`，但项目声明例外时必须服从项目映射。
4. 每个 chapter worker 内部仍严格执行 `1 -> 8` 八道工序，且单 worker 内部必须保持“一 step 一写回一 gate”的串行纪律。
5. 父层只做卷级调度、监制、批次日志、候选终稿汇总与 volume-ready 判定，不再把“上一章正文是否存在”当作卷内所有 worker 的硬阻塞门。
6. 当卷内全部 `chapter_refs` 都达到 `candidate_final_draft` 后，父层再把整卷交给 `4-Validation` 做卷级终验。

一句话裁决：

- `3-Drafting` 的业务正文真源仍然是一组 `3-Drafting/第N卷/第N章.md`。
- `3-Drafting` 的执行治理真源已经改成卷级批次。
- 当诉求是明确的 chapter-native 直写时，路由应切到 `正文/` child，由它输出 `projects/story/<项目名>/3-Drafting/第N卷/第N章.md`。
- 当诉求命中 `正文/` child 时，本地脚本只负责上下文装配与写回，正文创作本身必须由豆包 provider 实际执行。

## Parent Positioning

### 父层拥有

- `volume scope` 锁定与章节范围裁定
- `team.yaml` 监制/生产团队读取与并发 dispatch 裁定
- 卷级 `continuity pack` 装配
- 卷内每章 worker 的启动、阻断、重试与批次日志
- `第V卷.写作日志.yaml` 的唯一写回
- 卷级 `candidate_volume_draft` 判定
- 失败时回流到当前章 worker、最早受影响 step、或 upstream source fix 的总裁定

### 父层不拥有

- 越权改写 `2-Planning/整体规划.md`、`第N卷/卷规划.md`、`第N卷/第N章.md`
- 用“卷级大生成”覆盖每个 chapter worker 的正式写回
- 把 10 章并成一份总正文文件冒充 canonical manuscript
- 在没有明确阻断说明时，把本地顺序执行说成“后台多线程并发”

## Execution Units

卷内每个 chapter worker 仍固定走 8 道正式工序；其中 `Step 2` 为父层 owning 的 shared 节奏兑现工序，其余步骤继续由受治理子技能承担：

| order | execution unit | worker 内职责 |
| --- | --- | --- |
| 1 | `1-单章叙事起盘` | 建立本章叙事骨架与首轮可读正文 |
| 2 | `父层 owning Step 2 / 2-节奏优化` | 兑现 planning 已锁节奏 handoff，校准本章推进脉冲、段落呼吸、`pulse_ladder` 与 `rhythm_type` |
| 3 | `3-场景和氛围渲染` | 强化空间、感官与情景气压 |
| 4 | `4-角色形象刻画` | 强化动作、人物偏移、关系受压与行为选择 |
| 5 | `5-对白优化` | 让对话自然、鲜活，并准确服务角色、关系与叙事 |
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
- `./_shared/drafting-quality-gate-contract.md`
- `./_shared/chapter-rhythm-execution-contract.md`
- `./_shared/sequel-continuity-contract.md`
- `./_shared/chapter-board-locating-contract.md`
- `../4-Validation/_shared/validation-dimension-registry.yaml`
- `../_shared/context-loading-contract.md`
- `../_shared/core-constraints.md`

## Canonical Runtime

### 正文真源

- `projects/story/<项目名>/3-Drafting/第N卷/第N章.md`

### chapter-native 直写 child 真源

- `projects/story/<项目名>/3-Drafting/第N卷/第N章.md`
- 仅当显式命中 `正文/` child 时启用。
- 该路径要求 YAML 头显式包含 `global_context + style_context + north_star_chapter_brief`。

### 卷级批次真源

- `projects/story/<项目名>/3-Drafting/第V卷.写作日志.yaml`

### 业务语义

- 每一章正文只有一份 `第N卷/第N章.md`
- 每一卷只有一份卷级批次日志
- 卷级日志记录 worker 状态、step history、inline validation 摘要、监制回指与恢复指针

## Volume Continuity Contract

本阶段不再把“上一章终稿”设为卷内并发的硬启动门。

新的连续性规则固定为：

1. **硬输入**是 `2-Planning` 已声明的三层规划真源：
   - 整书 `整体规划.md`
   - 当前卷 `第V卷/卷规划.md`
   - 当前章 `第V卷/第N章.md`
   - 其中当前章必须明确给出 `章末达成 / 本章任务线 / 本章冲突 / 本章线索 / 本章伏笔`
2. **可选增强输入**才是上一章终稿：
   - 若前序集已完成，允许当前章 worker 读取它做二次校准
   - 若前序集尚未完成，不得因此阻塞当前章开工
3. 当前章 worker 必须优先服从三层规划真源，而不是临场猜测上一章会怎么写。
4. 若当前章正文与章级规划、卷级规划或整书规划明显冲突，应在当前卷批次内触发 targeted re-sync，而不是恢复旧的“全卷串行等上一章”模型。

## Team / Subagent Contract

默认执行模式固定为：

- `dispatch_mode = team-supervised-parallel-workers`
- `worker_granularity = one-chapter-per-worker`
- `worker_count = 当前卷章节数，默认 10，但项目声明例外时以项目映射为准`

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
- `2-Planning/整体规划.md`
- 当前卷 `2-Planning/第V卷/卷规划.md`
- 当前卷各章 `2-Planning/第V卷/第N章.md`
- `volume_ref / volume_num`
- 当前卷的 `chapter_refs`
- `team.yaml`

### 可选增强输入

- 卷内已完成前序集的 `第N章.md`
- 既有 `第V卷.写作日志.yaml`
- 历史批次或 crash 后残留的 batch artifact

### 硬规则

1. `2-Planning/第V卷/卷规划.md + 第N章.md` 是本阶段的 primary planning carrier；默认 `10 章 = 1 卷`，但项目若在 `STATE.json.progress.volumes_planned` 或等效真源里声明例外，当前卷目录必须服从项目映射。
2. 父层必须先锁 `整体规划 + 卷规划 + chapter_refs`，再允许任何 worker 开始。
3. 当前卷 worker 默认并发，但单 worker 内仍必须严格串行执行 `1 -> 8`。
4. `第N章.md` 是 worker 级单一正文真源；不得生成 `第N章-pass2.md` 等 sibling manuscript。
5. `第V卷.写作日志.yaml` 是父层批次日志真源；不得再并行维护第二份卷级 batch ledger。
6. “上一章终稿”从阻塞门降为可选增强门；卷内并发不得因为等待上一章全文而停摆。
7. 若某 worker inline validation 失败，只阻断该 worker 或显式波及的受影响 workers，不得把整卷静默拖死。
8. 当卷内全部章节达到 `candidate_final_draft` 前，不得把整卷宣布为 ready-for-validation。
9. `第V卷.写作日志.yaml` 不是允许“Step 8 完成摘要回填”了事的稀疏台账；父层必须为当前卷每一章写满 `1 -> 8` 八条正式 `process_log_entry`，并为每一步同步落下对应 hook 结果，形成完整的 `chapter_refs x 8 步` 审计轨迹。
10. 任一章节若缺少某一步正式 `process_log_entry`、缺少该步 hook 结果、或以汇总性补记冒充逐步留痕，则该章节不得获得 `candidate_final_draft`；父层也不得把整卷推进到 `candidate_volume_draft`。
11. 任一章节若正文仍是“压缩剧情稿 / 摘要式成稿 / 仅够证明 planning 已落位”的密度，而未达到章节级小说正文，不得获得 `candidate_final_draft`。
12. 默认必须通过 `scripts/drafting_manuscript_guard.py` 的 `chapter-complete manuscript` 守门，才可把当前 `第N章.md` 视为可收口正文；该守门至少检查正文主体长度、段落密度与 planning `exit_hook` 落位。
13. 卷级 `candidate_volume_draft` 不等于“可直接进 `4-Validation`”；在准备移交终验前，父层必须先写回 `第V卷.写作日志.yaml -> quality_gate_snapshot`。
14. 默认必须通过 `scripts/drafting_volume_quality_guard.py` 的卷级质量守门，才能把下一稳定入口写成 `4-Validation`；若 guard 判定 `rework_required_before_validation`，必须回切到 `3-Drafting`，不得继续伪装成“待 validation”。

## Dispatch Order Contract

### 卷级主干

1. `N1-VOLUME-LOCK`
2. `N2-CONTEXT-ASSEMBLY`
3. `N3-WORKER-DISPATCH`
4. `N4-WORKER-PROGRESSIVE-REWRITE`
5. `N5-VOLUME-READY-GATE`
6. `handoff to 4-Validation`

### Worker 内部固定顺序

`1-单章叙事起盘 -> hook -> 父层 owning Step 2 / 2-节奏优化 -> hook -> 3-场景和氛围渲染 -> hook -> 4-角色形象刻画 -> hook -> 5-对白优化 -> hook -> 6-心理活动描写 -> hook -> 7-追读力强化 -> hook -> 8-润色 -> hook -> candidate_final_draft`

### 并发规则

- 允许并发：
  - 卷内不同 chapter workers
  - 同一 worker 内部的候选比较 / reviewer 会诊 / 句式实验
- 禁止并发：
  - 单个 worker 的正式 step 写回
  - 同一 `第N章.md` 上的多 worker 写入
  - 同一卷级日志的无锁并发覆写

## Output Contract

### Canonical outputs

- `projects/story/<项目名>/3-Drafting/第N卷/第N章.md`
- `projects/story/<项目名>/3-Drafting/第V卷.写作日志.yaml`

### 卷级完成定义

父层只有在以下条件同时成立时，才能产出 `candidate_volume_draft`：

- 当前卷全部 `chapter_refs` 都已有 `第N章.md`
- 每个 worker 都已完成 `Step 8`
- 每个 worker 的 inline hooks 均为 `pass`
- 每个 `第N章.md` 都已通过 `scripts/drafting_manuscript_guard.py`，不再属于摘要式压缩稿
- `第V卷.写作日志.yaml.chapter_step_history` 中每个 `chapter_ref` 都已写满 8 条按顺序排列的正式 step 记录
- `第V卷.写作日志.yaml.chapter_hook_results` 中每个 `chapter_ref` 都已写满 8 条与 step 对位的一步一 gate 结果
- 卷级日志中不存在未处理的 `block_reason`

### 预终验质量门

父层把 `candidate_volume_draft` 移交给 `4-Validation` 前，还必须额外满足：

- `第V卷.写作日志.yaml` 已写入 `quality_gate_snapshot`
- `quality_gate_snapshot.verdict == ready_for_validation`
- 五个默认 guard axes 全部 `pass`：
  - `anti_formula_progression`
  - `relationship_friction`
  - `spatial_separation`
  - `antagonist_face`
  - `volume_closure`
- `scripts/drafting_volume_quality_guard.py` 返回 `pass`

若以上任一条件不成立：

- 当前卷可保留 `candidate_volume_draft`
- 但下一稳定入口必须仍是 `3-Drafting`
- `resume/` 与 runtime 不得把该卷误判为 ready-for-validation

## Failure Routing Contract

- 单 worker 质量问题：
  - 回到该 worker 的最早受影响 step
- 卷内 continuity pack 失真：
  - 回到 `2-Planning`
- `Cards / Init` 题材真源冲突：
  - 回到相应 source owner
- 因上层权限无法真实并发：
  - 显式报告并进入降级执行

## Completion Contract

- 当前卷的章节范围、卷规划目录与 team 监制配置已锁定
- 卷内每个 worker 的 step 进度与 block 状态可追踪
- 全部章节已形成 `candidate_final_draft` 后，才把整卷交给 `4-Validation`
