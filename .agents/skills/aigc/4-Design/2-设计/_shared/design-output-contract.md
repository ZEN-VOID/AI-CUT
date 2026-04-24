# 4-Design / 2-设计 Shared Output Contract

本文件是 `4-Design/2-设计/{场景,角色,道具}` 的共享输出真源，负责统一三类设计主体的 prompt、图片快路径与派生产物边界。

slot 级 carrier 映射、review bundle 与 rework 落点统一下沉到：

- `.agents/skills/aigc/4-Design/2-设计/_shared/design-slot-review-contract.md`

## Canonical Scope

| concern | canonical rule | local variation allowed |
| --- | --- | --- |
| 设计真源 | 各 leaf 自己声明的 `scene_design.json`、`character_design.json` 或逐道具 Markdown | leaf 可保留自己的 canonical carrier，但不得改写共享 prompt 与图片快路径规则 |
| 人读投影 | `[场景名].md`、`[角色名].md`、`<prop_id>-<canonical_name>.md` | 文件名按 leaf 主键规则生成 |
| 全局风格前缀 | `projects/aigc/<项目名>/2-Global/全局风格.md` 中 `## JSON 直接提取字段` 下 `- 全局风格：...` 的字段值 | 只允许提取该字段值；不得压缩整份 Markdown，不得混入 frontmatter、章节说明、类型元素或设计元素；进入 `prompt整合` 时应转写为英文自然语句 |
| 生图提示词 | `full_generation_prompt = prompt整合` 的完整英文段落 | leaf 可保留 `design_prompt / final_prompt / prompt_integration` 等兼容字段，但最终入参必须是英文 integrated prompt，而不是局部字段拼接；`Integrated prompt` 正文目标为约 2000 UTF-8 bytes |
| 自动图片 | 默认调用内置 `$imagegen` / `image_gen` 的单主体 T2I 快路径，模型口径为 `GPT-IMAGE-2`，执行模式继承 `.agents/skills/aigc/_shared/image-generation-execution-contract.md` | 可显式关闭、dry-run 或 request-only；API/CLI/nano-banana 仅作为用户显式 fallback，不得作为默认路径；`request_ready` 不得伪装成已产图成功 |

## Markdown Template Registry

输出落盘时只允许以下三份 Markdown 模板作为人读投影结构真源：

| domain | canonical template | renderer / gate |
| --- | --- | --- |
| `角色` | `.agents/skills/aigc/4-Design/2-设计/角色/templates/character_masterprompt.structured.v2.md` | `validate_character_design_projection.py` 必须校验同结构；新增 renderer 时只能读取本模板填槽 |
| `道具` | `.agents/skills/aigc/4-Design/2-设计/道具/templates/prop_masterprompt.structured.v2.md` | `build_prop_design_packets.py` 必须读取本模板填槽 |
| `场景` | `.agents/skills/aigc/4-Design/2-设计/场景/templates/scene_masterprompt.structured.v2.md` | `build_scene_design_packets.py` 必须读取本模板填槽 |

硬规则：

1. `references/`、`CONTEXT.md`、`SKILL.md`、示例文档、compat JSON 说明与脚本注释不得重新定义完整 Markdown 输出模板。
2. 示例只能说明字段映射、输入来源或 manifest 形态；不得包含可被复制为落盘结构的完整 `**物语** / **解构** / **prompt整合**` 模板块。
3. 若需要修改输出结构，先改本表中的对应 `templates/*.structured.v2.md`，再同步 renderer、validator 与 leaf `SKILL.md`。

## Global Style Prefix Contract

1. 每个设计主体文件的最终图像提示词必须自动加载统一全局风格前缀。
2. 第一来源固定为：
   - `projects/aigc/<项目名>/2-Global/全局风格.md`
3. 提取规则固定为：
   - 只读取 `- 全局风格：` 后的字段正文。
   - 若 Markdown 中有多个 `- 全局风格：`，取最后一个作为当前投影。
   - 禁止把 YAML frontmatter、分析章节、候选取舍、类型元素兼容投影或设计元素文本拼入 `global_style_prefix`。
