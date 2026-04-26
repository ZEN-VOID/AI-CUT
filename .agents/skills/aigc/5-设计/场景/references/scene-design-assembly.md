# Scene Design Assembly Rules

本文件是 `5-设计/场景` 的复杂装配细则。主 `SKILL.md` 持有入口、字段、门禁与输出真源；本文件只解释如何把上游三真源、`0-Init` 与 `2-Global` 装配成场景设计包。

## Source Assembly Order

| source | role | hard rule |
| --- | --- | --- |
| `场景清单.json.scenes[]` | 场景对象池、identity、coverage、scene_type 第一来源 | 不得被 research / bridge 改名 |
| `场景研究.json.scenes[]` | evidence、detail_profile、scene_blueprint、compendium、quality_profile | 缺失时从 catalog `design_context` 保守补证并标记 `research_degraded` |
| `scene_design_bridge.json.scenes[]` | fixed_anchor_bridge、variable_state_bridge、prompt_anchor、negative_constraints | 缺失时从 research/catelog 降级推断并标记 `bridge_degraded` |
| `0-Init/*.yaml` | story premise、world mode、anti-goals、emotional north star | 不覆盖场景主键 |
| `2-Global/*.md` | Style Backbone、类型元素、设计元素、导演偏置 | 不覆盖对象池 |

## Matching Rules

1. 首选 `scene_id` 精确匹配。
2. 其次用 `scene_key / scene_name` 匹配。
3. 再其次用 `aliases[] / first_appearance.group_id / first_appearance.shot_id` 辅助匹配。
4. 匹配冲突时，以 `场景清单.json` 的 identity 为准；research / bridge 只能补证，不能反向改名。

## Design Packet Minimum Shape

每个 scene 进入 synthesis 前至少应形成：

```json
{
  "scene_id": "SCENE-001",
  "scene_name": "社区中央广场",
  "scene_type": "exterior",
  "story_premise": "...",
  "style_backbone": "...",
  "scene_style": "...",
  "direction_anchor": "...",
  "negative_guardrails": ["..."],
  "compendium": "...",
  "fixed_anchor_bridge": {},
  "variable_state_bridge": {},
  "prompt_anchor": {},
  "quality_flags": [],
  "source_trace": {}
}
```

缺字段时不得臆造。允许写 `TBD`，但必须同步写入 `quality_flags[]` 与 `_manifest.json.notes`。

## Three-Layer Convergence

thinking sidecar 固定使用三层：

1. `粗裁决 / Base Range`
   - 锁 `scene_id / scene_name / scene_type / world_mode / style_backbone / direction_anchor`。
   - 失败信号：场景原型被泛化，或设计之向缺失。
2. `细裁决 / Range Narrowing`
   - 锁参照、文化元素、结构、布局、材料、配件和动线。
   - 失败信号：参照只剩流派名，空间不可画草图。
3. `离散裁决 / Final Selection`
   - 锁氛围、构图、摄影参数、prompt 整合顺序和 Midjourney 参数。
   - 失败信号：prompt 新增了前两层不存在的业务事实。

每层必须说明：

- 服务字段
- 叙事判断
- 合理判断
- 审美判断
- 为什么是这个结果
- 如果不是这个结果，最可能滑向什么错误读法

## Cultural Archetype Verification

命中以下任一类场景时，必须先查证或执行保守模式：

- 寺庙、道观、祠堂、祭坛、法会空间、戏台
- 城隍庙、阴司殿堂、奈何桥、黄泉渡口等民俗/神话空间
- 明确宗教、民俗、礼制、神话或历史制式空间

最低要求：

1. 优先使用上游 research / bridge 已提供的可靠来源。
2. 若来源不足且允许联网，至少查 2 个独立来源。
3. 若不能查证，必须写 `conservative_consensus_required`，并使用保守共识，不得假装确定。
4. 查证或保守结果至少回落到 `reference / cultural_elements / structure / materials / accessories / guardrails` 中的 4 项。

## Reference Selection Rules

