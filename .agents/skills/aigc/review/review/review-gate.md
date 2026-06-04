# Review Gate

## Default Provider

- 默认辅助 provider：`code-reviewer`
- provider 配置：`_shared/execution-provider.yaml`
- runner：`scripts/aigc_review_runner.py`

上层策略若阻断顾问与复核流程 或外部 reviewer 调度，允许使用本地 checklist，但必须报告：

- 不可用来源层级
- provider 路径
- 实际采用的本地路径
- 本地 checklist的 reviewer

## Verdict Model

| review_status | meaning |
| --- | --- |
| `FAIL-COVENANT` | fact pack required slice 缺失，不能进入维度审计 |
| `FAIL-BLOCKING` | 存在 critical/high issue，阻断 handoff |
| `PASS-WITH-WARNINGS` | 可放行但需要携带非阻断修复项 |
| `PASS` | 可进入下一阶段、provider handoff 或 release |

## Routing Decision Contract

| routing_decision | 适用条件 |
| --- | --- |
| `back_to_stage_contract` | 问题主要落在当前阶段产物或节点 |
| `back_to_source_contract` | 问题来自上游真源、规划冲突或治理断链 |
| `block_provider_handoff` | provider pack、引用或 continuity 不可信 |
| `handoff_next_stage` | 当前 scope 可放行到唯一下一入口 |
| `hold_for_human_review` | 自动审计无法稳定裁决 |

## Dimension Review Gates

