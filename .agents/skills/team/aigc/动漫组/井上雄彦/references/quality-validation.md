# 井上雄彦 Skill 质量验证

验证时间：2026-04-20  
验证对象：`../SKILL.md`

## 自动质量检查

命令：

```bash
python3 .agents/skills/team/aigc/动漫组/井上雄彦/scripts/quality_check.py \
  .agents/skills/team/aigc/动漫组/井上雄彦/SKILL.md
```

结果：6/6 通过。

| 检查项 | 结果 |
|---|---|
| 心智模型数量 | PASS：6 个心智模型 |
| 模型局限性 | PASS：每个模型均含局限 |
| 表达 DNA | PASS：13 项风格特征 |
| 诚实边界 | PASS：5 条 |
| 内在张力 | PASS：至少 2 处明确张力 |
| 一手来源占比 | PASS：12/17（71%） |

## 调研汇总检查点

命令：

```bash
python3 .agents/skills/team/aigc/动漫组/井上雄彦/scripts/merge_research.py \
  .agents/skills/team/aigc/动漫组/井上雄彦
```

结果摘要：

- 著作：6 个独立来源
- 对话：5 个独立来源
- 他者/机构：4 个独立来源
- 总来源数：15
- 信息不足维度：无

## 仓库合同检查

命令：

```bash
python3 scripts/skill_context_audit.py --root .agents/skills/team/aigc/动漫组/井上雄彦 --strict
python3 scripts/aigc_skill_audit.py --strict
```

结果：

- `skill_context_audit`: discovered_skill_docs=1, failures=0
- `aigc_skill_audit`: failures=1

说明：

- `aigc_skill_audit.py --strict` 的唯一失败项是仓库内既有问题：`.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/SKILL.md` 缺失，和本次新建的井上雄彦 skill 无直接关联。

## Sanity Check

### 测试 1：已知事实型

Prompt：井上雄彦式怎么看《THE FIRST SLAM DUNK》为什么不是简单复刻原作？

期望：

- 必须提到“新视点”“人物仍活着”“作者年龄带来的更新”。
- 必须避免只说技术升级或情怀回归。

验证：模型 3、5 与 `THE FIRST` / 文化庁评价足以覆盖。

### 测试 2：边缘推断型

Prompt：如果把一个现代轮滑竞技故事交给井上雄彦式来做，他会先看什么？

期望：

- 先看身体真实、视点选择、人物缺口和现场取材。
- 明确说明这是基于长期模型的推断，而不是本人公开说过的项目计划。

验证：模型 1、2、4 与启发式 1、3、5 能覆盖。

### 测试 3：Voice Check

Prompt：这个篮球主角太像热血模板了，帮我用井上雄彦视角改。

期望输出风格：

- 先指出身体与人物缺口，再给场面级修正。
- 语气应克制、具体，不是鸡血教练或玄学大师。

验证：表达 DNA、Type Map 与 Repair Playbook 能覆盖。

## 后置精炼结论

本轮已应用的精炼点：

- 把 skill 中的“井上感”明确从画风表层拉回到身体、视点、痛感与媒介重写。
- 将 2026-04-17 `REAL` 17 卷与 2026-04-18 `REAL × NEW ERA` 写入时间线，保证最新锚点清晰。
- 在 team 根索引与 registry / routes 中同步登记新成员，避免 skill 落盘后仍处于路由失联状态。

残余风险：

- 公开可直接抓取的一手长访谈仍偏少；若后续拿到《漫画がはじまる》全文、`THE FIRST SLAM DUNK` 官方完整访谈或更多日文长谈，应优先补强 `02-conversations.md` 与 `03-expression-dna.md`。
