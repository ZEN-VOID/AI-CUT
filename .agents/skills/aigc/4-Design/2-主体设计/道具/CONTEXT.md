# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/道具/2-设计` 的经验层知识库，不是过程日志。
- 调用本叶子技能时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 只有 bridge，没有 design master | 父 skill 合同层 | 建立 `道具设计.json` 作为 canonical truth | 固定 `bridge -> design master -> prompt sidecar` 的顺序 | 下游不再直接拼接 bridge |
| prompt sidecar 抢走业务真源 | 输出治理层 | 把 prompt 文案全部下放 `prop_design_prompt.json` | 固化“canonical truth 与 prompt sidecar 分层” | design master 中不再出现长 prompt |
| 路径错写成 `4-Design/角色/4-道具` | 路径归一层 | 在父 skill 与 runner 中统一规范化到 `4-Design/道具/2-设计/第N集/` | 将 path normalization 记入 manifest 与 shared I/O | 输出目录稳定一致 |
| team 存在但没有明确后台执行规则 | subagent 编排层 | 在父 skill 与 team 文档同时补写后台执行规则 | 把 team 和父 skill 一起作为 validator 的检查对象 | 调用层不再误解成交互式前台流程 |
| prompt 架构师脱离 canonical truth 自创事实 | prompt handoff 层 | 强制 prompt 只消费 `道具设计.json` | 固化“prompt 不改业务事实”禁令 | prompt 内容能回链 design master |
| 上游已经判定为关键剧情道具，但设计阶段仍按普通摆件处理 | 设计汇流层 | 把 `narrative_significance` 收入口径固定到 `design_thesis` 与 `prompt` | 固化“bridge 的叙事意义必须影响结构/痕迹/提示重点” | `道具设计.json.design_thesis.narrative_significance` 与 `prop_design_prompt.json.narrative_focus` 同时存在 |
| specialists 并行存在，但父 skill 仍像线性说明书，无法单读复现汇流 | 编排真源层 | 在主 `SKILL.md` 明写 tranche、节点、汇流和审计门 | 固化“subagent 机制保留，但主技能单文档统筹” | 不读 references 也能看懂整条 design synthesis 链 |

## Repair Playbook

1. 先看 `prop_design_bridge.json` 是否已经存在且字段完整。
2. 再看 `道具设计.json` 是否真的只保留设计事实，而不是长 prompt。
3. 若问题出在 prompt 漂移，先修 `prop_design_prompt.json` 与 `提示词架构师.md`，不要回写 canonical truth。
4. 若问题出在关键剧情道具被弱化，先检查 `narrative_significance` 是否从 bridge 传到了 design/prompt。
5. 若问题出在事实漂移，先修结构/材质/痕迹 patch 与 team 拓扑。
6. 最后检查 `_manifest.json` 是否记录了路径归一、coverage 和 drift 结论。

## Reusable Heuristics

- 对道具设计来说，最值钱的不是“某次 prompt 写得很华丽”，而是“结构、材质、痕迹这些字段能被多次复用”。
- 让 `模型师 + 材质工艺师 + 痕迹叙事师` 并行，通常比单角色串行更稳，因为这三类 patch 的写入槽位天然分离。
- prompt 架构师应晚于 canonical synthesis；否则 prompt 很容易反过来绑架业务事实。
- 若 `1-清单` 已把某个道具标成特殊叙事道具，`2-设计` 不能只保留一个“重要”标签，必须把它转成轮廓、痕迹、连续性和 prompt 焦点。
- 用户给错路径时，不要把错路径写成新的真源；要在 manifest 里记录一次 path normalization，然后统一落到 canonical 目录。
- 对道具设计来说，`agents_plan` 最适合承载 bridge 消费顺序、字段补位顺序与 audit 返工摘要；最终三件套真源仍只能由父 skill 写回。
- 对 subagent 型叶子技能来说，知行合一不是取消角色分工，而是把“门禁 -> brief -> 并行 patch -> canonical -> prompt -> audit”明确写成父 skill 主文档中的可执行网络。
- 上游 `2-Global` 的类型文档一旦统一为 `类型元素.md`，下游示例命令和帮助文本也必须跟着统一；旧参数名最多只能保留为兼容别名，不能继续占据主示例位。
