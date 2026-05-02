# Storyboard Sheet Workflow

本文件承载 `B-分镜故事板` 的思行一体化节点。业务拓扑是先串行锁源、组装 prompt 和绑定主体，再按 imagegen 当前能力逐组或受控批量生成，最后统一汇流审查。

## Mermaid Workflow

```mermaid
flowchart TD
    N1["N1 Intake"] --> N2["N2 Load Project Context"]
    N2 --> N3["N3 Extract Groups from 4-分组"]
    N3 --> N4["N4 Assemble Fixed-Prefix Storyboard Prompts"]
    N4 --> N5["N5 Bind YAML Subject References"]
    N5 --> N6{"Review Gate"}
    N6 -->|"prompt_only"| N9["N9 Persist Prompt Package"]
    N6 -->|"generate"| N7["N7 Dispatch imagegen Group Batch"]
    N7 --> N8["N8 Persist Images and Results"]
    N8 --> N9
    N6 -->|"fail"| R["Repair owning section"]
    R --> N3
    N9 --> N10["N10 Close Report"]
```

## Thinking-Action Nodes

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 锁定任务目标、mode、集号和分镜组范围 | 用户请求、目标项目 | 判定 `prompt_only` / `single_group_generate` / `episode_batch_generate` / `group_batch_generate` / `repair` / `review_only` | mode note | `N2` | 目标范围明确 |
| `N2-CONTEXT` | 加载项目与技能上下文 | `SKILL.md`、`CONTEXT.md`、`MEMORY.md`、`north_star.yaml` | 读取项目偏好与图像阶段上下文 | input manifest | `N3` | 必需文件可读 |
| `N3-GROUP-INDEX` | 从 `4-分组` 建立组级索引 | `第N集.md` | 解析 `## x-y-z`、组正文、底部 YAML 和分镜数量 | `group-index.json` | `N4` | 每个 ID 唯一可回指 |
| `N4-PROMPT` | 生成组级 storyboard prompt | group index | 添加固定英文开头，直接接入现有组正文主体 | prompt markdown | `N5` | 固定开头与完整性通过 |
| `N5-REF-BIND` | 保守绑定 YAML 主体参照 | prompt package、5-设计生成目录 | 多视图优先、主图次之、缺图移除槽位；为每个已绑定本地图记录 `context_role` | reference manifest | `N6` | 无猜测路径 |
| `N6-REVIEW` | 执行生成前审查 | prompt、manifest | 检查 ID、固定开头、组正文、路径、mode；生成模式下逐张 `view_image` 已绑定本地参照图并记录上下文状态 | review note | `N7` / `N9` / repair | 必需项通过，参照图已可见 |
| `N7-IMAGEGEN` | 批量调用 imagegen | imagegen plan | 每组独立任务，使用已进入上下文的参照图，默认顺序或受控批量执行；更高吞吐执行方式必须由工具能力和用户显式要求共同支持 | plan/result json | `N8` | 不覆盖、不越权 |
| `N8-PERSIST` | 持久化生成图像 | generated assets | 保存到项目目录，记录源路径 | images + results | `N9` | 项目内路径存在 |
| `N9-WRITE` | 写业务工件 | prompt、manifest、result | 写 prompt 文档、manifest、plan、report | file list | `N10` | 文件命名正确 |
| `N10-CLOSE` | 汇流交付 | 所有证据 | 总结 generated / skipped / failed 与返工入口 | 执行报告 | done | review verdict `pass` 或 `pass_with_todo` |

## Parallel Boundary

- `N1-N6` 是串行门禁，不应并发绕过。
- `N7` 默认按 `group_id` 顺序或受控批量执行；每个任务只能写自己的图片和结果记录。
- `N9-N10` 必须统一汇流，避免多个任务同时改写同一个报告文件。
