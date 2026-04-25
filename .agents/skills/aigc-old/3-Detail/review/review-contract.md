# 3-Detail Review Contract

本文件是 `3-Detail` 的质量门禁层。它不拥有业务主真源，只负责在交付前把结构、字段、知识证据和 closure 质量映射到可返工节点。

## Review Scope

| dimension | checks | rework owner |
| --- | --- | --- |
| `structure` | `meta + groups[].global/detail` 是否与 `_shared/episode_detail.json` 同构 | `N1/N2` |
| `composition_first` | 是否固定先执行 `1-分镜构图`，并先锁分镜数与镜级骨架 | `N2` |
| `field_boundary` | 角色、氛围、摄影、运镜、转场是否没有互相抢权 | `N3-N6` |
| `continuity` | 时间、正文、主体锚定、运镜与转场是否连续 | `N2/N6` |
| `academy_translation` | 学院派知识是否回译到字段对象，而非教材摘抄 | `N1/N3-N6` |
| `report_evidence` | `validation-report.md` 是否有 `Layered Trace`、校验、知识证据与 closure | `N7/N8` |
| `script_boundary` | scripts 是否只做机械校验，不做主创 | `scripts/` |

## Required Checks

1. 运行 `scripts/validate_node_packs.py`，确认节点包与 references 兼容入口没有断链。
2. 运行 `scripts/validate_creative_guidance.py`，确认路由画像、正反例、评审标尺、知识接线和 closure guide 均可读取。
3. 对运行时产物运行 `scripts/validate_stage_output.py <第N集.json>`。
4. 对模板壳运行 `scripts/validate_stage_output.py _shared/episode_detail.json`，确认模板仍可作为空壳通过。
5. 读取 `templates/output-template.md`，确认报告模板没有改写 `SKILL.md` 的 Output Contract。

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | JSON、报告、知识证据、closure 均达标。 |
| `pass_with_todo` | 可交付，但存在非阻断 TODO。 |
| `needs_rework` | 必须回到指定节点或分区返工。 |
| `blocked` | 缺上游输入、权限、路径或用户裁决。 |

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: structure | field | continuity | academy | report | script | template
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Provider Policy

- 默认本地 review checklist 已足以覆盖 `3-Detail` 阶段门禁。
- 若上层环境和用户授权允许，可把 `code-reviewer` 作为辅助 provider 检查结构、脚本边界和潜在回归。
- 若上层策略阻断真实 reviewer 或 subagent 调度，按本地 checklist 降级，并在最终报告中说明阻断来源、原计划路径、实际路径与未启动的 reviewer。

## Completion Gate

不得在以下情况宣布完成：

- `N2` 骨架未先行成立。
- 后序字段反向改变分镜数、时间、正文切分点或主体锚定。
- `validation-report.md` 缺少 `## Academy Knowledge Evidence`。
- `validation-report.md` 缺少 `思考过程 / 关键证据 / 风险/例外 / 下一入口`。
- validator 失败且报告没有明确阻塞与返工入口。
