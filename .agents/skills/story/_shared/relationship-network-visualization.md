# Character Relationship Network Visualization Contract

本文件是 `story2026` 的人物关系网络可视化合同。定义基于角色卡和人物状态快照的关系网络数据格式，供工具/脚本生成可视化图谱。

本文件不拥有正文写权，不是独立阶段。关系图谱数据由 `return` 阶段在卷完成时增量生成。

## Core Data Model

### Node Schema（人物节点）

```yaml
nodes:
  - id: "char_001"
    name: "主角A"
    role: "protagonist"           # protagonist/antagonist/supporting/minor
    faction: "势力A"
    status: "active"              # active/inactive/deceased/unknown
    current_power_level: 5        # 当前能力等级（如有）
    emotional_state: "焦虑"
    volume_appearances: [1,2,3]   # 出场卷号
    chapter_appearances: [1,3,5,7,8,9]  # 出场章号
    bio_summary: "前朝遗孤，身负血仇，在水源村隐姓埋名三年"
```

### Edge Schema（关系边）

```yaml
edges:
  - source: "char_001"
    target: "char_002"
    relationship_type: "alliance"  # alliance/enmity/family/romance/mentor/rival/neutral
    intensity: 0.7                 # 0.0-1.0 关系强度
    trust_level: 0.6              # 0.0-1.0 信任度
    history:
      - volume: 1
        event: "初次相遇"
        delta: {intensity: 0.3, trust: -0.2}  # 初始不信任
      - volume: 2
        event: "共同对抗BossX"
        delta: {intensity: 0.5, trust: 0.6}   # 并肩作战后信任上升
    current_tension: "隐忧"        # 当前关系中的紧张因素
    expected_trajectory: "上升"    # 上升/下降/稳定/不确定
```

### Volume Relationship Delta（卷级关系变化）

```yaml
volume_relationship_delta:
  volume: 3
  changes:
    - edge: ["char_001", "char_003"]
      before: {relationship_type: "neutral", intensity: 0.1}
      after: {relationship_type: "enmity", intensity: 0.8}
      trigger_event: "揭露身份"
      narrative_significance: "主角的真实身份被配角C发现，C的立场因家族利益转向敌对"
```

## Visualization Contract

### 生成时机
- 每卷 `return` actualization 完成后
- 输出位置：`projects/story/<项目名>/visualizations/relationship-network-v{V卷号}.json`

### 建议可视化方式
- 力导向图（Force-directed graph）：展示人物群落结构和核心节点
- 节点大小：按出场频率/剧情重要性
- 边粗细：按关系强度
- 边颜色：按关系类型（联盟=蓝、敌对=红、亲情=绿、爱情=粉、师徒=紫）
- 节点颜色：按势力/派系
- 时间轴动画：展示关系强度随卷演进的动态变化

### Token Budget
- 图谱数据生成：≤500 tokens/卷
- 不加载完整角色卡，使用 `character-planning-bridge.md` 的结构化摘要
