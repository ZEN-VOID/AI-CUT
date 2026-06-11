# Chapter Polishing Contract

本文件展开 `story-polishing` 的章节润色细则。入口、路由、gate 和输出真源仍归根 `SKILL.md`。

## Stage Position

- 当前技能是 `story2026` 主链 `4-润色` 阶段的根执行包。
- 当前章润色业务真源固定为 `projects/story/<项目名>/4-润色/第N卷/第N章.md`。
- 源输入固定为 `projects/story/<项目名>/3-初稿/第N卷/第N章.md`。
- `4-润色` 根目录是唯一阶段技能入口，不形成 A/B/C 子技能、返工归属或 frontmatter 真源。

## Total Input Contract

### Required

- `projects/story/<项目名>/3-初稿/第N卷/第N章.md`
- `projects/story/<项目名>/0-初始化/north_star.yaml`
- `projects/story/<项目名>/2-卷章/整体规划.md`
- `projects/story/<项目名>/2-卷章/第N卷/卷规划.md`
- `projects/story/<项目名>/2-卷章/第N卷/第N章.md`
- `volume_num / chapter_num`

### Conditional

- `MEMORY.md` 与项目 `CONTEXT/`
- 既有 `4-润色` 目标章
- 上一章初稿或润色稿
- 内置验收 finding / 用户局部问题描述
- `acceptance_repair` 模式下的维度 findings 和 repair brief

## Hard Rules

1. 润色主输入只能是 `3-初稿` 源章。
2. 默认最小局部修补：保留初稿段落顺序、句群骨架、长短不齐、局部粗粝和人物原声。
3. 无用户授权时不得整章重排、短句化清洗、通用顺滑化或改写核心事件。
4. 新产物 frontmatter 只保留 `修订阶段: 润色`、`初稿来源` 与 `字数: XXX字`。
5. 旧稿已有 `润色模型` 时只作 legacy metadata；不得据此路由到旧子目录。
6. planning、cards、项目上下文、执行环境和 sidecar 路径不得写入正文 YAML。
7. AI 腔必须定位到具体坏点后修，不得把“去 AI 味”作为整章洗稿口令。
8. 场景密度、信息延迟、身体反应、物件和空间压力只要承担叙事功能就应保留。
9. 输出必须是完整章节 prose，不得输出点评、建议、差异说明或多个版本。
10. 脚本、模板、正则和映射表不得生成润色正文；正文必须来自 LLM-first 主创。

## Frontmatter Contract

```yaml
修订阶段: 润色
初稿来源: 3-初稿/第N卷/第N章.md
字数: XXX字
```

## Minimal Repair Contract

- 先列坏点，再定 affected span，再执行正文修补。
- finding 指向局部时，只修局部及必要上下文。
- finding 指向全章结构失效时，必须报告扩大范围原因；正式整章重润需要用户授权。
- 修补后应保留初稿的事实顺序、人物意图、信息揭示和章末牵引。

## Built-in Acceptance Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否锁定源初稿和 canonical 润色输出路径？ | `source_anchor` | `FAIL-POLISH-SOURCE` | `P1-SOURCE-LOCK` | source lock note |
| 是否保留初稿事实、骨架、文本分布和人物气口？ | `minimal_repair` | `FAIL-POLISH-SCOPE` | `P3-REPAIR-PLAN` | diff summary |
| 润色是否没有造成结构、连续性、逻辑、人物、时间线或任务汇聚回退？ | `regression_structure_logic` | `FAIL-POLISH-REGRESSION` | `P3-REPAIR-PLAN` / `P4-CREATIVE-POLISH` | regression issue map |
| 是否保留并强化题材质感、场景密度、句群节奏和追读力？ | `genre_texture_density` / `reader_pull` | `FAIL-POLISH-TEXTURE` / `FAIL-POLISH-READER-PULL` | `P4-CREATIVE-POLISH` | before/after evidence |
| AI 腔修补是否定位到具体特征？ | `anti_ai_features` | `FAIL-POLISH-AI-FEATURES` | `P3-REPAIR-PLAN` | issue list |
| 润色是否由 LLM-first 主创，脚本没有生成正文？ | `creative_authorship` | `FAIL-POLISH-AUTHORSHIP` | `P4-CREATIVE-POLISH` | script audit |
| 输出是否只写入 canonical path，并同步生成 `第N章.acceptance.json`？ | `output_state` | `FAIL-POLISH-WRITEBACK` | `P6-WRITEBACK-STATE` | expected vs actual path |

## Acceptance Output

每次正式写回润色稿时必须同步写入：

```text
projects/story/<项目名>/4-润色/第N卷/第N章.acceptance.json
```

终稿验收通过时 `accepted_manuscript_stage` 必须为 `4-润色`，`handoff_targets` 必须包含 `return`。
