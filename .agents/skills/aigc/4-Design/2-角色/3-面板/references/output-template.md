# Output Template

## 1. 每角色 layout packet

```json
{
  "meta": {
    "project_name": "项目名",
    "episode_id": "第1集",
    "skill_id": "aigc/4-Design/2-角色/3-面板",
    "generated_at": "2026-04-12T12:00:00-07:00",
    "template_path": ".agents/skills/aigc/4-Design/2-角色/3-面板/templates/角色面板-提示词.json",
    "source_character_design": "projects/项目名/4-Design/2-角色/2-设计/第1集/character_design.json",
    "source_role_markdown": "projects/项目名/4-Design/2-角色/2-设计/第1集/角色名.md"
  },
  "subject": {
    "role_id": "role-001",
    "role_name": "角色名",
    "role_tier": "lead",
    "costume_state": "baseline",
    "identity_badge": "role-001+角色名",
    "group_portrait": false
  },
  "design_subject_source": "markdown_prompt_integration",
  "design_subject": "……",
  "prompt_payload": {
    "layout": {},
    "render_style_contract": {},
    "rule_profile": {},
    "prompt_segments": {},
    "prompt_text": "……"
  },
  "references": {
    "reference_images": [],
    "explicit_references": []
  },
  "render_contract": {
    "target_skill_id": "nano-banana-multiview-character",
    "render_mode": "CHARACTER_ATMOSPHERIC_DOSSIER",
    "aspect_ratio": "16:9",
    "layout": "three-column"
  },
  "output": {
    "packet_filename": "role-001-角色名-baseline-CharacterPanel-layout.json",
    "target_image_filename": "role-001-角色名-baseline-CharacterPanel.png"
  }
}
```

## 2. `_manifest.json`

```json
{
  "meta": {
    "project_name": "项目名",
    "episode_id": "第1集",
    "skill_id": "aigc/4-Design/2-角色/3-面板"
  },
  "inputs": {
    "character_design": "projects/项目名/4-Design/2-角色/2-设计/第1集/character_design.json",
    "template": ".agents/skills/aigc/4-Design/2-角色/3-面板/templates/角色面板-提示词.json"
  },
  "outputs": {
    "packet_files": [
      "role-001-角色名-baseline-CharacterPanel-layout.json"
    ],
    "manifest": "_manifest.json"
  },
  "selected_roles": [
    "role-001"
  ],
  "statistics": {
    "role_count": 1,
    "group_portrait_count": 0,
    "reference_image_count": 0
  },
  "handoff_targets": [
    "5-Image",
    "nano-banana-multiview-character"
  ]
}
```

## Hard Rules

1. 每个 packet 必须包含 `subject.identity_badge`。
2. `design_subject_source` 只能是 `markdown_prompt_integration` 或 `fallback_json_synthesis`。
3. `prompt_payload.prompt_text` 必须同时包含角色主体与 layout 约束。
4. `_manifest.json.statistics.role_count` 必须与实际 packet 数一致。
