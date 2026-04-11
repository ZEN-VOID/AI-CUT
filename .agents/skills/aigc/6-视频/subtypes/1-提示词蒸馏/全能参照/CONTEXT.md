# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `6-视频/subtypes/1-提示词蒸馏/全能参照` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在父级 `6-视频` 合同之后加载本文件。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| prompt 只覆盖分镜组的局部字段 | 输入覆盖层 | 回到“整组全部内容”重新蒸馏 | 在 `FIELD-VID-SUBJ-01` 固化“组级全覆盖” | 每个条目都能回链整组与全部分镜 |
| `剧本正文` 或 `全局风格` 被改写 | 固定文本层 | 恢复原文直贴 | 在输出契约里显式标记“fixed verbatim block” | 两段文本与上游逐字一致 |
| prompt 中暴露了字段标题 | 文本编排层 | 重写为无标题融合文本 | 在 `FIELD-VID-SUBJ-02` 固化只保留组ID/镜ID标签 | 除组ID/镜ID外无显式字段名 |
| 压缩后远低于 1800 字或显著超出 2000 字 | 字数预算层 | 调整非固定字段压缩力度 | 在策略表加入 `tight/normal/underflow` 预算规则 | `prompt_char_count` 处于目标窗或有保守例外说明 |
| `reference_images` 缺失，或 `image_markers` 的 URL/主体/图号与上传顺序不一致 | 请求模板层 | 保留 `reference_images: []`，并回到 `model.image_markers` 重排补齐三元信息 | 在模板真源中固定“双字段承接”与顺序规则 | 请求 JSON 能稳定映射真实上传顺序 |

## Repair Playbook

1. 先查 `分镜组列表` 是否为合法 director schema 结构。
2. 再查每个分镜组的 `剧本正文` 和 `全局风格` 是否被原文保留。
3. 再查其余组级与镜级字段是否已经全部进入 prompt，只是压缩程度不同。
4. 再查 prompt 是否只有 `分镜组ID / 分镜ID` 显式标签。
5. 最后查 `prompt_char_count` 与输出模板字段是否完整。

## Reusable Heuristics

- 这类视频请求整理最容易错的不是“文采不够”，而是把整组信息缩成了局部摘要。
- 对本子技能来说，`剧本正文` 与 `全局风格` 更像硬锁文本，而不是可自由润色的素材。
- 字数吃紧时，优先把非固定字段压成高密度短语，不要碰固定原文块。
- “隐藏字段标题”不等于“删除信息结构”；最稳的做法是只保留 `分镜组ID / 分镜ID` 作为显式骨架，其余内容揉进自然文本。
- 最稳的做法是把 `reference_images` 当作上传顺序位保留，再用 `image_markers` 承接 URL、主体和图号语义。
- 当模板开始被多个视频子技能共用时，应把它提升到 `6-视频/_shared/`，子技能只保留回指与局部编排规则。
- 当同一份 prompt 既要给工具消费又要给人读时，最稳的是 `json` 保结构、`txt` 保阅读，不把两种职责硬塞进同一个文件。
- 一旦采用双输出，必须持续强调：`txt` 是 derived display view，`json` 才是 completeness carrier；否则后续很容易有人误拿 TXT 当主真源。

## Case Log

### Case-20260410-AIGC-VIDEO-SUBJECT-REFERENCE-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `6-视频/subtypes/1-提示词蒸馏/全能参照` 建立了从 `编导/第N集.json` 分镜组内容到 Dreamina 风格视频请求 JSON 的叶子合同。
- root_cause_or_design_decision: 用户需求已经明确给出上游路径、shared schema、目标模板类型、固定保留字段、字数窗与字段隐藏规则；若仍停留在“视频阶段空壳”会导致每次都重新解释 prompt 压缩逻辑。
- final_fix_or_heuristic: 将“整组全覆盖、固定块原文保留、其余字段均匀压缩、除组ID/镜ID外隐藏标题、`meta + prompt_style + model + prompt + prompt_char_count` 结构”写成稳定的叶子执行合同，并补实际 JSON 模板文件。
- prevention_or_replication_checklist:
  - [x] 固定原文块已写入合同
  - [x] 字数窗与 fallback 已写入策略
  - [x] JSON 模板已落盘
  - [x] `reference_images` 图片标记结构已固定
- evidence_paths:
  - `.agents/skills/aigc/6-视频/subtypes/1-提示词蒸馏/全能参照/SKILL.md`
  - `.agents/skills/aigc/6-视频/subtypes/1-提示词蒸馏/全能参照/CONTEXT.md`
  - `.agents/skills/aigc/6-视频/subtypes/1-提示词蒸馏/全能参照/references/output-template.md`
  - `.agents/skills/aigc/6-视频/_shared/video-generation-input.template.json`
- user_feedback_or_constraint: 用户明确要求“针对上游编导文件，分镜组内全部内容做基础蒸馏；每组 1800-2000 字；`剧本正文/全局风格` 固定不变；除组ID/镜ID外隐藏字段标题；参照图暂留空”。

### Case-20260410-AIGC-VIDEO-SUBJECT-DUAL-OUTPUT

- milestone_type: source_contract_change
- outcome: 将 `全能参照` 重新定义为 `第N集.json + 第N集.txt` 双输出模式，并接入 `6-视频/_shared/视频生成入参.template.txt`。
- root_cause_or_design_decision: 叶子子技能原先只有结构化 JSON 视图，缺少一个按“提示词 + 字数统计”直接阅读的文本产物，不利于人工审校和快速复制。
- final_fix_or_heuristic: 采用“JSON 承载结构、TXT 承载阅读”的双输出合同；JSON 继续服务工具，TXT 只保留提示词正文与字数统计。
- prevention_or_replication_checklist:
  - [x] 共享 txt 模板已回指
  - [x] 双输出落点已写入合同
  - [x] `第N集_subject_reference.json` 旧命名已切换
  - [x] 输出契约与执行流程已同步
- evidence_paths:
  - `.agents/skills/aigc/6-视频/_shared/视频生成入参.template.txt`
  - `.agents/skills/aigc/6-视频/subtypes/1-提示词蒸馏/全能参照/SKILL.md`
  - `.agents/skills/aigc/6-视频/subtypes/1-提示词蒸馏/全能参照/references/output-template.md`
  - `.agents/skills/aigc/6-视频/subtypes/1-提示词蒸馏/全能参照/references/execution-flow.md`
- user_feedback_or_constraint: 用户明确要求在共享层新增 `视频生成入参.template.txt`，并将 `全能参照` 改为 `第N集.json` 与 `第N集.txt` 双输出。
