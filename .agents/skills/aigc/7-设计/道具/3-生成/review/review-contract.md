# Review Contract

本文件定义 `道具/3-生成` 的验收门禁。review 不拥有业务主真源改写权；修复建议必须回流到 `SKILL.md`、`references/`、`steps/` 或对应模板。

## Default Provider

- 默认辅助 provider：外部 reviewer provider。
- 仓库层合同允许 `$aigc-prop-generation` 命中时启用 worker/reviewer provider 路径。
- 若当前运行环境不使用外部 provider，主 agent 直接执行本地 review checklist。
- 本地 checklist 只记录 review verdict、finding 和必要修复项。

## Review Checklist

| check_id | gate | pass condition | fail route |
| --- | --- | --- | --- |
| `REV-PROP-GEN-01` | 上游取证 | 每组资产回指一个 `2-设计` Markdown | `references/prop-generation-contract.md` |
| `REV-PROP-GEN-02` | 主图忠实度 | 主图 JSON 直接引用设计文档 `4. 解构`，未重新设计主体，未回退引用旧英文整合 prompt | `templates/single-subject-prompt.json` |
| `REV-PROP-GEN-03` | 多视图参照 | 多视图 JSON 使用对应 `主体ID-主体名称-主图` 作为 `reference_image`，真实生成模式下该主图已 `view_image` 进入对话上下文 | `templates/prop-multiview-prompt.json` |
| `REV-PROP-GEN-04` | 命名 | 图像与 JSON 同 stem，文件名包含主体 ID，且包含 `-主图` 或 `-多视图` | `SKILL.md Output Contract` |
| `REV-PROP-GEN-05` | 路径 | 所有项目资产落入 `projects/aigc/<项目名>/7-设计/道具/3-生成/` | `$imagegen` persistence gate |
| `REV-PROP-GEN-06` | 非越界 | 未修改 `2-设计`、父级 registry、角色/场景生成目录或其他 worker 文件 | 根写入边界 |
| `REV-PROP-GEN-07` | 参照上下文 | 多视图 JSON / 报告记录 `reference_context_status: visible_in_conversation_context`；prompt-only 可为 `pending_view_image` | `steps/prop-generation-workflow.md` |

## Review Flow

```mermaid
flowchart TD
    A["收集 checked_outputs"] --> B["检查上游 source_design_doc"]
    B --> C["检查主图 JSON 引用 4. 解构"]
    C --> D["检查多视图 reference_image"]
    D --> E["检查命名与同 stem"]
    E --> F["检查 canonical 输出路径"]
    F --> G["检查非越界写入"]
    G --> H{"review 路径"}
    H -->|"reviewer provider"| I["记录 review_status=external_reviewer"]
    H -->|"local checklist"| J["记录 review_status=local_checklist"]
    I --> K{"verdict"}
    J --> K
    K -->|"pass"| L["交付"]
    K -->|"pass_with_followups"| M["交付并列 followups"]
    K -->|"needs_rework"| N["路由到失败节点"]
```

## Verdict Schema

```yaml
verdict: pass | pass_with_followups | needs_rework | blocked
reviewer: ""
review_status: external_reviewer | local_checklist | not_requested
checked_outputs:
  - subject: ""
    subject_id: ""
    main_image: ""
    main_prompt_json: ""
    multiview_image: ""
    multiview_prompt_json: ""
    reference_context_status: ""
findings: []
next_action: ""
```

## Provider Rule

- 默认优先使用外部 reviewer provider。
- 若工具不可用外部顾问与复核 provider 调度，主 agent 直接执行本地 review checklist。
- 本地 review checklist 只记录 verdict、finding、修复动作和 residual risk。
