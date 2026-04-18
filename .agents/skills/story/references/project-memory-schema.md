# `.webnovel/project_memory.json` Schema

`project_memory.json` 用于保存**已经被验证过的正向经验**，可由手工维护或专门工具按需沉淀。

它不是过程日志，而是项目级可复用 heuristic 库。

## 推荐结构

```json
{
  "schema_version": "story2026/project-memory/v2",
  "patterns": [
    {
      "id": "hook-crisis-0100",
      "pattern_type": "hook",
      "heuristic": "当卷末前两章已经抬高外部压力时，章末用选择钩比纯危机钩更能拉住追读。",
      "applicable_scope": {
        "genres": ["xuanhuan", "shuangwen"],
        "stage": "3-Drafting",
        "chapter_range_hint": "卷末前2章"
      },
      "evidence_refs": [
        "正文/第0100章.md",
        "Validation/第100-100章审查报告.md"
      ],
      "source_chapter": 100,
      "validated_at": "2026-04-06T10:00:00Z",
      "promotion_scope": "project-only"
    }
  ]
}
```

## Pattern 字段

| 字段 | 说明 |
|---|---|
| `id` | 稳定标识，建议 `type-topic-chapter` |
| `pattern_type` | `hook / pacing / dialogue / payoff / emotion / structure / style` |
| `heuristic` | 可复用启发式，不写流水账 |
| `applicable_scope` | 适用题材、阶段、章节区间等 |
| `evidence_refs` | 至少一条正文或审查证据路径 |
| `source_chapter` | 来源章节 |
| `validated_at` | 被确认有效的时间 |
| `promotion_scope` | `project-only / cross-project-candidate / skill-candidate` |

## 写入规则

- 只追加 milestone 级成功模式。
- 避免重复写入同义 heuristic。
- 若只是一次偶然好用但尚未验证，不应进入本文件。
