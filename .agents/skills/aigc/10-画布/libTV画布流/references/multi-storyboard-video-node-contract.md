# Multi-Storyboard Video Node Contract

本文件定义“多分镜图视频节点生成”的标准模式。它适用于用户提供一组连续分镜参照图，并要求在 LibTV 创建单个视频节点时按分镜顺序消费这些图，同时额外补充角色、场景、道具或主体参照图。

## Trigger

命中以下任一条件时必须加载本细则：

- 用户明确说“多分镜图参照模式”“多分镜参照模式”“多分镜图视频节点”。
- 用户提供多张按文件名数字序号排序的分镜参照图，并要求生成一个连续视频节点。
- 用户额外要求“指明具体分镜段参照分镜图”。
- 用户提供 Flash Prompt Pack、分镜段时间轴或逐段动作说明，且每段应绑定对应参照图。

本细则不替代 `image-order-contract.md`；它在图片顺序锁定之上，进一步规定 prompt 中的分镜段落、主体参照和校验证据。

## Reference Domains

多分镜图视频节点必须区分两类参照：

1. `storyboard_refs[]`：分镜段参照图。用于镜头构图、运动方向、动作承接、武器轨迹、压迫感和节奏。
2. `subject_refs[]`：主体参照图。用于锁定角色、场景、道具、服装、武器和外观一致性。

默认槽位规则：

- 当用户明确提供“按顺序还原分镜图”或“分镜段参照分镜图”时，`storyboard_refs[]` 按文件名数字序号或用户列出的 Image 顺序优先占用 `{{Image 1}}...{{Image S}}`。
- 额外角色、场景、道具、主体参照图追加到分镜参照之后，占用 `{{Image S+1}}...`。
- 若任务不是多分镜图模式，仅有标准分组稿 YAML 主体参照，则仍以 `image-order-contract.md` 的 YAML `图片N` 顺序为准。
- 若用户显式指定某张图必须是某个 `{{Image N}}`，以用户指定为准，但必须在 manifest、submit plan、prompt 和 final query 中保持同一顺序。

## Prompt Standard

多分镜图视频节点 prompt 的最低合格结构为：

1. `源理解 / 统一正向提示词`：描述场景、招式、视觉风格、动作逻辑和总体连续性。
2. `参照模式说明`：说明 `{{Image 1}}...` 中哪些是分镜参照，哪些是主体参照；若为构图示意参照，必须写明“不复制拼贴痕迹、不复制人物抠图边缘、不完全照搬单帧构图”。
3. `分镜段 XX`：每个分镜段独立成段，段首必须同时包含：
   - 分镜段编号，例如 `分镜段 01`
   - 时间范围，例如 `0.0-2.0s`
   - 对应参照图占位符，例如 `{{Image 1}}`
   - 参照图名称或来源锚点，例如 `独孤九剑086`
4. 每个分镜段正文必须写明：
   - 本段关键动作
   - 构图或镜头运动
   - 角色和武器的物理运动关系
   - 与上一段或下一段的承接关系
   - 本段需要清晰的关键帧或接触点
5. `连续运动总约束`：汇总动作链，例如 `贴地环绕 -> 剑尖点地 -> 反作用力弹起 -> 空中转身 -> 从天落剑 -> 镰刀残影格挡 -> 火花压制`。
6. `声音 / 负面约束`：无台词、无字幕、无 Logo、无水印、无背景音乐；保留环境声、衣袍破风、武器摩擦、金属撞击、火花迸裂等合理声音。
7. `fenced YAML`：列出分镜参照与主体参照的槽位映射，便于审计。

标准段首示例：

```text
分镜段 01（0.0-2.0s，参照 {{Image 1}} / 独孤九剑086）：接上一镜低空飞掠的动作，令狐冲贴近地面绕着镰刀武士高速旋转飞行...
```

标准底部 YAML 示例：

```yaml
分镜参照:
  - 图片1: "独孤九剑086 / {{Image 1}} / node i-xxx / 段01 0.0-2.0s 贴地环绕高速飞行"
  - 图片2: "落剑式构图示意 / {{Image 2}} / node i-yyy / 段02 2.0-4.0s 剑尖点地借力"
角色参照:
  - 图片3: "CHAR-005-令狐冲-1 / {{Image 3}} / node i-zzz / 只锁定令狐冲外观"
```

