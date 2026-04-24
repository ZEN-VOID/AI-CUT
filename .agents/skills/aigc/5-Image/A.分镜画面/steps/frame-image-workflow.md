# Frame Image Workflow

## Business Requirement Analysis

| slot | conclusion |
| --- | --- |
| `business_goal` | 将单一 `分镜ID` 稳定推进到 request JSON、参照绑定和 provider handoff。 |
| `business_object` | `3-Detail/第N集.json`、单帧 request JSON、本地资产、provider handoff 包。 |
| `constraint_profile` | LLM 主创 prompt，脚本只辅助；参照绑定保守；provider 必须唯一。 |
| `success_criteria` | 输出路径兼容旧三段 runtime，且每段有可复核 gate。 |
| `non_goals` | 不生成组级故事板，不处理漫画页，不宣告图片已真实产出。 |
| `complexity_source` | 蒸馏段内部包含锁镜、上下文打包、LLM 主创、prompt 装配、模板填充和审计；后三段又可跳过、续跑、返工，但最终要汇流为一个单帧画面闭环。 |
| `topology_fit` | 串行主干 + 条件跳过 + provider 分支 + 汇流审计。 |

## Thinking-Action Node Network

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `F0-intake` | 锁定 mode 与输入层 | 用户请求、项目根、集号、shot id 或 request JSON | 判定 `one_shot_full / distill_only / bind_only / handoff_only / repair` | `mode_note` | `F1`、`F5`、`F7` 或阻断 | mode 不明确不得继续 |
| `F1-shot-lock` | 唯一定位分镜 | `3-Detail/第N集.json`、四段式 `分镜ID` | 遍历 canonical groups，锁 `group_id + shot_id + source_shot_ids`，必要时仅通过 compat projection 对照旧 helper | `shot_lock_record` | `F2` 或阻断 | 命中必须唯一 |
| `F2-context-pack` | 打包组级与镜级上下文 | group global、shot detail、可选 compat helper、可选 design hint | 提取 prompt 所需事实、正文边界、字段缺口与 `ready/partial` 状态 | `frame_context_pack`、`coverage_note` | `F3` | 上下文须可回链 |
| `F3-llm-distill` | 生成单帧 prompt 正文 | `frame_context_pack`、蒸馏合同 | LLM 直出 `single_frame_shot`、组级设计块、单镜融写行，并按固定前缀装配 prompt | `single_frame_shot`、`prompt_draft`、`prompt_char_count` | `F4` | 不得脚本主创，不得整组摘要化 |
| `F4-request-write` | 写 request JSON 并完成蒸馏审计 | 共享模板、prompt、shot lock、output mode | 填 `meta / prompt_style / model / prompt / prompt_char_count`，保留引用空槽位，按需写 `_manifest.json` | `第N集.json`、可选 `_manifest.json`、`distillation_audit` | `F5`、`F7`、`F9` 或返工 | 模板骨架完整且 prompt 可追溯 |
| `F5-reference-candidates` | 推导引用候选 | request JSON、Assets、4-Design | 生成候选、歧义与拒绝列表 | `candidate_report` | `F6` | 弱证据不得直接绑定 |
| `F6-reference-write-audit` | 写绑定三件套 | 候选裁决、provider mode | 写 JSON、manifest、match report 并审计 | `binding_gate` | `F7` 或返工 | next_entry 必须存在 |
| `F7-provider-route` | 锁 provider | request 或 bound JSON、用户 provider | 选择唯一 provider 或输出推荐主案 | `provider_decision` | `F8` 或阻断 | provider 不唯一不得最终计划 |
| `F8-submit-pack` | 写 handoff 包 | provider-specific 解析 | 写 `submit-plan.json + submit-brief.md` | `handoff_pack` | `F9` | output_dir 同目录 |
| `F9-converge` | 统一闭环 | 各段产物与跳过说明 | 输出执行摘要、验证、返工入口 | `handoff_note` | done | 不允许多个主真源 |

## Branch Rules

- `distill_only`: `F0 -> F1 -> F2 -> F3 -> F4 -> F9`。
- `bind_only`: `F0 -> F5 -> F6 -> F9`。
- `handoff_only`: `F0 -> F7 -> F8 -> F9`。
- `one_shot_full`: `F0 -> F1 -> F2 -> F3 -> F4 -> F5/F6 -> F7/F8 -> F9`。
- 显式 `prompt_only / no_reference`: `F4 -> F7`，但 `F9` 必须记录跳过原因。

## Failure Loops

- 锁镜失败回 `F0-F1`。
- prompt 对象越界回 `F2-F3`。
- 模板字段缺失回 `F4`。
- 引用歧义回 `F5-F6`。
- provider 不唯一回 `F7`。
- 输出路径漂移回 `F8`。

## Distillation Subnetwork

`F1-F4` 是旧 `分镜帧` 蒸馏方法的完整消化段，对应旧叶子 `N1-N8` 的能力面，但写回仍服从本融合技能的三段汇流。

