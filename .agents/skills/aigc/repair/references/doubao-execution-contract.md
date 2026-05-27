# Doubao Execution Contract

本文件定义 `aigc-repair` 调用 `.agents/skills/api/anyfast/llm/doubao-seed-2.0-pro/` 的执行边界。

## Provider Role

`doubao-seed-2.0-pro` 是本技能的默认执行大模型，用于：

- 高推理中文分析和任务拆解。
- 多阶段 repair plan、影响图、source owner 推断和写回顺序建议。
- 更友好的中文润色、影视执行表达优化和自然中文气口处理。
- 在不破坏源层规则的前提下提供创意候选、镜头/表演/设计增强方向和主题联想。

## Local Chinese Rationale

本技能把豆包放在执行 lane 的重点原因，不只是“换一个模型调用”：

- 当前主模型优先承担结构化工程能力：读规则、拆任务、定位 owner、控制写回顺序、维护审计证据。
- 豆包优先承担中文表达能力：更自然的中文语序、更贴近短剧/影视语境的口吻、更顺滑的用户-facing 报告、更少翻译腔和模板腔。
- 豆包优先承担本土文化语境下的创意激发：人物关系、社会语境、职场/家庭/江湖/短剧叙事、情绪张力和生活细节候选。
- 该优势必须被工程化约束：不能把“更有本土味”扩张成改事实、改对白、改角色设定、改镜头编号或绕过 owning stage。
- 当任务同时包含结构化修复与中文创作表达时，默认分工是 `当前模型整理上下文与门禁 -> 豆包生成分析/润色/候选 -> 当前模型按源层规则验收和写回`。

它不拥有：

- 根 `aigc` 路由裁决权。
- owning stage 的 canonical truth。
- 图像/视频生成结果真源。
- 未经 review gate 的自动写回权。

## Orchestration Rule

1. 当前模型先加载 `$aigc-repair`、目标 owning skill、项目 `MEMORY.md` / `CONTEXT/` 和相关源层规则。
2. 当前模型整理出 `doubao_task_packet`，不得把杂乱上下文原样倾倒给 provider。
3. 调用 `.agents/skills/api/anyfast/llm/doubao-seed-2.0-pro/scripts/doubao_seed_chat.py`，优先使用结构化 `messages` 或清晰 `system + prompt`。
4. 豆包输出只能作为 `provider_suggestion`、`provider_draft` 或 `provider_analysis`，必须经过 owning stage 和本技能 review gate 才能写回 canonical 文件。
5. 若 provider 调用失败，标记 `provider_status: degraded`，允许输出 plan 或当前模型草案，但不得宣称豆包已执行。

## Task Packet Shape

```yaml
doubao_task_packet:
  task_id: ""
  mode: impact_assessment | repair_plan | execute_repair | polish_and_inspire | asset_repair_route | audit_only
  project_root: "projects/aigc/<项目名>/"
  target_locality:
    path: ""
    stage: ""
    leaf: ""
    object_id: ""
  source_rules_reviewed:
    - skill_path: ""
      rule_summary: ""
  change_intent: ""
  fixed_facts:
    - ""
  forbidden_changes:
    - ""
  requested_output:
    format: markdown | patch_plan | replacement_block | candidate_set
    language: zh-CN
  acceptance_gate:
    - ""
```

## Chinese Polish Rules

- 优化中文顺序、语气、可读性、镜头执行感、动作清晰度和术语自然度。
- 消除翻译腔、模板腔和生硬工程腔，让表达更贴合中文影视制作、短剧叙事和用户沟通语境。
- 保留剧情事实、对白、字段名、编号、路径、YAML、分镜 ID、资产 ID 和引用关系。
- 不把抽象文采替代阶段合同要求；影视阶段优先可拍、可演、可生成、可审查。
- 对用户-facing 报告使用清晰中文，避免模板腔、空泛口号和过度术语堆叠。

## Creative Inspiration Rules

