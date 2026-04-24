# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/1-Planning/3-分组` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/1-Planning/references/grouping-contract.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > 父 `1-Planning/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 输入没有锁到 `2-格式/第N集.md` | 输入真源层 | 回到规划主稿重新锁定当前集范围 | 在 `SKILL.md + validator` 固化输入根门禁 | 输入清单与当前集一致 |
| `3-分组` 重新依赖外部 planning specialist / reviewer | 真源治理层 | 收回到 `references/grouping-contract.md` 的内部能力面 | 在 `SKILL.md + audit` 固化 `Internal Capability Fusion Contract` | 不再引用旧规划组文档 |
| 分组切口混用了 `分镜组ID` 与 `分镜ID` | ID 合同层 | 改回三段式 `分镜组ID` | 在模板、validator 与父 skill 固化“组三级、镜四级” | 标题语义稳定 |
| 量化规则只写在 reference，计算仍靠手填 | 计算真源层 | 回到 quantizer 重新计算 | 让 validator 直接消费 quantizer 结果 | `effective_text_chars` 不再只是说明字段 |
| 台词权重升级后 reference 与 quantizer 系数不一致 | 计算真源层 | 同轮更新 reference 表与 quantizer 常量，并回刷受影响 grouped output | 把 voice_text 系数视为单一计算真源变更，不允许只改文档或只改代码 | quantizer 输出、执行报告与 validator 重新一致 |
| reviewer gate 越权接管组边界 | 复核边界层 | reviewer 仅保留说明，不改 authoritative 数值 | 在 `SKILL.md` 固化 reviewer gate 的非 owned truth 边界 | grouped script 只由父 skill 写回 |
| 组尾重复借入下一组开端后污染字窗判定 | 展示增强层 | 先用 canonical 正文完成量化裁决，再在结果落定后追加隐藏 `尾钩借焰` | 在 `SKILL.md + reference + postprocess + quantizer + validator` 固化“先量化定组，后挂尾钩” | 尾钩存在时，本组 `effective_text_chars` 仍只对应 canonical 分组正文 |
| 分组量化回查主故事源时误读旧 `Init/` 路径 | 初始化输入索引层 | 改回 `0-Init/story-source-manifest.yaml` 再解析 `primary_story_source.path` | 在 reference、脚本与经验层统一固定 `0-Init` 作为初始化目录真源 | quantizer / validator 能稳定命中主故事源而不落回旧路径 |
| 先按叙事整场切组，再倒推 `分镜组时长映射` 让结果过窗 | 量化先行层 | 回到默认时长窗口重新拆/并组，移除无上游证据的时长偏离 | 在 `SKILL.md` 固化“无显式时长证据不得靠时长映射兜底” | 分组边界先由 quantizer 约束，再由结构断点解释 |
| 把“独立信息落点 / 连续峰值”当成不拆组的充分理由 | 边界裁决层 | 先在同一上游场景单位内做 beat 级拆组试算，再决定是否保留单组 | 在 `SKILL.md + reference` 固化“beat 拆组检查先于保留说明” | `warn_high` 或 `warn_low` 的保留理由不再跳过同场景拆组 |
| 同场景只做首轮拆组，不递归复查残余 beat 链 | 递归边界检查层 | 对已拆出的子组继续检查内部 beat 断点，必要时再拆一轮 | 在 `SKILL.md + reference` 固化“同场景拆组必须递归复查子组” | 不再出现“已经拆过一次，但子组仍明显过宽”的残留切口 |
| `### 场景N` 与 `## 【episode-scene-group】` 被当成同一种标题 | 场景/分组语义边界层 | 回读 `2-格式`，把 `### 场景N` 还原为上游场景单位锚点，把组标题只作为节拍标题 | 在 `SKILL.md + reference + template + validator` 固化“场景标题逐字继承上游，分组标题不得改写场景” | validator 能发现分组阶段发明、重命名或遗漏上游场景标题 |
| 已被下游 `分镜ID` 消费的低字数组被误并 | 锁定锚点优先级层 | 恢复原 `分镜组ID`，并回查 `2-Global / 3-Detail` 固定镜数、beat 与四段式 `分镜ID` | 在 `SKILL.md + reference + validator` 固化“锁定分镜组优先于 warn_low 并组建议” | 低于 `warn_low` 的组若保留，`judgement_basis` 必须写明并组检查或锁定分镜依据 |
| 执行报告只写量化结果，缺少每组计算过程 | 报告证据层 | 让 quantizer 生成 canonical `quantization_trace` 并回填报告 | 在 `SKILL.md + reference + validator` 固化“每组必须登记 duration/window/effective_chars 计算链” | 报告可直接复核每组量化过程，而不必反推脚本 |
| 复跑 `postprocess_grouping_output.py` 时，人工补充的 episode 级 handoff 元数据被 renderer 默认值静默覆盖 | 报告回写层 | renderer 优先保留已有 `handoff_summary / duration_policy / bootstrap_output`，只有缺失时才回退到 frontmatter 或默认值 | 把“保留人工 handoff 决策”写成 renderer 合同；报告重渲染只能补 canonical 字窗字段，不能重置人工 episode 级判断 | 重跑 postprocess 后，既有 handoff 决策仍存在，且组级量化字段同步更新 |

