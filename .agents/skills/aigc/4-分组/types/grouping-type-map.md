# Grouping Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


本文件定义 `4-分组` 的输入类型、风险画像和对应策略。

## Type Profile Variables

| variable | values | meaning |
| --- | --- | --- |
| `episode_scope` | `single_episode`、`episode_range`、`all_ready_episodes` | 本轮处理集数范围 |
| `source_state` | `complete_cinematography`、`partial_cinematography`、`legacy_grouped`、`broken_markup` | 上游摄影稿状态 |
| `dialogue_density` | `low`、`normal`、`high` | 对白对边界的压力 |
| `style_payload` | `normal`、`long_north_star`、`missing_fields` | north_star 三项字段状态 |
| `bridge_risk` | `low`、`medium`、`high` | 组间首尾帧衔接难度 |
| `repair_need` | `none`、`id_fix`、`boundary_fix`、`bridge_fix`、`stats_fix` | 修复主入口 |

## Mapping Matrix

| type signal | step impact | reference impact | review impact |
| --- | --- | --- | --- |
| `source_state=complete_cinematography` | 直接进入 `N3-SCENE-MAP` | 读取 boundary 与 bridge | 标准 review |
| `source_state=partial_cinematography` | 标记缺镜头语言的 atomic unit，不替上游补写原有镜头语言；只按已有正文裁决分组边界 | boundary contract 保真优先 | 报告上游缺口 |
| `source_state=legacy_grouped` | 仅作为 repair evidence，不当作新真源 | output contract 防平行真源 | 检查是否需迁移到 `4-分组/` |
| `dialogue_density=high` | 降低每组对白上限到约 4 句 | dialogue constraint | 审查对话组过载 |
| `style_payload=long_north_star` | 预留更多组头字数，正文组更短 | north-star projection | 禁止摘要 north_star |
| `style_payload=missing_fields` | 阻塞或请求用户修复 | missing field handling | 不得猜测补字段 |
| `bridge_risk=high` | 每组边界优先选择强视觉承接点 | bridge-shot contract | pairwise bridge review |
| `repair_need=stats_fix` | 保留正文，仅修 YAML | statistics contract | YAML 与正文一致性 |

## Source Detection Hints

- 若正文含 `stage: 3-摄影`、`source_directing_path`、`镜头语言：`，通常为 `complete_cinematography`。
- 若只有部分画面字段存在 `镜头语言：`，为 `partial_cinematography`，本阶段不补摄影正文。
- 若输入来自 `1-Planning/3-分组/`、`5-分组/` 或含旧式 `【分组正文】`，为 `legacy_grouped`，不得覆盖本技能 canonical 输入。
- 若场景标题、frontmatter 或字段标签混乱，先标记 `broken_markup` 并进入 repair 或阻塞。
