# Query Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


本文件集中维护 `$aigc-query` 的查询类型变量和真源映射。

## Type Variables

| variable | values |
| --- | --- |
| `truth_role` | `project_governance`、`stage_output`、`subject_asset`、`media_asset`、`governance_system`、`conflict_diagnosis` |
| `stage_scope` | `0-初始化`、`1-分集`、`2-美学`、`3-主体`、`4-编剧`、`5-导演`、`6-分镜`、`7-摄影`、`8-分组`、`9-图像`、`10-画布`、`legacy` |
| `status_question` | `existence`、`completion`、`validation`、`location`、`next_entry` |
| `evidence_level` | `path_only`、`summary`、`with_validation`、`with_governance` |

## Signal Matrix

| user signal | truth_role | canonical source | review gate |
| --- | --- | --- | --- |
| 当前状态、停在哪、下一步、断点 | `project_governance` | `governance-state.yaml`、`STATE.json` | 是否区分轻量状态与治理快照 |
| 第N集、分集、美学协议、主体注册表、编剧稿、导演稿、分镜稿、摄影稿、分组稿，以及显式 legacy 表演稿/氛围稿/光影稿 | `stage_output` | active: `1-分集`、`2-美学`、`3-主体`、`4-编剧`、`5-导演`、`6-分镜`、`7-摄影`、`8-分组`; archived: `5-表演`、`6-氛围`、`9-光影` | 是否补查执行报告，并标注 archived 阶段不参与默认链 |
| 角色、场景、道具、主体、设计资产 | `subject_asset` | `3-主体/` | 是否说明清单/设计/生成层级 |
| 分镜画面、故事板、视频、参照视频、审片报告 | `media_asset` | `9-图像/`、`10-画布/分镜画面参照/`、`10-画布/分镜故事板参照/`、`10-画布/C-主体参照/`、`10-画布/D-主板混合参照/`、review evidence | 是否说明 provider 输出、阶段工件与审片结论差别 |
| 路由、registry、技能是否 active | `governance_system` | registry/routes、阶段 `SKILL.md` | 是否区分制度源与项目源 |
| 路径不一致、旧目录、新目录冲突 | `conflict_diagnosis` | project layout + registry/routes | 是否给出主真源裁决 |

## Canonical Stage Map

| stage_scope | current carrier | legacy fallback |
| --- | --- | --- |
| `0-初始化` | `0-初始化/` | `0-Init/` |
| `1-分集` | `1-分集/第N集.md` | `1-Planning/` |
| `4-编剧` | `4-编剧/第N集.md` | `2-编导/第N集.md`, `3-Detail/第N集.json` |
| `5-导演` | `5-导演/第N集.md` | `2-编导/第N集.md` |
| `6-分镜` | `6-分镜/第N集.md` | `3-运动/第N集.md` |
| `7-摄影` | `7-摄影/第N集.md` | `4-摄影/第N集.md` |
| `8-分组` | `8-分组/第N集.md` | none |
| `3-主体` | `3-主体/{场景,角色,道具}/` | `4-Design/` |
| `9-图像` | `9-图像/` | `5-Image/` |
| `10-画布` | `10-画布/{分镜画面参照,分镜故事板参照,C-主体参照,D-主板混合参照}/` | `6-Video/`、`7-Cut/` |
