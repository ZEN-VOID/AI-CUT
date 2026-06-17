# Cross-Project Experience Reuse Contract

本文件是 `story2026` 的跨项目创作经验复用合同。定义如何在多个小说创作项目之间沉淀、共享和检索创作经验，让后来的项目从前面项目的实践中受益。

本文件不拥有正文写权，不是独立阶段。

## Core Principle

每个小说创作项目会产出两类可复用资产：
1. **显式资产**：技能包中的合同/规则/检查清单（这些是跨项目通用的，已沉淀在 `.agents/skills/story/` 中）
2. **隐式资产**：项目级别的经验模式——"这个题材的读者喜欢什么""这个类型的陷阱在哪里""这个写作技巧在类似场景中反复被证实有效"

本合同聚焦于隐式资产的沉淀和复用。

## Experience Data Model

### 项目经验卡（Project Experience Card）

每完成一个项目的创作（或达到重要里程碑），生成一张经验卡：

```yaml
project_experience_card:
  project_id: "浪花传说之琉球篇"
  genre: "都市异能"
  sub_genre: "悬疑"
  total_volumes: 8
  total_chapters: 80
  completion_status: "completed"  # completed/drafting/hiatus
  
  # 创作统计
  stats:
    avg_chapter_length: 3500
    avg_acceptance_score: 7.2
    rework_rate: 0.15            # 返工率
    most_reworked_dimension: "presence_texture"
    most_stable_dimension: "structure_realization"
  
  # 题材经验
  genre_insights:
    - category: "读者偏好"
      insight: "都市异能读者对'隐藏身份被揭露'场景的期待远高于纯战斗场景"
      confidence: "high"
      evidence: "8次读者互动反馈 + 章节阅读数据"
    - category: "陷阱"
      insight: "异能体系过度解释（每次新能力都上说明书）导致读者跳过率上升"
      confidence: "high"
      evidence: "3-5卷的读者反馈趋势"
    - category: "有效技巧"
      insight: "将异能限制与日常生活绑定（比如能力使用后需要大量进食）增加了真实感"
      confidence: "medium"
      evidence: "第2卷读者好评集中出现"
  
  # 人物经验
  character_insights:
    - archetype: "冷面导师"
      effective_patterns: ["不解释动机但行动一致", "关键救援不留名"]
      failed_patterns: ["突然变温柔", "长篇解释自己的过去"]
      
  # 节奏经验
  rhythm_insights:
    - pattern: "都市异能最佳节奏"
      description: "3章异世界/异能事件 + 1-2章日常生活/关系发展"
      effectiveness: "high"
      
  # 失败经验
  lessons_learned:
    - lesson: "前期能力体系设计太开放导致后期失控"
      prevention: "在1-设定阶段锁定能力体系的上限和例外规则"
      severity: "critical"
```

### 经验知识图谱

```yaml
experience_knowledge_graph:
  nodes:
    - type: "project"
      id: "project_001"
    - type: "genre"
      id: "genre_urban_ability"
    - type: "technique"
      id: "tech_hide_identity"
    - type: "pattern"
      id: "pattern_3_1_rhythm"
  
  edges:
    - source: "project_001"
      target: "genre_urban_ability"
      type: "belongs_to"
    - source: "project_001"
      target: "tech_hide_identity"
      type: "effectively_used"
    - source: "project_001"
      target: "pattern_3_1_rhythm"
      type: "verified_effective"
      confidence: "high"
```

## Usage Patterns

### 新项目启动时
1. 按 `north_star.genre_contract` 匹配相同题材的历史项目经验卡
2. 加载与当前项目最相关的经验 insights（题材经验 + 节奏经验 + 陷阱警示）
3. 在 `0-初始化` 阶段将相关经验注入 MEMORY.md

### 创作过程中
1. 遇到特定类型场景（如"感情线首次冲突"）时，检索历史项目中该场景类型的高效写法
2. 遇到同样问题时，参考类似问题的历史解决方案

### 项目完成时
1. 汇总全卷验收数据生成经验卡
2. 提取关键 insights（筛选 confidence ≥ medium）
3. 将验证有效的经验晋升到对应题材包的 `knowledge-base/`

## Storage

### 存储位置
- 经验卡：`projects/story/_experiences/`（所有项目共享）
- 按题材索引：`projects/story/_experiences/by-genre/{题材名}/`
- 按技巧索引：`projects/story/_experiences/by-technique/{技巧名}/`

### Token Budget
- 经验卡生成：项目完成时一次性工作，≤2000 tokens
- 经验检索：新项目启动时加载最相关 3-5 条 insights，≤500 tokens
- 不参与每章创作时的上下文加载

## Elevation Path

当经验被 ≥3 个项目验证有效后：
1. 将经验从项目级晋升到题材包级（`3-初稿/types/网文/{题材名}/knowledge-base/`）
2. 在对应的 `CONTEXT.md` 中增加引用
3. 项目经验卡中标记"已晋升"，避免重复维护

## 与 Skill Learning Writeback 的关系

- `/SKILL.md 中的 Learning / Context Writeback`：单项目内的经验学习（短周期）
- 本合同的经验复用：跨项目的经验沉淀（长周期）
- 两者的接口：当 Learning Writeback 中的稳定规则被多个项目验证有效后，通过本合同晋升到共享层
