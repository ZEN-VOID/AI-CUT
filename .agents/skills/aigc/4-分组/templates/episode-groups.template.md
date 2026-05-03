# Episode Groups Template

```markdown
---
项目名: <项目名>
集数: 第N集
stage: 4-分组
source_cinematography_path: projects/aigc/<项目名>/3-摄影/第N集.md
north_star_path: projects/aigc/<项目名>/0-初始化/north_star.yaml
output_path: projects/aigc/<项目名>/4-分组/第N集.md
grouping_policy: dialogue_4_to_6_and_target_1680_hard_1980_and_atomic_visual_unit
bridge_policy: paired_entry_exit_shots
review_status: pending
---

# 第N集分镜组

## 1-1-1

视频生成的画面风格，光影和氛围与场景参照图保持一致。不生成文字字幕和BGM，仅生成物理互动音效与环境和氛围音效。 <投影 north_star.yaml 全局风格.全局风格提示词原文>
<直引 north_star.yaml 类型元素.类型元素提示词>
<直引 north_star.yaml 细分风格.画面风格>

<从 3-摄影 划定的分镜剧本正文，同步原换行>

出场画面：
<1-2 秒非对白补位画面；与下一组入场画面一致>

```yaml
字数统计: 0字
角色:
  - <角色名>
场景:
  - <场景名>
道具:
  - <重要叙事道具>
```
```
