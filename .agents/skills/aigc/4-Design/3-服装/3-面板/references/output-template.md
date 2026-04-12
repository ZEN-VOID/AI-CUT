# Output Template

## 1. 每服装 layout packet

```json
{
  "meta": {
    "project_name": "项目名",
    "episode_id": "第1集",
    "skill_id": "aigc/4-Design/3-服装/3-面板",
    "source_design": "projects/项目名/4-Design/3-服装/2-设计/第1集/服装设计.json"
  },
  "subject": {
    "costume_id": "costume-role-001-baseline",
    "canonical_label": "角色名-常服",
    "identity_badge": "costume-role-001-baseline+角色名-常服"
  },
  "layout_contract": {
    "template_type": "COSTUME_SYSTEM_DOSSIER",
    "aspect_ratio": "16:9"
  },
  "prompt_segments": {
    "identity_prompt": "",
    "layout_prompt": "",
    "negative_prompt_global": ""
  },
  "output": {
    "packet_filename": "costume-role-001-baseline-角色名-常服-CostumePanel-layout.json",
    "target_image_filename": "costume-role-001-baseline-角色名-常服-CostumePanel.png"
  }
}
```