| old node | fused node | absorbed responsibility |
| --- | --- | --- |
| `N1-INPUT-GATE` | `F0/F1` | 判断单帧任务、检查 detail root readiness、排除故事板/漫画页 |
| `N2-SHOT-LOCK` | `F1` | 在 canonical `groups[].detail.分镜列表` 中唯一锁定目标分镜 |
| `N3-CONTEXT-PACK` | `F2` | 打包组级事实、镜级事实、正文桥接和字段覆盖清单 |
| `N4-SINGLE-FRAME-DISTILL` | `F3` | LLM 生成只服务当前帧的 `single_frame_shot` |
| `N5-PROMPT-ASSEMBLY` | `F3` | 逐字前缀 + 组级设计块 + 单镜融写行，并统计字数 |
| `N6-TEMPLATE-FILL` | `F4` | 共享模板填充 `meta / prompt_style / model`，保留引用槽位 |
| `N7-CONVERGENCE-AUDIT` | `F4/F9` | 蒸馏段先审计，融合链最终再汇流 |
| `N8-WRITEBACK-HANDOFF` | `F4/F9` | 写 `第N集.json`，按需 `_manifest.json`，交给绑定或 handoff |

## Distillation Detail Cards

### `F1-shot-lock`

| focus | actions | fail signal |
| --- | --- | --- |
| 阶段边界 | 确认当前对象是单一 `分镜ID`，排除组级故事板、漫画页和多镜合并 | 非单帧诉求仍进入蒸馏 |
| 真源 readiness | 检查 `3-Detail/第N集.json`，经 adapter 判断为 `detail_in_progress | ready` | detail root 未就绪 |
| 唯一锁镜 | 遍历 canonical `groups[]`，在 `detail.分镜列表` 中匹配四段式 `分镜ID`，记录 group、shot、组内序号 | 命中 0 次或多次 |
| compat 对照 | 如需旧 helper，仅通过 compat projection 对照顺序，不让旧 helper 反客为主 | 从旧 helper 直接当 canonical |

### `F2-context-pack`

| focus | actions | fail signal |
| --- | --- | --- |
| 组级事实 | 提取 `分镜组ID / global.剧本正文 / 全局风格 / 类型元素 / 导演意图` | 组级关键字段缺失且无 exception note |
| 正文桥接 | 优先用 target shot `剧本正文`；必要时用 `正文回指` 回链 `正文切分参考[]`；桥接失败时只把整组正文当边界参考 | 靠整组正文猜当前帧 |
| 镜级事实 | 提取时间、主体、角色、动作、氛围、构图、摄影、运镜、转场；legacy 字段只作补证 | 镜级字段被压成泛化摘要 |
| coverage | 输出 `ready / partial` 与缺口，不为完整度虚构事实 | 缺字段却继续当 ready |

### `F3-llm-distill`

| focus | actions | fail signal |
| --- | --- | --- |
| 主创边界 | LLM 直接生成 `single_frame_shot`、组级设计块和单镜融写行 | prompt 由脚本主创 |
| 固定前缀 | 逐字保留四行英文前缀，不改写、不删句、不挪位 | 前缀缺失或顺序漂移 |
| 组级设计块 | 用 `全局风格 / 类型元素 / 导演意图` 组织一行组级设计块，跳过缺失字段 | 独立复述整组 `剧本正文` |
| 单镜融写行 | 以 `xx秒-xx秒｜分镜<组内序号>：` 起行，融写当前帧可见事实 | 变成整组剧情、长对白或多镜描述 |
| 字数预算 | 按 `full / normal / tight / ultra` 压缩，只删减和合并，不新增事实 | 超限后新增不存在的画面细节 |

### `F4-request-write`

| focus | actions | fail signal |
| --- | --- | --- |
| `meta` 回链 | 写 `shot_level=storyboard_frame`、`source_tranche=分镜帧`、`group_id`、长度为 1 的 `source_shot_ids` | JSON 无法回链目标分镜 |
| `prompt_style` | 标注单帧类型、`language=mixed`、字符限制位 | 类型与帧级任务不匹配 |
| `model` 骨架 | 保留共享模板参数和 `reference_images / image_markers` 空槽位 | 删引用槽或伪造绑定 |
| 输出模式 | 默认 `json_only`；仅要求 `full_trace` 时补 `_manifest.json` | manifest 成为第二主真源 |
| 蒸馏审计 | 检查输入回链、对象边界、prompt 结构、模板兼容、下游可消费性 | 未审计就进入绑定或 handoff |

## Distillation Field Master

| field_id | output field | requirement | fused step | fail code |
| --- | --- | --- | --- | --- |
| `FIELD-FRAME-DISTILL-01` | `meta.shot_level / meta.group_id / meta.source_shot_ids` | 单一目标帧可完整回链 | `F1/F4` | `FAIL-FRAME-DISTILL-INPUT` |
| `FIELD-FRAME-DISTILL-02` | `frame_context_pack` | 组级、镜级、正文桥接和缺口说明完整 | `F2` | `FAIL-FRAME-DISTILL-CONTEXT` |
| `FIELD-FRAME-DISTILL-03` | `prompt / prompt_char_count` | 固定英文前缀 + 组级设计块 + 单镜融写行，字数准确 | `F3` | `FAIL-FRAME-DISTILL-PROMPT` |
| `FIELD-FRAME-DISTILL-04` | `prompt_style / model` | 单帧类型与共享模板骨架完整，引用槽位保留 | `F4` | `FAIL-FRAME-DISTILL-TEMPLATE` |
| `FIELD-FRAME-DISTILL-05` | `第N集.json / _manifest.json` | 输出模式清楚，可交给 `F5` 或 `F7` | `F4/F9` | `FAIL-FRAME-DISTILL-HANDOFF` |

## Distillation Audit Rules

- 锁镜失败：回 `F0-F1`。
- 上下文包漏字段：回 `F2`。
- `single_frame_shot` 越界：回 `F3`。
- prompt 前缀、顺序或字数漂移：回 `F3`。
- 模板骨架或引用槽缺失：回 `F4`。
- 输出模式不清或路径漂移：回 `F4/F9`。