| review_gate | dimension | fail_code | blocking_condition |
| --- | --- | --- | --- |
| `GATE-DIM-DA-01` | `设计对位` | `FAIL-DA-01` | 未锁定同一 fact pack 下的 `10-分组` 与 `11-主体` canonical refs。 |
| `GATE-DIM-DA-02` | `设计对位` | `FAIL-DA-01` | 场景、角色、道具清单或设计脱离分组 truth。 |
| `GATE-DIM-DA-03` | `设计对位` | `FAIL-DA-01` | 设计审美、研究补充或 provider 偏好覆盖 upstream constraint。 |
| `GATE-DIM-DA-04` | `设计对位` | `FAIL-DA-02` | list、design、panel / generation handoff 的主体 ID、路径或 slot bundle 不一致。 |
| `GATE-DIM-DA-05` | `设计对位` | `FAIL-DA-02` | 下游缺少可消费设计包或 handoff readiness 不成立。 |
| `GATE-DIM-DA-06` | `设计对位` | `FAIL-DA-03` | 对位问题未归因到 list、design、panel/generation 或 upstream group。 |
| `GATE-DIM-DA-07` | `设计对位` | `FAIL-DA-03` | 维度 sidecar 越权写最终 route/status 或缺少聚合字段。 |
| `GATE-DIM-DE-01` | `分镜执行连续性` | `FAIL-DE-01` | 未锁定同一 scope 的当前 2-10 阶段真源与 validator evidence。 |
| `GATE-DIM-DE-02` | `分镜执行连续性` | `FAIL-DE-01` | 编剧、美学、导演、表演、氛围、分镜、摄影、光影、分组链路无法逐层追溯或镜头/组编号错位。 |
| `GATE-DIM-DE-03` | `分镜执行连续性` | `FAIL-DE-01` | 组镜连续性断裂、吞 beat、重复镜头、越组外溢或 atomic unit 截断。 |
| `GATE-DIM-DE-04` | `分镜执行连续性` | `FAIL-DE-01` | 时长、对白/动作负载、节奏或 AIGC 视频可执行性不一致。 |
| `GATE-DIM-DE-05` | `分镜执行连续性` | `FAIL-DE-02` | 分组 handoff carrier 不稳定，不能安全交给下游。 |
| `GATE-DIM-DE-06` | `分镜执行连续性` | `FAIL-DE-02` | 分镜链路问题被误归因到 design/image/video provider。 |
| `GATE-DIM-DE-07` | `分镜执行连续性` | `FAIL-DE-03` | 维度 packet 缺少聚合所需 evidence、runtime 或 blocking scope。 |
| `GATE-DIM-GC-01` | `治理闭环` | `FAIL-GC-01` | 未读取当前 scope 的 validation carrier、STATE、governance-state、fact pack 与 source trace。 |
| `GATE-DIM-GC-02` | `治理闭环` | `FAIL-GC-01` | validation report 与当前 mode、stage/checkpoint 或 scope_ref 不对位。 |
| `GATE-DIM-GC-03` | `治理闭环` | `FAIL-GC-01` | STATE、governance-state、fact pack、source trace 或 handoff/rework targets 冲突。 |
| `GATE-DIM-GC-04` | `治理闭环` | `FAIL-GC-02` | route、handoff target、source owner 或 rework target 不唯一、不可执行或循环。 |
| `GATE-DIM-GC-05` | `治理闭环` | `FAIL-GC-02` | source trace 无法解释 blocking finding 的来源层与返工层。 |
| `GATE-DIM-GC-06` | `治理闭环` | `FAIL-GC-02` | provider / downstream handoff 阻断缺少 resume 或 repair bridge。 |
| `GATE-DIM-GC-07` | `治理闭环` | `FAIL-GC-03` | 维度 sidecar 越权写最终 route/status 或直接改业务真源。 |
| `GATE-DIM-PS-01` | `规划与种子兑现` | `FAIL-PS-01` | 未锁定同一 fact pack 下的 MEMORY、分集与编剧 refs。 |
| `GATE-DIM-PS-02` | `规划与种子兑现` | `FAIL-PS-01` | 初始化长期约束或 handoff obligations 在分集阶段丢失或被改写。 |
| `GATE-DIM-PS-03` | `规划与种子兑现` | `FAIL-PS-01` | 分集未把 episode scope、集标、源文范围、保真边界或下游义务稳定交给编剧。 |
| `GATE-DIM-PS-04` | `规划与种子兑现` | `FAIL-PS-02` | 编剧稿未真实消费初始化与分集 seed，形成脱离上游的独立稿。 |
| `GATE-DIM-PS-05` | `规划与种子兑现` | `FAIL-PS-02` | seed 漂移或 obligation 缺口未归因到 `0-初始化`、`1-分集` 或 `2-编剧`。 |
| `GATE-DIM-PS-06` | `规划与种子兑现` | `FAIL-PS-03` | 维度审计越界到构图、设计、图像 provider 或视频 provider。 |
| `GATE-DIM-PS-07` | `规划与种子兑现` | `FAIL-PS-03` | 维度 packet 缺少聚合字段、runtime 或越权写最终 route/status。 |
| `GATE-DIM-ID-01` | `图像交付就绪` | `FAIL-ID-01` | 未锁定同一 fact pack 下的图像请求、故事板、引用绑定与 handoff refs。 |
| `GATE-DIM-ID-02` | `图像交付就绪` | `FAIL-ID-01` | 分镜画面请求对象无法回指分组与设计，frame landing、prompt package 或 reference slots 断链。 |
| `GATE-DIM-ID-03` | `图像交付就绪` | `FAIL-ID-01` | 分镜故事板的 panel/frame units、source span、场景图或主体参照错位。 |
| `GATE-DIM-ID-04` | `图像交付就绪` | `FAIL-ID-01` | 引用绑定把 JSON、缺图说明、pending marker 或不可见路径当成可用图片。 |
| `GATE-DIM-ID-05` | `图像交付就绪` | `FAIL-ID-02` | provider handoff pack 缺 submit plan、brief/prompt package、output root、manifest 或 status。 |
| `GATE-DIM-ID-06` | `图像交付就绪` | `FAIL-ID-03` | 图像交付问题未归因到图像、设计或分组 source owner。 |
| `GATE-DIM-ID-07` | `图像交付就绪` | `FAIL-ID-03` | 维度 sidecar 越权写最终 route/status 或直接修改业务文件。 |
| `GATE-DIM-VD-01` | `视频交付就绪` | `FAIL-VD-01` | 未锁定同一 fact pack 下的 B/C/D 视频路线与 provider handoff refs。 |
| `GATE-DIM-VD-02` | `视频交付就绪` | `FAIL-VD-01` | 故事板参照流的组正文、图片绑定、duration hint 或远端 prompt 边界不稳定。 |
| `GATE-DIM-VD-03` | `视频交付就绪` | `FAIL-VD-01` | 主体参照流的 YAML 主体、slot、reference order、预算或本地路径禁区不可追溯。 |
| `GATE-DIM-VD-04` | `视频交付就绪` | `FAIL-VD-01` | 主板混合参照未同时满足故事板总参照与主体参照绑定，或 slots 与 uploads 错层。 |
| `GATE-DIM-VD-05` | `视频交付就绪` | `FAIL-VD-01` | motion、duration、audio expectation 或 reference continuity 未达到 provider 可执行门槛。 |
| `GATE-DIM-VD-06` | `视频交付就绪` | `FAIL-VD-02` | provider handoff pack 缺官方执行路径、submit plan、brief/final YAML、queue/session 或 output root。 |
| `GATE-DIM-VD-07` | `视频交付就绪` | `FAIL-VD-03` | 视频交付问题未归因到 B/C/D 路线、`14-审片` 或上游图像、设计、分组 owner。 |
| `GATE-DIM-VD-08` | `视频交付就绪` | `FAIL-VD-03` | 维度 sidecar 越权写最终 route/status 或直接修改视频/provider/上游文件。 |

