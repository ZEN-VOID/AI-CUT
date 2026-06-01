# CHANGELOG

## 2026-06-01

- 收束字段落点规则：`3-运动` 不再新增独立 `运动强化：` 字段，改为在原有 `画面`、`动作`、`表演`、`调度` 等运动承载字段内原位扩写。
- 接入初始化冻结综合消费：项目任务读取 `team.yaml.init_synthesis.stage_seed_summary."3-运动"`、`init_handoff.motion_seed` 与 `north_star.yaml.创作阶段不变量.运动`，压缩为 `init_team_synthesis_context`。
- 明确 `3-运动` 不调用 team 身份、不解析旧 stage profile、不补造创作阶段顾问问答；初始化综合只影响动作连续性、起点/路径/终点和参照帧约束。
- 同步 SKILL、workflow、review、模板、README 和 `agents/openai.yaml`。

## 2026-05-31

- 初始化 `3-运动` Skill 2.0 包。
- 建立运动五要素、上一画面状态回顾、source 保真和 `motion_state_ledger` 审查合同。
- 新增输出模板、review gate、guardrails、类型包和机械校验脚本。
- 强化参照系规则：同一场景或连续动作段尽量统一 `primary_reference_frame`，新增最佳参照系识别机制、`group_reference_profile` 报告证据和对应 review gate。
- 修正阶段边界：`3-运动` 默认按同一场景或连续动作段统一参照系；仅当输入源显式已有分镜组或 group_id 时继承源内组边界，不在本阶段生成下游分镜组。
