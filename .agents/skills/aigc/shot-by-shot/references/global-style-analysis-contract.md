# Global Style Analysis Contract

`全局风格解析.md` 是 `shot-by-shot` 输出给项目风格底座的解析细则。它参照 `global-style-director` 的字段逻辑，但在本技能中只作为 side context，不直接生成或改写 `style_contract.json`、`north_star.yaml` 或其他初始化 canonical 文件。

## Scope

- 目标：从参考素材中提炼全片可继承的媒介属性、渲染管线、美学范式、叙事节奏锚点和无污染风格提示词候选。
- 落点：`projects/aigc/<项目名>/CONTEXT/shot-by-shot/<reference_slug>/全局风格解析.md`。
- 非目标：不得复制参考片具体角色、场景、道具、构图、镜头顺序、颜色组合、材质组合或受版权保护的画面表达。
- 下游：供 `0-初始化`、`3-摄影`、`5-设计` 和项目风格复核加载；若需要进入 `style_contract.json`，必须由 owning stage 另行执行。

## Field Map

| field_id | Markdown 区块 | 内容要求 | 失败码 |
| --- | --- | --- | --- |
| `GLOBAL-NARRATIVE-RESEARCH` | `## 叙事与世界约束` | TL;DR、主题三联、世界三联、时代/地域/叙事类型/节奏倾向，信息不足时标记推导补位 | `FAIL-GLOBAL-NARRATIVE-WEAK` |
| `GLOBAL-STYLE-ROUTE` | `## 路由决议` | 明确 `R1-STANDARD-INHERIT`、`R2-DECONTAMINATE`、`R3-TYPE-BACKFILL` 或 `R4-EXACT-LOCK` 之一及原因 | `FAIL-GLOBAL-ROUTE` |
| `GLOBAL-MEDIUM-STACK` | `## 媒介与技术栈` | 真人/2D/3D 或混合媒介选择，2-3 个核心渲染技术栈，说明如何服务叙事 | `FAIL-GLOBAL-MEDIUM` |
| `GLOBAL-AESTHETIC-PARADIGM` | `## 美学范式` | 明确美学流派、气质和叙事服务理由，不使用空泛词 | `FAIL-GLOBAL-PARADIGM` |
| `GLOBAL-PACING-ANCHOR` | `## 叙事节奏锚定` | 慢/中/快节奏、判断依据、拍摄段落执行字窗、无明确逻辑根源时默认中节奏 | `FAIL-GLOBAL-PACING` |
| `GLOBAL-POLLUTION-AUDIT` | `## 去污染审计` | 默认审计颜色/材质/构图/摄影越权项；`R4` 时审计原文保真 | `FAIL-GLOBAL-POLLUTION` |
| `GLOBAL-STYLE-PROMPT` | `## 全局风格提示词候选` | 默认 200 字以内纯中文无污染提示词；`R4` 可保留用户锁定原文但必须标明 exact | `FAIL-GLOBAL-PROMPT` |

## Routing Rules

| route_id | trigger | action |
| --- | --- | --- |
| `R1-STANDARD-INHERIT` | 输入丰满且无显式锁定 | 推导媒介、技术栈、流派并蒸馏无污染提示词 |
| `R2-DECONTAMINATE` | 草稿或参考表达含污染项 | 清洗颜色、材质、构图、摄影越权项，只保留底层渲染与美学范式 |
| `R3-TYPE-BACKFILL` | 输入稀疏 | 用叙事类型、情感目标、时代和世界约束反推稳妥底座 |
| `R4-EXACT-LOCK` | 用户明确要求原文直通、逐字继承、不要净化 | 保真记录原文为项目级锁定候选，不做净化或删改 |

## Default Pollution Boundary

默认模式下，`全局风格提示词候选` 禁止出现：

- 具体颜色词。
- 具体材质词。
- 构图术语。
- 焦段、光圈、光源位置、推拉摇移等摄影/运镜词。
- 下游对象细节，例如角色外貌、场景物件、道具形状、剧情动作。

`R4-EXACT-LOCK` 命中时允许保留用户原文，但必须在 `## 用户锁定风格原文` 中逐字落盘，并在审计中声明未净化原因。

## Required Markdown Shape

`全局风格解析.md` 至少包含：

1. `## 使用边界`
2. `## 叙事与世界约束`
3. `## 路由决议`
4. `## 媒介与技术栈`
5. `## 美学范式`
6. `## 叙事节奏锚定`
7. `## 去污染审计`
8. `## 全局风格提示词候选`
9. `## Do Not Import`
