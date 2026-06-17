# Volume-Level Quality Audit Contract

本文件是 `story2026` 的卷级质量审计合同。它在卷内所有章通过终稿验收后，从卷级视角审计整体质量，防止"每章验收 PASS 但整卷节奏崩塌"。

本文件不拥有正文写权，不是独立阶段。审计由 `4-润色` 在卷级验收聚合时自动执行，审计结果写入 `volume.acceptance.json`。

## Core Principle

章级验收保证"这一章没有问题"，卷级审计保证"这些章放在一起没有问题"。卷级审计关注的是章与章之间的关系——关系质量无法从单章验收中推导。

## Volume-Level Audit Dimensions

### 1. `character_arc_integrity`（卷内人物弧线完整性）

检查卷内每个核心人物的成长轨迹是否完整、连贯：

| 检查项 | 评估标准 | 量化锚点 |
|--------|----------|----------|
| 出场密度 | 核心人物在卷内出场章数 ≥ 该人物上线卷内章节数的 60% | ≥60%=5分, 40-60%=3分, <40%=0分 |
| 状态变化 | 人物经历 ≥1 次可识别的状态变化（能力、关系、认知、立场、信念） | ≥2次=7分, 1次=5分, 0次=0分 |
| 变化节奏 | 人物变化是否有递进逻辑（非跳跃、非反复） | 递进=7分, 勉强=3分, 反复/跳跃=0分 |
| 配角功能 | 配角出场是否都服务于核心冲突、信息揭示或主角弧线 | 100%有功能=7分, 有闲置配角=3分, 多闲置=0分 |
| 人物声口一致 | 同一人物在卷内的对白风格、思维模式是否一致 | 一致=5分, 有小的不一致=3分, 明显矛盾=0分 |

失败码：`FAIL-VOL-CHARACTER-ARC`

### 2. `rhythm_waveform_integrity`（卷级节奏波形完整性）

检查整卷的章间节奏是否形成有效波形：

| 检查项 | 评估标准 | 量化锚点 |
|--------|----------|----------|
| 强度分布 | `rhythm_intensity` 分布是否合理（低:中:高 ≈ 2:5:3 或合理的叙事节奏分布） | 合理=5分, 偏平=3分, 极端=0分 |
| 波形连续性 | 相邻章 `previous_next_contrast` 是否形成有意义的承接/对比 | 全部有意义=7分, 有断裂=3分, 多断裂=0分 |
| 高潮累积 | 卷级高潮章（标记为"卷内高潮"的章）之前是否有足够的蓄势积累 | 充分=7分, 不足=3分, 无蓄势=0分 |
| 过渡章质量 | 低强度过渡章是否有微兑现（不能空转） | 全部有兑现=5分, 有空转=3分, 多空转=0分 |
| 尾钩链 | 全卷章末钩子是否形成连续牵引链（每章钩子都被下一章承接） | 连贯=7分, 有断链=3分, 多断链=0分 |
| 模式丰富度 | 卷内使用的 `selected_mode` 是否覆盖 ≥2 种（非全同构） | ≥2种=5分, 全同构=0分 |

失败码：`FAIL-VOL-RHYTHM-WAVEFORM`

### 3. `payoff_density_distribution`（卷级爽点密度分布）

检查卷内爽点的分布是否均衡、递进：

| 检查项 | 评估标准 | 量化锚点 |
|--------|----------|----------|
| 密度趋势 | 卷内爽点密度是否呈逐步上升趋势（前1/3卷蓄势，后1/3卷释放） | 上升=7分, 波动=3分, 下降=0分 |
| 类型多样性 | 卷内 `payoff_type` 是否覆盖 ≥3 种（认知/行动/情绪/关系/世界感/软线索/状态修复） | ≥3种=5分, 1-2种=3分, 1种=0分 |
| 连续高点警示 | 是否有连续 ≥3 章 `rhythm_intensity=高` | 无=pass, 有=FAIL |
| 空转警示 | 是否有 ≥2 章低强度章无任何微兑现 | 无=pass, 有=FAIL |
| 卷级大爽点 | 卷末或卷内至少有一个被标记为"卷级大爽点"的 payoff | 有=5分, 无=0分 |

失败码：`FAIL-VOL-PAYOFF-DENSITY`

### 4. `strand_convergence`（卷级 Strand 三条线收敛）

检查主线、感情线、世界观线在本卷的推进情况：

| 检查项 | 评估标准 | 量化锚点 |
|--------|----------|----------|
| 主线推进 | 主线任务在本卷是否有实质推进（非原地踏步） | 有推进=5分, 微推进=3分, 停滞=0分 |
| 感情线活跃 | 感情线在本卷是否被触及（含暗流、微妙变化） | 触及=5分, 未触及=0分 |
| 世界观展开 | 世界观线在本卷是否有新揭示/新地点/新规则 | 有新=5分, 有重复=3分, 无=0分 |
| 三线交织 | 多条线是否有在同一章/场景中交汇的时刻 | ≥2处交融=7分, 1处=3分, 无=0分 |
| Strand 平衡 | 按 `_shared/strand-weave-pattern.md` 中的缺席规则，主线缺席 ≤5章，感情线缺席 ≤10章，世界观线缺席 ≤15章 | 全部不超标=pass, 有超标=FAIL |

失败码：`FAIL-VOL-STRAND-CONVERGENCE`

### 5. `volume_internal_consistency`（卷内自洽性）

检查卷内是否有明显的自相矛盾：