| world signal | reference strategy | forbidden fallback |
| --- | --- | --- |
| `historical / 古代 / 朝代 / 武侠` | 历史时期建筑或空间制式类型学 | 现代建筑大师作为唯一参照 |
| `modern / contemporary` | 现代建筑、室内、城市或景观参照，可具体到大师与作品 | 空泛“现代感” |
| `future / cyberpunk / sci-fi / 末世` | 未来城市基础设施、界面系统、材料老化与能源结构类型学 | 回落木石砖传统空间 |
| `myth / afterlife / religion` | 图像学、礼制空间、仪轨动线与象征材料 | 只写神秘氛围 |

## Prompt Integration Rules

`prompt整合` 只能从以下来源回收：

- story premise / compendium
- reasoning pivot
- style backbone / scene style
- direction anchor / negative guardrails
- reference / structure / materials / circulation
- atmosphere / composition / camera setup

生成规则：

1. `prompt整合` 必须针对同一模板文件中其上方全部已落位内容做整合，而不是只承接当前场景主体字段。
2. 从 `2-Global/全局风格.md` 自动加载 `global_style_prefix`，并在 prompt 中转写为英文 `Global style prefix`。
3. 最终生图入参必须为 `prompt整合` 的完整英文段落，结构为 `Global style prefix:` + `Integrated prompt:`。
4. `Integrated prompt` 必须使用英文自然语句，尽量覆盖 `解构` 中的空间结构、材质、氛围、构图、摄影机与负面约束，不得另设平行 prompt 小节。
5. `Integrated prompt` 正文必须完全为英文 ASCII 文本，目标约 2000 UTF-8 bytes，硬门范围为 1800-2200 bytes。
6. 场景 prompt 必须固定为空镜头参照图，包含 `empty environmental shot` 与 `no characters`，不得让角色、人物、人群、手部或表演动作进入画面。

禁止：

- 在 prompt 中新增未在结构化字段出现的建筑制式、宗教器物或年代设定。
- 把 `物语`、`解构` 全文直接拼成 prompt，或把中文字段逐项堆叠成 prompt。
- 只保留抽象情绪词而丢失空间结构。
- 为了叙事感而加入人物、群像、手部、角色动作或剧照式表演。

## Output Mapping

| canonical JSON slot | Markdown projection | note |
| --- | --- | --- |
| `scenes[].story_premise / compendium` | `物语` | 优先继承上游 compendium |
| `scenes[].reasoning_pivot` | `解构 / Reasoning Pivot` | 承接物语到结构与镜头 |
| `scenes[].structured_fields.scene_design` | `解构 / Scene Design` | 场景设计字段 |
| `scenes[].structured_fields.cinematography` | `解构 / Cinematography` | 摄影字段 |
| `scenes[].prompt_integration` | `prompt整合 / Integrated prompt` | 约 2000 bytes 的英文自然语言整合 prompt |
| `scenes[].design_prompt` | `scene_design.json` | canonical prompt |
| `scenes[].prompt` | `scene_design.json` | legacy alias, must equal `design_prompt` |
| `scenes[].global_style_prefix` | `prompt整合 / Global style prefix` | 来自 `2-Global/全局风格.md` 的 `- 全局风格：` 字段的英文转写 |
| `scenes[].full_generation_prompt` | `prompt整合` 整段 | provider-ready final prompt，必须含英文全局风格前缀 |
| `scenes[].final_prompt` | `scene_design.json` | legacy provider-ready alias, should equal `full_generation_prompt` |

## Validation Checklist

- `scene_id / scene_name` 沿用清单，不被 research / bridge 改名。
- `research_status / bridge_status / init_status / global_status` 已写入 source trace。
- `Style Backbone` 与 `Scene Style` 分工明确。
- `设计之向` 与 `反向禁忌` 同时进入 thinking sidecar、structured fields 与 prompt。
- Markdown 三段式齐全，且 `prompt整合` 可被稳定抽取。
- `design_prompt == prompt`。
- `full_generation_prompt` 含 `global_style_prefix`，且可直接交给 built-in imagegen。
- `_manifest.json` 只做审计侧车。