4. 允许回退来源：
   - `projects/aigc/<项目名>/0-Init/north_star.yaml`
   - `projects/aigc/<项目名>/0-Init/init_handoff.yaml`
5. 回退只用于 `全局风格.md` 缺失或没有 `- 全局风格：` 字段时的降级留痕，不得替代 `2-Global` 的默认主权。
6. `prompt整合` 的语义是对同一模板文件中其上方全部已落位内容做英文整合，而不是抽取式摘要；它必须把 `解构` 中的关键结构、材质、角色/空间/器物锚点、镜头/摄影信息与负面约束编织成一段可直接生图的完整 brief，不得只复述主体名或拼接局部字段。
7. `prompt整合` 必须保留 `Global style prefix:` 与 `Integrated prompt:` 两行标签；两行正文都应使用英文自然语句。全局风格前缀必须可追溯到 `2-Global/全局风格.md` 的 `- 全局风格：` 字段。
8. `Integrated prompt:` 后的正文必须完全为英文 ASCII 文本，不得含中文、中文标点或其他非英文字符；目标长度为约 2000 UTF-8 bytes，硬门范围为 1800-2200 bytes。低于下限视为整合不足，高于上限视为未压缩到 provider-ready brief。

## Reference Image Cleanliness Contract

`2-设计` 的同目录同名图片默认会作为后续 `3-面板 / 5-Image / 6-Video` 的参照图，因此必须先防止主体污染：

| domain | required clean image mode | contamination forbidden in `Integrated prompt` |
| --- | --- | --- |
| `场景` | empty environmental shot | 任何角色、人物、人群、手部、表演动作或角色主体，不得把场景图变成剧照 |
| `角色` | character on a solid color background | 场景背景、建筑、房间、街道、道具环境、叙事场面或其他人物 |
| `道具` | isolated pure prop view | 任何角色、手、手持姿态、身体局部、使用者、场景表演或复杂环境 |

固定英文锚句：

1. 场景 `Integrated prompt` 必须包含 `empty environmental shot` 与 `no characters`。
2. 角色 `Integrated prompt` 必须包含 `solid color background` 与 `no scene background elements`。
3. 道具 `Integrated prompt` 必须包含 `isolated pure prop view`、`no hands` 与 `no characters`。

这些锚句是下游参照图防污染 hard gate，不得为了画面生动性删改。

## Worldview Fidelity Gate

`2-设计` 不只要防“主体污染”，还必须防“世界观污染”。当上游 bridge / research 信息不足时，leaf 可以做受控回退，但不得把别的项目默认值、占位名或错世界设定注入当前项目 prompt。

硬规则：

1. 任何 leaf 只要生成结果中出现下列占位/错域信号，必须在落盘前直接失败，不得继续自动生图：
   - `Character 001`、`Character 002` 等编号替名
   - `Documented Scene`
   - `the catalogued prop`
   - 独立 `unknown`
   - 来自旧项目的错域风格词，如 `urban-drama`、`urban-romance`、`near-future`、`holographic`
2. `角色` prompt 必须显式锁定当前项目的人种/地域/世界观边界；当项目属于东亚武侠语境时，人物不得漂到西方面孔、现代时装肖像或全球时尚棚拍默认值。
3. `场景` prompt 的默认 typology 必须优先从当前 `scene_name + aliases + variants + must_show_anchors` 判型；不得因为项目级全局风格中出现其他地点词而把夜市误判成王府或把港口误判成近未来社区。
4. `道具` prompt 的默认材质与结构必须优先服从当前 `canonical_name` 的器物语义；不得把木牌、税单、册子、钱袋等回退成金属科幻件或抽象工业构件。
5. 当 bridge / research 仅给出“待补”“unknown”“情绪张力待补”等低质量占位时，leaf 必须使用当前项目 domain-specific fallback，而不是把占位词原样写入 prompt。
6. 项目专属的名称翻译、角色画像、场景家族默认值、道具器物默认值，必须落在 `projects/aigc/<项目名>/CONTEXT/4-design-fallback-registry.json` 或等价项目级 registry；通用 builder 只负责读取 registry，不得把某个项目的私有 fallback 长驻硬编码在 leaf 脚本里。

