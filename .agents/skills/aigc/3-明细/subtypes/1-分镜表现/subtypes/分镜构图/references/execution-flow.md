# aigc 3-明细 / 1-分镜表现 / 分镜构图 / Execution Flow

本文件承载 `分镜构图` 叶子的统一写位、sidecar 与返回 patch 规则。

## Canonical Landing

- 统一根文件：`projects/<项目名>/编导/第N集.json`
- sidecar 输出：`projects/<项目名>/编导/evidence/1-分镜表现/构图方案-第N集.md`
- 返回责任：为父级 `1-分镜表现` 生成逐镜静态构图方案与 `分镜表现` patch 草案
- 本叶子未被调度时不得写占位，不得参与聚合

## Upstream Consumption Contract

1. `panel_count / refined_range / template_id / candidate_counts / decision_reason / aesthetic_peak_plan / single_panel_long_take_evidence` 的真源固定在上游 `分镜密度`。
2. 本层先消费上游镜数裁决，再把它落成逐镜构图；不得复制出第二套镜数真源。
3. 若连续两轮仍无法满足模板级门槛，只允许申请父级回退上游裁决，不得静默硬过。

## Duration Read Chain (Mandatory)

1. 每个分镜组默认总时长为 `15秒`，可被 episode meta 的 `默认组时长` 覆盖。
2. 非均匀组时长必须由 `分镜组时长映射` 显式登记偏离项。
3. 本层与 validator 固定按以下顺序读取组总时长：
   - `分镜组时长映射`
   - `默认组时长`
   - `切分时长策略`
4. 本层只做帧级切分，不重新定义组总时长真源。

## Workflow

1. 完整读取 `projects/<项目名>/编导/第N集.json`，并继承上游 `分镜密度` sidecar 的镜数裁决。
2. 先确认父级 `1-分镜表现` 已将本叶子纳入本轮 `selected_subskills[]`；若未命中，立即停止。
3. 锁定当前分镜组总时长、场景类型与组内节奏，逐镜补全静态构图字段与时间切分。
4. 以 `template_id` 为门槛检查当前设计是否满足景别、角度、层次与峰值镜要求。
5. 将结果写入 sidecar，并返回给父级 `1-分镜表现` 的 `分镜表现` patch 草案。
6. 本叶子不直接创建第二份 shot 主文件；统一根文件的正式写回由父技能聚合执行。

## Hard Gates

1. 第一个分镜必须从组起始时间起笔，最后一个分镜必须覆盖到组总时长结束。
2. 相邻分镜时间必须连续无间隙；否则触发 `FAIL-TIME-CONTINUITY`。
3. 全部分镜时长之和必须等于组总时长；否则触发 `FAIL-TIME-OVERFLOW`。
4. 若全组构图均为安全常规构图、未形成至少一帧构图审美峰值，触发 `FAIL-ANTI-MEDIOCRITY`。
5. 若同集序列重复率过高，触发 `FAIL-SEQUENCE-COLLAPSE`。

## Council Runtime Inheritance (Mandatory)

`分镜构图` 不单独定义顾问团运行时，而是强制继承 `3-明细` 根技能与 `1-分镜表现` 父技能的顾问团合同。

执行规则：

1. 直接进入本叶子技能时，仍必须先读取 `projects/<项目名>/team.yaml` 与 `.agents/skills/aigc/_shared/council-runtime/module-spec.md`。
2. 若顾问团启用，则由 `监制` 先对静态镜头字段、构图一致性与可执行性提供前置建议。
3. 阶段级 `projects/<项目名>/编导/validation-report.md` 前后若命中 `评审`，仍按 `3-明细` 根技能的闸门执行。
4. 本叶子技能不夺取主代理的统一根文件写回权。
