# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在父级 `6-Video` 合同之后加载本文件。
- 规范真源以同目录 `SKILL.md` 为准；本文件只沉淀经验、修复顺序与里程碑案例。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| prompt 只覆盖分镜组的局部字段 | 输入覆盖层 | 回到“整组全部内容”重新蒸馏 | 在 `FIELD-VID-SUBJ-02` 固化“整组全覆盖” | 每个条目都能回链整组与全部分镜 |
| `剧本正文` 或 `全局风格` 被改写 | 固定文本层 | 恢复原文直贴 | 在 `SKILL.md` 的 Prompt Assembly Contract 固化 fixed verbatim block | 两段文本与上游逐字一致 |
| prompt 中暴露了字段标题 | 文本编排层 | 重写为无标题融合文本 | 在 `FIELD-VID-SUBJ-02` 固化只保留组ID/镜ID标签 | 除组ID/镜ID外无显式字段名 |
| prompt 读起来像字段硬裁切拼接，出现大量 `…` 半截短语 | 压缩执行层 | 回到镜级压缩步骤，把字段值改写成自然句式后再落盘 | 在 `SKILL.md` 固化“禁止用省略号硬截断代替语义压缩” | 抽查 `prompt` 时不再出现大面积机械省略号 |
| 压缩后远低于 1800 字或显著超出 2000 字 | 字数预算层 | 调整非固定字段压缩力度 | 在策略表加入 `tight/normal/underflow` 预算规则 | `prompt_char_count` 处于目标窗或有保守例外说明 |
| `prompt_char_count` 与 JSON 中实际 `prompt` 长度不一致 | 输出统计层 | 回到最终 JSON 主体，以实际落盘 `prompt` 文本重新计数 | 在 `SKILL.md` 固化“按最终落盘 prompt 计数并回读 JSON 复核” | `len(prompt) == prompt_char_count` |
| `第N集.txt` 中 section header 与 prompt 首行重复显示同一 `分镜组ID` | TXT 派生视图层 | 保留 section header，并去掉 TXT 中重复的 prompt 首行组 ID | 在 `SKILL.md` 固化“TXT 已显示组 ID 时不得重复显示 prompt 首行组 ID” | `第N集.txt` 每组只出现一次组 ID header |
| `reference_images` 缺失，或 `image_markers` 的 URL/主体/图号与上传顺序不一致 | 请求模板层 | 保留 `reference_images: []`，并回到 `model.image_markers` 重排补齐三元信息 | 在模板真源与 `SKILL.md` 中固定双字段承接与顺序规则 | 请求 JSON 能稳定映射真实上传顺序 |
| `references/*.md` 继续被当作规范入口 | 真源治理层 | 把字段系统、流程、输出契约、类型策略全部回收到 `SKILL.md` | 禁止在主合同继续引用 `references/` 作为 Canonical Module | 主合同不再出现 `references/*.md` 规范依赖 |
| 合同章节很多，但执行者仍无法判断失败后该回哪一层返工 | 思行网络层 | 把线性流程改写为带 `route_out/gate` 的思行节点网络 | 在 `SKILL.md` 固化 `N0-N8` 节点、汇流门与返工入口 | 每个节点都能回答“做什么、看什么证据、失败回哪” |
| 三件套已写出，但对用户的结案信息只剩路径，没有思考过程和关键证据 | 结案闭环层 | 在最终闭环中补 `思考过程 + 关键证据 + 风险/例外` | 新增 `FIELD-VID-SUBJ-05` 并把闭环四段写成硬合同 | 执行结果可复核，不再只剩文件清单 |

## Repair Playbook

1. 先查 `分镜组列表` 是否为合法 director schema 结构。
2. 再查每个分镜组的 `剧本正文` 和 `全局风格` 是否被原文保留。
3. 再查其余组级与镜级字段是否已经全部进入 prompt，只是压缩程度不同。
4. 再查 prompt 是否只有 `分镜组ID / 分镜ID` 显式标签。
5. 最后查 `prompt_char_count`、`reference_images`、`image_markers` 与 `_manifest.json` 是否完整。

