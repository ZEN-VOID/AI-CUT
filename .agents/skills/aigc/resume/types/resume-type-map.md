# Resume Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


本文件集中管理 `$aigc-resume` 的类型变量、恢复模式矩阵和风险策略。steps 消费这里形成的 `resume_type_profile`，不在 steps 内重复维护完整类型表。

## Type Profile Variables

| variable | allowed values | meaning |
| --- | --- | --- |
| `intent_type` | `continue`, `checkpoint_rebuild`, `governance_repair`, `gate_reentry`, `review_repair`, `rebootstrap`, `query`, `review` | 用户请求本质 |
| `state_depth` | `none`, `lightweight`, `structured` | 状态证据深度 |
| `artifact_depth` | `none`, `init_core`, `stage_outputs`, `multi_stage_outputs` | 产物证据深度 |
| `risk_level` | `low`, `medium`, `high`, `destructive` | 继续执行风险等级 |
| `runtime_profile` | `current_chinese`, `legacy_english`, `mixed`, `unknown` | 项目路径口径 |
| `gate_status` | `not_needed`, `present_pass`, `present_blocked`, `missing_required`, `unknown` | 治理 gate 状态 |
| `route_profile` | `unique`, `ambiguous`, `blocked` | 下一入口可裁决性 |
| `review_bridge_state` | `absent`, `present`, `stale`, `ambiguous` | review bridge / repair route 状态 |
| `shelved_stage_signal` | `none`, `legacy_7_cut`, `unsupported_stage` | 是否命中搁浅或未开放阶段 |

## Mode Mapping

| signals | resume mode | step impact | review impact |
| --- | --- | --- | --- |
| `intent_type=rebootstrap` | `init_rebootstrap_reroute` | 立即回 `0-初始化` | 检查未误用续跑 |
| `state_depth=lightweight` + `artifact_depth=init_core` + `risk_level=low` | `lightweight_init_continue` | 允许低风险下一入口 | 不要求先补 `governance-state.yaml` |
| `state_depth=none` 或 init core 缺失 | `governance_rebuild` | 回根或初始化补状态 | 阻断高风险继续 |
| `artifact_depth=stage_outputs` + `route_profile=unique` + `gate_status!=missing_required` | `stage_continue` | 回目标阶段 | 检查阶段产物非空 |
| `gate_status=missing_required` 或 `present_blocked` | `gate_reentry` | 回根 gate 或 review | 标注 blocker |
| `intent_type=review_repair` 或 `review_bridge_state=present` | `review_repair_reentry` | 消费 repair route | 不发明 repair 内容 |
| `runtime_profile=mixed` 或 `route_profile=ambiguous` | `root_reroute` | 回根重新判型 | 输出 drift reason |
| `shelved_stage_signal=legacy_7_cut` | `root_reroute` 或 `blocked_safety_stop` | 报告后期/剪辑阶段搁浅，不直接续跑 | 输出 shelved reason |
| `risk_level=destructive` | `blocked_safety_stop` | 禁止默认执行 | 输出安全替代检查 |

## Risk Levels

| risk_level | examples | required gate |
| --- | --- | --- |
| `low` | 只读查询、确认下一入口、读取状态 | 项目根唯一 |
| `medium` | 补非破坏性治理工件、继续单阶段草稿 | 状态 + 产物双证据 |
| `high` | 进入批量生成、跨阶段推进、覆盖已有阶段产物 | `mission-brief.yaml`、`route-plan.yaml`、必要时 `preflight-verdict.yaml` |
| `destructive` | 删除源文本、清空资产、Git hard reset | 显式用户授权且通常不由 resume 执行 |

## Runtime Profile Mapping

| runtime_profile | signal | action |
| --- | --- | --- |
| `current_chinese` | 存在 `0-初始化`、`1-分集`、`2-编导`、`5-设计` 等新版目录 | 按新版口径继续 |
| `legacy_english` | 只存在 `0-Init`、`1-Planning`、`5-Image` 等旧目录 | 报告 legacy 输入，回根决定迁移或兼容 |
| `mixed` | 中英文目录并存、`4-设计/5-设计` 并存且状态工件不一致 | `root_reroute` 或 `governance_rebuild` |
| `unknown` | 无法证明项目根或阶段布局 | block 并请求项目路径 |

## Type Profile Output

```yaml
resume_type_profile:
  intent_type: ""
  state_depth: ""
  artifact_depth: ""
  risk_level: ""
  runtime_profile: ""
  gate_status: ""
  route_profile: ""
  review_bridge_state: ""
  shelved_stage_signal: ""
  resume_mode: ""
  unique_next_entry: ""
  blockers: []
```
