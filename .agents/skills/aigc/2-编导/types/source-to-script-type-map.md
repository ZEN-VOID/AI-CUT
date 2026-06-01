# Source To Script Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。

## Type Profile Variables

| variable | values | detection cue | strategy |
| --- | --- | --- | --- |
| `source_shape` | `plain_novel` / `sectioned_episode` / `mixed_frontmatter_body` | 是否含 frontmatter、`【剧本正文】`、章节标题 | 只把正文真源作为改编对象，frontmatter 用于证据 |
| `dialogue_density` | `low` / `medium` / `high` | 中文双引号对白数量 | 高密度时先冻结对白清单，再补 `对白画面` |
| `system_rule_density` | `low` / `medium` / `high` | 系统提示、规则条目、公告、黑板文字、好感度等 | 使用 `系统画面`、`规则显影`、`旁白（系统提示）` |
| `inner_pressure_density` | `low` / `medium` / `high` | 感觉、意识到、记起、推理、恐惧、判断 | 投影为独白、内心独白、可感知心理反应、可执行表演提示；心理反应不得停留在抽象内心解释 |
| `location_pattern` | `single_location_multi_beat` / `multi_location` | 地点和日夜是否变化 | 单地点多 beat 不重复 slugline；多地点按空间变化新开场 |
| `sound_design_load` | `low` / `high` | 铃声、脚步声、机械音、哭声、尖叫、广播 | 每条音效必须配 `音效画面` |
| `disaster_cutaway_load` | `none` / `present` | 国运、新闻碎片、现实灾难、外部世界后果 | 用短促 `现实灾难画面` 或 `系统画面` 插针 |
| `subtext_load` | `low` / `medium` / `high` | 试探、隐瞒、不信任、心虚、保护、施压、求证、不能直说 | 在编剧层只保留上游潜台词事实与主角内心独白，不做表演行为化；行为化交给 `2-编导` performance layer |
| `screenplay_enhancement_request` | `none` / `format_repair` / `authorized_adaptation_requested` | 用户是否要求新增式、适当增强、更影视化、新对白/新桥段 | `format_repair` 只修字段与可拍性；`authorized_adaptation_requested` 不进入 canonical，必须阻断或另行授权候选稿 |

## Route Matrix

| type_profile | required references | review emphasis |
| --- | --- | --- |
| `dialogue_density=high` | `field-routing-and-audio-visual-contract.md` | 对白冻结、引号内无动作 |
| `system_rule_density=high` | `field-routing-and-audio-visual-contract.md`、`hollywood-quality-spec.md` | 系统提示主体、规则可视化 |
| `inner_pressure_density=high` | `script-adaptation-contract.md`、`field-routing-and-audio-visual-contract.md`、`novel-to-screen-language-contract.md` | 内视不进入动作画面；主角视角判断优先进入 `内心独白（主角）` 或可拍反应；对白不改原意 |
| `location_pattern=single_location_multi_beat` | `script-adaptation-contract.md` | 同 slugline 去重 |
| `sound_design_load=high` | `field-routing-and-audio-visual-contract.md` | 音效与音效画面配对 |
| `disaster_cutaway_load=present` | `hollywood-quality-spec.md` | 压力插针短促，不挤占主叙事 |
| `subtext_load=high` | `novel-to-screen-language-contract.md` | 保留上游主观判断与未出口信息，不新增对白；表演行为化交给 `2-编导` performance layer |
| `screenplay_enhancement_request=authorized_adaptation_requested` | `script-adaptation-contract.md` | 阻断 canonical；提示需要另行授权候选稿 |

## Type Profile Output

执行前形成最小画像：

```yaml
type_profile:
  source_shape: mixed_frontmatter_body
  dialogue_density: high
  system_rule_density: medium
  inner_pressure_density: high
  location_pattern: single_location_multi_beat
  sound_design_load: high
  disaster_cutaway_load: present
  subtext_load: high
  screenplay_enhancement_request: none
```

`type_profile` 只决定投影策略，不允许决定删减上游事实。