## Reusable Heuristics

- 这类视频请求整理最容易错的不是“文采不够”，而是把整组信息缩成了局部摘要。
- 对本子技能来说，`剧本正文` 与 `全局风格` 更像硬锁文本，而不是可自由润色的素材。
- 字数吃紧时，优先把非固定字段压成高密度短语，不要碰固定原文块。
- “隐藏字段标题”不等于“删除信息结构”；最稳的做法是只保留 `分镜组ID / 分镜ID` 作为显式骨架，其余内容揉进自然文本。
- “压缩”不等于“把字段值切半再加省略号”；如果读起来像半字段残片，说明执行方法已经偏离合同。
- 最稳的做法是把 `reference_images` 当作上传顺序位保留，再用 `image_markers` 承接 URL、主体和图号语义。
- 当同一份 prompt 既要给工具消费又要给人读时，最稳的是 `json` 保结构、`txt` 保阅读，不把两种职责硬塞进同一个文件。
- 一旦采用双输出，必须持续强调：`txt` 是 derived display view，`json` 才是 completeness carrier。
- 只要有落盘前裁剪、去尾换行或 TXT 派生改写，`prompt_char_count` 就必须以后写回 JSON 的最终 `prompt` 字符串为准，不能拿中间草稿长度顶替。
- 当 `txt` 已经把 `分镜组ID` 放在 section header，最稳的是把 prompt 首行同组 ID 从 `txt` 视图剥离，只保留 `json` 主体里的原始 prompt。
- 当 `references/` 开始充当规则入口时，真正的问题不是“文件多”，而是子技能出现了第二真源；应直接把规范收回 `SKILL.md`。
- 这类“固定块原文保留 + 压缩块受预算约束 + 三件套落盘”的叶子技能，最稳的结构不是再加几条 checklist，而是改成“串行主干 + 条件预算分支 + 汇流门”的思行网络。
- 如果节点没有显式写出 `route_out` 和 `gate`，执行者最容易在 `underflow`、标题泄露或三件套不一致时直接凭感觉补救，最后留下不可复核的半闭环。

## Case Log

### Case-20260410-AIGC-VIDEO-SUBJECT-REFERENCE-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `6-Video/1-提示词蒸馏/全能参照` 建立了从 `3-Detail/第N集.json` 分镜组内容到 Dreamina 风格视频请求 JSON 的叶子合同。
- root_cause_or_design_decision: 用户需求已经明确给出上游路径、shared schema、目标模板类型、固定保留字段、字数窗与字段隐藏规则；若仍停留在“视频阶段空壳”，每次都要重新解释 prompt 压缩逻辑。
- final_fix_or_heuristic: 将“整组全覆盖、固定块原文保留、其余字段均匀压缩、除组ID/镜ID外隐藏标题、`meta + prompt_style + model + prompt + prompt_char_count` 结构”写成稳定叶子合同。
- prevention_or_replication_checklist:
  - [x] 固定原文块已写入合同
  - [x] 字数窗与 fallback 已写入策略
  - [x] 共享模板已回指
  - [x] `reference_images` 图片标记结构已固定
