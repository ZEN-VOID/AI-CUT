# Episode Motion Template

```markdown
---
stage: 3-运动
source_path: projects/aigc/<项目名>/2-编导/第N集.md
output_path: projects/aigc/<项目名>/3-运动/第N集.md
---

# 第N集

【剧本正文】

<!-- 生产稿保留 source 原字段名与顺序，只替换或扩写冒号后的字段值。 -->
<同一 source 字段名>：<扩写后的字段值>

<!-- 不新增独立 `运动强化：` 或任何对照标签；每个被扩写字段需满足：motion_subject / start_point / path / end_point / reference_frame；同一场景或连续动作段尽量沿用同一 primary_reference_frame；只有输入源显式已有分镜组时才继承源内组边界 -->
```
