# 马荣成 Skill 质量验证

验证时间：2026-04-16  
验证对象：`../SKILL.md`

## 自动质量检查

命令：

```bash
python3 .agents/skills/team/动漫组/马荣成/scripts/quality_check.py .agents/skills/team/动漫组/马荣成/SKILL.md
```

结果：6/6 通过。

| 检查项 | 结果 |
|---|---|
| 心智模型数量 | PASS：6 个心智模型 |
| 模型局限性 | PASS：每个模型包含局限 |
| 表达 DNA | PASS：特征充足 |
| 诚实边界 | PASS：5 条 |
| 内在张力 | PASS：覆盖画技/留白/IP/产业张力 |
| 一手来源占比 | PASS：约 67% |

## 仓库合同检查

命令：

```bash
python3 scripts/skill_context_audit.py --root .agents/skills/team/动漫组/马荣成 --strict
python3 scripts/aigc_skill_audit.py --strict
```

结果：

- `skill_context_audit`: discovered_skill_docs=1, failures=0
- `aigc_skill_audit`: failures=0, warnings=0

## Sanity Check

### 测试 1：已知事实型

Prompt：马荣成式怎么看《中华英雄》的动作分镜为什么影响港漫？

期望：

- 必须提及写实画功、电影动作转漫画关键帧、踢腿两格省略、复杂翻腾展开。
- 必须避免只说“热血”“霸气”。

验证：SKILL 的模型 1、2、3 与启发式 4、5 能覆盖。

### 测试 2：边缘推断型

Prompt：如果把《风云》改成竖屏短剧/短视频动画，马荣成式会怎么判断？

期望：

- 先抽视觉 DNA：人物剪影、招式、关系、黑白气势。
- 再改写媒介语法：竖屏构图、关键帧、动作省略、场景压缩。
- 明确不确定：马荣成本人未公开讨论该新媒介，属于基于模型推断。

验证：模型 6、字段 `ma.media_translation` 与诚实边界能覆盖。

### 测试 3：Voice Check

Prompt：这个武侠主角太平，帮我用马荣成视角改。

期望输出风格：

- 先指出“平”的画面原因：剪影、站姿、黑白关系、动作关键帧。
- 再给可执行画面修正，而不是武侠口号。
- 语气应是工艺型漫画顾问，不是江湖宗师。

验证：表达 DNA、Type Map 与 Repair Playbook 能覆盖。

## 后置精炼结论

本轮已应用的精炼点：

- 增加 `ma.fact_check` 字段，专门处理年份、销量、改编和最新动态的事实风险。
- 将“画神”表述降级为被批判对象，避免人格崇拜；转向基本功、练习和团队实践。
- 对《中华英雄》1980/1982 年份差异单独写入诚实边界与时间线。
- 将跨媒介改编从“IP 扩张”细化为“视觉 DNA 先行，再改媒介语法”。

残余风险：

- 公开长篇一手创作论有限，若未来获得完整访谈、演讲或书籍，应优先补 `references/research/02-conversations.md` 与表达 DNA。
