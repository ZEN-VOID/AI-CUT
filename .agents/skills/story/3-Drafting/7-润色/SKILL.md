---
name: story-drafting-polish
description: Use when `3-Drafting` needs the governed child skill that performs the final integrated polish pass, including anti-commentary voice, anti-repetition, naturalness, and prose refinement.
governance_tier: lite
---

# 3-Drafting / 7-润色

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 必须回读父层 `3-Drafting/SKILL.md` 与 `../_shared/drafting-child-output-contract.md`。
- 正式处理前，必须读取 Step 6 已写回后的当前 `第N集.md`。
- 必须同时按需读取以下局部子模块：
  - `反评论腔/module-spec.md`
  - `反重复用词/module-spec.md`
  - `自然感/module-spec.md`
  - `文笔优化/module-spec.md`

## Parent Positioning

本 child 负责：

- 统一做去评论腔、去机械重复、去 AI 工业感、文笔收束
- 把前 6 道工序的成果真正融成一篇“像真人写的小说”

它不负责：

- 推翻前 6 步的剧情主干
- 越权给出 validation 通过与否判定

## Canonical Sources

- `../SKILL.md`
- `../CONTEXT.md`
- `../_shared/drafting-child-output-contract.md`
- `反评论腔/module-spec.md`
- `反重复用词/module-spec.md`
- `自然感/module-spec.md`
- `文笔优化/module-spec.md`
- `../../_shared/core-constraints.md`

## Business Requirement Analysis Contract

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 把已有的故事、节奏、氛围、人物、对白、张力成果收束成自然、克制、有人味的最终正文。 |
| `business_object` | Step 6 后正文、风格卡、team 确定的监制/评审偏向。 |
| `constraint_profile` | 润色不能抹平角色和节奏差异；允许风格强化，但不允许变成大师桥段模仿秀。 |
| `success_criteria` | 正文明显减少 AI 评语腔、机械重复和工业平滑感，同时文笔更稳、更自然。 |
| `topology_fit` | `root reread -> anti-commentary -> anti-repetition -> naturalness -> prose finish` |

## Total Input Contract

- 必需输入：
  - 当前 `第N集.md`
  - `写作日志.yaml`
- 条件必需输入：
  - `1-Cards/1-风格卡/**/*.json`
  - `team.yaml`（若项目已锁监制/评审偏好）
- 硬规则：
  - 润色是终修，不是再起一篇。
  - 模仿只能借“文笔判断和气质控制”，不能复制已知固定桥段。

## Output Contract

- `manuscript_patch`
  - 候选终稿正文
- `process_log_entry`
  - `step_id: 7`
  - `focus_dimension: integrated_polish`
- owned manuscript dimension：
  - 反评论腔
  - 反重复用词
  - 自然感
  - 文笔优化

## Immediate Validation Hook Contract

- 本 step 写回后，父层必须按 `../../4-Validation/_shared/validation-dimension-registry.yaml` 触发当前 step 登记的 inline validators。
- 该 step 的 hook 全部通过后，只形成 `candidate_final_draft`，仍必须进入 `4-Validation` 才能获得最终 PASS。

## Visual Map

```mermaid
flowchart TD
    A["回读 Step 6 正文"] --> B["反评论腔"]
    B --> C["反重复用词"]
    C --> D["自然感校正"]
    D --> E["文笔优化与总收束"]
```

## Thinking-Action Network

| node_id | field_id | objective | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-ROOT-REREAD` | `FIELD-DR7-01` | 回读当前正文 | 读取 Step 6 结果、风格卡、team 偏向 | `input_note` | -> `N2` | 正文最新 |
| `N2-ANTI-COMMENTARY` | `FIELD-DR7-02` | 去评论腔与上帝评语口吻 | 清理直白点评与代替读者作答 | `commentary_note` | -> `N3` | 叙述不过界 |
| `N3-ANTI-REPETITION` | `FIELD-DR7-03` | 减少机械复用 | 检查重复词、重复句式、重复表达路径 | `repeat_note` | -> `N4` | 用词不机械 |
| `N4-NATURALNESS` | `FIELD-DR7-04` | 去 AI 工业感 | 调整衔接、留白、轻微不规则感 | `natural_note` | -> `N5` | 真人感成立 |
| `N5-PROSE-FINISH` | `FIELD-DR7-05` | 做文笔总收束 | 统一句法、韵律、风格气质 | `finish_note` | done | 最终版成立 |

## Lite Field Contract

| field_id | output_slot | pass_standard | fail_code | rework_entry |
| --- | --- | --- | --- | --- |
| `FIELD-DR7-01` | 当前正文 | 已回读张力版正文 | `FAIL-DR7-01` | `N1` |
| `FIELD-DR7-02` | 评论腔修正 | 明显减少上帝评语与直白代答 | `FAIL-DR7-02` | `N2` |
| `FIELD-DR7-03` | 重复修正 | 机械重复词/句显著减少 | `FAIL-DR7-03` | `N3` |
| `FIELD-DR7-04` | 自然感修正 | 工业平滑感明显下降 | `FAIL-DR7-04` | `N4` |
| `FIELD-DR7-05` | 最终润色版正文 | 文笔稳定、自然、可交接 | `FAIL-DR7-05` | `N5` |

## Completion Contract

- 当前正文已通过四个局部子模块的终修。
- 当前正文只达到 `candidate_final_draft` 边界，而不是最终 `validated_final_draft`。
- `process_log_entry` 已记录终修聚焦点与留给 validation 的注意事项。