## Parent Contract Review Gates

| review_gate | contract | fail_code | blocking_condition |
| --- | --- | --- | --- |
| `GATE-REVIEW-ROOT-01` | `review-root-contract` | `FAIL-REVIEW-ROOT-SCOPE` | review mode、stage/checkpoint、scope_ref 或 aggregate path 不唯一。 |
| `GATE-REVIEW-ROOT-02` | `review-root-contract` | `FAIL-REVIEW-ROOT-AUTHORITY` | 根裁决字段不由 aggregate 唯一拥有，或维度 sidecar 并列裁决。 |
| `GATE-REVIEW-ROOT-03` | `review-root-contract` | `FAIL-REVIEW-ROOT-BOUNDARY` | review 父层直接改写阶段 canonical 业务真源。 |
| `GATE-REVIEW-ROOT-04` | `review-root-contract` | `FAIL-REVIEW-ROOT-PATH` | aggregate、fact pack、repair、summary 或 provider artifacts 路径不对位。 |
| `GATE-REVIEW-ROOT-05` | `review-root-contract` | `FAIL-REVIEW-ROOT-AGGREGATION` | aggregate 缺少 selected dimensions、runtime、scores、issues 或 severity 聚合字段。 |
| `GATE-REVIEW-ROOT-06` | `review-root-contract` | `FAIL-REVIEW-ROOT-ROUTE` | 上游 source truth 问题未返回 `back_to_source_contract` 或缺 source owner。 |
| `GATE-REVIEW-ROOT-07` | `review-root-contract` | `FAIL-REVIEW-ROOT-ROUTE` | provider handoff 阻断缺可执行 repair route 或恢复条件。 |
| `GATE-REVIEW-ROOT-08` | `review-root-contract` | `FAIL-REVIEW-ROOT-ROUTE` | PASS/PASS-WITH-WARNINGS 缺唯一下一入口或出现循环/互斥 handoff。 |
| `GATE-REVIEW-ROOT-09` | `review-root-contract` | `FAIL-REVIEW-ROOT-REPORT` | review summary 与 aggregate 冲突或替代 JSON gate truth。 |
| `GATE-REVIEW-FACT-01` | `review-fact-pack-spec` | `FAIL-REVIEW-FACT-MINIMUM` | fact pack 最小字段缺失或 scope 与 aggregate 不对位。 |
| `GATE-REVIEW-FACT-02` | `review-fact-pack-spec` | `FAIL-REVIEW-FACT-SLICE` | checkpoint_inline required slice 不完整。 |
| `GATE-REVIEW-FACT-03` | `review-fact-pack-spec` | `FAIL-REVIEW-FACT-SLICE` | stage_acceptance required slice 不完整。 |
| `GATE-REVIEW-FACT-04` | `review-fact-pack-spec` | `FAIL-REVIEW-FACT-SLICE` | package_release required slice 不完整。 |
| `GATE-REVIEW-FACT-05` | `review-fact-pack-spec` | `FAIL-REVIEW-COVENANT` | mandatory dimensions 未消费同一份 fact pack。 |
| `GATE-REVIEW-FACT-06` | `review-fact-pack-spec` | `FAIL-REVIEW-COVENANT` | required slice 缺失时仍进入 provider 或 dimension review。 |
| `GATE-REVIEW-FACT-07` | `review-fact-pack-spec` | `FAIL-REVIEW-FACT-AUTHORITY` | fact pack 被当成第二业务真源。 |
| `GATE-REVIEW-FACT-08` | `review-fact-pack-spec` | `FAIL-REVIEW-FACT-PROVIDER-SCOPE` | provider 或本地 checklist 越权读取未登记文件、旧路径或缓存。 |
| `GATE-REVIEW-FACT-09` | `review-fact-pack-spec` | `FAIL-REVIEW-FACT-LINKAGE` | fact pack、aggregate、dimension reports 或 repair sidecar 缺 scope/path 回指。 |
| `GATE-REVIEW-CHILD-01` | `review-child-output-contract` | `FAIL-REVIEW-CHILD-SHAPE` | 维度 reviewer 未按 `dimension_packet + dimension_report_ref` 输出。 |
| `GATE-REVIEW-CHILD-02` | `review-child-output-contract` | `FAIL-REVIEW-CHILD-MINIMUM` | dimension packet 最小字段缺失。 |
| `GATE-REVIEW-CHILD-03` | `review-child-output-contract` | `FAIL-REVIEW-CHILD-AUTHORITY` | 维度 reviewer 独立写 root verdict、route 或 handoff 字段。 |
| `GATE-REVIEW-CHILD-04` | `review-child-output-contract` | `FAIL-REVIEW-CHILD-SOURCE` | source truth 冲突缺 source owner、evidence 或返工目标。 |
| `GATE-REVIEW-CHILD-05` | `review-child-output-contract` | `FAIL-REVIEW-CHILD-REPORT` | dimension report 未落在 aggregate 同级目录或无法被引用。 |
| `GATE-REVIEW-CHILD-06` | `review-child-output-contract` | `FAIL-REVIEW-CHILD-RUNTIME` | 本地 checklist 降级缺 execution mode、spec refs 或 provider 不可用原因。 |
| `GATE-REVIEW-CHILD-07` | `review-child-output-contract` | `FAIL-REVIEW-CHILD-AGGREGATION` | 维度输出不可被父层计算 scores、severity、critical issues 或 blocking scope。 |
| `GATE-REVIEW-CHILD-08` | `review-child-output-contract` | `FAIL-REVIEW-CHILD-AUTHORITY` | 最终 route 未由父层 aggregate 统一裁决。 |

## Covenant Early Exit

- `review_fact_pack.missing_required_refs` 非空时，runner 必须直接写 `FAIL-COVENANT`。
- 早停时不得调用 `code-reviewer`，不得生成维度 sidecar，避免把证据缺口误包装成维度审查结论。
- 早停仍必须写 aggregate packet、repair sidecar 与 review summary。
