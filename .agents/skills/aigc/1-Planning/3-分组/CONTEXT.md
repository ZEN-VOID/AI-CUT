# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/1-Planning/3-分组` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/1-Planning/3-分组/SKILL.md` 时，应自动预加载本文件。
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
| `3-分组` 重新依赖外部 planning specialist / reviewer | 真源治理层 | 收回到 `3-分组/SKILL.md` 的内部能力面 | 在 `SKILL.md + audit` 固化 `Internal Capability Fusion Contract` | 不再引用旧规划组文档 |
| 分组切口混用了 `分镜组ID` 与 `分镜ID` | ID 合同层 | 改回三段式 `分镜组ID` | 在模板、validator 与父 skill 固化“组三级、镜四级” | 标题语义稳定 |
| 量化规则只写在 reference，计算仍靠手填 | 计算真源层 | 回到 quantizer 重新计算 | 让 validator 直接消费 quantizer 结果 | `effective_text_chars` 不再只是说明字段 |
| 台词权重升级后 reference 与 quantizer 系数不一致 | 计算真源层 | 同轮更新 reference 表与 quantizer 常量，并回刷受影响 grouped output | 把 voice_text 系数视为单一计算真源变更，不允许只改文档或只改代码 | quantizer 输出、执行报告与 validator 重新一致 |
| reviewer gate 越权接管组边界 | 复核边界层 | reviewer 仅保留说明，不改 authoritative 数值 | 在 `SKILL.md` 固化 reviewer gate 的非 owned truth 边界 | grouped script 只由父 skill 写回 |
| 组尾重复借入下一组开端后污染字窗判定 | 展示增强层 | 先用 canonical 正文完成量化裁决，再在结果落定后追加隐藏 `尾钩借焰` | 在 `SKILL.md + reference + postprocess + quantizer + validator` 固化“先量化定组，后挂尾钩” | 尾钩存在时，本组 `effective_text_chars` 仍只对应 canonical 分组正文 |
| 分组量化回查主故事源时误读旧 `Init/` 路径 | 初始化输入索引层 | 改回 `0-Init/story-source-manifest.yaml` 再解析 `primary_story_source.path` | 在 reference、脚本与经验层统一固定 `0-Init` 作为初始化目录真源 | quantizer / validator 能稳定命中主故事源而不落回旧路径 |
| 先按叙事整场切组，再倒推 `分镜组时长映射` 让结果过窗 | 量化先行层 | 回到默认时长窗口重新拆/并组，移除无上游证据的时长偏离 | 在 `SKILL.md` 固化“无显式时长证据不得靠时长映射兜底” | 分组边界先由 quantizer 约束，再由结构断点解释 |

## Repair Playbook

1. 先确认 `2-格式/第N集.md` 是否是唯一输入主证据。
2. 再确认 quantizer 是否真的参与组界裁决。
3. 再看 grouped script 是否保持正文结构，只在切口处新增组标题。
4. 最后才检查 reviewer gate 是否被误开或越权。

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