推荐校验点：

- `角色`：检查 prompt 是否同时满足 `solid color background`、当前项目世界观、人种/地域边界与角色专属身份钩子。
- `场景`：检查 prompt 是否能从 `scene_name` 直接回指当前空间家族，而不是只剩抽象功能。
- `道具`：检查 prompt 是否保住主材质、主结构、受力/磨损逻辑，而不是只剩“generic prop”。

## Thinking-Action Placement Contract

参照图洁净规则必须进入 leaf 的思维-执行节点，而不是只写在模板末端：

| domain | thought placement | execution placement | mandatory node evidence |
| --- | --- | --- | --- |
| `场景` | 在 `N6-CAMERA` 先把剧情人物动作转写为空间痕迹、动线、环境状态或物体尺度线索 | 在 `N7-PROMPT` 注入 `empty environmental shot / no characters`，在 `N10-AUTO-IMAGE` 前复核禁止人物、人群、手部、表演动作 | `reference_cleanliness_note.scene_empty_shot = true` |
| `角色` | 在 `N6-CAMERA` 先判定这是角色定妆参照，不是剧情剧照或场景板 | 在 `N7-PROMPT` 注入 `solid color background / no scene background elements`，在 `N10-AUTO-IMAGE` 前复核禁止场景背景、建筑、房间、街道、其他人物 | `reference_cleanliness_note.character_solid_background = true` |
| `道具` | 在 `NODE-PROP-DESIGN-03` 先把手持、使用、触碰、角色动作转写为器物表面、功能端、受力点或离屏使用语境 | 在 `NODE-PROP-DESIGN-03` 注入 `isolated pure prop view / no hands / no characters`，在 `NODE-PROP-DESIGN-05` 前复核禁止手、身体局部、持有者、角色或复杂场景 | `reference_cleanliness_note.prop_isolated_view = true` |

通用执行顺序：

1. 先判定当前输出是后续参照资产，而不是叙事剧照。
2. 再将上游剧情动作中可能引入污染主体的词，转写为本域允许的可视证据。
3. 然后生成英文 `Integrated prompt`，并注入固定英文锚句。
4. 最后自动生图前复验锚句与禁止主体；失败必须回到 prompt 节点，不得靠后期裁切补救。

推荐落盘字段：

```json
{
  "global_style_prefix": "从 2-Global/全局风格.md 的 `- 全局风格：` 字段提取得到的统一风格前缀",
  "global_style_prefix_en": "英文转写后的统一风格前缀",
  "prompt_integration": "对同一模板上方全部内容整合出的约 2000 bytes 英文自然语言提示词",
  "full_generation_prompt": "Global style prefix: global_style_prefix_en + Integrated prompt: prompt_integration",
  "prompt_source": {
    "global_style": "projects/aigc/<项目名>/2-Global/全局风格.md",
    "subject_design_file": "同目录主体设计文件"
  }
}
```

## Auto Image Fast Path

设计文件稳定落盘后，必须继续进入单主体自动生图：

```bash
python3 .agents/skills/aigc/4-Design/2-设计/_shared/scripts/run_design_auto_image.py \
  --design-file "projects/aigc/<项目名>/4-Design/<主体>/2-设计/第N集/<主体文件>.md"
```

默认情况下该命令会先写 `generated/requests/<主体文件>-auto-image-request.json`，状态为 `request_ready`。随后由 Codex 会话调用内置 `$imagegen` / `image_gen`，按 `GPT-IMAGE-2` 口径逐张生成，并把选定输出从 `$CODEX_HOME/generated_images/...` 复制到侧车声明的 `output_dir/output_filename`；原始生成文件必须保留。

批量或补跑时必须使用共享 guard，而不是让各 leaf 自己判断“是否已经完整生图”：

