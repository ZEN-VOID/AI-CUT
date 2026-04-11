# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `6-视频/subtypes/1-提示词蒸馏/首帧参照` 的经验层知识库，不是过程日志。
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
| prompt 直接照搬整组 `剧本正文` | 桥段提取层 | 回到目标 `分镜ID`，重做剧情桥段裁切 | 在 `FIELD-VID-FFR-02` 固化“剧情桥段只对应目标帧” | 剧情桥段与目标镜级事实对齐 |
| `全局风格` 被改写 | 固定文本层 | 恢复原文直贴 | 在输出契约里显式标记“fixed verbatim block” | 与上游逐字一致 |
| prompt 中暴露了字段标题 | 文本编排层 | 重写为无标题融合文本 | 在 `FIELD-VID-FFR-02` 固化只保留组ID/镜ID标签 | 除组ID/镜ID外无显式字段名 |
| 帧级请求没有带出所属 `分镜组ID` | 来源定位层 | 补回 `meta.group_id` 与显式 `分镜组` 标签 | 在字段表中要求 `group_id + source_shot_ids` 成对存在 | 可同时回链到组级与帧级 |
| 为了凑字数而虚构桥段细节 | 字数预算层 | 回退到保守桥段表达，允许 underflow | 在策略表中固化 `ambiguous/underflow` 保守退化规则 | manifest 中有原因备注且无新事实 |

## Repair Playbook

1. 先查目标 `分镜ID` 是否真实存在于某个 `分镜组`。
2. 再查 `剧情桥段` 是否只描述该目标分镜可支持的动作、状态或事件阶段。
3. 再查 `全局风格` 是否保持原文。
4. 再查其余组级与镜级字段是否已压缩进 prompt，且没有字段标题残留。
5. 最后查 `prompt_char_count`、双输出文件与 manifest 是否一致。

## Reusable Heuristics

- 帧级视频请求最容易失真在“把整组剧情搬过来”，而不是“文字不够华丽”。
- `剧情桥段` 的职责是把整组剧本正文切成目标镜头可见的一小段，不是重写剧情，也不是摘要整组剧情。
- 当一个分镜组只有 1 个分镜时，直接使用整段 `剧本正文` 作为剧情桥段，通常最稳。
- 当一个分镜组有多个分镜而桥段边界不够清晰时，优先锚定目标分镜的可见动作、人物状态和空间关系，保守缩写，不虚构过渡。
- 帧级 prompt 仍然需要组级空气层，所以最稳结构通常是：`剧情桥段 + 全局风格 + 压缩后的类型元素/导演意图 + 目标镜级字段`。
- 帧级提示词的字数窗应低于组级；若上游信息有限，允许 underflow，但必须把原因写进 manifest，而不是用空泛修辞补字数。

## Case Log

### Case-20260410-AIGC-VIDEO-FIRST-FRAME-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `6-视频/subtypes/1-提示词蒸馏/首帧参照` 建立了从 `编导/第N集.json` 单一 `分镜ID` 到帧级视频请求 JSON 的叶子合同。
- root_cause_or_design_decision: 用户需求已明确要求“站在分镜帧颗粒度，按分镜ID组织提示词，并把剧本正文切成对应分镜帧的剧情桥段”；若仍沿用组级 `全能参照` 规则，会把最关键的帧级桥段提取问题留成隐式人工判断。
- final_fix_or_heuristic: 将“单帧定位、剧情桥段提取、全局风格固定保留、其余字段均匀压缩、双输出模式、参照图暂留空”的规则写成稳定的叶子执行合同，并让 `meta.source_shot_ids` 固定承载单一目标 `分镜ID`。
- prevention_or_replication_checklist:
  - [x] 帧级来源定位已写入合同
  - [x] `剧本正文 -> 剧情桥段` 规则已写入策略
  - [x] 双输出落点已写入合同
  - [x] `source_shot_ids` 已回链共享模板
- evidence_paths:
  - `.agents/skills/aigc/6-视频/subtypes/1-提示词蒸馏/首帧参照/SKILL.md`
  - `.agents/skills/aigc/6-视频/subtypes/1-提示词蒸馏/首帧参照/CONTEXT.md`
  - `.agents/skills/aigc/6-视频/subtypes/1-提示词蒸馏/首帧参照/references/output-template.md`
  - `.agents/skills/aigc/6-视频/_shared/video-generation-input.template.json`
- user_feedback_or_constraint: 用户明确要求默认读取 `projects/<项目名>/编导/第N集.json`，模板参照共享 JSON/TXT 模板，提示词以分镜组内容为基础，但当前站在分镜帧颗粒度，只处理单一 `分镜ID`，并将剧本正文调整为对应分镜帧的剧情桥段。
