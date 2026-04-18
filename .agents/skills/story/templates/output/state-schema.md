# state.json 结构说明

> 该文件为运行态精简状态，避免体量膨胀。实体等大数据存于 index.db。
>
> 以下示例与 `update_state.py` 当前校验字段保持一致。
>
> 说明：章节编排、任务、线索、伏笔等规划真源不写入 `state.json`，默认读取 `Planning/8-全息地图.json`。
>
> 执行态补充说明：任务断点与 run registry 不写入本文件，分别写入 `.webnovel/workflow_state.json`、`.webnovel/execution_state.json` 与 `.webnovel/task_log.jsonl`。

```json
{
  "project_info": {
    "title": "",
    "genre": "",
    "target_words": 0,
    "target_chapters": 0
  },
  "progress": {
    "current_chapter": 0,
    "total_words": 0,
    "last_updated": "",
    "volumes_completed": [],
    "current_volume": 1,
    "volumes_planned": [
      {"volume": 1, "chapters_range": "1-100", "planned_at": "2026-02-01"}
    ]
  },
  "protagonist_state": {
    "name": "",
    "power": {"realm": "", "layer": 0, "bottleneck": ""},
    "location": {"current": "", "last_chapter": 0},
    "golden_finger": {"name": "", "level": 0, "cooldown": 0}
  },
  "relationships": {},
  "world_settings": {
    "power_system": [],
    "factions": [],
    "locations": []
  },
  "review_checkpoints": [
    {"chapters": "1-5", "report": "Validation/第1-5章审查报告.md", "reviewed_at": "2026-02-26 20:00:00"}
  ],
  "strand_tracker": {
    "last_quest_chapter": 0,
    "last_fire_chapter": 0,
    "last_constellation_chapter": 0,
    "current_dominant": "quest",
    "chapters_since_switch": 0,
    "history": []
  },
  "plot_threads": {
    "active_threads": [],
    "foreshadowing": []
  },
  "disambiguation_warnings": [],
  "disambiguation_pending": [],
  "chapter_meta": {
    "0001": {
      "hook": {"type": "危机钩", "content": "...", "strength": "strong"},
      "pattern": {
        "opening": "冲突开场",
        "hook": "危机钩",
        "emotion_rhythm": "低→高",
        "info_density": "medium"
      },
      "ending": {"time": "夜晚", "location": "宗门大殿", "emotion": "紧张"}
    }
  }
}
```
