# CHANGELOG

## 2026-04-25

- 从 `.agents/skills/aigc-old/review` 迁入 review 父技能、旧六维审计材料、`_shared/` runner 兼容合同与 `agents/openai.yaml`。
- 按 `skill-工作车间` 的 Skill 2.0 包结构补齐 `references/`、`steps/`、`review/`、`types/`、`templates/`、`scripts/`、`knowledge-base/` 与根 `README.md`。
- 将父 `SKILL.md` 收束为入口、路由、动态引用、字段映射与 Output Contract；旧长细则拆入分区文件。

## 2026-04-26

- 将六个旧 review 维度目录从局部 `SKILL.md + CONTEXT.md` 收束为父包 `references/dimensions/*.md` 细则。
- 将维度经验合并回父级 `CONTEXT.md`，避免 review 维度继续以独立 skill identity 被发现或直达调度。
- 同步 registry、runner runtime 记录、README、OpenAI 入口和 `_shared/` 兼容合同，统一使用 `dimension_spec_ref` 指向维度细则。
