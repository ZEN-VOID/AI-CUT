# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/2-Global` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/2-Global/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-23

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `2-Global` 仍把四份 Markdown 当默认真源 | 输出治理层 | 收回到按集 `第N集.json` 直写 | 在 `SKILL.md + references/io-contract.md + references/writeback-contract.md` 同步固化单一 JSON 输出 | `2-Global` 的 creative 输出只剩 `第N集.json` |
| `第N集.json` 不是围绕模板填，而是边写边发明结构 | 模板治理层 | 回到 `.agents/skills/aigc/2-Global/templates/episode-root.template.json` 对齐字段 | 在 `references/io-contract.md` 中把模板声明为唯一填写真源 | 所有字段都能直接对应模板槽位 |
| 组级字段仍通过 Markdown 中转 | handoff 层 | 直接在 JSON 中定稿 `global.*` | 在 `group_design_seed_contract` 固化“直接写 JSON，不经 Markdown 中转” | `3-Detail` 不再依赖 `2-Global/*.md` 才能消费上游 seed |
| `groups[].global.剧本正文` 写成摘要 | 组壳写回层 | 强制把命中组全文完整入壳 | 在 `Writeback Policy` 与验收清单中固化全文入壳规则 | 下游可直接继承原组文本 |
| 项目级字段和组级字段混写 | 结构分层层 | 项目级写入 `project_global`，组级写入 `groups[].global` | 在模板与 I/O 合同中固定分层 | `project_global.全集类型元素` 不再漂到组级，组级类型/导演意图不再污染项目总则 |
| 旧下游仍依赖 Markdown，导致切换卡住 | 兼容层 | 明确 Markdown 只做 derived projection | 在合同中写明 compat projection 不拥有真源地位 | JSON-first 切换后仍可渐进兼容旧消费者 |
| `SKILL.md` 继续堆满字段表和长 prose，导致主骨架难扫描 | 技能骨架层 | 把字段细则、patch 细则和 compat 细则下沉到 `references/` | 在主合同固定 `skeleton-first` 与 `Reference Loading Guide` | 主 `SKILL.md` 可快速看清模式、节点、门禁与输出 |
| `2-Global` 只有线性说明，没有真正的思行网络 | 编排表达层 | 在主合同补 `Mode Selection + Mermaid + Thinking-Action Node Contract` | 固定使用 3 张以上 Mermaid，并让节点同时承担判断与动作 | 能一眼看出 `N1-N7` 主干及其汇流顺序 |
| 增量 patch 时不区分 `group_scope / field_scope`，导致局部修复扩大成全量覆盖 | patch scope 层 | 先锁 mode 与 scope，再做 patch-in-place | 在 `references/增量写回与兼容投影.md` 固化 scope 策略 | 局部升级不会污染未命中组或字段 |
| `导演意图` 像剧本正文随手截句，只复述“发生了什么” | 导演导向层 | 把每组 `导演意图` 重写成“观看策略 + 执行抓手 + 禁用方向”三层导向 | 在模板、字段映射、handoff 合同和 `validate_director_intent.py` 中固定防回归 | `groups[].global.导演意图` 能直接转入 `3-Detail` 的镜头、表演、调度、节奏或空间判断 |
| `全局风格` 被动画/国漫示例污染，真人古装项目出现描线、赛璐璐、夸张残影或非物理光效 | 风格基线层 | 回到 `references/全局风格词最佳实践.md`，用写实摄影、物理照明、真实材质、克制镜头与反动画化禁区重写 | 在 N3、模板、字段验收与 review gate 中固定真人古装影视默认基线 | `project_global.全局风格` 能直接作为真人古装生图/生视频统一前缀，且不含动画化词汇 |

## Repair Playbook

1. 先看 `2-Global/SKILL.md` 是否仍以按集 `第N集.json` 为唯一 creative 输出，并且 input/output 首尾合同没有漂移。
2. 再看 `references/思行网络.md`、`references/字段与验收映射.md`、`references/增量写回与兼容投影.md` 是否只细化主合同，没有形成第二真源。
3. 再看 `references/io-contract.md` 与 `references/writeback-contract.md` 是否仍把 `第N集.json` 定义为唯一创作业务真源，并把 `templates/episode-root.template.json` 定义为模板。
4. 再看 `_shared/group_design_seed_contract.md` 是否仍要求 `3-Detail` 从 JSON 直接继承，而不是从 Markdown 抽取。
5. 若用户反馈 `导演意图` 太弱，先检查它是否缺少“观看策略 / 执行抓手 / 禁用方向”，不要只润色句子。
6. 最后才看是否需要保留兼容 Markdown 投影。
7. 若用户要求优化 `全局风格`，先判断项目是否属于真人古装影视；命中时优先采用写实摄影基线，不要从动画、国漫、赛璐璐或夸张武侠残影示例里抽词。

## Reusable Heuristics

- `2-Global` 最稳的形态不是“四份长文定稿后再抽 JSON”，而是“围绕 `templates/episode-root.template.json` 模板直接填好按集 `第N集.json` 字段”。
- 若要和 `3-Detail` 对齐，真正要对齐的是“模板中心 + 单一 JSON 真源 + 直接 patch-in-place”，而不是只对齐文件后缀。
- `project_global` 负责项目级稳定项，`groups[].global` 负责当前集组级 seed；这层分工一旦混掉，`3-Detail` 就会失焦。
- `groups[].global.剧本正文` 必须保留原组全文；任何“为了更结构化所以顺手摘要一下”的做法都会伤到下游。
- 兼容 Markdown 可以保留，但只能是 derived projection，不能再被当作 canonical creative truth。
- 当 `2-Global` 变复杂后，主 `SKILL.md` 应该只保留模式、Mermaid、节点主干、输入输出和验收门；字段表、patch 细则和 compat 细则优先下沉到 `references/`。
- 对这类阶段 skill，真正的“知行合一”不是多写一段思考说明，而是让 `mode / node / gate / writeback` 位于同一骨架里。
- 增量升级默认优先做 `patch-in-place`，除非上游真源或项目级总则发生变化，否则不要顺手全量重写。
- 好的 `导演意图` 应该比剧情摘要多一层导演判断：它要告诉 `3-Detail` 这一组如何组织观看、如何落到现场动作、哪些拍法会把戏拍歪。
- 好的真人古装 `全局风格` 不靠堆名词显得高级，而是同时锁住真实人物质感、服饰/材质纹理、物理照明、动态范围、电影化纵深、克制镜头、真实动作反馈和反动画化禁区。
