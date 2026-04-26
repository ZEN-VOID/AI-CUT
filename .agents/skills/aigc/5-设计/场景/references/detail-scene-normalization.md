# Detail Scene Normalization

## Purpose

本文件是 `5-设计/场景` 的局部细则真源。

它解决两类问题：

1. 当前仓 `3-Detail` shot fields 应如何稳定抽出主场景家族。
2. 旧仓 `场景研究 / scene bridge / quality` 应如何折叠进当前单 catalog。

## Legacy -> Current Mapping

| legacy carrier | current landing |
| --- | --- |
| `场景清单.json.scenes[]` | `场景清单.json.scenes[]` |
| `场景研究.json.scenes[].evidence_ledger` | `场景研究.json.scenes[].evidence_ledger` |
| `场景研究.json.scenes[].detail_profile / architecture_profile / scene_blueprint` | `场景研究.json.scenes[].detail_profile / scene_blueprint` |
| `场景研究.json.scenes[].scene_bible_card / display_profile / compendium` | `场景研究.json.scenes[].scene_bible_card / display_profile / compendium` |
| `scene_design_bridge.json.scenes[].design_bridge_profile` | `scene_design_bridge.json.scenes[].design_bridge_profile` |
| `场景研究.json.quality_overview` | `场景研究.json.quality_overview` 与 `场景清单.json.statistics.quality_overview` 摘要回显 |

## Scene Extraction Priority

1. 主锚优先认 `分镜明细[].氛围表现.层次` 中可复用的空间实体。
2. `分镜明细[].分镜构图 / 摄影美学` 负责补足 framing、色光与材质，不单独发明新场景。
3. `角色背景面 / 分镜表现 / 摄影美学 / 时间段 / 组间设计.导演意图` 只做 fallback 补证。
4. `剧本正文` 只在主锚抽取失败时回退解歧。

## Main Scene vs Variant

### 主场景家族

- 广场、池、走廊、楼道、楼梯间、电梯、门厅、庭院、街巷、殿堂、码头、山路、河岸等可复用空间实体
- 要求能跨镜复用
- 要求适合成为 `scene_name`

### 变体层

- 方位：东侧、西侧、门内、门外、窗边、尽头、外缘
- 边界：门禁、隔断、转角、桥位、台阶
- 状态：清晨、深夜、停电、警报、潮湿、余烬
- 气氛：压迫、松弛、静默、危险前兆

这些内容默认进：

- `group_scene_map[].scene_variant`
- `design_context.scene_blueprint.variable_state_layer`

## Folded Design Context Minimum

每个 scene 的 `场景研究.json` 研究条目最低必须包含：

1. `evidence_ledger`
2. `detail_profile`
3. `scene_blueprint`
4. `scene_bible_card`
5. `display_profile`
6. `compendium`
7. `quality_profile`

每个 scene 的 `scene_design_bridge.json` 桥接条目最低必须包含：

1. `design_bridge_profile`
2. `prompt_anchor`
3. `fixed_anchor_bridge`
4. `variable_state_bridge`
5. `negative_constraints`
6. `quality_flags`

## Quality Gate

以下任一情况出现时，必须落 `quality_flags` 或 `needs_manual_review`：

- `scene_name` 仍是完整背景句
- branch-owned 主锚为空时直接跳到 legacy 背景句，导致 canonical scene family 又被 compatibility projection 抢走
- 证据只剩单条弱文本
- 建筑/空间/材质/色光/拓扑全部缺失
- bridge 只有 prose，没有机读 handoff 字段

## Failure Closure

若出现以下症状，优先回到本文件再检查主 `SKILL.md`：

- 场景数量暴涨到接近镜头数
- canonical scene name 出现大量背景残句
- 旧仓 research 字段被拆回并列 sidecar
- `2-设计/场景` 仍需手工重组 prompt bridge