| 检查项 | 评估标准 | 量化锚点 |
|--------|----------|----------|
| 时间线自洽 | 卷内各章时间推进是否前后一致（无时光回溯） | 一致=5分, 有小偏差=3分, 明显矛盾=0分 |
| 人物状态连贯 | 同卷内人物状态变化是否连续（无跳跃回退） | 连贯=5分, 有小断裂=3分, 明显矛盾=0分 |
| 物件连贯 | 关键物件在本卷的出现、使用、流转是否合理 | 合理=5分, 有小问题=3分, 丢失/矛盾=0分 |
| 地理/场景自洽 | 同卷内场景位置关系是否自洽（人物位移不瞬移） | 自洽=5分, 有小偏差=3分, 瞬移=0分 |

失败码：`FAIL-VOL-CONSISTENCY`

### 6. `reader_journey_quality`（卷级读者旅程质量）

从读者整体体验角度评估本卷：

| 检查项 | 评估标准 | 量化锚点 |
|--------|----------|----------|
| 入卷牵引 | 本卷第一章是否有效承接上卷尾钩 | 承接自然=5分, 勉强=3分, 断裂=0分 |
| 出卷牵引 | 本卷最后一章是否有效设置进入下一卷的牵引 | 牵引强=5分, 有牵引=3分, 无=0分 |
| 阅读疲劳风险 | 连续高强度章(≥3章 rhythm_intensity=高)或连续低强度(≥3章无实质推进) | 无=pass, 有=FAIL |
| 读者情绪曲线 | 卷内读者情绪是否有起有伏（非单向单调） | 有起伏=5分, 基本单向=3分, 扁平=0分 |
| 卷级记忆点 | 卷内是否有 ≥2 个高记忆场景（可在卷尾回忆时自然想起） | ≥2=5分, 1个=3分, 无=0分 |

失败码：`FAIL-VOL-READER-JOURNEY`

## Audit Execution Rules

### Trigger Conditions

卷级质量审计在以下条件下自动触发：
1. 卷内所有章的终稿验收已通过（`volume.acceptance.json` 的 `aggregation_status == complete`）
2. 跨卷连续性追踪数据已更新（`cross-volume-tracker.json` 已写入）

### Audit Output

审计结果写入 `projects/story/<项目名>/4-润色/第V卷/volume.acceptance.json` 的 `volume_quality_audit` 字段：

```json
{
  "volume_quality_audit": {
    "audit_status": "PASS | PASS_WITH_WARNINGS | NEEDS_REWORK",
    "audit_timestamp": "ISO 8601",
    "dimension_results": {
      "character_arc_integrity": {"score": 0-10, "verdict": "PASS | WARN | FAIL", "issues": []},
      "rhythm_waveform_integrity": {"score": 0-10, "verdict": "PASS | WARN | FAIL", "issues": []},
      "payoff_density_distribution": {"score": 0-10, "verdict": "PASS | WARN | FAIL", "issues": []},
      "strand_convergence": {"score": 0-10, "verdict": "PASS | WARN | FAIL", "issues": []},
      "volume_internal_consistency": {"score": 0-10, "verdict": "PASS | WARN | FAIL", "issues": []},
      "reader_journey_quality": {"score": 0-10, "verdict": "PASS | WARN | FAIL", "issues": []}
    },
    "volume_scores": {
      "overall": 0-10,
      "scores_by_dimension": {}
    },
    "warnings": [],
    "failures": [],
    "rework_recommendations": [],
    "audit_evidence_refs": []
  }
}
```

### Verdict Rules

| audit_status | 条件 |
|-------------|------|
| `PASS` | 所有维度 verdict 为 PASS，无 FAIL 维度 |
| `PASS_WITH_WARNINGS` | ≥1 个维度 WARN，但无 FAIL；卷级 pass 但标注预警 |
| `NEEDS_REWORK` | ≥1 个维度 FAIL；阻断 return，返回到有问题的章进行修复 |

### Rework Routing

当 `NEEDS_REWORK` 时：
- **单章问题**（如某章节奏问题）→ 返回到该章的 4-润色 P3-REPAIR-PLAN
- **模式问题**（如连续多章同构）→ 返回到 2-卷章/3-章级 重新规划
- **一致性回退**（如跨章人物矛盾）→ 触发 repair 诊断，定位源章后修复

### Token Budget

卷级审计执行时，不必全量加载卷内所有章正文。加载策略：
- **必加载**：各章的 `rhythm_intensity` / `payoff_type` / `selected_mode` / `previous_next_contrast` 摘要（来自 planning）
- **必加载**：各章的 `stage_acceptance_packet` 关键字段
- **按需加载**：在 FAIL 或 WARN 时逐章加载具体段落验证
- **预算上限**：卷级审计上下文消耗 ≤ 该卷总章数的 planning 摘要 token 量 + 2000 token 审计合同

## Integration Points

| 集成点 | 位置 | 动作 |
|--------|------|------|
| 卷级验收聚合 | `4-润色/review/review-contract.md` | 在 volume acceptance aggregation 完成后触发审计 |
| 审计节点 | `4-润色/SKILL.md` | 新增 P5A-VOLUME-AUDIT 节点 |
| 跨卷追踪 | `_shared/cross-volume-continuity-contract.md` | 审计在执行前需读取当前卷的 cross-volume-tracker |
| return 阻断 | `return/SKILL.md` | NEEDS_REWORK 时阻断 return 流程 |
