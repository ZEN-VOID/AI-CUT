# Query Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


本文件集中维护 `$aigc-query` 的查询类型变量和真源映射。

## Type Variables

| variable | values |
| --- | --- |
| `truth_role` | `project_governance`、`stage_output`、`subject_asset`、`media_asset`、`governance_system`、`conflict_diagnosis` |
| `stage_scope` | `0-初始化`、`1-分集`、`2-编剧`、`3-美学`、`4-导演`、`5-表演`、`6-氛围`、`7-分镜`、`8-摄影`、`9-光影`、`10-分组`、`11-主体`、`12-图像`、`13-画布`、`14-审片`、`legacy` |
| `status_question` | `existence`、`completion`、`validation`、`location`、`next_entry` |
| `evidence_level` | `path_only`、`summary`、`with_validation`、`with_governance` |

## Signal Matrix

| user signal | truth_role | canonical source | review gate |
| --- | --- | --- | --- |
| 当前状态、停在哪、下一步、断点 | `project_governance` | `governance-state.yaml`、`STATE.json` | 是否区分轻量状态与治理快照 |
| 第N集、分集、编剧稿、美学协议、导演稿、表演稿、氛围稿、分镜稿、摄影稿、光影稿、分组稿 | `stage_output` | `1-分集`、`2-编剧`、`3-美学`、`4-导演`、`5-表演`、`6-氛围`、`7-分镜`、`8-摄影`、`9-光影`、`10-分组` | 是否补查执行报告 |
| 角色、场景、道具、主体、设计资产 | `subject_asset` | `11-主体/` | 是否说明清单/设计/生成层级 |
| 分镜画面、故事板、视频、参照视频、审片报告 | `media_asset` | `12-图像/`、`13-画布/分镜画面参照/`、`13-画布/分镜故事板参照/`、`13-画布/C-主体参照/`、`13-画布/D-主板混合参照/`、`14-审片/` | 是否说明 provider 输出、阶段工件与审片结论差别 |
| 路由、registry、技能是否 active | `governance_system` | registry/routes、阶段 `SKILL.md` | 是否区分制度源与项目源 |
| 路径不一致、旧目录、新目录冲突 | `conflict_diagnosis` | project layout + registry/routes | 是否给出主真源裁决 |

## Canonical Stage Map

| stage_scope | current carrier | legacy fallback |
| --- | --- | --- |
| `0-初始化` | `0-初始化/` | `0-Init/` |
| `1-分集` | `1-分集/第N集.md` | `1-Planning/` |
| `2-编剧` | `2-编剧/第N集.md` | `2-编导/第N集.md`, `3-Detail/第N集.json` |
| `4-导演` | `4-导演/第N集.md` | `2-编导/第N集.md` |
| `7-分镜` | `7-分镜/第N集.md` | `3-运动/第N集.md` |
| `8-摄影` | `8-摄影/第N集.md` | `4-摄影/第N集.md` |
| `10-分组` | `10-分组/第N集.md` | none |
| `11-主体` | `11-主体/{场景,角色,道具}/` | `4-Design/` |
| `12-图像` | `12-图像/` | `5-Image/` |
| `13-画布` | `13-画布/{分镜画面参照,分镜故事板参照,C-主体参照,D-主板混合参照}/` | `6-Video/`、`7-Cut/` |
| `14-审片` | `14-审片/` | none |
