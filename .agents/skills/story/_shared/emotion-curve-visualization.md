# Emotion Curve & Rhythm Waveform Visualization Contract

本文件是 `story2026` 的情绪曲线与节奏波形可视化合同。定义基于章级 planning 和验收数据的情绪/节奏量化格式，供生成可视化图表。

本文件不拥有正文写权，不是独立阶段。

## Core Data Model

### Chapter Rhythm Data Point（章级节奏数据点）

每章生成一个数据点：

```yaml
chapter_rhythm_point:
  chapter_ref: "第3卷/第5章"
  global_chapter_num: 25
  rhythm_intensity: 7             # 0-10, from planning
  selected_mode: "动能式"          # 势能式/动能式/浪能式
  payoff_type: "行动"
  reader_pull_score: 6            # 0-10, from acceptance
  prose_reader_pull: 6
  emotion_trajectory:              # 本章内情绪走向
    start: "紧张(7)"
    peak: "释放(9)"
    end: "余韵+不安(5)"
  strand_activities:               # 三条线活跃度
    main: 8                        # 0-10
    romance: 2
    world: 3
  events_summary: "攻破山寨→发现被囚禁的神秘人→山寨引爆→逃出"
```

### Volume Waveform Aggregate（卷级波形聚合）

```yaml
volume_waveform:
  volume_ref: "第3卷"
  chapter_count: 10
  chapters: [<Chapter Rhythm Data Point>, ...]
  waveform_metrics:
    avg_intensity: 5.4
    intensity_variance: 4.8
    mode_distribution:
      势能式: 4
      动能式: 4
      浪能式: 2
    consecutive_high_chapters: 0    # 连续高强度章数（≥3则警告）
    hook_continuity_score: 8        # 钩子连续性 0-10
  strand_metrics:
    main_line_avg_activity: 7.2
    romance_line_avg_activity: 3.1
    world_line_avg_activity: 2.8
    strand_balance_score: 6         # 0-10, 三线平衡度
```

## Visualization Contract

### 1. 情绪曲线图（Emotion Curve）

- **X轴**：章号（全局或卷内）
- **Y轴**：情绪强度（0-10）
- **曲线**：使用本章的 `emotion_trajectory` 数据绘制
- **标注**：
  - 章标签 + payoff_type 图标
  - 关键事件简注（如"Boss战"/"身份揭露"/"休整"）
- **颜色编码**：势能式=蓝、动能式=红、浪能式=绿

### 2. 节奏波形图（Rhythm Waveform）

- **X轴**：章号
- **Y轴**：rhythm_intensity
- **叠加**：
  - 柱状图：rhythm_intensity
  - 折线图：reader_pull_score（虚线叠加）
  - 阴影区域：高强度（>7）/低强度（<4）
- **模式标签**：在每章上方标注 selected_mode
- **对比**：上一卷波形叠加为灰色参考线

### 3. Strand 活跃度热力图

- **X轴**：章号
- **Y轴**：三条线
- **颜色深度**：按 strand_activities 的值（0-10）
- **缺席警示**：连续缺席超过阈值的章用红色边框标记

## Generation & Output

### 生成时机
- 每卷 `return` actualization 完成后
- 输出位置：`projects/story/<项目名>/visualizations/rhythm-waveform-v{V卷号}.json`

### Token Budget
- 波形数据生成：≤400 tokens/卷
- 使用 planning 摘要和验收包数据，不加载正文原文
