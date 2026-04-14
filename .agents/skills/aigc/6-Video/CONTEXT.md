# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/6-Video` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/6-Video/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 执行者跳过视频请求整理层，直接写 CLI 命令 | 阶段边界层 | 回到 `6-视频` 先生成请求 JSON | 在父级 `When Not to Use` 和 handoff 里固化与 `dreamina-cli` 的边界 | 视频任务先有请求对象再提交 |
| 输入不再读取 `3-Detail/第N集.json`，而改读临时稿或历史 sidecar | 输入真源层 | 回退到 canonical director root file | 在父级 `Execution Summary` 固化唯一主文件 | 新任务先声明 source file |
| 任务明明是分镜组蒸馏，却被误判成首帧类路径 | 父级路由层 | 默认回到 `1-提示词蒸馏/全能参照` | 在父级 `Route Summary` 固化唯一默认入口 | 分镜组视频请求默认落到 `1-提示词蒸馏/全能参照` |
| 只输出 prompt，不输出请求字段与落点 | 输出契约层 | 补写 episode JSON 与 manifest | 在 `output-template.md` 固化“prompt 不是唯一交付” | JSON 能直接进入视频工具或 handoff |
| 继续沿用 `6-视频` 搁浅旧认知 | 根级状态同步层 | 同步更新根技能、registry、routes 与 HARNESS | 把“阶段由搁浅转为部分可执行”视为必须向上同步的元修复 | 根技能与控制面不再把 `6-视频` 视为 frozen |
| 父合同把 `2-视频生成` 写成可执行，但叶子自身仍分散规则或路径口径漂移 | 子路径合同层 | 收敛到唯一 `.agents/skills/aigc/6-Video/2-视频生成/` 路径，并把 provider 空目录降级为 `providers/` 槽位 | 在审计脚本新增“叶子路径、主合同与 sidecar 目录说明必须一致”检查 | `2-视频生成` 的文档、磁盘与审计口径一致 |
| 组级与帧级叶子各自微调 prompt 风格，导致 `图生视频` 句法顺序开始分叉 | 共享句法治理层 | 把跨兄弟叶子的 `图生视频` 句法原则提升到 `6-Video/_shared/image-to-video-prompt-principles.md`，叶子 spec 只写本地 specialization | 当同一 tranche 的多个叶子共享 prompt 取向时，先建立 shared principles 真源，再允许子 spec 做局部特化 | 两个叶子的整体句法顺序和压缩原则保持同源 |

## Repair Playbook

1. 先确认当前任务是否仍属于“视频请求整理层”，而不是已进入模型提交层。
2. 再确认 `projects/aigc/<项目名>/3-Detail/第N集.json` 是否存在且字段完整到可被蒸馏。
3. 再判断当前是组级 `1-提示词蒸馏/全能参照`、帧级 `1-提示词蒸馏/首帧参照`，还是提交前的 `2-视频生成`。
4. 若命中未补齐子路径，显式报告缺口，不下伪执行链。
5. 若阶段状态已变更，记得同步回根技能、registry、routes 与 `HARNESS.md`。

## Reusable Heuristics

- `6-视频` 的第一复杂度不是“怎么生成视频”，而是“怎样先把上游真源变成稳定的视频请求对象”。
- 对当前仓来说，`3-Detail/第N集.json` 比任何临时 prompt 草案都更接近视频阶段的第一事实源。
- 视频阶段与 `dreamina-cli` 的边界应固定为：`6-视频` 负责请求对象，`dreamina-cli` 负责提交与轮询。
- 当阶段从 `shelved` 升级为“部分可执行”时，最容易漏掉的不是叶子文件，而是根技能、registry、routes 与 HARNESS 的同步。
- 当同一视频入参模板开始被多个叶子子技能共用时，应优先提升到 `6-视频/_shared/`，不要继续留在某个子技能私有 `templates/` 中演化。
- 当视频入参既要给工具消费，又要给人直接审读时，优先采用 `第N集.json + 第N集.txt` 双输出，而不是只保留 JSON。
- 当同一 tranche 同时承载组级与帧级叶子子技能时，共享模板必须先抽成中性骨架，再由叶子子技能各自补 `shot_level + source_shot_ids` 约束；不要把组级字段硬写死成全阶段默认。
- 当组级与帧级叶子都要往 `图生视频` 最佳实践靠拢时，最容易漂移的不是字段集合，而是句法顺序；这类共享取向应先沉到 `6-Video/_shared/`，不要让兄弟 spec 各自演化成第二真源。
- 当请求对象已经稳定、任务目标也已转向真实生成时，最稳的做法不是直接跳到 provider 命令，而是先通过 `2-视频生成` 产出可复核的 handoff 包。
