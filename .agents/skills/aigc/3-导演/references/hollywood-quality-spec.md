# Hollywood Quality Specification

## Purpose

本规格包为 `3-导演` 提供"高质量但不越过保真"的质量标准参照。它定义了什么样的导演创作可以被视为好莱坞级质量，同时明确了哪些越权行为是禁止的。

## Quality Standards

### 允许的高质量创作

| quality dimension | indicator | example |
| --- | --- | --- |
| 戏剧实质深度 | 人物压力、选择、隐藏恐惧可见化 | 角色不是"害怕"，而是"手指压住纸角、呼吸变浅、避开视线" |
| 画面密度 | 画面可感知变量（道具、空间、光、声音）承托情绪 | 沉默不是空白，而是"灯管嗡鸣消失、笔尖悬停、群像迟半拍" |
| 节奏控制 | 从密到疏、从压迫到释放、从静到动 | 高潮前的等待、高潮后的余波 |
| 表演承托 | 演员有可执行的微表情、身体联动和道具动作 | 不只写"愤怒"，而写"咬肌绷紧、声音变硬、手背青筋凸起" |
| 视觉主轴 | 整集有可记忆的母题链和材质/色彩弧 | 纸面→火光→殷红→海雾压低 |

### 禁止的越权行为

| forbidden action | reason | example |
| --- | --- | --- |
| 新增剧情事实 | 破坏上游保真 | "新增角色背景故事" |
| 新增对白 | 改写上游正文 | "为角色添加内心独白对白" |
| 新增因果 | 改变事件逻辑 | "让角色因为新原因做出选择" |
| 新增桥段 | 增加上游没有的事件 | "新增追逐戏" |
| 摄影越权 | 越界到下游 5-摄影 | "写分镜编号、机位、景别、镜头运动" |
| 改写对白 | 改变角色语言 | "让角色说更高级的话" |
| 改写场景顺序 | 改变叙事结构 | "调整事件发生的先后" |
| 改写场景标题 | 改变场景功能 | "把场景改得更戏剧化" |

## Quality Evidence Fields

当 `hollywood_quality_notes` 被产出时，必须包含：

```yaml
hollywood_quality_notes:
  quality_dimension: ""  # 戏剧实质/画面密度/节奏控制/表演承托/视觉主轴
  upstream_anchor: ""     # 回指上游原文
  what_improved: ""       # 具体提升了什么
  fidelity_verified: true # 确认没有越权
  risk_check:
    no_new_fact: true
    no_new_dialogue: true
    no_new_causality: true
    no_photography_overreach: true
```

## Integration

- 由 `N3-DIR-SUBSTANCE` 消费，用于判断编导创作内核是否符合好莱坞质量标准
- 由 `N4-DIR-PEAK` 消费，用于判断高潮画面强化是否越权
- 由 `N9-DIR-DRAFT` 嵌入正文，不得以注释形式泄露
- 由 `N10-DIR-REVIEW` 验证 `hollywood_quality_notes` 是否有回指上游锚点和风险检查

## Review Checklist

- `hollywood_quality_notes` 是否回指上游原文？
- 提升的内容是否只改变表现层，不改变剧情层？
- 是否没有新增对白、事实、桥段或摄影方案？
- 证据是否包含风险检查？