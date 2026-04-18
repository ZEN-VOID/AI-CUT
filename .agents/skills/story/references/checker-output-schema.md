# story2026 校验输出与聚合 Schema

本文件是 `4-Validation -> review -> 3-Drafting Step 4` 的统一字段合同。

分三层：

1. 单个 checker 的结构化输出
2. `4-Validation` 的阶段聚合输出
3. `review_metrics` 的正式落库字段

说明：

- 单章场景默认使用 `chapter`。
- 区间审查可在聚合层补 `start_chapter/end_chapter`，单个 checker 不强制。
- 允许扩展字段，但不得删除本文件定义的强制字段，也不得用私有字段替代强制字段。
- checker 白名单与职责边界不在本文件定义，统一回指 `validation-team-contract.md`。

## 1. Checker Output

```json
{
  "agent": "consistency-checker",
  "chapter": 100,
  "overall_score": 85,
  "pass": true,
  "issues": [
    {
      "id": "ISSUE_001",
      "type": "设定一致性",
      "severity": "critical|high|medium|low",
      "location": "第100章，第3段",
      "description": "问题描述",
      "suggestion": "修复建议",
      "can_override": false
    }
  ],
  "metrics": {},
  "summary": "简短总结"
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `agent` | string | ✅ | checker id |
| `chapter` | int | ✅ | 章节号 |
| `overall_score` | int | ✅ | 0-100 |
| `pass` | bool | ✅ | 此 checker 是否通过 |
| `issues` | array | ✅ | 标准问题列表 |
| `metrics` | object | ✅ | checker 专属指标 |
| `summary` | string | ✅ | 面向聚合层的摘要 |

扩展字段约定：

- 可追加 checker 私有字段，如 `hard_violations`、`override_eligible`。
- 私有字段仅增强解释，不得绕过 `issues`。

## 2. Validation Aggregate Output

`4-Validation` 聚合后，至少产出：

```json
{
  "validation_status": "PASS|FAIL-QUALITY|FAIL-COVENANT|FAIL-RUNTIME",
  "validation_mode": "normal_review|historical_recheck",
  "selected_agents": [
    "context-agent",
    "consistency-checker",
    "continuity-checker",
    "ooc-checker",
    "immersion-voice-checker"
  ],
  "issues": [],
  "severity_counts": {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 0
  },
  "critical_issues": [],
  "overall_score": 84.5,
  "dimension_scores": {
    "consistency": 8.8,
    "continuity": 8.5,
    "character": 8.1,
    "immersion": 7.9,
    "reader_pull": 8.7
  },
  "anti_ai_force_check": "pending|pass|fail",
  "spoiler_risk": "low|medium|high|critical",
  "contrivance_risk": "low|medium|high|critical",
  "cold_commentary_risk": "low|medium|high|critical",
  "routing_decision": "back_to_drafting_step_4|handoff_to_review_and_loopback|handoff_to_loopback_support",
  "handoff_targets": [
    "review/",
    "5-Loopback"
  ]
}
```

强约束：

- `issues / severity_counts / critical_issues` 必须能回溯到具体 checker。
- `anti_ai_force_check / spoiler_risk / contrivance_risk / cold_commentary_risk` 是一等字段，不得藏入 `notes`。
- `PASS` 才能把 `handoff_targets` 指向 `review/` 与 `5-Loopback` 的主 actualization 流程。

## 3. review_metrics Sink

`review/` 正式落库时，至少保留这些字段：

```json
{
  "start_chapter": 100,
  "end_chapter": 100,
  "overall_score": 84.5,
  "dimension_scores": {},
  "anti_ai_force_check": "pending",
  "spoiler_risk": "low",
  "contrivance_risk": "medium",
  "cold_commentary_risk": "low",
  "severity_counts": {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 0
  },
  "critical_issues": [],
  "report_file": "Validation/第100-100章审查报告.md",
  "notes": "selected_agents / validation_mode / routing_decision 等压缩为单行补充说明"
}
```

## 问题严重度定义

| severity | 含义 | 处理方式 |
|---|---|---|
| `critical` | 严重问题，必须修复 | 阻断进入 actualization |
| `high` | 高优先级问题 | 优先修复 |
| `medium` | 中等问题 | 建议修复 |
| `low` | 轻微问题 | 可选优化 |

## 常用 Checker metrics

### `reader-pull-checker`

```json
{
  "metrics": {
    "hook_present": true,
    "hook_type": "危机钩",
    "hook_strength": "strong",
    "prev_hook_fulfilled": true,
    "micropayoff_count": 2,
    "micropayoffs": ["能力兑现", "认可兑现"],
    "is_transition": false,
    "debt_balance": 0.0
  }
}
```

### `high-point-checker`

```json
{
  "metrics": {
    "cool_point_count": 2,
    "cool_point_types": ["装逼打脸", "越级反杀"],
    "density_score": 8,
    "type_diversity": 0.8,
    "milestone_present": false
  }
}
```

### `consistency-checker`

```json
{
  "metrics": {
    "power_violations": 0,
    "location_errors": 1,
    "timeline_issues": 0,
    "entity_conflicts": 0
  }
}
```

### `ooc-checker`

```json
{
  "metrics": {
    "severe_ooc": 0,
    "moderate_ooc": 1,
    "minor_ooc": 2,
    "speech_violations": 0,
    "character_development_valid": true
  }
}
```

### `continuity-checker`

```json
{
  "metrics": {
    "transition_grade": "B",
    "active_threads": 3,
    "dormant_threads": 1,
    "forgotten_foreshadowing": 0,
    "logic_holes": 0,
    "outline_deviations": 0
  }
}
```

### `pacing-checker`

```json
{
  "metrics": {
    "dominant_strand": "quest",
    "quest_ratio": 0.6,
    "fire_ratio": 0.25,
    "constellation_ratio": 0.15,
    "consecutive_quest": 3,
    "fire_gap": 4,
    "constellation_gap": 8,
    "fatigue_risk": "low"
  }
}
```

### `spoiler-checker`

```json
{
  "metrics": {
    "active_foreshadowing_count": 4,
    "silence_window_breaks": 1,
    "premature_solution_hits": 0,
    "straightforward_hint_hits": 2,
    "spoiler_risk": "medium"
  }
}
```

### `immersion-voice-checker`

```json
{
  "metrics": {
    "commentary_tone_hits": 1,
    "manual_dialogue_exposition_hits": 2,
    "abstract_commentary_hits": 1,
    "detached_narration_hits": 0,
    "anti_ai_force_check": "fail",
    "contrivance_risk": "medium",
    "cold_commentary_risk": "high"
  }
}
```

## 版本说明

- 当前根级 schema 已与 `4-Validation/SKILL.md`、`review/SKILL.md`、`3-Drafting/step-3-review-gate/appendix-review-gate.md` 对齐。
- 若后续新增 checker 或风险字段，必须同步更新本文件与对应持久化 schema。
