# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/2-设计/道具` 的经验层知识库，不是过程日志。
- 调用本叶子技能时，应在 `aigc -> 4-Design -> 2-设计 -> 1-清单/道具` 之后加载本文件。

## Context Health

- soft_limit_chars: 22000
- hard_limit_chars: 44000
- status: ok
- last_checked_at: 2026-04-14

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍把 `prop_design_bridge.json` 当第一输入根 | 输入真源层 | 恢复为 `道具清单.json.props[].design_context` 第一输入语义 | 在 `SKILL.md`、`IO_CONTRACT.md` 与 runner 中同步固定 `catalog-first` | manifest 标记 `used_catalog_primary_input = true` |
| 默认只写 compat JSON，不写 Markdown 主稿 | 输出治理层 | 先写 `prop-*.md + _manifest.json` | 在合同与脚本里把 compat JSON 改成显式开关 `--write-compat-json` | 未开开关时只落 Markdown 主稿 |
| `prompt整合` 节点格式漂移，导致下游无法提取 | 下游 handoff 层 | 固定使用 `**prompt整合**` 标记 | 在审计节点与脚本校验中显式检查段落标记 | 每份设计卡都能稳定命中 `**prompt整合**` |
| 特殊叙事道具在设计卡里被压平 | 设计汇流层 | 把 `narrative_significance` 写入 `物语 / 解构 / prompt整合` 三段 | 在设计卡模板里固定“特殊叙事道具必须有额外视觉焦点” | critical/notable 道具在三段均可见 |
| compat JSON 与 Markdown 主稿内容漂移 | compat projection 层 | 改为“先 Markdown，后 projection”的单向投影 | 在 manifest 中记录 compat projection 状态，并把 JSON 生成建立在 Markdown 数据模型之上 | compat JSON 只从当前轮 Markdown 投影 |
| 逐道具设计卡存在但没有同名图片或图片 prompt 缺全局风格前缀 | auto image layer | 以 Markdown `**prompt整合**` 加 `2-Global/全局风格` 生成 `full_generation_prompt` | 回指共享输出合同并新增 `NODE-PROP-DESIGN-05 / FIELD-PROP-DESIGN-07` | `<prop_id>-<canonical_name>.<ext>` 与 Markdown 同目录同 stem |
| 道具脚本手工拼 Markdown，未绑定原参照模板 | template source layer | 新增 `templates/prop_masterprompt.structured.v2.md` 并让脚本从模板渲染 | `SKILL.md` 回指模板真源，禁止脚本私造第二结构 | 设计卡含 `## Photography ##` 与 `## Prop Design ##` 原参照标题 |
| 旧式输出模板 reference 内含完整设计卡样例，容易被误当成第二输出模板 | template canonical source layer | 直接移除旧式输出模板 reference，不保留替代说明文件 | 父级共享输出合同登记三模板注册表；仓库 audit 检查旧式输出模板 reference 不得回流 | 道具目录下不再存在平行输出模板 reference |
| `prompt整合` 只拼接全局前缀和局部道具 prompt，或 Integrated prompt 过短 | prompt integration layer | 改为约 2000 bytes 英文自然语言整合同模板上方全部内容 | 道具脚本生成 `Global style prefix + Integrated prompt`，覆盖 `解构 / Photography / Prop Design`，并避免非 ASCII 回流 | `prompt整合` 英文段落含功能骨架、材质、状态痕迹、文化元素、人体工学和负面约束 |
| 未识别的新项目全局风格被包装成 `Translate this project style...` 并携带中文原文 | global style translation layer | 为当前风格族补英文转写；未知 fallback 返回保守英文风格句而非中文翻译指令 | `translate_global_style_prefix()` 不得透传中文原文，所有 fallback 必须是 provider-ready English ASCII | `rg "Translate this project style" <道具2-设计输出>` 无命中 |
| 道具参照图混入手、角色或手持状态，导致后续道具引用带人物污染 | reference cleanliness layer | 将道具 prompt 固定为纯道具图 | `SKILL.md / IO_CONTRACT / build_prop_design_packets.py` 固定 `isolated pure prop view`、`no hands`、`no characters` | prop prompt 不要求手、角色、身体局部、使用者、手持姿态或复杂场景 |
| 道具设计卡仍把使用/触碰/手持当成画面主体，只在 prompt 末尾写 no hands | thinking-action node layer | 在 `NODE-PROP-DESIGN-03` 先把使用逻辑转写为器物表面、功能端、受力点、状态痕迹或离屏使用语境 | `NODE-PROP-DESIGN-03/05` 登记 `reference_cleanliness_note`，自动生图前复验纯道具锚句 | prompt 含 `isolated pure prop view / no hands / no characters`，且没有正向手、身体局部、持有者、角色或复杂场景 |
| 中文道具名或中文设计片段未被英文映射，生图主体退化为 `documented prop` 占位 | prompt subject binding layer | 为当前项目常见道具名与状态片段补英文映射，并把 fallback 改成“主体名 + 功能/材质/状态”描述 | `build_prop_design_packets.py` 的 `translate_prop_name / translate_fragment` 不得让 provider-facing prompt 回退成空泛主体占位；新增项目发现占位语时先修映射再重生图 | `rg "documented prop\\|documented visual priority\\|documented story premise" <道具2-设计输出>` 无命中，抽样图像主体与文件 stem 对齐 |
| 道具输出写完后没有进入 `team.yaml` 驱动的监制强化 | council closeout layer | 在 `NODE-PROP-DESIGN-06` 固定读取项目根 `team.yaml` 并按共享合同的 refine / gate 分层与道具设计型 reviewer 补选规则起 council | 用 `_shared/subagent-supervision-contract.md` 固定 `roles.supervision.members + optional 4-Design review gate members + 张叔平/叶锦添补选 -> real subagents` | 当前轮道具输出完成后可回溯 `supervision_review_note`，且 reviewer 不是阶段 skill 误命中 |

