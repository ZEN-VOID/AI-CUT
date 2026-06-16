# Episode Groups Template

```markdown
---
项目名: <项目名>
集数: 第N集
stage: 8-分组
source_camera_path: projects/aigc/<项目名>/7-摄影/第N集.md
visual_tone_path: projects/aigc/<项目名>/2-美学/画面基调/全局风格协议.md
north_star_path: projects/aigc/<项目名>/0-初始化/north_star.yaml
output_path: projects/aigc/<项目名>/8-分组/第N集.md
grouping_policy: lighting_shot_line_sum_target_14_5s_band_10_14_5s_hard_max_14_5s_end_on_half_second_source_override_supported
first_storyboard_line_policy: hulong_frame_tail_state_anchor_and_sound_folded_into_normal_timecoded_line
review_status: pending
---

# 第N集分镜组

## 1-1-1

场景1：<场景标题>

全局风格：
视频生成的画面风格，光影和氛围与场景参照图保持一致。需要生成现场物理互动音效、氛围感音效、环境声、自然现象声、动作声，不要生成任何字幕，不要生成背景音乐。<根据当前分镜组场景类型、光影、色彩、材质、动作和摄影证据，从 2-美学/画面基调/全局风格协议.md 的 Global Style Prompt 整理出的自然语句，300字以内>

分镜1（0-N.5秒）：<按普通分镜画面语言整理本组开始画面，并保留上游摄影/光影信息；只写可见主体、动作、场景、关键道具、空间关系、声音余波和光线，不写特殊字段、来源说明或规则说明；本组最终累计结束秒必须以 .5 结尾>
<从 7-摄影 划定的后续分镜行，同步原换行；正文中的 `分镜N（起始秒-结束秒）：` 按当前分镜组从 0 连续累加改写>

```yaml
字数统计: 0字
时长估算: 约0秒
角色:
  - id: CHR-001
    name: <subject-registry canonical_name>
场景:
  - id: SCN-001
    name: <subject-registry canonical_name>
道具:
  - id: PRP-001
    name: <subject-registry canonical_name>
```

## 1-1-2

场景1：<同上一组时重复同一场景标题；若已切到下一场则写对应场景标题>

全局风格：
视频生成的画面风格，光影和氛围与场景参照图保持一致。需要生成现场物理互动音效、氛围感音效、环境声、自然现象声、动作声，不要生成任何字幕，不要生成背景音乐。<根据当前分镜组场景类型、光影、色彩、材质、动作和摄影证据，从 2-美学/画面基调/全局风格协议.md 的 Global Style Prompt 整理出的自然语句，300字以内>

分镜1（0-N.5秒）：<按回龙帧口径先复现上一组尾帧状态锚点：可见主体、动作/姿态/运动余势、关键道具/介质/环境残留、光线/烟雾/水汽/碎片/声音余波、保护线/战斗线/空间方位关系；再只调整景别和镜头视角进入本组开始画面；若该点来自对白画面、独白画面、旁白画面或音效画面，同步带入对应声音内容；只写画面和必要声音，不写特殊字段、来源说明或规则说明；本组最终累计结束秒必须以 .5 结尾>
<从 7-摄影 划定的下一组分镜行，同步原换行；正文中的 `分镜N（起始秒-结束秒）：` 按当前分镜组从 0 连续累加改写>

```yaml
字数统计: 0字
时长估算: 约0秒
角色: []
场景: []
道具: []
```
```