```bash
python3 .agents/skills/aigc/4-Design/2-设计/_shared/scripts/ensure_design_auto_images.py \
  --project "<项目名>" \
  --domain "场景" \
  --episode "第1集"
```

该 guard 默认写 `generated/requests/design_auto_image_batch.json`，把所有缺同 stem 图片的 Markdown 聚合为 `{ "tasks": [...] }`。helper 不再直接调用 API；它只交付内置 imagegen 可消费的侧车与 manifest。真实生图必须由当前 Codex 会话按 tasks 顺序逐张调用内置 `image_gen` 完成。

硬规则：

1. 图片输出目录必须与当前主体设计文件同目录。
2. 图片文件 stem 必须与当前主体设计文件一致；默认复制为 `.png`，除非内置工具输出被用户显式选择为其他可用位图格式。
3. prompt 入参必须是包含英文 `global_style_prefix` 转写和英文 `prompt_integration` 的 `full_generation_prompt`，不得只传主体局部 prompt。
4. 自动图片是 derived asset，不得反向改写 `scene_design.json`、`character_design.json`、逐道具 Markdown 或 `1-清单` 真源。
5. 若内置 `image_gen` 失败、输出无法定位或复制回项目失败，应记录为图片步骤失败并阻塞“完整完成”声明；不得把只有设计文件或 request sidecar 的状态宣布为已完成自动生图。
6. 自动生图 helper 不再等待远端 provider；若用户显式 fallback 到 API/CLI，才需要按对应 fallback 合同记录 API key、网络或 provider 失败。
7. 批量状态必须按“每个 Markdown 设计文件都有同 stem 图片”判定；只要缺任一主体图片，`_manifest.json.auto_image.status` 必须是 `failed`，不得因部分图片存在而写成 `success`。
8. 默认 request sidecar 写出时 `_manifest.json.auto_image.status` 必须写 `request_ready`，并记录 `execution_mode / request_batch_path / provider_skill / provider_mode / default_model`；后续验收再根据同 stem 图片是否存在判定最终成功。

## Subject Handoff Table

| domain | design_file | prompt source | auto_image_output |
| --- | --- | --- | --- |
| `场景` | `[场景名].md` + `scene_design.json.scenes[]` | `scenes[].full_generation_prompt`，回退 Markdown `**prompt整合**` 完整英文段 | `[场景名].<ext>` |
| `角色` | `[角色名].md` + `character_design.json.roles[]` | `roles[].full_generation_prompt`，回退 Markdown `**prompt整合**` 完整英文段 | `[角色名].<ext>` |
| `道具` | `<prop_id>-<canonical_name>.md` | Markdown `**prompt整合**` 内的 `Global style prefix` + `Integrated prompt` 英文段 | `<prop_id>-<canonical_name>.<ext>` |

## Manifest Requirements

每个 leaf 的 `_manifest.json` 应记录图片快路径状态：

```json
{
  "auto_image": {
    "provider_skill": "imagegen",
    "provider_mode": "built-in image_gen",
    "default_model": "GPT-IMAGE-2",
    "mode": "single-subject-t2i",
    "execution_mode": "codex-builtin-imagegen",
    "max_concurrent": 1,
    "prompt_field": "full_generation_prompt",
    "output_dir_policy": "same_directory_as_design_file",
    "filename_policy": "same_stem_as_design_file",
    "status": "request_ready | success | failed | skipped_by_user | dry_run",
    "request_batch_path": "",
    "generated_source_path": "",
    "image_paths": []
  }
}
```

## Completion Gate

`4-Design/2-设计` 的正式完成条件为：

1. 主体设计真源已落盘。
2. 人读设计文件已落盘。
3. `full_generation_prompt` 已包含统一全局风格前缀。
4. 单主体图片请求已按默认内置 imagegen 模式写出并执行；最终验收时图片已由内置 `image_gen` 生成并复制到设计文件同目录，且文件名 stem 一致。
5. `_manifest.json` 已记录 prompt 来源、provider、输出路径与失败/成功状态。