## Repair Playbook

1. 先看 `道具清单.json` 是否已经存在且包含 `props[].design_context`。
2. 再确认 `north_star / init_handoff / 全局风格 / 类型元素` 是否成功装配到当前轮上下文。
3. 若问题出在 prompt 提取，先查 `**prompt整合**` 段落格式，不要急着改兼容 JSON。
4. 若问题出在“设计不够像特殊叙事道具”，先检查 `narrative_significance` 是否穿过了三段设计卡。
5. 若问题出在旧下游兼容，最后才打开 compat projection，而不是反过来让 compat JSON 主导当前链路。
6. 自动生图前检查 `reference_cleanliness_note`：缺 `isolated pure prop view / no hands / no characters` 或出现正向手、身体局部、持有者、角色、复杂场景时，回到 `NODE-PROP-DESIGN-03`。
7. 设计卡落盘后，用 `run_design_auto_image.py --design-file <prop_id>-<canonical_name>.md` 验证同目录同名图片快路径。
8. 当前轮道具 canonical 输出与 projection 落盘后，再读取项目根 `team.yaml` 做 `NODE-PROP-DESIGN-06`；图片状态只作证据。
9. `NODE-PROP-DESIGN-06` 先按 shared contract 区分 stage-end refine 与 final-stage gate；显式 reviewer 不足时，按道具目标补入 `张叔平 + 叶锦添`。

## Reusable Heuristics

- 对当前仓的 `2-设计/道具` 来说，最关键的真源裁决不是“有没有 JSON”，而是“Markdown 设计卡能否单独支撑下游”。
- `design_handoff` 已经足够密时，`2-设计` 应该做的是设计升级，而不是把 `1-清单` 再翻译一遍。
- 一旦 runtime 已经稳定采用 `**prompt整合**` 抽取，源层就必须把这件事写成硬门槛，而不是把它留给面板层猜。
- compat JSON 的正确用法是“给旧下游保留投影”，不是“给新源层提供借口继续双真源”。
- 道具自动图是单道具概念图，不是 PROP_DESIGN_SHEET；多视图仍应交给 `3-面板/道具` 或 `nano-banana/multiview-prop`。
- 道具 Markdown 结构以 `templates/prop_masterprompt.structured.v2.md` 为唯一模板真源；脚本只能填槽，不再保留平行输出模板 reference。
- 道具 `prompt整合` 应是一段约 2000 bytes 的英文 prop-art brief：从模板上方所有字段整合可视化指令，尤其不要遗漏 `Prop Design` 的材质、纹理、功能、状态痕迹和负面约束；画面固定为 `isolated pure prop view`，不得加入手、角色或手持元素。
- 全局风格转写失败时，脚本宁可落一个保守但纯英文的 provider-ready 风格前缀，也不要把中文原文包进 `Translate this project style...`；后者会把翻译任务推给生图模型并污染下游面板请求。
- 道具纯物图不是把“手”删除这么简单；先把手持/触碰/使用动作改写为器物自身的结构证据和状态证据，再写 prompt，才能避免模型补手或补持有者。
- 用户确认画面风格、角色图、场景图与道具图效果稳定时，不应为修主体错配而重写全局风格；优先只修 `prompt整合` 的主体绑定、英文名映射和状态证据，保留已验证的黑白恐怖漫画风格前缀。
- 道具输出后的监制强化优先看 `roles.supervision.members`；若项目把 `roles.review` 显式挂到 `4-Design` final-stage gate，则并入 reviewer roster；当当前阶段更偏道具视觉系统审稿时，再补入设计组/美学组 reviewer。对道具默认是 `张叔平 + 叶锦添`。
