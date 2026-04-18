# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `resume/` 的经验上下文知识库，不是执行流水账。
- 每次调用 `resume/` 时，应自动预加载本文件，用于判断恢复范围、识别危险恢复建议与沉淀恢复 heuristics。
- 优先级固定为：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok
- action_policy:
  - ok: 优先更新 Type Map / Repair Playbook / Reusable Heuristics。
  - warn: 对当前 skill context 做定向压缩与结构整理。
  - critical: 先归档旧案例，再继续大规模追加。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
|---|---|---|---|---|
| `resume/` 仍把 query 当成正式断点恢复对象 | skill contract | 在 `SKILL.md` 明确只正式支持 `story-write` / `story-review` | 把 unsupported scope 写成显式表格，禁止伪造断点续跑 | `resume` 文档不再把 query 描述成 tracked workflow |
| 恢复建议仍引用 `git reset --hard` 或假定存在章节 tag | script gate + reference contract | 同时修 `workflow_manager.py` 与 `workflow-resume.md`，改成 preview-confirm cleanup / manual inspection | 在 skill 与脚本双层写死“禁止 destructive 默认动作” | `detect`/参考文档/skill 文档都不再出现默认硬回滚 |
| 恢复后默认退回旧 `大纲/` | shared data-flow contract | 在 `resume` 写死 holomap-first | 在 `resume` 与共享 data-flow 文档中同步固定 | 恢复继续 drafting/query 时明确优先 `全息地图.json` |
| `resume/` 与 `5-Loopback` actualization 职责混淆 | stage contract | 在 `resume/SKILL.md` 明确其是 satellite recovery skill | 在 `5-Loopback` 与 `resume` 同时固定边界 | 不再把恢复动作描述成 truth writeback |
| 旧文档仍把 `Step 1.5` 当当前正式 tracked step | drafting contract drift | 改成 legacy compatibility note | 在 `resume` 文档中区分“当前 tracked step”与“旧状态兼容” | 当前 step 表以 `workflow_manager.get_pending_steps()` 为准 |
| `resume` 只看 `workflow_state.json`，看不到全阶段 run / stage_progress / task log | execution-state contract | 为 `resume` 增加 `execution_state.json + task_log.jsonl` 读取语义，并把 registry 扩到全阶段 commands | 在脚本与参考文档同步固定“三件套分工” | `resume/status` 可判断 init/cards/plan/validate/loopback/query 等非 drafting run |

## Repair Playbook

1. 先确认问题是“文档说错了”、还是“脚本真的给错了恢复建议”。
2. 层层上溯：`Symptom -> Direct Cause -> resume 合同/参考文档/脚本 -> AGENTS.md`。
3. 优先修高杠杆源头：
   - `scripts/workflow_manager.py`
   - `resume/SKILL.md`
   - `resume/references/workflow-resume.md`
4. 再补本次恢复话术，不允许只在最终回答里口头规避。
5. 修完后必须验证：
   - 是否仍出现危险默认动作
   - 是否仍误导到旧规划真源
   - 是否仍把 unsupported task 当成 tracked workflow

## Reusable Heuristics

- `resume/` 恢复的不是“用户记忆中的上一步”，而是“当前系统还能证明的最后稳定入口”。
- 只要 workflow 没有正式记录某类任务，就不要为了体验平滑而伪造“断点续跑”。
- 恢复建议若涉及删除正文或 Git 操作，优先做 preview-confirm 两段式，再执行实际清理。
- `resume/` 最容易过时的不是命令名，而是“它以为自己在接回哪个 stage”；每次大改 stage 边界后都要重新核对。
- 当 `detect` 输出只是诊断原料时，`resume/` 还必须做人类可执行的二次归一化，不能把脚本内部动作说明直接当 SOP。
- 一旦仓库已经有 `workflow_state + execution_state + task_log` 三件套，恢复判断就不该再只靠单一 current_task；优先看 run registry，再看兼容断点，再看事件链。
- `resume/` 的正式支持清单必须跟 `workflow_manager.py` registry 同步缩放；命令下线后，不保留“理论上还能恢复”的幽灵入口。

