# Canonical Outputs

## 1. episode 级 `场景面板.json`

路径：

`projects/<项目名>/4-Design/1-场景/3-面板/第N集/场景面板.json`

最小骨架：

```json
{
  "meta": {
    "project_name": "项目名",
    "episode_id": "第1集",
    "source_scene_design": "projects/<项目名>/4-Design/1-场景/2-设计/第1集/场景设计.json",
    "skill_id": "aigc/4-Design/1-场景/3-面板",
    "generated_at": "2026-04-12T12:00:00-07:00"
  },
  "layout_contract": {
    "aspect_ratio": "16:9",
    "panel_count": 9,
    "grid": "3x3"
  },
  "panels": [
    {
      "scene_key": "ancient-hall--night",
      "scene_name": "皇城大殿",
      "scene_variant": "夜",
      "identity_badge": "ancient-hall--night + 皇城大殿",
      "source_scene_ids": [
        "1-1-10-1"
      ],
      "panel_prompt": "",
      "negative_prompt": "",
      "panel_handoff": "",
      "layout_path": "projects/<项目名>/4-Design/1-场景/3-面板/第1集/ancient-hall--night-layout.json",
      "design_markdown_path": "projects/<项目名>/4-Design/1-场景/2-设计/第1集/ancient-hall--night.md"
    }
  ]
}
```

## 2. per-scene `*-layout.json`

路径：

`projects/<项目名>/4-Design/1-场景/3-面板/第N集/<scene_key>-layout.json`

最小骨架：

```json
{
  "meta": {
    "project_name": "项目名",
    "episode_id": "第1集",
    "scene_key": "ancient-hall--night",
    "scene_name": "皇城大殿",
    "source_scene_design": "projects/<项目名>/4-Design/1-场景/2-设计/第1集/场景设计.json"
  },
  "subject": {
    "scene_key": "ancient-hall--night",
    "scene_name": "皇城大殿",
    "scene_variant": "夜",
    "identity_badge": "ancient-hall--night + 皇城大殿",
    "source_scene_ids": [
      "1-1-10-1"
    ]
  },
  "layout_contract": {
    "aspect_ratio": "16:9",
    "panel_count": 9,
    "grid": "3x3"
  },
  "prompt": "",
  "negative_prompt": "",
  "panel_handoff": "",
  "output_hint": {
    "downstream_stage": "5-Image",
    "suggested_filename": "ancient-hall--night-ScenePanel.png"
  }
}
```

## 3. `_manifest.json`

```json
{
  "episode_id": "第1集",
  "selected_scene_keys": [
    "ancient-hall--night"
  ],
  "source_inputs": [],
  "output_files": [],
  "review_status": "pass"
}
```

## Hard Rules

1. `场景面板.json` 必须覆盖本轮命中的所有场景，顺序与 `场景设计.json.scene_designs[]` 的命中顺序一致。
2. 每个 `panels[].layout_path` 必须对应一个实际存在的 `<scene_key>-layout.json`。
3. `identity_badge` 必须稳定包含 `scene_key + scene_name`。
4. `panel_prompt` 不得为空，且必须可回链到 `final_scene_prompt / panel_handoff`。
