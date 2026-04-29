# Chapter Drafting Workflow

本文件承载 `story-drafting-gpt-native` 的思行网络。节点必须同时表达判断、动作、证据、路由和 gate。

## Topology

当前技能采用 hybrid 拓扑：前段串行锁源与判型，中段先启动 team supervision subagents，再按起草/续写/重写/修复分支汇流到 GPT 原生主创，后段接 writeback 与卷级 review handoff。

```mermaid
flowchart TD
    N1["N1-SOURCE-LOCK"] --> N2["N2-TYPE-PROFILE"]
    N2 --> N3["N3-CONTEXT-PACK"]
    N3 --> N3S["N3S-SUPERVISION-PACKET"]
    N3S --> N4{"N4-DRAFT-BRANCH"}
    N4 -->|"chapter_draft"| N5A["N5A-NEW-DRAFT-PROMPT"]
    N4 -->|"chapter_rewrite"| N5B["N5B-REWRITE-PROMPT"]
    N4 -->|"chapter_continue"| N5C["N5C-CONTINUE-PROMPT"]
    N4 -->|"local_repair"| N5D["N5D-REPAIR-PROMPT"]
    N5A --> N6["N6-GPT-NATIVE-DRAFT"]
    N5B --> N6
    N5C --> N6
    N5D --> N6
    N6 --> N7["N7-VALIDATE-WRITEBACK"]
    N7 --> N8["N8-REVIEW-HANDOFF"]
    N8 --> G{"Gate"}
    G -->|"pass"| Done["canonical chapter file"]
    G -->|"fail"| R["Root-Cause Route"]
    R --> N3
```