## Repair Playbook

1. 先确认 `2-格式/第N集.md` 是否是唯一输入主证据。
2. 再确认 quantizer 是否真的参与组界裁决。
3. 再看 grouped script 是否保持正文结构，只在切口处新增组标题。
4. 最后才检查 reviewer gate 是否被误开或越权。
5. 若执行报告被重渲染，先比对 `handoff_summary / duration_policy / bootstrap_output` 是否被保留，再看组级量化字段。

## Reusable Heuristics

- `3-分组` 最稳的定位不是摘要板，而是“在 `2-格式` 正文里切出组边界后的 grouped script”。
- 对当前阶段来说，最有效的抗漂移机制不是再造 specialist 文档，而是“主合同 digest + quantizer + validator”三件套。
- 节奏复核在规划阶段只应作为 reviewer gate 存在，除非用户明确要求，否则不要把它升级成单独执行面。
- 对 `3-分组` 来说，`effective_text_chars` 一旦进入 validator，就不应再允许人工说明替代 authoritative 结果。
- `voice_text` 系数一旦调整，必须同步回刷 reference、quantizer 和已落盘的 grouped output；这类变更会直接改变 `hard_text_window` 判断，不能只改未来项目。
- 若要增强组间牵引，优先用 `尾钩借焰` 借下一组的首个叙事拍点，而不是直接挪动组界；最稳口径是“先纯量化定组，再隐藏挂钩”，而不是把尾钩再塞回字窗判定。
- 对 `尾钩借焰`，最稳的思维·执行拆法仍是“两节点制”：先做 `eligibility gate`，再做 `inject`；但量化节点必须停在尾钩之前，不能与尾钩重新缠在一起。
- 当 `3-分组` 需要从初始化层回查主故事源时，路径真源固定是 `0-Init/story-source-manifest.yaml`；只要 reference 或脚本写回了旧 `Init/`，后续量化就会静默失去输入索引。
- 若 grouped script 一眼看上去只是“按剧情段落排得顺”，先检查是不是偷用了时长偏离去给既定分组补合法性；真正的量化先行结果通常会先出现同场景内拆组，再由叙事断点解释其合理性。
- 对同一场景内的高压情绪戏，`独立信息落点` 只能说明“拆完后为什么保留这个子组”，不能直接说明“整场不拆”；先看 beat 断点，再看是否保留低字数组。
- 同场景拆组不能停在“已经拆过一次”；只要某个子组内部还能自然读出新的 beat 链，就继续复查，直到边界收敛到不可再拆的子拍。
- 读 `3-分组` 产物时，先把 `### 场景N` 当作上游锚点，把 `## 【episode-scene-group】` 当作分组边界；两者一一对应只是一种结果，不是规则本身。但一旦分镜组已经进入 `2-Global / 3-Detail` 并生成四段式 `分镜ID`，该组界就是下游锚点，不能再用 `warn_low` 并组建议取消。
- 当执行报告要给人复核时，最稳的做法不是再解释一遍结果，而是直接登记 quantizer 生成的 `quantization_trace`；这样 `duration/window/effective_chars` 三段链能保持单一真源。
- 对 `3-分组` 来说，报告模板也应是显式真源；如果只给 grouped script 模板、不给报告模板，执行报告很容易重新退回“只写结果、不写过程”。
- 报告 renderer 最容易误伤的是 episode 级 handoff 决策，而不是组级量化字段；组级字段应重算，episode 级人工判断应保留。
