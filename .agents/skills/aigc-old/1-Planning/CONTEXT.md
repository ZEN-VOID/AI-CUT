# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/1-Planning` 单包融合后的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/1-规划/SKILL.md` 时，应自动预加载本文件。
- 原 `1-分集 / 2-格式 / 3-分组` 的局部经验已迁入 `knowledge-base/episode-splitter-heuristics.md`、`knowledge-base/script-format-heuristics.md`、`knowledge-base/grouping-heuristics.md`；当前业务口径中，历史 `2-格式` 称为 `2-剧本`，runtime 路径不改。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 分区规范 > 项目记忆/项目上下文 > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 24000
- hard_limit_chars: 48000
- status: ok
- last_checked_at: 2026-04-24

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 旧 `1-分集 / 2-格式 / 3-分组` 子包入口复活 | 技能包结构层 | 删除或迁移旧子包 `SKILL.md`，改回父包 mode + reference | 在 `SKILL.md`、audit 与迁移矩阵中固定“单包三模式” | `find .agents/skills/aigc/1-规划 -name SKILL.md` 只返回父包 |
| 原三包细则迁移后找不到去向 | legacy upgrade 层 | 回到 `references/legacy-migration-matrix.md` 补 target owner | 每次融合/重命名先写迁移矩阵，再删除旧入口 | 每个旧文件/section 均可追到 `references/`、`knowledge-base/`、`scripts/` 或 `templates/` |
| 父 `SKILL.md` 又堆回三份长细则 | 动态引用层 | 抽回对应 `references/*-contract.md` | 根入口只保留 mode selection、引用表、门禁与输出合同 | validator 能看到 `Reference Loading Guide` 且 `SKILL.md` 可扫描 |
| `1-分集 / 2-格式 / 3-分组` 真源边界混写 | 输出治理层 | 回到 `references/planning-io-contract.md` 重锁 runtime 输出边界 | 固化“技能包单一，项目 runtime 子路径保留” | 三类项目产物不互相覆盖 |
| `2-剧本` 又退回外部判模/标准剧/解说剧 agent | 模式内真源层 | 使用 `script_format` mode 与 `references/script-format-contract.md`，并统一归一到标准剧本投影 | 入口元数据只推荐 `$aigc-planning`，旧别名只保留为历史说明 | 旧子技能别名不再出现在路由脚本 |
| `3-分组` 又退回外部 specialist/reviewer 双真源 | 模式内真源层 | 使用 `grouping` mode 与 `references/grouping-contract.md` | reviewer 只作为内部 gate 或本地 review 合同，不占写回权 | grouped script 只由本包和脚本链校验 |
| 脚本路径仍指向旧子包目录 | 引用同步层 | 更新到 `scripts/`、`templates/`、`references/` 父级路径 | 重命名时全仓 `rg` 旧路径并同步 | `rg` 不再命中旧 `.agents/skills/aigc/1-规划/<子包>/...` 文件路径 |
| 迁移时把项目 runtime 子目录误删 | runtime/skill tree 混淆层 | 恢复 `projects/aigc/<项目名>/1-Planning/1-分集/2-格式/3-分组` 业务落盘边界 | 在父 skill 明确“技能包融合不等于 runtime 融合” | `project-runtime-layout.md` 与 planning I/O 说法一致 |
| `2-剧本` 为每集生成独立执行报告 | 输出治理层 | 收束为唯一 runtime 报告 `2-格式/执行报告.md`，每集只作为报告内 episode 区块 | 对齐 `1-分集`、`2-剧本`、`3-分组` 三个子目录均单报告口径 | `rg '第N集-执行报告|第<n>集-执行报告'` 只剩禁止性说明 |
| 宽泛执行 `1-Planning` 后在分集处停住 | 路由判型层 | 将“执行/继续/完成 1-Planning 且无断点要求”判为 `full_chain` | 明确三步子路径是内部处理边界，不是默认用户交互断点 | `types/planning-type-map.md` Ambiguity Rules 指向 full_chain |
| `3-分组` 退化为一场景一组 | 量化裁决层 | validator 拦截“一场景一组但不在 warn_window”的结果，并要求 judgement_basis 写明量化门槛 | 在 grouping contract 固化“场景标题只是锚点，量化才是裁决门” | `validate_grouping_output.py` 对低/高窗场景匹配输出返回失败 |
| `2-剧本` 把场景标题写成剧情摘要 | 剧本语义层 | 改为好莱坞标准剧本 slugline：`内景/外景 场所 - 日/夜` | 在 script format contract 与 validator 固化 slugline 门禁 | `validate_script_output.py` 拦截缺少 `内景/外景` 或 `- 日/夜` 的标题 |
| `2-剧本` 把同一 slugline 的叙事 beat 拆成多个场景号 | 场景语义层 | 相同 `内景/外景 + 场所 + 日/夜` 沿用同一场景号，beat 拆分交给 `3-分组` | validator 拦截同一 slugline 多编号和同编号多 slugline | 第1集同一教室日景只允许 `场景1`，组可为 `1-1-1/1-1-2/...` |
| `2-剧本` 或 `3-分组` 反复打印相同场景标题 | 标题呈现层 | 连续同一 slugline 只保留首次标题；同一分镜组内同场景标题只出现一次 | script validator 拦截连续重复标题，grouping validator 拦截同组重复标题 | 第1集 `2-剧本` 只出现一次 `场景1`，第1集每个分镜组内也只出现一次 |
| 把项目 `CONTEXT/` 里的预设参照误升为分集真源 | 源层路由层 | 立即回到 `Original/`，优先按 `Original/Story/` 已给原文/章节边界分集；`CONTEXT/` 只作为 preset/reference 写入辅证字段 | 在 `planning-io-contract.md` 和 `episode-splitter-contract.md` 固化 `Original = 故事源真源`、`CONTEXT = 预设参照` | 例如 `projects/aigc/诡校/Original/Story/第1-3章.md` 明确存在时，不得按 `CONTEXT/剧本_诡校_第一卷.md` 的七场结构解成7集 |
| 业务口径仍叫 `2-格式`，导致误以为只做标题/字段格式化 | 表述层 | 源层显示名改为 `2-剧本`，明确这是剧本主稿投影阶段 | 保留 mode id `script_format` 与 runtime 路径 `2-格式/`，在合同和模板中写明 display name 与路径兼容关系 | 用户看到阶段名时不会误解为“只处理格式”，脚本仍能读取旧路径 |

