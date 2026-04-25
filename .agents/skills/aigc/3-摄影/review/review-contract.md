# Review Contract

本文件定义 `3-摄影` 的质量门禁。

## Review Modes

| mode | trigger | action |
| --- | --- | --- |
| `mechanical_check` | 落盘前或修复时 | 检查 `镜头语言：` 覆盖、`分镜N` 连续、路径和命名 |
| `cinematic_quality_review` | 交付前 | 检查构图、运镜、转场、光影、色彩是否服务戏剧 |
| `faithfulness_review` | 有改写风险时 | diff 上游 `2-编导`，确认正文事实、对白、顺序未被改写 |

## Acceptance Checklist

| gate_id | check | pass criteria |
| --- | --- | --- |
| `GATE-CINE-01` | 输入回指 | frontmatter 或报告记录 `source_directing_path` |
| `GATE-CINE-02` | 画面覆盖 | 所有命中画面性句子下方就近有 `镜头语言：` |
| `GATE-CINE-03` | 分镜编号 | 每个镜头语言块从 `分镜1:` 开始，连续编号，无跳号 |
| `GATE-CINE-04` | 节拍合理 | 分镜数量与当前画面句子的动作、信息、情绪节拍匹配 |
| `GATE-CINE-05` | 画面节奏 | 低信息/过场句收敛，关键揭示/强情绪/空间重置句发散，描述密度与信息重要性匹配 |
| `GATE-CINE-06` | 连续性回看 | 当前镜头语言已在内部承接临近至少前 3 个画面单位；不足 3 个时承接已有画面单位，输出不机械展示回看过程 |
| `GATE-CINE-07` | 专业可执行 | 分镜包含景别、景深、镜头视角、镜头类型、运镜速度，并按需要补充构图、机位、运动、光影、色彩或转场中的有效选择 |
| `GATE-CINE-08` | 动态流畅 | 镜头语言呈现从起点到终点的变化、组合运镜、速度曲线和注意力转移路径，不是静态标签列表 |
| `GATE-CINE-09` | 空间一致 | 没有无动机跳轴、反向运动、景别断崖、光色突变或风格断裂 |
| `GATE-CINE-10` | 戏剧服务 | 技法服务角色、危险、信息揭示或空间压迫，不是孤立炫技 |
| `GATE-CINE-11` | 原文保真 | 除新增 frontmatter/report 和 `镜头语言` 外，不改写 `2-编导` 正文 |
| `GATE-CINE-12` | 输出路径 | 写入 `projects/aigc/<项目名>/3-摄影/第N集.md` 和 `执行报告.md` |

## Failure Routing

| fail_code | symptom | rework target |
| --- | --- | --- |
| `FAIL-CINE-02` | 漏掉画面性句子 | `references/visual-matching-contract.md` |
| `FAIL-CINE-03` | 分镜过粗、过碎或固定模板化 | `references/beat-analysis-contract.md` |
| `FAIL-CINE-04` | `镜头语言` 缺失或编号断裂 | `templates/output-template.md`、`scripts/validate_cinematography_markup.py` |
| `FAIL-CINE-05` | 镜头语言空泛 | `references/cinematic-technique-library.md` |
| `FAIL-CINE-05B` | 镜头语言静态呆板，没有变化和组合运镜 | `references/dynamic-lens-language-contract.md` |
| `FAIL-CINE-05C` | 当前镜头语言与临近镜头断裂、跳轴、跳色或空间跳跃 | `references/shot-continuity-contract.md` |
| `FAIL-CINE-05D` | 镜头语言不分轻重，低信息过度发散或重信息过度收敛 | `references/visual-rhythm-analysis-contract.md` |
| `FAIL-CINE-06` | 改写原编导稿 | `SKILL.md` Output Contract 和本文件 `faithfulness_review` |

## Review Output

执行报告至少记录：

- 输入文件与输出文件。
- 处理集号。
- 画面性句子数量。
- `镜头语言` 块数量。
- 机械校验结果或人工 review 结果。
- 画面节奏张弛结果。
- 镜头连续性、空间一致性和风格一致性结果。
- 需要返工的行号或字段标签。
