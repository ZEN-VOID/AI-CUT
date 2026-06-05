# Grouping Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


本文件定义 `10-分组` 的输入类型、风险画像和对应策略。

## Type Profile Variables

| variable | values | meaning |
| --- | --- | --- |
| `episode_scope` | `single_episode`、`episode_range`、`all_ready_episodes` | 本轮处理集数范围 |
| `source_state` | `complete_lighting`、`partial_lighting`、`direct_screenplay`、`legacy_grouped`、`broken_markup` | 上游输入状态 |
| `dialogue_density` | `low`、`normal`、`high` | 对白对边界的压力 |
| `duration_signal` | `shot_line_explicit`、`bracket_explicit`、`llm_planned_from_screenplay`、`missing`、`legacy`、`mixed` | 上游是否提供 `分镜N（起始秒-结束秒）：` 或 `[起始秒-结束秒]` 时间段 |
| `style_payload` | `normal`、`long_visual_tone`、`missing_global_style_prompt` | `Global Style Prompt` 字段状态 |
| `continuity_risk` | `low`、`medium`、`high` | 相邻组首帧衔接难度 |
| `repair_need` | `none`、`id_fix`、`boundary_fix`、`continuity_fix`、`stats_fix` | 修复主入口 |

## Mapping Matrix

| type signal | step impact | reference impact | review impact |
| --- | --- | --- | --- |
| `source_state=complete_lighting` | 直接进入 `N2-SOURCE-INVENTORY` 和 `N3-GROUP-BOUNDARY` | 读取 boundary | 标准 review |
| `source_state=partial_lighting` | 标记缺时间码、缺场景锚点或部分分镜行不完整的 atomic unit，不替上游补写；只按已有正文裁决分组边界 | boundary contract 保真优先 | 报告上游缺口 |
| `source_state=direct_screenplay` | 不阻断到 `9-光影`；由 LLM 直接从剧本字段、对白承托、动作落点和物件证据规划约 14.5 秒/组，补写连续时间码分镜行，并让最终累计结束秒以 `.5` 结尾 | direct screenplay intake rule | 报告源路径、时间码为本阶段规划、`.5` 收束、无法做 `9-光影` 分镜行级 diff |
| `source_state=legacy_grouped` | 仅作为 repair evidence，不当作新真源 | output contract 防平行真源 | 检查是否需迁移到 `10-分组/` |
| `dialogue_density=high` | 先看分镜行总时长是否已给足对白承托；约 4 句只作为风险提示 | dialogue constraint | 审查对话组过载 |
| `duration_signal=shot_line_explicit` | 以每条 `分镜N（起始秒-结束秒）：` 行作为 atomic unit 累计时长；落盘后改写为当前分镜组基准下连续累计时间码 | group duration band | 审查组内 `时长估算` 与最后结束秒一致 |
| `duration_signal=bracket_explicit` | 兼容 `[起始秒-结束秒]` 行，以完整画面/声音 atomic unit 累计时长；报告声明不是默认光影稿格式 | group duration band | 审查兼容格式与 source override 说明 |
| `duration_signal=llm_planned_from_screenplay` | 直接以剧本声画 atomic unit 规划组内连续时间码；每组优先约 14.5 秒、通常 10-14.5 秒、不得超过 14.5 秒，最终累计结束秒以 `.5` 结尾 | direct screenplay intake rule | 审查是否保留剧本事实、英文对白和声画承托，且报告时间码来源与 `.5` 收束 |
| `duration_signal=missing / legacy / mixed` | 若用户未指定 source override 或 direct screenplay，回到 source owner 补 canonical 时间段；若用户已要求直接接手剧本，切换 `direct_screenplay` 而不是阻断 | group duration band | 报告缺时间段来源或 direct screenplay 路径 |
| `style_payload=long_visual_tone` | 不影响组内时长或计入场景标题行/正文后的 1680 字风险口径；`全局风格：` 单行内容应从 `画面基调.Global Style Prompt` 抽取当前组匹配部分并压到 300 字以内；不得输出 `Visual Slogan`、`Design Principle`、`Visual Gene Profile` 或 `Negative Traits` 独立行 | visual tone projection | 禁止完整照抄全局风格母稿到每个组；禁止凭空新增当前组无证据风格 |
| `style_payload=missing_global_style_prompt` | 阻塞或请求用户修复 | missing field handling | 不得猜测补字段 |
| `continuity_risk=high` | 每组边界优先选择能被下一组第一个普通 `分镜N（0-N秒）：` 或 `[0-N秒]` 行以回龙帧口径完整代入、且只需调整景别和镜头视角即可进入本组的原尾帧/原首帧；若锚点来自对白、独白、旁白或音效画面，同步保留对应声音内容 | `SKILL.md#Thinking-Action Node Map` | first storyboard continuity review |
| `repair_need=stats_fix` | 保留正文，仅修 YAML | statistics contract | YAML 与正文一致性 |

## Source Detection Hints

- 若正文含 `stage: 9-光影`、`source_camera_path` / `source_lighting_path`，且存在 `分镜N（起始秒-结束秒）：` 行，通常为 `complete_lighting`。
- 若正文含 `stage: 2-编导`、`source_episode_path`、剧本正文、场景标题、对白、动作、音效、转场等字段，但缺少分镜时间码，且用户要求由 `10-分组` 接手，判为 `direct_screenplay`。
- 若只有部分分镜行存在时间码，或只有兼容 `[起始秒-结束秒]` 行而非光影稿格式，为 `partial_lighting` 或 `specified_source_override`，本阶段不补上游正文。
- 若输入来自 `1-Planning/3-分组/`、`10-分组/` 或含旧式 `【分组正文】`，为 `legacy_grouped`，不得覆盖本技能 canonical 输入。
- 若场景标题、frontmatter 或字段标签混乱，先标记 `broken_markup` 并进入 repair 或阻塞。
