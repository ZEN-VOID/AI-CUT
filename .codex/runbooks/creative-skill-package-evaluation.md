# Creative Skill Package Evaluation Runbook

## Purpose

定义创作型技能包综合质量评估的标准执行流程，使评估不只停留在主观评论，而能形成可重复的运行路径。

## Shared Truth Sources

- 共享框架：`.codex/agents/aigc/质评组/_shared/creative-skill-package-evaluation-framework.md`
- 发布级别：`.codex/agents/aigc/质评组/_shared/creative-skill-package-release-levels.md`
- 报告模板：`.codex/templates/quality-evaluation/creative-skill-package-evaluation-report.md`
- 动态评测应基于当前技能真源、运行样本、validator 与回归证据即时组织，不要求目标技能预先维护固定 benchmark 文档

## Standard Flow

1. 锁定评估目标。
   - 明确目标技能树、作用域、评估目标与比较基线。
2. 判定评估模式。
   - `static`：只看静态真源。
   - `dynamic`：重点看真实运行证据。
   - `hybrid`：静态 + 动态双轨。
3. 收集证据束。
   - 最少读取 `SKILL.md`、`CONTEXT.md`、相关 `references/`、`subtypes/`、模板、schema、runbook。
   - 若评估创作稳定性，补收代表性样本、回放记录、回归结果。
4. 判定证据等级。
   - 依据 `L0-L4` 给出证据级别。
5. 基于当前真源与运行样本即时设计动态评测任务。
   - 至少覆盖 baseline、regression。
   - 条件允许时补 boundary、stress、adversarial。
   - 若已有可信 benchmark 文档，可作为辅助输入，但不得代替本轮即时取证。
6. 执行四层主评估。
   - 契约治理层
   - 创作能力层
   - 工程运行层
   - 演化持续层
7. 执行横切专项检查。
   - 路由质量
   - 知识拓扑
   - 质量上限/质量下限
   - 反作弊检查
8. 生成改进优先级。
   - 只保留 `1-3` 个最高杠杆动作。
9. 推荐发布级别。
   - 使用 `R0-R4`。
10. 输出评估报告。
   - 使用 `.codex/templates/quality-evaluation/creative-skill-package-evaluation-report.md`。

## Hard Gates

- 出现隐藏第二真源且影响执行：直接降为 `FAIL-COVENANT`。
- 无法回答 canonical landing 或 repair entry：不得高于 `PASS-WITH-REWORK`。
- 仅有 `L0-L1` 证据：不得推荐 `R2+`。
- 缺少动态回归证据：不得推荐 `R3+`。

## Root-Cause Closure

任何非平凡失败都必须给出：

- `root cause location`
- `immediate fix`
- `systemic prevention fix`

并附：

`Symptom -> Direct Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`
