# Prompt Distillation Contract

本文件承接旧 `首帧参照` 的核心语义，负责 `distill/` 段的创作与落盘约束。

## Ownership

`distill/` 拥有：

- 单一 `分镜ID` 或 episode 级多个单镜目标到首帧视频请求对象的转换。
- `正文切分参考[] -> 正文回指 -> 目标帧剧情桥段` 的提取、保守压缩与例外说明。
- 组级设计块、单镜融写行、TXT 派生视图和 manifest 追溯。
- `reference_images / image_markers` 的 provider-neutral 骨架。

`distill/` 不拥有：

- 修改 `3-Detail/<episode>.json`。
- 生成、挑选或上传图片。
- provider 提交、轮询、下载。

## Input Gate

- 第一事实源为 `projects/aigc/<项目名>/3-Detail/<episode>.json`。
- 只消费稳定 canonical detail root：`meta + groups[].global/detail.分镜列表`。
- 若兼容投影存在，只能作为 helper view，不得成为新的第一真源。
- 每个目标分镜必须能稳定得到 `分镜ID`、所属 `分镜组ID`、组级 `global.*`、目标镜头时间、剧本正文、主体锚定、角色/运动/氛围/视觉强化/分镜构图/摄影/运镜/转场等镜级事实。
- 若目标 `shot_id` 未给出，可按旧 `首帧参照` episode carrier 口径批量生成多条“单镜一条”请求。

## LLM Authorship

- prompt 正文与 `第N集.txt` 主稿必须由 LLM 主创。
- 脚本不得用字段拼接、模板灌字或启发式补句替代创作判断。
- `scripts/` 可以校验字数、字段覆盖、路径、JSON schema 和 manifest，但不拥有创作真源。

## Prompt Contract

- 最终 prompt 采用 `BC` 结构：
  1. 组级设计块。
  2. 单镜融写行。
- 不再保留独立 A 段整组 `剧本正文`；剧本信息通过 `正文回指` 或对应剧本片段融进目标镜级行。
- 每条镜级行以 `xx秒-xx秒｜分镜<组内序号>：` 开头。
- 完整四段式 `分镜ID` 只保留在 `meta.source_shot_ids`、manifest 等结构化回链字段中。
- 除镜级序号标签外，不得暴露字段标题，不得写成 `字段标题：字段值`。
- 默认以可朗读自然句融合信息；只有预算逼近上限时才允许局部短语化。
- 高优先保留：剧情桥段、主体动作/表演、景别、分镜构图、运镜手法、镜头速度、镜头视角、主要空间关系。

## TXT Contract

`distill/<episode>.txt` 是人工审阅主稿，按集组织，每个目标分镜固定包含：

1. `分镜组ID`
2. `全局风格 + 类型元素 + 导演意图`
3. `分镜N，x-y秒`
4. `剧本正文：`
5. `主体锚定：`
6. `分镜明细：`
7. `字数统计：xxx`

硬规则：

- 每个目标分镜都必须独立成块，不得退回“只展示 prompt 和字数统计”。
- `剧本正文`、`主体锚定.场景`、`主体锚定.角色` 不得压缩。
- `主体锚定.道具` 可轻量压缩，不得改事实。
- `分镜明细` 必须展开到下一层字段后，改写为镜头语言优先的自然 prose。
- 禁止隐性字段串联：即便没有显式字段名，只要句子仍按字段顺序平铺，也视为失败。

## Distill Artifacts

- `distill/<episode>.json`
- `distill/<episode>.txt`
- `distill/_manifest.json`

`json` 是 completeness carrier，`txt` 是 derived display view，`manifest` 是追溯和异常说明载体。
