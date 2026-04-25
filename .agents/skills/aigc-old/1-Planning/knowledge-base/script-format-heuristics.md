# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/1-Planning/2-剧本` 的经验层知识库，不是过程日志；历史 runtime 路径仍为 `2-格式/`。
- 调用 `.agents/skills/aigc/1-规划/references/script-format-contract.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > 父 `1-Planning/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 又把 `标准剧 / 解说剧 / 双案` 拆成外部 agent 依赖 | 真源治理层 | 收回到 `references/script-format-contract.md` 的统一标准剧本投影 | 在 `SKILL.md + audit` 固化 `Internal Capability Fusion Contract` | `2-剧本` 不再引用旧规划组文档 |
| 又按旧逻辑误切 `解说剧` 或 `双案` | 剧本策略层 | 归一回 `标准剧` 并在执行报告写明原因 | 在 `Unified Standard Format Contract` 固化“唯一 canonical 出口=标准剧” | `selected_variant=标准剧` 可复盘 |
| 旁白主体漂移 | 体裁纪律层 | 统一为单一旁白主体，默认 `讲述者` 或项目约定主体 | 在 validator 增加主体一致性检查 | 不再出现多旁白主体混写 |
| 对白被润色或改写 | 文本保真层 | 回滚为上游逐字文本 | 保留对话冻结门禁 + 上游对白比对 | `WARN/FAIL-DIALOGUE-FREEZE` 可定位 |
| 引号内混入动作或文本画面错配 | 共享门禁层 | 动作下沉到 `*画面`，重排同命题配对 | 在 `N5-normalize + validator` 固化高频结构门禁 | `FAIL-ACTION-MIXED / FAIL-VISUAL-MISSING` 可拦截 |
| `总字数` 未按最终正文回填 | 收尾层 | 重算并回写 `总字数` 后重跑 validator | 将“字数回填 -> validator 复跑”固定为出口清单 | `FAIL-WORDCOUNT-STALE` 不再复发 |
| 提前把分组/节奏结论写进剧本主稿 | 下游边界层 | 删除越权字段，只保留 handoff 接口 | 在 `Downstream Interface Contract` 固化非 owned truth | 主稿只承载本阶段内容 |
| 场景标题使用中文数字导致下游 `3-分组` validator 无法解析场景号 | 跨阶段 I/O 兼容层 | 改回 `### 场景1：...` 这类阿拉伯数字标题 | 在 `2-剧本` 合同中固定场景标题编号格式，避免把示例写成中文数字 | `3-分组` 可稳定识别组起始场景 |
| storyboard_script 上游用 `角色名：台词` 而非中文引号，导致对白冻结校验误报 warnings | validator source extraction 层 | 扩展 `validate_script_output.py` 的上游对白抽取，兼容中文引号与角色冒号归因两种形式 | 对 `storyboard_script` / 分镜脚本源，validator 不应假设所有上游对白都已被中文引号包裹 | `validate_script_output.py --upstream <1-分集/第N集.md>` 对冒号式对白不再产生 `WARN-DIALOGUE-FREEZE` |
| 相同 `内景/外景 场所 - 日/夜` 被拆成多个场景号 | 标准剧本 slugline 语义层 | 相同 slugline 沿用同一场景号，把 beat 拆分交给 `3-分组` | 在 `2-剧本` 合同与 validator 中区分“真实场景号”和“分镜组号” | 同一教室日景不会出现 `场景1/2/3/4` 四个编号 |
| 相同 slugline 连续重复打印为多个标题 | 场景标题呈现层 | 只保留首次场景标题，后续 beat 直接续写正文 | validator 增加连续重复标题门禁 | 第1集同一教室日景只出现一次 `### 场景1` |
| `2-剧本` 把 `1-分集` 原文压缩成标准剧梗概 | 上游保真层 | 回刷为完整原文结构化投影，只新增场景标题和字段标签；适合主观叙事的描写可转为独白但不得删减事实 | validator 在传入 `--upstream` 时检查正文保留长度比和段落覆盖率 | 压缩稿会触发 `FAIL-UPSTREAM-PRESERVATION` |
| 把小说叙述句直接塞进 `动作画面` | 剧本化字段层 | 按语境改写为 `环境描写/角色动作/音效/道具特写/系统画面/规则显影/群像画面/心理反应` 等正式字段 | 在合同与 validator 中固定 `动作画面` 只承载可拍动作；各类画面允许剧本化改写但不删事实 | `WARN-ACTION-PROSE-LIKE` 可定位明显违和行 |
| `音效` 行混入画面动作，或缺少对应承托画面 | 声画字段纯度层 | 拆为 `音效` + `音效画面`：前者只写听觉本体，后者只写可见源头、人物反应或空间承托 | 在合同和 validator 中把 `音效画面` 固化为和 `对白画面/独白画面/旁白画面` 同级的就近配对字段 | `FAIL-VISUAL-MISSING` 可拦截缺少 `音效画面` 的音效行 |

## Repair Playbook

1. 先确认输入是否唯一来自 `1-分集` 输出物。
2. 再确认业务分析与标准剧本策略是否明确。
3. 再检查共享硬门禁：对白冻结、主体、双引号、动作剥离、声画配对、字数回填。
4. 最后才看 validator 是否覆盖到当前失败类型。
5. 若用户指出“动作画面像小说原文”，先分流字段标题，再做画面剧本化改写；不要为了保留原句而牺牲影视剧本可拍性。
6. 若用户指出“声画混杂”，先按字段组检查：对白/独白/旁白/音效只保留文本或声音本体，对应 `*画面` 承载画面动作、表演和空间信息。

## Reusable Heuristics

- `2-剧本` 最稳的形态不是“skill + 一堆外部规划组 agent”，而是“一个 skill 内化标准剧本投影与执行闭环”。
- 唯一 canonical 出口始终是 `标准剧`；用户或上游提出讲述型消费时，只调整旁白/独白策略，不切 `解说剧`。
- `2-剧本` 若要保留剧本策略思行证据，应该优先落到 `agents-plan/` 侧车，而不是再长出第二份主稿。
- 下游 `3-分组` 真正需要的是稳定的 `selected_variant + dialogue/narration policy + source_profile`，不是在剧本阶段提前拿到组边界或节奏蓝图。
- 若主稿还要继续进入 `3-分组`，场景标题应统一写成 `场景1/场景2/...`，不要混用中文数字。
- 场景编号只跟 slugline 变化走；同一地点同一日/夜内的角色入场、规则宣告、系统公告、能力觉醒，属于 beat 或分镜组变化，不属于新场景。
- 连续同一 slugline 不需要重复打印标题；如果只是为了分段阅读，应交给空行或下游分镜组，不要新增或重复场景标题。
- 对 `storyboard_script` 输入，源文本常把对白写成 `角色名（语气）：台词` 并夹在画面描述行内；对白冻结校验应先兼容这种上游形态，再判断主稿是否改写台词。
- `动作画面` 不是兜底桶；环境、音效、道具、系统文字、规则显影、群像反应和心理判断应各自归位。对白尽量冻结，画面类字段可做剧本化改写，只要不删事实、不改顺序。
- `音效` 也不是画面桶；一条声音最好紧跟一条 `音效画面`，让后续分镜知道“听到什么”和“看到什么”分别来自哪里。
