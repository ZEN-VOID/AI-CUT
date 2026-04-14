# CHANGELOG.md

本文件记录 `aigc/4-Design/角色/2-设计` 的结构性改动，不参与默认预加载。

## 2026-04-12

- `Case-20260412-AIGC-ROLE-DESIGN-SKILL-BOOTSTRAP`
  - 新建 `2-设计` 父 skill、经验层、shared I/O、模板参考与 `agents/openai.yaml`。
  - 新建 `.codex/agents/aigc/设计组/角色设计/team.md`，并把 `设计统筹 / 形象建模 / 服装设计 / 妆容设计 / 个性塑造 / 角色一致性复核 / 真源审计` 落为正式 agent contracts。
  - 将 `2-设计` 的 canonical 输出锁定为 `character_design.json + 逐角色 Markdown + _manifest.json`。

- `Case-20260412-AIGC-ROLE-DESIGN-PARENT-STATUS-SYNC`
  - 将 `.agents/skills/aigc/4-Design/SKILL.md` 与 `.agents/skills/aigc/4-Design/角色/SKILL.md` 中的 `2-设计` 状态从 `pending` 同步为 `active`。
  - 为 `.agents/skills/aigc/4-Design/CONTEXT.md` 与 `.agents/skills/aigc/4-Design/角色/CONTEXT.md` 补充本轮设计技能激活记录。

## 2026-04-13

- `Case-20260413-AIGC-ROLE-DESIGN-THREE-PART-MARKDOWN`
  - 将逐角色 Markdown 模板改为固定三段式 `物语 / 解构 / prompt整合`。
  - 在主 `SKILL.md` 中补入 `物语` 的 `biography-first` 规则、`解构` 的 `Reasoning Pivot` 首行约束，以及 `prompt整合` 必须消费 `story_premise + reasoning_pivot` 并尾拼全局风格引用的 hard rule。
  - 为 `character_design.json.roles[]` 最低字段补入 `biography / story_premise / reasoning_pivot / structured_fields / prompt_integration`，保证机器侧与 Markdown 同源。

- `Case-20260413-AIGC-ROLE-DESIGN-NODE-AUGMENTATION`
  - 为父 `SKILL.md` 增补 `V-STYLE-CONVERGENCE / V-ATTRIBUTE-CERTAINTY / V-PHOTO-CONTRACT`，并新增 `N5B-STRUCTURED-LOCK`，把风格收敛、基础属性保守标记、默认摄影合同与结构拆解写成硬节点。
  - 为 shared I/O 补入 `attribute_certainty + photo_contract` 的字段归属和 hard rules。
  - 同步更新 `设计统筹 / 形象建模 / 妆容设计 / 角色一致性复核 / team` 合同，并补齐缺失的 `.codex/agents/aigc/设计组/角色设计/服装设计.md`。

- `Case-20260413-AIGC-ROLE-DESIGN-PROP-PROJECTION-AUGMENT`
  - 将 `templates/角色设计卡.template.md` 直接改为用户指定的 prop-style 三段式：`# [prop_name_en] / 物语 / 解构 / prompt整合`。
  - 将 `解构` 固定收束为 `## Photography ##` 与 `## Prop Design ##` 两段参数表，并按用户给定字段顺序落位。
  - 在主 `SKILL.md` 中同步补入“纯道具主体 / Prop Style 收敛 / 作品参照 / 参照转译 / 镜头服务主体”的节点判断，并显式声明展示投影不改 canonical JSON 命名。
