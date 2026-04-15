# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `3-Detail/水月` 的经验层知识库，不是过程日志。
- 命中 `.agents/skills/aigc/3-Detail/水月/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `aigc/3-Detail` 父合同 > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 16000
- hard_limit_chars: 32000
- status: ok
- last_checked_at: 2026-04-14

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍把 grouped script 写成第二份水月成稿 | 输出合同层 | 回到 patch sidecar，只保留 factual fields | 在 `SKILL.md + template + validator` 固定 `inherit_only` | 输出不再出现 prose 重写 |
| `水月` sidecar 混入 `分镜ID / 时间段 / 摄影美学` | 字段 ownership 层 | 删除 cinematic 字段，回到 factual patch | 用 validator 固定 `水月` 只拥有 factual 字段 | sidecar 无越权字段 |
| `出场角色及穿搭` 写得很美但不可回填 | 组级回填层 | 改写成 `角色名-服装简述` 的短句格式 | 在模板与 validator 固定格式预期 | 父层可直接回填 |
| `beat_patches[]` 只有抽象感受，没有空间和走位 | factual 颗粒度层 | 回到 `运动表现 + 氛围表现`，补 `角色背景面 / 角色站位走位` | 在 `SKILL.md` 固定 beat patch 最低字段集合 | factual patch 可直接 merge |
| `镜头消费提示` 写成空泛辞藻 | 可消费性层 | 改成能给切镜消费的动作/关系/视线抓手 | 在 `FIELD-WM-07` 固定“可被镜头消费”标准 | 下游能直接读出镜头抓手 |
| `beat_id` 每次都变，导致父层无法 merge | patch 对齐层 | 回退到 `<group_id>-bNN` 规则 | 在 `Beat Patch Contract` 固定统一命名规则 | 父层对齐稳定 |
| factual patch 很丰富，但仍夹带新剧情 | 事实边界层 | 回到固定 `剧本正文`，删掉越权新增事实 | 在 `SKILL.md` 固定“不发明新剧情” | patch 能逐条回指原文 |
| 把 `角色表现 / 运动表现 / 氛围表现` 直接写成 shared 镜级并列字段 | shared schema 投影层 | 撤回内部主链字段，恢复 canonical factual 槽位 | 在 shared schema 与本 `CONTEXT.md` 固定“内部主链先汇流，再写最终字段” | 下游只消费 `角色背景面 / 角色站位走位 / 道具及状态 / 镜头消费提示` |
| 把 `水月` 误当成最终 shot-level `分镜表现` owner | 父子 handoff 层 | 回退到 beat-level evidence，只保留 `镜头消费提示` | 在父层 merge 契约中固定“由父层按 `beat_refs[]` 投影到 `分镜明细[].分镜表现`” | `水月` sidecar 不再冒充最终镜级真源 |
| validator / template 继续把 `分镜明细[].分镜表现` 当作 `水月.target_fields` | 校验门层 | 把 `target_fields` 收回 `beat_patches[].镜头消费提示` | 在 `template + validator + runtime sample` 同步固定“`分镜表现` 只属于父层 merge 结果” | `validate_watermoon_output.py` 会直接拦截错误 green |

## Repair Playbook

1. 先确认 grouped script 是不是唯一真源，避免拿错输入。
2. 再核对 shared root 中 `剧本正文` 是否稳定存在。
3. 若 patch 发散，先重做组锚点，不要直接修句子。
4. 若人物成立但空间发虚，优先补 `运动表现 + 氛围表现`，不要继续堆情绪词。
5. 若 `出场角色及穿搭` 空泛，回到角色与服装识别锚点，不要写审美短评。
6. 写 sidecar 时优先检查 ownership：只要出现 cinematic 字段，就说明越权了。

## Reusable Heuristics

- `水月` 的核心不再是“写得更长”，而是“把 grouped script 变成可 merge 的 factual patch”。
- `水月` 最稳的落点是 `group patch + beat patch`，而不是一段 prose。
- `角色背景面 / 角色站位走位 / 道具及状态 / 镜头消费提示` 四项一旦分开写清，父层 merge 会稳定很多。
- `角色表现 / 运动表现 / 氛围表现 / 视觉强化` 是 `水月` 内部思考主链，不是 shared director schema 的最终镜级字段；它们必须先汇流，再落到 canonical factual 槽位。
- `水月` 最稳的定位不是最终 shot-level writer，而是 pre-shot evidence owner；`镜头消费提示` 要服务后续切镜和父层投影，而不是直接冒充 `分镜明细[].分镜表现`。
- `出场角色及穿搭` 应优先服务识别而不是文采；越短、越准、越可回填越好。
- 想让 factual patch 更稳，不是多写形容词，而是让每个 beat 都能明确回答：谁在什么位置，怎么动，什么道具在什么状态，镜头最该看见什么。
