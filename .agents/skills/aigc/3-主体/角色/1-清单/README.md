# aigc 3-主体/角色/1-清单

角色清单 Skill 2.0 包，用于从 `projects/aigc/<项目名>/3-主体/subject-registry.yaml` 的 `subjects.characters` 条目整理 canonical 角色清单；`1-分集` 和 `8-分组` 仅作 source anchor 或后置命名对齐证据。

## Directory Tree

```text
1-清单/
├── references/
│   ├── source-and-merge-contract.md
│   └── legacy-character-list-workflow.md
├── scripts/
│   └── README.md
├── templates/
│   └── output-template.md
├── review/
│   └── review-contract.md
├── knowledge-base/
│   └── character-list-heuristics.md
├── types/
│   └── character-identity-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
├── test-prompts.json
└── README.md
```

## Quick Entry

- 调用名：`$aigc-design-character-list`
- 上游真源：`projects/aigc/<项目名>/3-主体/subject-registry.yaml` 的 `subjects.characters` 条目。
- Canonical 输出：`projects/aigc/<项目名>/3-主体/角色/1-清单/角色清单.md`。
- 固定表头：`名称`、`首次登场`、`原文描述（关键词式）`。
- 多状态策略：同一角色的多服装、战斗、战损、受伤、少年、老年等作为同一 base character 的变体，不拆成新角色；必要时用 `变体：...` 短标签或 manifest sidecar 交接。

## Visual Overview

```mermaid
flowchart TD
    A["3-主体/subject-registry.yaml"] --> B["subjects.characters"]
    B --> C["候选证据表"]
    C --> D["LLM 身份归并"]
    D --> E["首次登场裁决"]
    E --> F["角色清单.md"]
    F --> G["review gate"]
```

## Guardrails

- 角色归并、别名判断、代称裁决由 LLM 完成。
- 脚本只能读取、抽取、校验和提示风险，不能生成 canonical 清单正文。
- 正文回查只允许用于解释 registry 条目的 source anchors，不得绕过 registry 另造候选。
- 状态变体不得污染角色清单主体数量；清单仍保持三列。