若 prompt 来源是正式分组稿且已有 YAML 主体行，提交到 LibTV 的 YAML 主体行仍应按 `image-order-contract.md` 变为：

```yaml
角色:
  - 图片6 令狐冲 {{Image 6}} i-WB4GXCLP6L
道具:
  - 图片7 长剑 {{Image 7}} i-example
```

此时分镜段后的参照图匹配和 YAML 主体参照图匹配都必须存在；一个用于动作段落，一个用于主体一致性。

## Manifest Standard

`<video_node_instance_id>-subject-reference-manifest.json` 必须记录：

- `reference_mode: "multi_storyboard_reference_with_subject_refs"` 或更具体的等价值。
- `order_contract: "storyboard_refs_first_then_subject_refs"`，除非用户显式指定不同顺序。
- `expected_image_order[]`，每一项至少包含：
  - `placeholder`
  - `node_id`
  - `name`
  - `role`
  - `time_range`（分镜参照必填，主体参照可省略）
  - `usage`

推荐角色：

- `storyboard_segment_01`
- `storyboard_segment_02`
- `character_reference_<name>`
- `scene_reference_<name>`
- `prop_reference_<name>`

## Validation Gate

最终查询后必须机械校验：

- `data.params.imageList[].nodeId` 等于 manifest 中 `expected_image_order[].node_id`。
- `data.params.mixedList[].nodeId` 等于同一顺序。
- `data.params.imageListOrder` 和 `data.params.mixedListOrder` 等于同一顺序。
- prompt 中存在所有 `{{Image N}}`。
- prompt 中每个分镜段标签存在，例如 `分镜段 01` 到 `分镜段 NN`。
- prompt 中每个分镜段时间范围存在。
- prompt 中每个分镜段段首或正文包含对应参照图名和 `{{Image N}}`。
- 若存在主体参照，prompt 的 YAML 或参照说明中必须包含主体名、`{{Image N}}` 和节点 ID / UUID。
- prompt 不包含 `{{Portrait N}}`。
- 未获授权时，节点没有生成结果 URL，queue 记录 `run_executed=false`。

## Anti-Patterns

- 只在底部 YAML 列出参照图，而正文分镜段不出现 `{{Image N}}`。
- 分镜段只写“参考图片1”，不写图名或时间范围。
- 分镜段只有抽象动作，没有写角色与武器的物理承接。
- 把角色参照图当成分镜段图使用，或把构图示意图当成必须完全复制的成片构图。
- 多分镜图视频节点仍沿用普通单段 prompt，导致每张分镜图无法审计。
- 使用脚本按模板批量套句生成分镜段正文；分镜动作、承接和审美判断必须由 LLM 直写。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否明确区分分镜参照图和主体参照图，并给出同一个 `{{Image N}}` 顺序？ | `GATE-LTVCTRL-MULTI-STORYBOARD` | `FAIL-LTVCTRL-MULTI-STORYBOARD-REFS` | manifest + prompt reference map | manifest, submit plan |
| 每个分镜段是否在段首或正文中绑定具体参照图名和 `{{Image N}}`？ | `GATE-LTVCTRL-MULTI-STORYBOARD` | `FAIL-LTVCTRL-MISSING-STORYBOARD-SEGMENT-REF` | prompt segment rewrite | final prompt query |
| YAML 或参照说明中的主体信息是否绑定主体名、`{{Image N}}` 和 node/UUID？ | `GATE-LTVCTRL-MULTI-STORYBOARD` | `FAIL-LTVCTRL-MISSING-SUBJECT-REF-MAP` | prompt YAML / manifest rewrite | prompt YAML, manifest |
| 分镜段数量、时间范围和分镜参照图数量是否一致？ | `GATE-LTVCTRL-MULTI-STORYBOARD` | `FAIL-LTVCTRL-STORYBOARD-COUNT-MISMATCH` | prompt + manifest alignment | final check JSON |