- evidence_paths:
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/SKILL.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/CONTEXT.md`
  - `.agents/skills/aigc/6-Video/_shared/video-generation-input.template.json`
- user_feedback_or_constraint: 用户明确要求“针对上游编导文件，分镜组内全部内容做基础蒸馏；每组 1800-2000 字；`剧本正文/全局风格` 固定不变；除组ID/镜ID外隐藏字段标题；参照图暂留空”。

### Case-20260410-AIGC-VIDEO-SUBJECT-DUAL-OUTPUT

- milestone_type: source_contract_change
- outcome: 将 `全能参照` 重新定义为 `第N集.json + 第N集.txt` 双输出模式，并接入 `6-Video/_shared/视频生成入参.template.txt`。
- root_cause_or_design_decision: 只有结构化 JSON 视图时，不利于人工审校和快速复制；需要一个按“提示词 + 字数统计”直读的副产物。
- final_fix_or_heuristic: 采用“JSON 承载结构、TXT 承载阅读”的双输出合同；JSON 服务工具，TXT 只展示提示词正文与字数统计。
- prevention_or_replication_checklist:
  - [x] 共享 TXT 模板已回指
  - [x] 双输出落点已写入合同
  - [x] 输出契约与执行流程已同步进主合同
- evidence_paths:
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/SKILL.md`
  - `.agents/skills/aigc/6-Video/_shared/视频生成入参.template.txt`
- user_feedback_or_constraint: 用户明确要求在共享层新增 `视频生成入参.template.txt`，并将 `全能参照` 改为 `第N集.json` 与 `第N集.txt` 双输出。

### Case-20260412-AIGC-VIDEO-SUBJECT-SINGLE-SOURCE-CONTRACT

- milestone_type: source_contract_change
- outcome: 将 `全能参照` 的 `references/chain-of-thought.md`、`execution-flow.md`、`output-template.md`、`type-strategies.md` 全量回收到 `SKILL.md`，终止 `references/` 充当二级规范真源。
- root_cause_or_design_decision: 旧结构把字段系统、执行流程、输出契约与类型策略拆到 `references/`，导致主合同只是索引页，同时还混用 `6-视频/subtypes/...` 旧路径，形成路径漂移和真源分裂。
- final_fix_or_heuristic: 以 `SKILL.md` 为唯一规范入口，`CONTEXT.md` 只保留经验层，`references/` 不再参与规范读取；同步补 `CHANGELOG.md` 与 `agents/openai.yaml`，并清理旧路径引用。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已内联字段系统、流程、输出契约与类型策略
  - [x] `CONTEXT.md` 已移除对 `references/*.md` 的规范回指
  - [x] `agents/openai.yaml` 已补建
  - [x] 旧路径与旧引用已纳入扫描
- evidence_paths:
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/SKILL.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/CONTEXT.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/CHANGELOG.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/agents/openai.yaml`
- user_feedback_or_constraint: 用户明确要求“针对 `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照` 执行全量升格重构，references 内容整合到 `SKILL.md` 内，不再以 references 作为载体引用”。

### Case-20260412-AIGC-VIDEO-SUBJECT-ZXY-REFACTOR

- milestone_type: source_contract_change
- outcome: 将 `全能参照` 从强化线性叶子合同重构为知行合一式单技能思行网络，并显式关闭“骨架 / 细则分层”。
- root_cause_or_design_decision: 旧合同虽然已经把字段系统、流程、类型策略与输出契约收回主 `SKILL.md`，但关键判断仍散在线性章节里；一旦遇到输入缺口、预算压力、标题泄露或三件套不一致，执行者很难明确知道应回到哪一层返工，也无法稳定输出思考过程。
- final_fix_or_heuristic: 保留现有输入、输出、模板、字段、字数窗与禁止项不变，把组织方式重写为 `业务需求分析 -> 总输入合同 -> 混合拓扑 -> N0-N8 思行节点 -> 汇流门 -> 一次性输出门`，并新增执行闭环字段 `FIELD-VID-SUBJ-05`。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已明确声明 `复杂链路的骨架 / 细则分层: false`
  - [x] 每个节点已补齐 `objective / inputs / actions / evidence / route_out / gate`
  - [x] 已新增汇流门与结案门
  - [x] 最终闭环已固定包含 `思考过程`
- evidence_paths:
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/SKILL.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/CONTEXT.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/CHANGELOG.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/agents/openai.yaml`
- user_feedback_or_constraint: 用户明确要求“根据知行合一的规范进行编排”，“复杂链路的骨架 / 细则分层：false”，并要求每一个思维·执行节点从哪些方面着手、一步一步足够细致。
