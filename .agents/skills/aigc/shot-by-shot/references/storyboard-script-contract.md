# Storyboard Script Contract

`分镜脚本.md` 是 `shot-by-shot` 执行后的标准表格式分镜脚本。字段和内容编排必须完全参照仓库示例 `input/苍穹裂缝·战神降维.numbers`。

## Source Example Fields

示例 Numbers 表格包含 19 列，顺序固定如下：

| order | column |
| --- | --- |
| 1 | `镜号` |
| 2 | `时长` |
| 3 | `画面描述` |
| 4 | `角色1` |
| 5 | `角色描述1` |
| 6 | `角色图1` |
| 7 | `角色2` |
| 8 | `角色描述2` |
| 9 | `角色图2` |
| 10 | `参考` |
| 11 | `景别` |
| 12 | `角色动作` |
| 13 | `情绪` |
| 14 | `场景标签` |
| 15 | `光影氛围` |
| 16 | `音效` |
| 17 | `对白` |
| 18 | `分镜提示词` |
| 19 | `视频运动提示词` |

## Content Arrangement Rules

- 每行对应一个镜头，不用剧情段落冒充镜头。
- `镜号` 使用连续数字；若绑定正式项目分镜 ID，可在 `参考` 或补充说明中保留四段式 ID，不替代示例列名。
- `时长` 使用秒数，保留一位小数更贴近示例。
- `角色描述1/2` 采用 `[角色名: 描述]` 形式；无第二角色时留空。
- `角色图1/2`、`参考` 无素材时留空，不臆造路径。
- `场景标签` 使用逗号分隔的短标签。
- `对白` 无对白时写 `无`。
- `分镜提示词` 按示例组织为连续段落，并用方括号承载功能块：`[画面构图：...]`、`[主体/人物空间：...]`、`[环境元素：...]`、`[光影与大气：...]`、`[视觉风格/质感：...]`、`[技术参数：...]`。
- `视频运动提示词` 以 `[摄影机运镜：...]` 开头，描述主体动作、环境物理动态、角色互动和时长，并以 `[时长：<秒数>s]` 收束。
- 可学习示例的字段组织和镜头生产信息密度，不得照搬示例的具体角色、剧情、台词、场景、神话符号或视觉表达。

## Markdown Shape

`分镜脚本.md` 至少包含：

1. `## 使用边界`
2. `## 字段来源`
3. `## 分镜脚本表`
4. `## 生成检查`

`## 分镜脚本表` 必须使用上述 19 列 Markdown table。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| `分镜脚本.md` 是否使用 Numbers 示例 19 列和固定顺序，从 `镜号` 到 `视频运动提示词` 完整无改名？ | `GATE-SBS-STORY-01` | `FAIL-STORYBOARD-19-COLUMNS` | `N5-BRIDGE` | Markdown table header 与列顺序检查 |
| 每行是否对应一个真实镜头，没有用剧情段落、场景段落或分析段落冒充分镜行？ | `GATE-SBS-STORY-02` | `FAIL-STORYBOARD-ROW-PER-SHOT` | `N2-SHOT-MAP` / `N5-BRIDGE` | shot boundary map 到 table row 的一一映射 |
| `镜号` 是否连续；正式四段式 ID 是否只放在 `参考` 或补充说明中，不替代表头？ | `GATE-SBS-STORY-03` | `FAIL-STORYBOARD-ID` | `N5-BRIDGE` | `镜号` 序列与 reference ID 说明 |
| `时长`、`角色描述1/2`、`对白`、`场景标签` 是否按示例格式写入，缺素材处不臆造？ | `GATE-SBS-STORY-01` | `FAIL-STORYBOARD-19-COLUMNS` | `N5-BRIDGE` | table body field audit |
| `角色图1/2`、`参考` 是否只使用真实素材路径或留空，不伪造图片或引用？ | `GATE-SBS-STORY-04` | `FAIL-STORYBOARD-ASSET-PATH` | `N5-BRIDGE` | asset/path evidence list |
| `分镜提示词` 是否按方括号功能块组织构图、主体空间、环境、光影、风格质感和技术参数？ | `GATE-SBS-STORY-05` | `FAIL-STORYBOARD-PROMPT-BLOCK` | `N5-BRIDGE` | prompt block coverage |
| `视频运动提示词` 是否以 `[摄影机运镜：...]` 开头，包含主体动作、环境动态、角色互动，并以 `[时长：<秒数>s]` 收束？ | `GATE-SBS-STORY-05` | `FAIL-STORYBOARD-PROMPT-BLOCK` | `N5-BRIDGE` | video motion prompt check |
| 是否只学习示例的信息密度和列编排，不照搬示例角色、剧情、台词、场景、神话符号或视觉表达？ | `GATE-SBS-STORY-06` | `FAIL-STORYBOARD-EXAMPLE-COPY` | `N4-PRINCIPLE` | example-copy audit 与 forbidden-copy ledger |
