---
name: comic
description: Use when 漫画项目需要从任意来源或小说进入完整三段链：漫画小说改编、九刀流 9 页漫画提示词 JSON、Seedream 一次生成 9 张连续竖版漫画页，并需要统一落盘到 projects/comic/[项目名]/。
governance_tier: full
---

# Comic 漫画总入口

## 1. 定位

本技能是 `.agents/skills/comic/` 的父级总入口，负责把漫画项目路由到三段受治理子技能，并统一项目落点：

```text
projects/comic/[项目名]/
  1-漫画小说改编/
  2-九刀流漫画提示词/
  3-漫画生成/
```

父技能只拥有路由、项目根、交接真源与验收总口径，不直接替代子技能写正文、写 JSON 或调用 Seedream。

## 2. 总输入合同

### 必需输入

- `project_name`
  - 漫画项目名。若用户未给，先从标题、源材料名或 JSON 文件名推断；无法可靠推断时询问。
- `task_intent`
  - `adapt_novel | make_prompts | generate_images | full_pipeline | inspect`

### 可选输入

- `source_material`
  - 原始素材、小说、漫画桥接包或已生成的 `nine_blade_comic_prompts.v1` JSON。
- `style_profile`
- `output_root`
  - 默认固定为 `projects/comic/[项目名]/`。

## 3. 路由拓扑

```mermaid
flowchart TD
    A["Comic Intake: 项目名 + 任务意图"] --> B{"输入类型/任务目标"}
    B -->|"任意素材/小说需改编"| C["1-漫画小说改编"]
    B -->|"已有小说/桥接包需9页提示词"| D["2-九刀流漫画提示词"]
    B -->|"已有 nine_blade JSON 需生图"| E["3-漫画生成"]
    B -->|"完整链路"| C
    C --> D
    D --> E
    E --> F["项目总验收"]
```

```mermaid
flowchart LR
    A["projects/comic/[项目名]/"] --> B["1-漫画小说改编/"]
    A --> C["2-九刀流漫画提示词/"]
    A --> D["3-漫画生成/"]
    B -->|"漫画小说主稿.md + 漫画桥接包.md"| C
    C -->|"nine_blade_comic_prompts.json"| D
    D -->|"9 images + reports"| E["交付证据"]
```

```mermaid
erDiagram
    COMIC_PROJECT ||--|| NOVEL_ADAPTATION : stage_1
    COMIC_PROJECT ||--|| NINE_BLADE_JSON : stage_2
    COMIC_PROJECT ||--|| COMIC_GENERATION : stage_3
    NOVEL_ADAPTATION ||--|| NINE_BLADE_JSON : hands_off
    NINE_BLADE_JSON ||--o{ COMIC_PAGE_IMAGE : generates
```

## 4. 子技能边界

| stage | 子技能 | 输入 | 输出 | 默认落点 |
| --- | --- | --- | --- | --- |
| 1 | [1-漫画小说改编](1-漫画小说改编/SKILL.md) | 任意素材、小说、热搜、图片/视频摘要 | `漫画小说主稿.md`、`漫画桥接包.md`、`思行裁决摘要.md` | `projects/comic/[项目名]/1-漫画小说改编/` |
| 2 | [2-九刀流漫画提示词](2-九刀流漫画提示词/SKILL.md) | 漫画小说主稿、桥接包或用户小说 | `nine_blade_comic_prompts.json` | `projects/comic/[项目名]/2-九刀流漫画提示词/` |
| 3 | [3-漫画生成](3-漫画生成/SKILL.md) | `nine_blade_comic_prompts.v1` JSON | 9 张漫画页、Seedream 报告、生成报告 | `projects/comic/[项目名]/3-漫画生成/` |

## 5. 思行节点

| node_id | objective | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- |
| `N1-PROJECT-LOCK` | 锁定项目名与项目根 | 建立或确认 `projects/comic/[项目名]/` | 用户请求、已有路径 | N2 | 项目根明确 |
| `N2-ROUTE` | 判断进入哪一段 | 按输入类型和任务目标路由 1/2/3 | 输入文件/文本类型 | 对应子技能 | 路由唯一 |
| `N3-HANDOFF` | 维护交接真源 | 确认上游输出是否满足下游输入 | 文件路径与 schema | 下一段或返工 | 不跳过必需 artifact |
| `N4-ACCEPTANCE` | 项目级验收 | 检查目标阶段产物是否落到项目根 | 子技能报告 | 完成或返工 | 路径和数量正确 |

## 6. 默认执行策略

- 用户只给素材并要求“做漫画”：默认 `full_pipeline`，依次走 1 -> 2 -> 3。
- 用户给小说并要求“出 9 张图提示词”：走 2。
- 用户给 `nine_blade_comic_prompts.json` 并要求“生成漫画”：走 3。
- 用户只问状态或路径：走 `inspect`，不改写内容。

## 7. 路径硬规则

- 项目根固定为 `projects/comic/[项目名]/`。
- 三段输出必须落到同名阶段目录：
  - `1-漫画小说改编/`
  - `2-九刀流漫画提示词/`
  - `3-漫画生成/`
- 下游不得把图片或报告回写到上游目录。
- 若用户显式指定其他输出根，必须在交付中说明偏离原因。

## 8. Root-Cause 合同

若出现路由错段、输出落到 `output/comic`、找不到上游 artifact、九页 JSON 与图片目录脱节，按以下链路上溯：

`Symptom -> Direct Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

- `Rule Source`：本父级 `SKILL.md`、对应子技能 `SKILL.md`、registry/routes。
- `Meta Rule Source`：仓库 `AGENTS.md` 的 Canonical Source Governance、`skill-知行合一` 的父子技能与一次性输出合同。
- 优先修父级路径/路由真源，再修子技能局部文案或脚本默认值。

