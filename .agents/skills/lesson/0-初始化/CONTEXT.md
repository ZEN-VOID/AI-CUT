# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `lesson/0-初始化` 的经验层知识库，不是第二份初始化合同。
- 调用 `.agents/skills/lesson/0-初始化/SKILL.md` 时，必须同时加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / meta 规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- recommended_action: keep-scaffold-heuristics

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 初始化阶段开始写课程大纲、目标蓝图、题库或课时正文 | scaffold-only 边界漂移 | 回到 `SKILL.md` 的 denylist，只创建目录、`MEMORY.md` 与 `CONTEXT/README.md` | 后续每个阶段自己拥有业务主稿和验收 gate | 新项目初始化后没有 `course-outline.md`、`objective-map.yaml` 或题库文件 |
| DOC/PPT/HTML 三端目录重复或散落 | 交付容器边界不清 | 固定三端叶子为 `8-多端交付生成/doc|ppt|html` | 不额外创建根 `outputs/`，避免双输出真源 | 三端成品只有一个 canonical 落点 |
| 共享课程内容模型缺少稳定入口 | content-model 真源缺口 | 初始化创建空 `content-model/modules|lessons|assessments` 容器 | 后续阶段把课程结构、课时正文、测评结构回写到同一内容模型 | `content-model/` 存在但初始化不写业务内容 |
| 用户长期口味没有进入项目记忆 | MEMORY 写回缺口 | 在 `MEMORY.md` 记录初始化时用户长期要求 | 将长期偏好和一次性任务指令分开 | 项目 `MEMORY.md` 可读到长期偏好或明确暂无 |
| 空阶段目录被误认为阶段已完成 | runtime 状态误读 | 明确空目录只是 readiness container | 后续查询/恢复只把真实文件产物视为阶段输出 | 初始项目不会因空目录被判定为 1-8 已执行 |

## Repair Playbook

1. 先确认任务是否真的属于 lesson/courseware 初始化。
2. 若是路径问题，先回到 `projects/lesson/<项目名>/` canonical root。
3. 若误生成业务文件，先移出初始化完成口径，并把内容交给 owning stage 重新判定。
4. 若 `MEMORY.md` 已存在，任何更新都只能合并、追加或按用户明确撤销替换，不得静默覆盖。
5. 若出现重复输出根，优先保留 `8-多端交付生成/doc|ppt|html` 作为三端交付位置。

## Reusable Heuristics

- lesson 初始化的目标是让课程课件项目能进入 `1-课程定位`，不是提前做教学设计。
- `sources/` 是原始资料或用户提供资料的入口；资料摘要和证据账本由 `2-资料吸收与知识建模` 负责。
- `content-model/` 是后续 DOC/PPT/HTML 的共享业务模型容器；初始化只能创建空容器，不写假模型。
- `assets/` 是图像、图表、媒体素材的共享容器；视觉策略由 `7-视觉媒体与交互设计` 负责。
- 三端最终交付物统一落到 `8-多端交付生成/` 的对应叶子，避免根层再出现第二套 `outputs/`。
- 每次发现初始化骨架与 lesson 主链命名不一致，优先修 `SKILL.md` 的 `Canonical Runtime Skeleton`。

## Case Log

> 仅记录里程碑级经验，避免过程流水。

### Case-001

- milestone_type: scaffold_contract_creation
- outcome: 建立 lesson 课程课件初始化阶段的 scaffold-only runtime spine。
- design_decision: 初始化创建 0-8 阶段、`sources/`、`content-model/`、`assets/`、项目 `MEMORY.md` 与 `CONTEXT/README.md`；不创建课程主创或交付成品。
- replication_checklist: 先判媒介和路径，再建 allowlist，最后读回 denylist。
- evidence_paths: `.agents/skills/lesson/0-初始化/SKILL.md`