## Repair Playbook

1. 先确认问题发生在技能树结构、项目 runtime 输出，还是脚本/模板引用层。
2. 若是技能树结构问题，先检查 `.agents/skills/aigc/1-规划` 是否只有父级 `SKILL.md + CONTEXT.md`。
3. 若是细则缺失，回到 `references/legacy-migration-matrix.md`，确认旧三包内容是否已迁入目标 owner。
4. 若是输出边界问题，先读取 `references/planning-io-contract.md`，不要直接修改项目产物。
5. 若是源层误判，先锁 `Original/` 下已存在的故事正文，再把项目 `CONTEXT/` 降级为预设参照；不要用参照文件的建议集数覆盖原文章节边界。
6. 若是 `2-剧本` 或 `3-分组` validator 失败，优先检查父级 `scripts/` 路径和模板路径是否已从旧子包迁出。
7. 若是审计失败，先运行 `python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/aigc/1-规划` 再跑仓库审计。
8. 每次新增稳定经验，优先写入最窄有效范围：父包共性经验写本文件；分集/格式/分组局部经验写 `knowledge-base/` 对应文件。
9. 若用户指出“规划执行不该中断”，先检查 `types/planning-type-map.md` 是否把宽泛执行请求路由到 `full_chain`，再检查 `validation-report.md` 是否只登记真实完成项。

## Reusable Heuristics

- 这次融合的核心不是取消 `1-分集 / 2-格式 / 3-分组` 的业务概念，而是取消它们作为三个可独立唤起的技能包。
- 最稳结构是“一个 `SKILL.md` 做 mode router，三份旧细则做 `references/` 真源，三份旧经验做 `knowledge-base/` 经验层”。
- 项目 runtime 子目录继续保留，因为它们是业务产物边界，不是技能包入口边界。
- 对内容创作链路，脚本越强，越要把它限制在 validator、quantizer、renderer、postprocess；正文、边界、变体和组界判断仍由 LLM 直接完成。
- `agents/openai.yaml` 只应宣传 `$aigc-planning` 一个入口；旧分集、格式、分组入口别名只作为迁移历史说明，不再出现在默认提示中。
- 融合后最容易遗漏的是跨技能引用：comic、backfill、audit、CHANGELOG 和旧报告里可能还会指向旧 skill path；修改时要区分“技能包路径”与“项目产物路径”。
- 三步子路径可以保留，因为它们是处理精度边界；但除非用户显式要求断点，否则执行 `1-Planning` 应连续跑完分集、格式、分组和验收。
- `2-剧本` 的报告粒度应与分集、分组一致：正文逐集，报告唯一；逐集 validator 结果写入 runtime 路径 `2-格式/执行报告.md`。
- 分组阶段的第一裁决不是“场景数”，而是量化窗口；场景标题只用于顺序继承和 source_span 回指。
- 标准剧的“场景标题”不是中文段落标题；应理解为 Hollywood screenplay slugline，动作、主题和系统分屏都下沉到正文画面字段。
- 标准剧本的场景号不是节拍号；同一 slugline 中的入场、宣告、公告、觉醒可以是多个分镜组，但不能写成多个场景号。
- 场景标题不是段落分割线；连续同场景内的 beat 直接续写，分组阶段再用 `## 【episode-scene-group】` 表达切口。
- 项目源层默认口径：`projects/aigc/<项目名>/Original/` 是故事源真源，`projects/aigc/<项目名>/CONTEXT/` 是预设参照；当二者冲突时，先按 `Original/Story/` 的原文/章节边界分集，再把 `CONTEXT/` 作为设定、机制和风格辅证。