## Node Network

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-SOURCE-LOCK` | 锁定唯一项目根、卷号、章号与输出路径 | 用户请求、项目根、chapter 参数 | 定位 `projects/story/<项目名>/` 与 `第N卷/第N章.md` | `source_lock_note`、canonical output path | `N2-TYPE-PROFILE` | 项目根与卷章唯一 |
| `N2-TYPE-PACKAGE` | 判定起草、续写、重写、修复或 dry-run，并选择题材类型包 | 目标章是否存在、用户意图、`types/type-map.md`、`types/网文/` | 生成 `type_profile` 并加载命中的 `types/网文/<题材>/` 固定上下文 | `type_profile`、`selected_type_package` | `N3-CONTEXT-PACK` | mode 唯一且不冲突；题材包已加载或缺口已报告 |
| `N3-CONTEXT-PACK` | 组装写作上下文包 | 三层 planning、global/style cards、`north_star`、`MEMORY.md`、项目 `CONTEXT/`、上一章 | 读取并压缩为 GPT 原生可消费上下文；上一章存在时生成连续性桥 | context pack、context refs、continuity bridge | `N3S-SUPERVISION-PACKET` | 必需输入齐备；上一章存在时必须有桥接约束 |
| `N3S-SUPERVISION-PACKET` | 启动隔离监制组 | context pack、项目 `team.yaml`、`team/SKILL.md + CONTEXT.md`、`roles.production.members` 中被请教的成员技能 | 真实启动 subagents，向不同领域大师提出具体请教问题，汇流创意脑洞、个人风格判断和可执行指导 | supervision packet、roster refs、consultation questions 或降级报告 | `N4-DRAFT-BRANCH` | 有真实 subagent 证据；监制包含 roster 来源、请教问题与可执行指导；被上层阻断时有降级说明 |
| `N4-DRAFT-BRANCH` | 按类型和题材包选择创作约束 | `type_profile`、`selected_type_package`、现稿状态、用户约束 | 路由到新章、重写、续写或修复分支 | branch decision | `N5A/B/C/D` | 分支与用户请求一致；题材包约束进入提示 |
| `N5A-NEW-DRAFT-PROMPT` | 为新章起稿生成 GPT 原生创作请求 | context pack、输出模板 | 保持 planning 义务，生成完整章请求 | prompt section | `N6-GPT-NATIVE-DRAFT` | 没有依赖现稿 |
| `N5B-REWRITE-PROMPT` | 为重写生成 GPT 原生创作请求 | context pack、现有正文、用户重写约束 | 保留成立事实，重构正文 | prompt section | `N6-GPT-NATIVE-DRAFT` | 已回读现稿 |
| `N5C-CONTINUE-PROMPT` | 为续写/补全生成 GPT 原生创作请求 | context pack、现有正文、章末目标 | 延续既有文气并补足未完成义务 | prompt section | `N6-GPT-NATIVE-DRAFT` | 承接点明确 |
| `N5D-REPAIR-PROMPT` | 为局部修复生成 GPT 原生创作请求 | review finding、现稿、源层约束 | 定位问题层并限制修复范围 | rework route note | `N6-GPT-NATIVE-DRAFT` | 不越权改 planning |
| `N6-GPT-NATIVE-DRAFT` | 由当前 GPT/LLM 会话生成完整章节文件 | branch prompt、系统提示、输出模板、完整上下文、supervision packet | 当前会话直接创作完整 Markdown | GPT-authored draft | `N7-VALIDATE-WRITEBACK` | LLM 主创真实发生 |
| `N7-VALIDATE-WRITEBACK` | 校验并写回 canonical 章节 | GPT-authored draft、frontmatter contract、heading contract | 校验 YAML、必需字段、标题、正文完整度；写回目标路径 | final chapter file、sidecar refs | `N8-REVIEW-HANDOFF` 或 Root-Cause Route | 校验通过且路径正确 |
| `N8-REVIEW-HANDOFF` | 准备卷级审计与返工闭环 | 当前卷章节集合、写作日志、sidecars、review 触发条件 | 卷完成时调用 `review/final_acceptance`，并汇流 `code-reviewer` findings；未满卷时记录 candidate 状态 | review handoff note | done | 不把单章 candidate 宣称为 validated final |

## Failure Routing

| fail_code | symptom | rework_entry |
| --- | --- | --- |
| `FAIL-GPTDRAFT-SOURCE` | 项目根、卷章或输出路径不唯一 | `N1-SOURCE-LOCK` |
| `FAIL-GPTDRAFT-TYPE` | 起草/续写/重写/修复误判 | `N2-TYPE-PROFILE` |
| `FAIL-GPTDRAFT-CONTEXT` | planning、cards、`north_star`、项目记忆或上下文缺失 | `N3-CONTEXT-PACK` |
| `FAIL-GPTDRAFT-SUPERVISION` | subagents 未真实启动、未说明降级，或监制包未进入创作 messages | `N3S-SUPERVISION-PACKET` |
| `FAIL-GPTDRAFT-CONTINUITY` | 上一章存在但本章开篇像重新开局、漏接事实/位置/情绪/悬念 | `N3-CONTEXT-PACK`、`N5*` |
| `FAIL-GPTDRAFT-PROMPT` | prompt 未对齐分支或照搬 planning 语言 | `N4-DRAFT-BRANCH`、`N5*` |
| `FAIL-GPTDRAFT-CREATIVE` | 当前 GPT 原生主创缺失、跑偏或被脚本替代 | `N6-GPT-NATIVE-DRAFT` |
| `FAIL-GPTDRAFT-WRITEBACK` | frontmatter、标题或输出路径不合规 | `N7-VALIDATE-WRITEBACK` |
| `FAIL-GPTDRAFT-REVIEW-HANDOFF` | 卷完成后未进入 `review`、`code-reviewer` findings 未汇流或返工目标缺失 | `N8-REVIEW-HANDOFF` |

## Evidence Gate

- dry-run 至少应产生 context pack 与上下文引用摘要。
- 正式创作至少应产生 context pack、基于项目 `team.yaml` 监制组请教的 supervision packet 或降级报告、GPT-authored draft sidecar、writeback summary 或等价证据，以及 canonical chapter file。
- 卷完成时必须产生 `review` handoff 或 aggregate 引用；未满卷时必须标记为 candidate draft。
- 任何由脚本拼接出的正文不得宣称按 `story-drafting-gpt-native` 完成。
