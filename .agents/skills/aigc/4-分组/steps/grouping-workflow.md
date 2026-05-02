# Grouping Workflow

本文件定义 `4-分组` 的思行一体执行拓扑。

## Business Requirement Analysis

| slot | answer |
| --- | --- |
| `business_goal` | 将逐集摄影稿切成完整分镜组，供后续设计、图像和视频阶段稳定消费 |
| `business_object` | `projects/aigc/<项目名>/3-摄影/第N集.md` 与 `0-初始化/north_star.yaml` |
| `constraint_profile` | 对白 4-6 句、完整组构成 <= 1980 字、画面句子多分镜不可截断、补位画面成对一致 |
| `success_criteria` | 每组 ID 真实、风格投影含置顶于第 1 行最前的全局固定前置词、正文保真、桥接自然、统计 YAML 可复查 |
| `non_goals` | 不改剧情、不改对白、不重写原有镜头语言、不生成图像/视频提示词 |
| `complexity_source` | 边界裁决、组间桥接、字数与完整性汇流 |
| `topology_fit` | 串行取证 + 场景内树形分组 + 相邻组 pairwise review + 统一验收 |

## Node Network

```mermaid
flowchart TD
    N1["N1-INTAKE<br/>锁定项目、集号、上游和 north_star"] --> N2["N2-PROJECT-STYLE<br/>投影三项风格字段"]
    N2 --> N3["N3-SCENE-MAP<br/>建立集/场/atomic unit 映射"]
    N3 --> N5["N5-GROUP-PLAN<br/>对白/字数/atomic unit 三重约束裁决"]
    N5 --> N6["N6-BRIDGE<br/>组间入场/出场补位成对设计"]
    N6 --> N7["N7-ASSEMBLE<br/>组头 + 原正文 + 补位 + YAML"]
    N7 --> N8{"N8-REVIEW<br/>结构、桥接、保真验收"}
    N8 -->|"pass"| N9["N9-WRITE<br/>写入 4-分组/第N集.md 与执行报告.md"]
    N8 -->|"north_star 缺失或投影错误"| N2
    N8 -->|"场景/ID 异常"| N3
    N8 -->|"超字数、对白过载或 atomic unit 被截断"| N5
    N8 -->|"入场/出场不一致或补位新增剧情"| N6
    N8 -->|"YAML 统计漏项"| N7
```

```mermaid
flowchart LR
    subgraph THINK["思维判断"]
        T1["输入真源判断"]
        T2["场景和组号判断"]
        T4["边界密度判断"]
        T5["桥接惯性判断"]
        T6["统计证据判断"]
    end
    subgraph EXEC["执行产物"]
        E1["input manifest"]
        E2["scene unit table"]
        E4["group boundary plan"]
        E5["bridge pair list"]
        E6["episode group draft"]
    end
    T1 --> E1 --> T2 --> E2 --> T4 --> E4 --> T5 --> E5 --> T6 --> E6
```

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 锁定项目、集号、上游和 north_star | 用户请求、项目目录 | 定位 `3-摄影/第N集.md`、`north_star.yaml`、项目记忆和上下文 | input manifest | `N2-PROJECT-STYLE` | 必需输入可读 |
| `N2-PROJECT-STYLE` | 投影三项风格字段 | north_star | 抽取 `全局风格.全局风格提示词`、`类型元素.类型元素提示词`、`细分风格.画面风格`，并把固定前置词 `视频生成的画面风格，光影和氛围与场景参照图保持一致。不生成文字字幕和BGM，仅生成物理互动音效与环境和氛围音效。` 放在第 1 行最前，再接全局风格原词 | style projection | `N3-SCENE-MAP` | 三项字段齐全且固定前置词已置顶于第 1 行最前 |
| `N3-SCENE-MAP` | 建立集/场/atomic unit 映射 | 摄影稿正文 | 提取场景标题、字段、镜头语言块和对白数 | scene unit table | `N5-GROUP-PLAN` | atomic unit 不跨场景 |
| `N5-GROUP-PLAN` | 裁决组边界 | scene unit table、style projection | 按三重约束形成组计划，预留补位画面字数 | group boundary plan | `N6-BRIDGE` | 每组候选 <= 1980 且完整 |
| `N6-BRIDGE` | 设计入场/出场补位 | 相邻组首尾 atomic unit | 逐对设计同一桥接画面，每集首组省略入场画面段 | bridge pair list | `N7-ASSEMBLE` | 相邻桥接画面一致，且不新增剧情 |
| `N7-ASSEMBLE` | 组装分组稿 | group plan、bridge pair、style projection | 写组头、入场、原正文、出场、YAML 统计 | episode group draft | `N8-REVIEW` | 正文同步原换行 |
| `N8-REVIEW` | 验收结构和质量 | 分组稿、上游、validator | 运行机械检查或人工 review，记录报告 | review result | `N9-WRITE` 或返工 | 所有 gate pass |
| `N9-WRITE` | 落盘交付 | accepted draft | 写 `4-分组/第N集.md` 与 `执行报告.md` | output files | done | 输出可复查 |

## Failure Routes

```mermaid
flowchart TD
    F0["N8-REVIEW 发现失败"] --> F1{"失败类型"}
    F1 -->|"north_star 三项缺失"| R2["返回 N2-PROJECT-STYLE"]
    F1 -->|"场景标题缺失或 ID 不连续"| R3["返回 N3-SCENE-MAP"]
    F1 -->|"组超 1980 字或镜头语言被截断"| R5["返回 N5-GROUP-PLAN"]
    F1 -->|"入场/出场不一致或新增剧情"| R6["返回 N6-BRIDGE"]
    F1 -->|"YAML 统计漏项"| R7["返回 N7-ASSEMBLE"]
    R2 --> F0
    R3 --> F0
    R5 --> F0
    R6 --> F0
    R7 --> F0
```

| failure | return_to |
| --- | --- |
| north_star 三项缺失 | `N2-PROJECT-STYLE`，先修复或请求授权 |
| 场景标题缺失或重复异常 | `N3-SCENE-MAP`，回上游摄影稿修复 |
| 组超 1980 字 | `N5-GROUP-PLAN`，移动完整 atomic unit |
| 同一镜头语言被截断 | `N5-GROUP-PLAN`，恢复 atomic unit |
| 出场/入场不一致，或补位新增剧情 | `N6-BRIDGE`，成对重写 |
| YAML 统计漏项 | `N7-ASSEMBLE`，重抽统计 |
| validator 失败 | `N8-REVIEW`，按 fail_code 返工 |
