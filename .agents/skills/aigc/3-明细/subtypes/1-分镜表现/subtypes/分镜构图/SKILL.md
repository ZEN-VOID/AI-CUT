---
name: aigc-detail-storyboard-composition
description: Use when `1-分镜表现` already knows how many inline storyboard inserts a group needs and must now assign static shot fields such as shot size, depth of field, composition style, layout, view angle, focal length, focus point, and aperture.
governance_tier: full
---

# aigc 3-明细 / 1-分镜表现 / 分镜构图

## 概述

`分镜构图` 负责把已经确定好的 `[分镜1..N]`，补成“每一镜该怎么看、持续多久、如何形成视觉峰值”的静态镜头设计对象。

它参考 `AIGC-ZEN-VOID` 的 `2-导演/5-分镜构图`，但在当前 `3-明细` 阶段只继承与内联脚本直接相关的静态字段，不继承导演阶段的整套 JSON 责任边界。

当前子技能维护两层结果：

1. `canonical shot` 真源：
   - `分镜ID`
   - `时间`
   - `角色及站位`
   - `场景及方位`
   - `道具及状态`
   - `景别 / 镜头属性 / 镜头框架 / 镜头类型 / 镜头视角 / 镜头速度`
   - `构图布局 / 构图方式`
   - `景深 / 焦距 / 对焦点 / 光圈`
   - `转场`（本阶段保留空值）
2. 面向父级插回主文件的八字段投影：
   - `景别 / 景深 / 构图风格 / 构图布局 / 镜头视角 / 焦距 / 对焦点 / 光圈`

其中：

- `panel_count / template_id / candidate_counts / single_panel_long_take` 的裁决真源属于上游 `分镜密度`。
- 本层负责把上游镜数真源真正落成可拍、可读、不过门槛塌缩的逐帧构图。

交付类型：`内容输出型`
## When to Use

- `panel_count` 已经确定，需要给每镜补静态镜头字段。
- 需要把“分镜插入”从纯编号，升级为可读的镜头表达。
- 需要借用导演阶段的构图经验，但适配当前脚本内联格式。
- 需要把上游镜数裁决落成 `groups[].分镜明细[]` 等价的 canonical shot 明细，再投影为父级可回写的单行摘要。
## When Not to Use

- 还没确定这一组到底几镜。
- 当前要补的是运镜、光影、色彩、转场。
- 输入证据不足到连主体视线或信息重心都无法判断。
## 核心约束（Mandatory）

- 工匠级契约继承：遵循 `skill-内容输出型/SKILL.md` 的反模板化与深度思考要求，本层不按安全镜头模板批量填空，而是为每一镜补有差异的静态镜头字段。
- Root-Cause 执行契约继承：一旦出现字段漂移、组内重复、视觉峰值缺失或职责越界，先按根 `AGENTS.md` 与本技能 `Root-Cause Execution Contract` 上溯规则源，再决定是否改正文。
- 自评偏差与缓解：LLM 容易把所有镜写成同景别同视角的保守配置，或把运镜、光色混入本层；执行时必须先继承上游 `panel_count -> template_id`，再检查组总时长、组间回溯、组内差异与峰值镜。
- 本层不重新决定候选镜数；只有在实际构图连续两轮都无法满足模板级门槛时，才允许按 `references/type-strategies.md` 的回退顺序请求上游微调。
- 组总时长读取链固定为：`分镜组时长映射 -> 默认组时长 -> 切分时长策略`。禁止把整集时长误判成组时长。
- 最终结果必须同时成立：时间连续、至少一帧构图审美峰值、同场景相邻组首帧回溯上一组尾势、边界不越界。
- `转场` 字段在本阶段保留空值；不得提前写运镜、光色或转场正文。
## Reference Modules (Mandatory)

`aigc 3-明细 / 1-分镜表现 / 分镜构图/SKILL.md` 只保留主合同、边界、门禁、回指和 Mermaid 摘要；专项细则以下列模块为真源：

- `references/chain-of-thought.md`
- `references/execution-flow.md`
- `references/type-strategies.md`
- `.agents/skills/aigc/3-明细/references/output-template.md`

硬规则：

1. 根 `SKILL.md` 仍是唯一主合同；`references/` 是模块化细则承载层，不是并行第二真源。
2. 若字段、流程、路由或输出契约需要升级，优先回写对应 `references/*.md`。
3. 主 `SKILL.md` 只保留摘要与回链，不重复展开长表格、长流程与长写位合同。
## Route Summary

- 当前技能的 VSM 变量、情况判定、策略映射与回退规则已下沉到 `references/type-strategies.md`。
- 主 `SKILL.md` 只保留入口边界与判路摘要，不再重复长表。
## Execution Summary

- canonical landing、共享运行时继承与完整 workflow 已下沉到 `references/execution-flow.md`。
- 主 `SKILL.md` 只保留阶段边界与执行摘要，不重复整段流程细则。
## Output Summary

- 输出内容模板统一继承父级 `.agents/skills/aigc/3-明细/references/output-template.md`，本技能不再定义本地 output-template 真源；局部写位与侧车规则继续由 `references/execution-flow.md` 与 `references/type-strategies.md` 承载。
- 主 `SKILL.md` 只保留输出职责摘要，不再重复整段模板正文。
## Field System Summary

- 字段主表、thought pass 与 pass table 已下沉到 `references/chain-of-thought.md`。
- 主 `SKILL.md` 只保留字段系统摘要，不再重复长表。
## Root-Cause Execution Contract (Mandatory)

当出现以下症状时，必须先修本子技能合同：

- `[分镜N]` 只剩编号，没有可读镜头信息
- 所有镜都写成“中景 + 平视 + 常规构图”
- 组内镜头虽然有差异，但没有一帧达到最大胆的构图峰值
- 时间字段断裂，或把整集总时长误读成单组总时长
- 同场景相邻组首帧没有回溯上一组尾帧核心动作/状态
- 构图阶段混入运镜、转场或色彩，职责越界
- 字段名各写各的，父级无法统一回写

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜构图/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜构图/CONTEXT.md`
- `Meta Rule Source`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/SKILL.md`
  - `.agents/skills/aigc/3-明细/SKILL.md`
  - 根 `AGENTS.md`
## SKILL / CONTEXT 分工（Mandatory）

- `SKILL.md` 锁定本层触发条件、唯一真源、执行顺序、写位边界与验收门槛。
- `CONTEXT.md` 沉淀失败类型、修复策略、成功 heuristic 与复用证据，不重写本层主合同。
- 经多轮验证稳定成立的经验，才允许从 `CONTEXT.md` 晋升回本 `SKILL.md` 或上层技能合同。
## Context Preload (Mandatory)

- 依次加载：
  - `.agents/skills/aigc/3-明细/SKILL.md + CONTEXT.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/SKILL.md + CONTEXT.md`
  - 本 `SKILL.md + CONTEXT.md`
- 需要细化局部思维链、执行流、类型策略与输出模板时，继续加载本目录 `references/*.md`。
