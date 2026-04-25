# 骆以军 Skill 质量验证

验证日期：2026-04-18

## 自动检查

命令：

```bash
python3 .agents/skills/team/study/文学系/骆以军/scripts/merge_research.py .agents/skills/team/study/文学系/骆以军
python3 .agents/skills/team/study/文学系/骆以军/scripts/quality_check.py .agents/skills/team/study/文学系/骆以军/SKILL.md
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-女娲/scripts/quality_check.py .agents/skills/team/study/文学系/骆以军/SKILL.md
python3 scripts/aigc_skill_audit.py --strict
```

结果：

| check | result |
|---|---|
| merge_research 汇总 | PASS，总来源数 32，一手标记 34/41，信息不足维度无 |
| 本地 quality_check.py | PASS，6/6 通过 |
| huashu-nuwa 源脚本 quality_check.py | PASS，6/6 通过 |
| team 根索引同步 | PASS，`.agents/skills/team/SKILL.md` 已加入 `骆以军` |
| AIGC skill tree audit | PARTIAL，脚本返回 3 个**仓内既有**失败，均不指向本次新增 skill |

## 质量检查结果

| 项目 | 结果 |
|---|---|
| 心智模型数量 | PASS，6 个 |
| 模型局限性 | PASS |
| 表达 DNA | PASS，11 项风格锚点 |
| 诚实边界 | PASS，6 条 |
| 内在张力 | PASS，2 处 |
| 一手来源占比 | PASS，11/17，65% |

## 调研汇总检查

`merge_research.py` 汇总结果：

| 维度 | 来源数量 | 关键发现 |
|---|---:|---|
| 著作 | 7 | 长篇极限运动、小说朝圣、知识支流回流叙事 |
| 对话 | 4 | 害羞说书、两个故事开场、紧张感转叙事引擎 |
| 表达 | 3 | 长句补丁、名词堆栈、自嘲后下沉 |
| 他者 | 4 | 巴洛克密度、私密告白与国族叙事并置 |
| 决策 | 5 | 西夏触发、手写坚持、贷款写长篇、AI 回答转向经验 |
| 时间线 | 9 | 从《西夏旅馆》到 2025 获奖与授课的持续活动 |

## 修复记录

### 失败现象

- 首轮 `quality_check.py` 报告“一手来源占比 2/4 = 50%”，未达 >50%。

### 分层追踪

- Symptom：来源占比校验失败
- Direct Cause：`SKILL.md` 的“调研来源”区只按分组标题区分一手/二手，没有给每条来源显式打标
- Rule Source：本 skill 的来源区写法与 `quality_check.py` 的标记统计接口不够贴合
- Meta Rule Source：`huashu-nuwa` Phase 4 对一手来源占比 >50% 的硬门槛

### 立即修复

- 将 `SKILL.md` 的每条来源改为显式 `[一手]` / `[二手]` 标记。

### 系统预防修复

- 已在 `CONTEXT.md` 的 Reusable Heuristics 增加规则：后续同类人物 skill 的“调研来源”区应按条目标记来源类型，避免再次误报。

## 仓内既有审计阻塞

`python3 scripts/aigc_skill_audit.py --strict` 返回以下非本次改动导致的失败：

1. `.agents/skills/aigc/0-初始化/SKILL.md` 缺少 planning interview 的 mandatory subagent rule
2. `.agents/skills/aigc/_shared/council-runtime/team.template.yaml` 缺少 `require_subagents_for_init_interview: true`
3. `.agents/skills/aigc/_shared/council-runtime/team.template.yaml` 缺少 `init_interview_owner_role: "planning"`

结论：本次新增的 `骆以军` skill 已通过局部验证；全仓严格审计仍受既有 harness 入口问题阻塞。

