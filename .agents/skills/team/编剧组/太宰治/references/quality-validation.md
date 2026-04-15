# 太宰治 Skill 质量验证

验证日期：2026-04-15

## 自动检查

命令：

```bash
python3 .agents/skills/team/编剧组/太宰治/scripts/quality_check.py .agents/skills/team/编剧组/太宰治/SKILL.md
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-女娲/scripts/quality_check.py .agents/skills/team/编剧组/太宰治/SKILL.md
python3 scripts/aigc_skill_audit.py --strict
```

结果：

| check | result |
|---|---|
| 心智模型数量 | PASS，6 个 |
| 模型局限性 | PASS |
| 表达DNA辨识度 | PASS，8 项 |
| 诚实边界 | PASS，6 条 |
| 内在张力 | PASS，5 处 |
| 一手来源占比 | PASS，9/13，69% |
| AIGC skill tree audit | PASS，failures 0，warnings 0 |

## 调研汇总检查

`merge_research.py` 汇总结果：

| 维度 | 来源数量 | 关键发现 |
|---|---:|---|
| 著作 | 8 | 主要作品群、道化/自白/没落/旧故事反写 |
| 对话 | 5 | 无现代访谈，用文本中的自白姿势替代 |
| 表达 | 5 | 轻佻入口、自嘲外壳、羞耻内核 |
| 他者 | 4 | 私小说/无赖派语境、战后价值失序、误读风险 |
| 决策 | 5 | 失败者、自我暴露、家庭没落、女性旁观 |
| 时间线 | 5 | 1909-1948 作品节点与 2026 前译介/纪念传播 |

## Sanity Check

| 测试点 | 预期 | 结果 |
|---|---|---|
| 《人間失格》相关问题 | 不只输出“绝望”，而输出“道化防御 + 羞耻自白 + 社会失配” | PASS |
| 《斜陽》相关问题 | 不只写“战后没落”，而落到家庭、饭桌、房屋、称谓和财产 | PASS |
| 《走れメロス》/旧故事改写 | 不只解构高尚，而保留伦理骨架并加入现代怯懦 | PASS |

## Edge Check

测试点：用太宰视角处理一个没有公开讨论过的现代短剧人物。

预期：输出应以“基于模型推断”为边界，不冒充太宰本人观点；重点给面具、羞耻动作、自白罪证和女性旁观者，而非编造生平材料。

结果：PASS。`SKILL.md` 的 Agentic Protocol 和 `dazai.fact_check / dazai.boundary` 字段可覆盖。

## Voice Check

测试点：100 字左右创作诊断。

预期：轻佻开口、低姿态转入、突然下沉，有太宰式辨识度；不写通用鸡汤，不堆“死亡/绝望”词。

结果：PASS。表达 DNA 与示例开口已提供可执行语气锚点。

## 修复记录

验证时发现 `quality_check.py` 的来源区正则存在跨标题贪婪匹配问题，会导致一手来源漏计。已修复：

- `.agents/skills/team/编剧组/太宰治/scripts/quality_check.py`
- `/Users/vincentlee/.codex/skills/meta/构建/技能/skill-女娲/scripts/quality_check.py`
- `.agents/skills/team/编剧组/太宰治/CONTEXT.md` Type Map

分层追踪：

`一手来源占比误报 -> quality_check.py 标题正则跨换行贪婪匹配 -> huashu-nuwa 脚本源层 -> AGENTS.md Root-Cause 学习回路 -> 修脚本 + CONTEXT 沉淀`