- 创意激发必须绑定源层目标：表演、镜头、场景、角色、道具、图像 prompt、视频运动或审片修复。
- 创意候选应体现中文本土语境中的人物关系、场景生活感、情绪张力和类型片/短剧可消费性，但不得使用不可验证的“训练语料来源”作为事实依据。
- 输出候选必须标明 `can_apply_now`、`needs_user_choice` 或 `stage_owner_required`。
- 不使用“训练集中相关主题”作为不可验证事实来源；只能把它作为广义题材联想和表达发散，最终仍受项目资料、源层合同和用户禁区约束。
- 创意候选不得自动覆盖 canonical truth；需要写回时走 `execute_repair` 和 review gate。

## Provider Evidence

正式执行应保存：

- 豆包文本输出 sidecar。
- `doubao_seed_report_*.json`。
- 最终 repair report 中的 `provider_evidence` 路径或降级原因。

若输出只来自当前模型，必须写：

```yaml
provider_evidence:
  provider: doubao-seed-2.0-pro
  status: degraded
  reason: ""
  fallback: current-model-local-plan
```

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否把 `doubao-seed-2.0-pro` 识别为中文分析、润色、创意候选的默认执行 lane，而不是可静默替换的普通 provider？ | `PASS-REPAIR-04` | `FAIL-AIGC-REPAIR-DOUBAO` | `N6-DOUBAO-LANE` | `doubao_task_packet.provider`、mode 选择、provider 或降级状态 |
| 当前模型是否先完成 repair 技能、owning stage、项目 `MEMORY.md` / `CONTEXT/` 与相关源层规则加载，再整理豆包输入？ | `PASS-REPAIR-02` | `FAIL-AIGC-REPAIR-SOURCE-RULE` | `N2-SOURCE-RULE-REVIEW` | `source_rules_reviewed` 中的 skill/context/reference/step/type/review 记录 |
| `doubao_task_packet` 是否结构化包含目标、固定事实、禁止改动、输出格式、语言和 acceptance gate，而不是把杂乱上下文原样倾倒给 provider？ | `PASS-REPAIR-04` | `FAIL-AIGC-REPAIR-DOUBAO` | `N6-DOUBAO-LANE` | 完整 `doubao_task_packet`、`forbidden_changes`、`acceptance_gate` |
| 豆包输出是否只作为 `provider_suggestion` / `provider_draft` / `provider_analysis`，写回前仍经过 owning stage 与 repair review gate？ | `PASS-REPAIR-05` | `FAIL-AIGC-REPAIR-REVIEW` | `N9-REVIEW-GATE` | provider output 分类、review verdict、写回前的 owner gate 记录 |
| provider 调用失败时，是否显式记录 `provider_status: degraded` 与 `fallback: current-model-local-plan`，且没有宣称豆包已执行？ | `PASS-REPAIR-04` | `FAIL-AIGC-REPAIR-DOUBAO` | `N6-DOUBAO-LANE` | `provider_evidence.status: degraded`、失败原因、fallback 范围 |
| 中文润色是否只优化语序、语气、可读性和执行感，未改剧情事实、对白、编号、字段、YAML、分镜 ID、资产 ID 或引用关系？ | `PASS-REPAIR-05` | `FAIL-AIGC-REPAIR-REVIEW` | `N9-REVIEW-GATE` | before/after diff、固定事实核对、字段/编号/引用一致性检查 |
| 创意激发是否绑定源层目标和用户禁区，并明确 `can_apply_now` / `needs_user_choice` / `stage_owner_required`，而非自动成为 canonical truth？ | `PASS-REPAIR-04` | `FAIL-AIGC-REPAIR-DOUBAO` | `N6-DOUBAO-LANE` | 候选状态字段、source target 映射、需要用户或 stage owner 吸收的标记 |
| 是否保存豆包文本 sidecar、`doubao_seed_report_*.json` 或在最终 repair report 中给出 provider evidence / 降级原因？ | `PASS-REPAIR-04` | `FAIL-AIGC-REPAIR-DOUBAO` | `N6-DOUBAO-LANE` | sidecar/report 路径、provider evidence 摘要、缺失时的 blocker |
