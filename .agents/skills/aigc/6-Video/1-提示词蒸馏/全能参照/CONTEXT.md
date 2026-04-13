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
| shared director schema 已升级到 `角色背景面 / 角色站位走位 / 出场角色及穿搭`，但视频 prompt 仍按旧字段心智压缩 | schema handoff 层 | 在组级压缩块显式纳入 `出场角色及穿搭`，并把镜级消费口径改成 `角色背景面 / 角色站位走位` | 在 `SKILL.md` 的输入门、N2/N3/N5 与验收清单中固定新字段，不再依赖旧字段名的隐式理解 | prompt 能读出角色背景关系、走位和组级穿搭摘要 |
| `剧本正文` 或 `全局风格` 被改写 | 固定文本层 | 恢复原文直贴 | 在 `SKILL.md` 的 Prompt Assembly Contract 固化 fixed verbatim block | 两段文本与上游逐字一致 |
| prompt 中暴露了字段标题 | 文本编排层 | 重写为无标题融合文本 | 在 `FIELD-VID-SUBJ-02` 固化只保留组ID/镜ID标签 | 除组ID/镜ID外无显式字段名 |
| prompt 只剩动作、情绪和空间，没有把镜级 `景别 / 运镜手法` 保留下来 | 镜头语法层 | 回到镜级压缩步骤，为每个分镜补回明确的景别结论与运镜结论 | 在 `SKILL.md` 的输入门、N2/N5 与验收清单中把 `景别 / 运镜手法` 固化为不可忽略字段 | 每个镜级条目都能读出镜头远近关系与运动方式 |
| prompt 读起来像字段硬裁切拼接，出现大量 `…` 半截短语 | 压缩执行层 | 回到镜级压缩步骤，把字段值改写成自然句式后再落盘 | 在 `SKILL.md` 固化“禁止用省略号硬截断代替语义压缩” | 抽查 `prompt` 时不再出现大面积机械省略号 |
| prompt 超出 1900 字上限，尤其出现在 5 镜以上长组仍沿用自然句展开时 | 字数预算层 | 先保住 fixed block，再把非固定字段从自然句切换成更精炼的自然短语 | 在策略表中把 `<= 1900` 固定为硬上限，并把 `>= 5` 镜长组仅写成预算预警信号，而非默认短语化动作 | 长组 prompt 会先做预算预估；只有接近上限时才切短语化压缩 |
| `prompt_char_count` 与 JSON 中实际 `prompt` 长度不一致 | 输出统计层 | 回到最终 JSON 主体，以实际落盘 `prompt` 文本重新计数 | 在 `SKILL.md` 固化“按最终落盘 prompt 计数并回读 JSON 复核” | `len(prompt) == prompt_char_count` |
| `第N集.txt` 中 section header 与 prompt 首行重复显示同一 `分镜组ID` | TXT 派生视图层 | 保留 section header，并去掉 TXT 中重复的 prompt 首行组 ID | 在 `SKILL.md` 固化“TXT 已显示组 ID 时不得重复显示 prompt 首行组 ID” | `第N集.txt` 每组只出现一次组 ID header |
| `reference_images` 缺失，或 `image_markers` 的 URL/主体/图号与上传顺序不一致 | 请求模板层 | 保留 `reference_images: []`，并回到 `model.image_markers` 重排补齐三元信息 | 在模板真源与 `SKILL.md` 中固定双字段承接与顺序规则 | 请求 JSON 能稳定映射真实上传顺序 |
| `references/*.md` 继续被当作规范入口 | 真源治理层 | 把字段系统、流程、输出契约、类型策略全部回收到 `SKILL.md` | 禁止在主合同继续引用 `references/` 作为 Canonical Module | 主合同不再出现 `references/*.md` 规范依赖 |
| 合同章节很多，但执行者仍无法判断失败后该回哪一层返工 | 思行网络层 | 把线性流程改写为带 `route_out/gate` 的思行节点网络 | 在 `SKILL.md` 固化 `N0-N8` 节点、汇流门与返工入口 | 每个节点都能回答“做什么、看什么证据、失败回哪” |
| 三件套已写出，但对用户的结案信息只剩路径，没有思考过程和关键证据 | 结案闭环层 | 在最终闭环中补 `思考过程 + 关键证据 + 风险/例外` | 新增 `FIELD-VID-SUBJ-05` 并把闭环四段写成硬合同 | 执行结果可复核，不再只剩文件清单 |
| `project_state.yaml` 已指向 `2-视频生成`，但 `6-Video/全能参照/第N集/` 三件套磁盘缺失 | 项目运行时同步层 | 先重建 `第N集.json + 第N集.txt + _manifest.json`，再保持既有 video-generation handoff，不回退项目状态 | 在 `SKILL.md` 的 artifact landing 与 handoff contract 固定 recovery rerun 规则，禁止视频提示词补跑把项目路由降级 | drift 修复后磁盘产物恢复且 `project_state.yaml` 仍保持后续入口 |

## Repair Playbook

