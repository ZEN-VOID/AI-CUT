# Character Design Workflow

本文件定义 `角色/2-设计` 的思行一体化流程。执行时先判断、再行动、再留证据。

## Topology

混合拓扑：项目上下文串行锁定，角色主体可并行分发给 subagents，最后统一汇流和 review。

```mermaid
flowchart TD
    A["N1 Intake"] --> B["N2 Project Context"]
    B --> C["N3 Character List"]
    C --> D["N4 Type Profile"]
    D --> E{"Subagent Dispatch"}
    E --> F["Research Patch"]
    E --> G["Story Patch"]
    E --> H["Visual Costume Patch"]
    E --> I["Cinematography Patch"]
    F --> J["N6 Merge Draft"]
    G --> J
    H --> J
    I --> J
    J --> K["N7 Review Gate"]
    K --> L{"Pass?"}
    L -->|"yes"| M["N8 Write Output"]
    L -->|"no"| J
```

## Thinking-Action Nodes

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 锁定项目、角色范围和不动范围 | 用户请求、项目路径 | 解析项目名、角色名、批量范围和只读边界 | `execution_scope` | `N2-PROJECT-CONTEXT` | 项目路径明确 |
| `N2-PROJECT-CONTEXT` | 加载项目风格和监制上下文 | `MEMORY.md`、`CONTEXT/`、`north_star.yaml`、`team.yaml` | 抽取全局风格、服装风格、设计相关大师上下文和禁区 | `project_design_context` | `N3-CHARACTER-LIST` | 缺失项已记录 |
| `N3-CHARACTER-LIST` | 锁定清单角色锚点 | `角色清单.md` | 读取待设计角色的名称、首次登场、原文描述关键词 | `character_intake_table` | `N4-TYPE-PROFILE` | 每个角色来自清单 |
| `N4-TYPE-PROFILE` | 判定角色类型和设计深度 | 清单行、项目上下文 | 应用 `types/character-design-type-map.md` | `type_profile` | `N5-SUBAGENT-DISPATCH` | 类型、深度和风险明确 |
| `N5-SUBAGENT-DISPATCH` | 启动默认 subagents 或记录降级 | `type_profile`、runtime 能力 | 分发研究、物语、视觉服装、摄影 patch；阻断时本地顺序执行并记录 | `subagent_or_downgrade_record` | `N6-MERGE-DRAFT` | 不静默跳过 subagents |
| `N6-MERGE-DRAFT` | 生成单一 canonical 设计稿 | 各 patch、模板 | LLM 汇流并写完整设计稿，不保留互相竞争的并列稿 | `character_design_draft` | `N7-REVIEW-GATE` | 字段齐全 |
| `N7-REVIEW-GATE` | 审查字段、风格、prompt 和 LLM-first | draft、review 合同 | 检查清单锚点、项目风格、解构字段、prompt 长度、脚本边界 | `review_result` | `N8-WRITE-OUTPUT` 或 `N6-MERGE-DRAFT` | 无阻断 finding |
| `N8-WRITE-OUTPUT` | 落盘 canonical markdown | 通过审查的设计稿 | 写入 `5-设计/角色/2-设计/<角色名>.md`，必要时写报告 | output files | done | 文件路径正确 |

## Failure Routes

| fail_code | symptom | rework_entry |
| --- | --- | --- |
| `FAIL-NO-LIST` | 找不到上游 `角色清单.md` | 回到 `N3-CHARACTER-LIST`，请求或生成上游清单 |
| `FAIL-NO-STYLE` | 未读取 `north_star.yaml` 或无法提炼全局风格 | 回到 `N2-PROJECT-CONTEXT` |
| `FAIL-SUBAGENT-SKIPPED` | 默认 subagent 路径被静默跳过 | 回到 `N5-SUBAGENT-DISPATCH` 并补降级报告 |
| `FAIL-PROMPT-LONG` | 英文提示词超过 2000 字符 | 回到 `N6-MERGE-DRAFT` 压缩 prompt |
| `FAIL-SCRIPT-AUTHORSHIP` | 脚本生成创作正文 | 停用脚本输出，回到 LLM 汇流 |
