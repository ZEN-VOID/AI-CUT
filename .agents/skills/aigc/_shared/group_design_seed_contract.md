# Group Design Seed Contract

本文件是 `aigc/2-Global -> 3-Detail` 之间 `分镜组壳 + 组间设计 + 分镜切换` 写入 shared episode root 的单一真源。

## Purpose

- 让 `2-Global` 在阶段末段把导演前置判断、既定分镜切换与完整分组正文直接写入与 `3-Detail` 相同的 episode JSON 模版。
- 让 `3-Detail` 优先继承已收束的 `组间设计`，而不是再次从三份 Markdown 长文中抽取。
- 保留 `2-Global/*.md` 作为长文本审阅/解释载体，但把跨阶段 handoff 的第一结构化真源固定为 `projects/aigc/<项目名>/3-Detail/第N集.json`。

## Canonical Carrier

- shared schema:
  - `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- shared root file:
  - `projects/aigc/<项目名>/3-Detail/第N集.json`
- target slot:
  - `final_output.main_content.分镜组列表[]`

## Ownership

| phase | owner | responsibility |
| --- | --- | --- |
| `2-Global` | `aigc-global` | 创建或 patch shared episode root 的 `metadata / 分镜组列表[].分镜组壳 / 分镜切换` |
| `3-Detail` | `aigc-detail` | 继承已存在的 `组间设计`，并补全 `分镜明细[]` 与 detail 级字段 |

硬规则：

1. `2-Global` 只拥有 `分镜组壳`、`组间设计` seed、`分镜切换` 真值与相关 metadata 的写入权，不得在本阶段发明 shot-level `分镜明细[]`。
2. `3-Detail` 默认继承 `组间设计`，不得在无明确返工理由时重写其含义。
3. `3-Detail` 默认继承 `分镜切换`，并在此基础上结合 `水月` 的 beat-level factual evidence 落真实切镜。
4. `2-Global/*.md` 是长文本解释侧车；下游第一结构化 handoff 以 shared episode root 为准。

## Mapping

| episode root field | upstream source | scope | max_chars | mapping rule |
| --- | --- | --- | --- | --- |
| `分镜组ID` | `1-Planning/3-分组/第N集.md` 的 `【x-x-x】` 标题 | 当前组 | exact | 保持三段式 `分镜组ID` 原样写回，不重复生成新编号 |
| `总时长` | `1-Planning/3-分组/第N集.md` 或配套 grouping 元数据 | 当前组 | exact | 直接继承当前组时长，不做主观改写 |
| `剧本正文` | `1-Planning/3-分组/第N集.md` 中命中组正文 | 当前组 | full_text | 完整整理该组正文入壳，只去掉重复组号标题，不得摘要、净化或改写语义 |
| `组间设计.全局风格` | `2-Global/全局风格/全局风格设计.md` 中字段标题 `全局风格` | 项目级稳定项 | 220 | 直接引用 Markdown 中已确认的一段项目级无污染统一风格前缀，作为当前组默认继承的 AIGC 风格底座 |
| `组间设计.类型元素` | `2-Global/类型元素/分组设计.md` 中 `第N集 -> 【组ID】` 命中段落里的字段标题 `类型元素` | 当前组 | 50 | 直接引用 Markdown 中已确认的一段组级类型信号，不在 JSON 现场改写 |
| `组间设计.导演意图` | `2-Global/设计元素/设计元素.md` 中 `第N集 -> 【组ID】` 命中段落里的字段标题 `导演意图` | 当前组 | 100 | 直接引用 Markdown 中已确认的一段组级执行导向，不在 JSON 现场改写 |
| `分镜切换` | `2-Global` 末段基于 `总时长 + 类型元素 + 导演意图 + 分组正文` 直接裁定的固定镜数 | 当前组 | exact | 只写一个具体数字，作为后续 `3-Detail` 必须接受的组级固定分镜数 |

## Distillation Rules

1. 字数窗必须在 Markdown 定稿阶段先满足；JSON 写入阶段只允许直接提取字段内容，不允许临场重写。
2. `剧本正文` 必须完整整理命中组全文；如果写入结果更像摘要而不是原组正文，视为失败。
3. `全局风格` 必须保持项目级稳定，不得被单组临时情绪污染；默认也不得混入景别偏置、具体颜色/材质/构图或镜头操作词。
4. `类型元素` 与 `导演意图` 都必须严格对齐当前 `分镜组ID`，不得跨组混写。
5. 三个字段都必须能被 `3-Detail` 直接消费；如果一句话不能转译成镜头、表演、调度、氛围或摄影方向，应回到 Markdown 继续压实，而不是在 JSON 里偷偷改句子。
6. `分镜切换` 只负责锁定组级固定镜数；former `镜花/1-切换` 的 fixed-shot-count 接受逻辑已在 `2-Global` 内化为阶段侧车说明，真实 `分镜ID / 时间段 / beat_refs[]` 仍由 `3-Detail` 的 `分镜构图` 落镜完成。

## Writeback Policy

1. `2-Global` 首次进入时，如 shared root 不存在，可基于 shared schema 创建同模版 episode root。
2. `2-Global` 写回 shared root 时，`metadata.document_phase` 应进入 `directing_in_progress`。
3. `2-Global` 写回 shared root 时，必须同时形成完整分镜组壳：`分镜组ID / 总时长 / 剧本正文 / 组间设计 / 分镜切换 / 分镜明细=[]`。
4. `3-Detail` 继续补齐时再进入 `detail_in_progress / ready`。
5. `3-Detail` 若发现 `剧本正文` 缺失、`组间设计` 缺失、字段错引或超出字数窗，应先报告上游 seed 缺口，再决定是否进入保守兼容回退。

## Phase Transition Reading Guide

- 读取真实项目时，按同一 `projects/aigc/<项目名>/3-Detail/第N集.json` 的 `metadata.document_phase` 理解 phase 推进：
  - `directing_in_progress`：`2-Global` 已写完整分镜组壳与 `分镜切换`，`分镜明细` 仍可为空数组。
  - `detail_in_progress`：`3-Detail` 已开始在同一 root 上补 `分镜明细[]`。
  - `ready`：同一份 root 已推进到可交付态。
- 重点检查：
  1. `组间设计` 是否稳定继承。
  2. `分镜切换` 是否已由 `2-Global` 稳定写成固定数值。
  3. `分镜明细[]` 是否只在 `3-Detail` 阶段扩展。
  4. phase 推进是否仍保持同一 canonical root，而不是另起第二份终稿。