1. 先查 `分镜组列表` 是否为合法 director schema 结构。
2. 再查每个分镜组的 `剧本正文` 和 `全局风格` 是否被原文保留。
3. 再查其余组级与镜级字段是否已经全部进入 prompt，只是压缩程度不同。
4. 再查 prompt 是否只有 `分镜组ID / 分镜ID` 显式标签。
5. 最后查 `prompt_char_count`、`reference_images`、`image_markers` 与 `_manifest.json` 是否完整。

## Reusable Heuristics

- 这类视频请求整理最容易错的不是“文采不够”，而是把整组信息缩成了局部摘要。
- 对本子技能来说，`剧本正文` 与 `全局风格` 更像硬锁文本，而不是可自由润色的素材。
- 字数上限现在以 `1900` 为硬门；压缩吃紧时，优先把非固定字段压成更精炼的自然短语，不要碰固定原文块。
- 当预算明显有余时，最稳的表达仍是自然语句，不要为了“看起来更省字”主动切成短语式表达。
- 当组内镜头达到 `5` 个或更多时，应更早做预算预估；只有自然语句版逼近上限时，才把非固定字段收束为更精炼的自然短语。
- 这类视频 prompt 不是只交代“发生了什么”，还要交代“镜头怎么拍”；景别描述和运镜手法都属于镜头语法，不可在压缩时省掉。
- 最稳的镜级压缩句型通常是“景别结论 + 运镜结论 + 空间/走位/动作结果”，这样既不暴露字段标题，也不容易漏掉镜头组织信息。
- “隐藏字段标题”不等于“删除信息结构”；最稳的做法是只保留 `分镜组ID / 分镜ID` 作为显式骨架，其余内容揉进自然文本。
- 当上游 schema 把“角色背后空间”“角色位移”“组级服装摘要”拆成三层时，视频 prompt 也应同步三层消费：`角色背景面` 提供空间朝向，`角色站位走位` 提供动作布局，`出场角色及穿搭` 提供整组视觉识别锚点。
- “压缩”不等于“把字段值切半再加省略号”；如果读起来像半字段残片，说明执行方法已经偏离合同。
- 最稳的做法是把 `reference_images` 当作上传顺序位保留，再用 `image_markers` 承接 URL、主体和图号语义。
- 当同一份 prompt 既要给工具消费又要给人读时，最稳的是 `json` 保结构、`txt` 保阅读，不把两种职责硬塞进同一个文件。
- 一旦采用双输出，必须持续强调：`txt` 是 derived display view，`json` 才是 completeness carrier。
- 只要有落盘前裁剪、去尾换行或 TXT 派生改写，`prompt_char_count` 就必须以后写回 JSON 的最终 `prompt` 字符串为准，不能拿中间草稿长度顶替。
- 当 `txt` 已经把 `分镜组ID` 放在 section header，最稳的是把 prompt 首行同组 ID 从 `txt` 视图剥离，只保留 `json` 主体里的原始 prompt。
- 当 `references/` 开始充当规则入口时，真正的问题不是“文件多”，而是子技能出现了第二真源；应直接把规范收回 `SKILL.md`。
- 这类“固定块原文保留 + 压缩块受预算约束 + 三件套落盘”的叶子技能，最稳的结构不是再加几条 checklist，而是改成“串行主干 + 条件预算分支 + 汇流门”的思行网络。
- 如果节点没有显式写出 `route_out` 和 `gate`，执行者最容易在 `underflow`、标题泄露或三件套不一致时直接凭感觉补救，最后留下不可复核的半闭环。
- 若 `全能参照` 三件套只是磁盘漂移丢失，而项目已经进入 `2-视频生成`，最稳的修法是只补 carrier 与 trace，不回退后续 handoff；否则会把 prompt 层修复误做成流程降级。

## Case Log

### Case-20260413-AIGC-VIDEO-OMNIREF-SCHEMA-SYNC

- milestone_type: source_contract_change
- outcome: 将 `全能参照` 对上游导演 schema 的消费口径同步到新字段分层：组级新增 `出场角色及穿搭`，镜级改为 `角色背景面 / 角色站位走位`。
- root_cause_or_design_decision: 旧合同虽然写了“整组全部内容”，但实际固定的压缩块清单仍停留在 `类型元素 / 导演意图 / 分镜明细[]`，没有把新增组级服装摘要写成硬要求，也没有显式承认镜级字段已改名。
- final_fix_or_heuristic: 在 `N1/N2/N3/N5` 与验收门中显式固定：输入完整性要检查 `出场角色及穿搭`，压缩块必须覆盖它，镜级消费默认以 `角色背景面 / 角色站位走位` 为准，避免视频 prompt 继续按旧字段混写。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已将 `出场角色及穿搭` 纳入完整性门
  - [x] `SKILL.md` 已将 `角色背景面 / 角色站位走位` 写入 N2 与验收清单
  - [x] `FIELD-VID-SUBJ-02` 已固定新的压缩块覆盖范围
- evidence_paths:
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/SKILL.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/CONTEXT.md`
  - `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- user_feedback_or_constraint: 用户要求根据更新后的 shared director schema，检查并同步 `6-Video/1-提示词蒸馏/全能参照`。
