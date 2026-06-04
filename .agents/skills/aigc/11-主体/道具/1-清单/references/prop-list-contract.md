# Prop List Contract

## Source Of Truth

- 唯一候选来源：`projects/aigc/<项目名>/10-分组/第N集.md` 每个分镜组底部 YAML 的 `道具` 字段。
- 证据回查范围：必要时只回查同一分镜组正文，用于确认别名、代称、首次登场和是否背景杂物。
- 禁止来源：角色目录、场景目录、后续设计稿、脚本猜测、项目外资料或 LLM 凭空补充。

## Canonical Output

- 路径：`projects/aigc/<项目名>/11-主体/道具/1-清单/道具清单.md`
- 形态：Markdown table
- 主体字段：`名称`、`首次登场`、`原文描述（关键词式）`

## Inclusion Rules

优先纳入：

- 叙事道具：推动剧情、触发行动、承载线索或关系。
- 规则道具：具有世界观规则、禁忌、能力、仪式或系统性用途。
- 视觉钩子：被特写、反复出现、颜色/形态强烈或承担镜头记忆点。
- 生成锁定物：后续图像或视频生成必须保持一致的物件。

默认过滤：

- 纯背景杂物、普通陈设、无特写的空间构件和氛围词。
- 只描述环境状态而非可设计物件的词。
- 与场景资产更相关、且不具备独立道具一致性需求的物件。

## Alias And Merge Rules

- 别名、代称、持有者称呼、短称、状态称呼和材质称呼应进入候选归并。
- 同一叙事道具只保留一个 canonical `名称`；别名可在执行报告中说明，不进入主体字段。
- 若两个称呼功能不同、首次登场不同且在剧情中可同时存在，则不得强行归并。
- 归并裁决必须由 LLM 结合 YAML 字段与同组正文证据完成。

## Non-Creative Boundary

本阶段不创作道具造型、材质细节、三视图、生成提示词或设计说明。这些内容属于后续 `2-设计` 和 `3-生成`。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每个最终道具主体是否都能回指 `10-分组/第N集.md` 某个分镜组底部 YAML 的 `道具` 字段，而不是角色目录、场景目录、后续设计稿、脚本猜测、项目外资料或 LLM 凭空补充？ | `REV-PROP-01` | `FAIL-PROP-SOURCE` | `N2-YAML-CANDIDATES` | `prop_candidates` 记录 `source_episode`、`group_id`、`yaml_prop_value`；执行报告列出删除或阻断的 YAML 外主体。 |
| 同组正文回查是否只服务别名、代称、首次登场和背景杂物判断，没有越组取证或把正文/项目资料变成新增候选来源？ | `REV-PROP-01` | `FAIL-PROP-EVIDENCE` | `N3-EVIDENCE` | `evidence_notes` 标明正文摘录所属分镜组、用途和未新增候选的说明。 |
| canonical 输出是否写入 `projects/aigc/<项目名>/11-主体/道具/1-清单/道具清单.md`，且可选 `执行报告.md` / `design-manifest.yaml` 没有替代主体清单？ | `REV-PROP-07` | `FAIL-PROP-RENDER` | `N6-RENDER` | 输出路径检查、写入文件清单，以及报告/manifest 的 sidecar 边界说明。 |
| 主体表格是否只包含 `名称`、`首次登场`、`原文描述（关键词式）` 三列，没有把别名、分类、设计方向、生成提示词或内部裁决字段写进主体字段？ | `REV-PROP-02` | `FAIL-PROP-RENDER` | `N6-RENDER` | 渲染后的表头检查、移除的多余字段记录和模板对齐说明。 |
| `首次登场` 是否取同一道具全部已知来源里最早的分镜组，优先写成 `第N集 x-y-z`，而不是取命名最完整、最近处理或设计最突出的那一组？ | `REV-PROP-03` | `FAIL-PROP-FIRST-APPEARANCE` | `N4-MERGE` | `first_appearance_map` 列出候选出现序列、最终最早组 ID 和被覆盖的较晚来源。 |
| 别名、代称、持有者称呼、短称、状态称呼和材质称呼是否进入候选归并，并由 LLM 裁决为单一 canonical `名称` 或说明不合并理由？ | `REV-PROP-04` | `FAIL-PROP-MERGE` | `N4-MERGE` | `merge_decision` 记录 alias/canonical 映射、同组证据、保留别名和不合并理由。 |
| 两个称呼若功能不同、首次登场不同且剧情中可同时存在，是否避免被语感、同名词根或脚本规则强行归并？ | `REV-PROP-04` | `FAIL-PROP-MERGE` | `N4-MERGE` | `merge_decision` 或待核项列明拆分理由、各自来源组和功能差异证据。 |
| 保留项是否至少具备叙事道具、规则道具、视觉钩子或生成锁定物之一的理由，而不是纯背景杂物、普通陈设、空间构件或氛围词？ | `REV-PROP-05` | `FAIL-PROP-FILTER` | `N5-FILTER` | `filter_decision` 标注每个保留项的保留类型，并列出被过滤的背景项及原因。 |
| 与场景资产更相关、且不具备独立道具一致性需求的物件，是否没有进入道具主体清单；若保留，是否说明其生成锁定或叙事功能？ | `REV-PROP-05` | `FAIL-PROP-FILTER` | `N5-FILTER` | 执行报告列出场景资产边界判断、保留例外理由和对应来源组。 |
| `原文描述（关键词式）` 是否只压缩 YAML 原词、同组正文可见词和动作关系词，没有扩写成道具造型、材质细节、三视图、生成提示词或设计说明？ | `REV-PROP-08` | `FAIL-PROP-DESIGN-OVERREACH` | `N6-RENDER` | 表格抽样、扩写删除记录和关键词来源说明；后续设计需求移交 `2-设计`。 |
| 归并、过滤、canonical 命名和重要性判断是否由 LLM 主判，脚本只做读取、YAML 定位、路径枚举、表格格式检查或机械校验？ | `REV-PROP-06` | `FAIL-PROP-LLM-FIRST` | `N4-MERGE` / `N5-FILTER` | 执行报告记录 LLM 裁决摘要、脚本辅助范围；若使用脚本，列明其未生成 canonical 名称或过滤判断。 |
