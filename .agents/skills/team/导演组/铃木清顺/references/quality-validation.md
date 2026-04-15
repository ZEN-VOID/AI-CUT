# 铃木清顺 Skill 质量验证

验证时间：2026-04-15

## 自动检查

### 女娲质量检查

命令：

```bash
python3 .agents/skills/team/导演组/铃木清顺/scripts/quality_check.py .agents/skills/team/导演组/铃木清顺/SKILL.md
```

结果：6/6 通过。

| 检查项 | 结果 |
|---|---|
| 心智模型数量 | PASS：6 个 |
| 模型局限性 | PASS |
| 表达DNA辨识度 | PASS |
| 诚实边界 | PASS：6 条 |
| 内在张力 | PASS：5 处 |
| 一手来源占比 | PASS |

### 调研摘要检查

命令：

```bash
python3 .agents/skills/team/导演组/铃木清顺/scripts/merge_research.py .agents/skills/team/导演组/铃木清顺
```

结果：来源数 21，信息不足维度：无。

修正记录：首次运行时来源数显示为 0，因为 URL 只集中在 `00-source-index.md`，而脚本只扫描 `01-06` 调研文件。已在每个维度文件补 `Sources` 小节，并在 `CONTEXT.md` 记录为可复用经验。

### Context 审计

命令：

```bash
python3 scripts/skill_context_audit.py --root .agents/skills/team/导演组/铃木清顺 --strict
```

结果：发现 1 个 `SKILL.md`，failures: 0。

## 语义测试

### Sanity 1：`Tokyo Drifter`

预期：不会只说“很酷/很彩色”，而会指出黑帮类型入口、歌谣、白场、纯色空间、明星姿态和类型规则被抽象化。

通过点：`SKILL.md` 模型 1、2、5 和启发式 1、3、6 均覆盖。

### Sanity 2：`Branded to Kill`

预期：不会只说“不可理解”，而会说明杀手等级、任务、气味、物件、身体失控、断裂剪辑和工业越界成本。

通过点：`SKILL.md` 模型 1、3、4、5 和启发式 4、5、9 均覆盖。

### Sanity 3：`Zigeunerweisen`

预期：不会把后期作品当成日活时期风格重复，而会指出流亡后类型速度转为梦、记忆、古董空间、死亡和仪式。

通过点：`SKILL.md` 模型 6 和 `CONTEXT.md` 的“晚期梦幻”类型映射覆盖。

### Edge Case：当代 AI 短片想做“清顺感”

预期：应提醒这不是随机怪异图像，而是“类型入口 + 一条规则失控 + 感官符号回环 + 制作/平台边界”；不能声称铃木清顺本人会怎么看 AI。

通过点：诚实边界、Agentic Protocol 和制作风险字段覆盖。

### Voice Check

100 字测试方向：

> 这场戏太顺了。先别解释杀手为什么回来，给他一个入口：他必须进那间白房间。然后让墙先变色，声音提前半拍进来，枪不响，电话响。观众还知道这是追杀，但规则已经坏了。不要全片都怪，只坏这一条。

判断：短促、具体、有类型入口、破坏点和可拍场面，不是通用影评。
