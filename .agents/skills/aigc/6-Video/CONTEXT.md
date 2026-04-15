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
| 只输出 prompt，不输出请求字段与落点 | 输出契约层 | 补写 episode JSON 与 manifest | 在父级与命中叶子的输出合同中固化“prompt 不是唯一交付” | JSON 能直接进入视频工具或 handoff |
| 继续沿用 `6-视频` 搁浅旧认知 | 根级状态同步层 | 同步更新根技能、registry、routes 与 HARNESS | 把“阶段由搁浅转为部分可执行”视为必须向上同步的元修复 | 根技能与控制面不再把 `6-视频` 视为 frozen |
| 父合同仍把提交前组织层写成 `2-视频生成`，但真实链路已经扩展为 `2-参照引用 -> 3-视频生成` | 子路径合同层 | 把父级与根级路由统一收束到真实链路，并把 provider 空目录继续降级为 `providers/` 槽位 | 在阶段父合同固定“先绑定引用，再进入生成 handoff”的显式分流 | `2-参照引用` 与 `3-视频生成` 的文档、磁盘与路由口径一致 |
| 组级与帧级叶子各自微调 prompt 风格，导致 `图生视频` 句法顺序开始分叉 | 共享句法治理层 | 把跨兄弟叶子的 `图生视频` 句法原则提升到 `6-Video/_shared/image-to-video-prompt-principles.md`，叶子 spec 只写本地 specialization | 当同一 tranche 的多个叶子共享 prompt 取向时，先建立 shared principles 真源，再允许子 spec 做局部特化 | 两个叶子的整体句法顺序和压缩原则保持同源 |
| 共享模板把参照图字段写死成 `image_url`，导致阶段真源提前绑定某个 provider 的入参语义 | 共享输入模板层 | 把 `image_markers` 升级为 `image_ref + ref_kind + related_subject + image_no` 的中性骨架 | 在父级合同固定“阶段模板 provider-neutral，provider-specific 解析下沉到 `3-视频生成` 或外部 provider skill” | 请求对象既能承接 Dreamina 本地路径，也不把其他 provider 锁死在 URL 语义 |
| 已有请求 JSON，但 `Assets/` 中选定好的参考图仍未回写进请求对象 | 参照绑定层 | 先进入 `2-参照引用`，完成从 `Assets/` 到 `reference_images / image_markers` 的绑定与严检 | 在父级 `Route Summary` 固定“参照图绑定不再临时下沉到 provider 命令层” | `3-视频生成` 收到的请求对象不再混有空骨架与临时引用 |
| 父级 `6-Video/SKILL.md` 继续回指已删除的 `references/*.md`，导致阶段入口存在失效真源 | 父级真源治理层 | 把阶段级字段、路由、landing 与 handoff 总合同收回父 `SKILL.md`，只保留 `_shared/` 与叶子本地 spec 作为现存载体 | 在父级合同禁止再引用不存在的 `references/*.md`，并把 full-tier 表格固定回主文档 | 父级入口不再出现断链回指，阶段总合同可独立阅读执行 |
| `bootstrap_compat` 下审计脚本直接跳过 active stage 父合同，导致断链也能绿灯通过 | 审计覆盖层 | 在兼容模式下仍审 active stage 父 `SKILL.md`，至少覆盖父级合同、缺失本地引用与 sibling `CONTEXT.md` | 在 `scripts/aigc_skill_audit.py` 与 `HARNESS.md` 固定“兼容模式可降级深层细节，但不能放过 active stage 父级断链” | 严格审计不会再把 active stage 父合同的失效回指静默放行 |

## Repair Playbook

1. 先确认当前任务是否仍属于“视频请求整理层”，而不是已进入模型提交层。
2. 再确认 `projects/aigc/<项目名>/3-Detail/第N集.json` 是否存在且字段完整到可被蒸馏。
3. 再判断当前是组级 `1-提示词蒸馏/全能参照`、帧级 `1-提示词蒸馏/首帧参照`、参照绑定层 `2-参照引用`，还是提交前的 `3-视频生成`。
4. 若命中未补齐子路径，显式报告缺口，不下伪执行链。
5. 若父级合同已经改成 `_shared/ + 叶子本地 spec` 结构，复扫是否还残留 `references/*.md` 旧回指。
6. 若阶段状态或审计口径已变更，记得同步回根技能、registry、routes 与 `HARNESS.md`。

## Reusable Heuristics

- `6-视频` 的第一复杂度不是“怎么生成视频”，而是“怎样先把上游真源变成稳定的视频请求对象”。
- 对当前仓来说，`3-Detail/第N集.json` 比任何临时 prompt 草案都更接近视频阶段的第一事实源。
- 视频阶段与 `dreamina-cli` 的边界应固定为：`6-视频` 负责请求对象，`dreamina-cli` 负责提交与轮询。
- 当阶段从 `shelved` 升级为“部分可执行”时，最容易漏掉的不是叶子文件，而是根技能、registry、routes 与 HARNESS 的同步。
- 当同一视频入参模板开始被多个叶子子技能共用时，应优先提升到 `6-视频/_shared/`，不要继续留在某个子技能私有 `templates/` 中演化。
- 当视频入参既要给工具消费，又要给人直接审读时，优先采用 `第N集.json + 第N集.txt` 双输出，而不是只保留 JSON。
- 当同一 tranche 同时承载组级与帧级叶子子技能时，共享模板必须先抽成中性骨架，再由叶子子技能各自补 `shot_level + source_shot_ids` 约束；不要把组级字段硬写死成全阶段默认。
- 当组级与帧级叶子都要往 `图生视频` 最佳实践靠拢时，最容易漂移的不是字段集合，而是句法顺序；这类共享取向应先沉到 `6-Video/_shared/`，不要让兄弟 spec 各自演化成第二真源。
- 当请求对象已经稳定但还没把 `Assets/` 里的选定参考图回写进去时，最稳的做法不是在 provider 命令里临时拼参数，而是先通过 `2-参照引用` 产出干净的绑定结果。
- 当请求对象与参照图都已稳定、任务目标也已转向真实生成时，最稳的做法不是直接跳到 provider 命令，而是先通过 `3-视频生成` 产出可复核的 handoff 包。
- 阶段级请求对象只应表达“参照图引用是什么”，不应提前假设它一定是 URL 或本地路径；把 `image_ref` 的最终落地格式交给 provider handoff 层解析，才能同时兼容 Dreamina 这类本地上传 CLI 和其他远程 API。
- `bootstrap_compat` 允许放松深层子路径细节，但不等于允许 active stage 父合同继续挂着失效引用；父级入口断链应继续被严格审计。
