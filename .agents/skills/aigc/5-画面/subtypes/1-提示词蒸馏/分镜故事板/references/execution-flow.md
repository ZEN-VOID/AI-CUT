# 分镜故事板执行流程细则

## Canonical Inputs

- `projects/<项目名>/编导/第N集.json`
- `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- `.agents/skills/aigc/5-画面/_shared/image-generation-input.template.json`

## Canonical Landing

- 子路径根目录：`projects/<项目名>/5-画面/分镜故事板/`
- 单集目录：`projects/<项目名>/5-画面/分镜故事板/第N集/`
- 汇总 JSON：`projects/<项目名>/5-画面/分镜故事板/第N集/第N集.json`
- 汇总清单：`projects/<项目名>/5-画面/分镜故事板/第N集/_manifest.json`（可选）

## 输入合同

### 必需输入

- `projects/<项目名>/编导/第N集.json`
- `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- `.agents/skills/aigc/5-画面/_shared/image-generation-input.template.json`
- `final_output.main_content.分镜组列表[]`

### 推荐输入

- `projects/<项目名>/3-明细/第N集.md` 作为人工可读 sidecar
- `projects/<项目名>/4-主体/` 下的角色、场景、道具参考图

### 输入处理原则

1. 一切组级/镜级事实以上游 `projects/<项目名>/编导/第N集.json` 为准。
2. `3-明细/第N集.md` 若存在，只作为人工可读校对 sidecar，不构成第二真源。
3. `4-主体` 只作为后续参照图槽位来源，不反向修改镜头事实。
4. 当前阶段允许直接使用上游内容，不做压缩；但不得虚构新镜头。

## Mandatory Workflow

1. 读取上层 `.agents/skills/aigc/5-画面/SKILL.md + CONTEXT.md`。
2. 读取 `projects/<项目名>/编导/第N集.json`，校验其符合 `.agents/skills/aigc/_shared/director_episode_output.schema.json` 的共享字段壳。
3. 从 `final_output.main_content.分镜组列表[]` 遍历每个分镜组，提取：
   - `分镜组ID`
   - `剧本正文`
   - `组间设计.全局风格`
   - `组间设计.类型元素`
   - `组间设计.导演意图`
   - 全部按原顺序排列的 `分镜明细[]`
4. 将上述内容组织为 `storyboard_group` 内容块；内容允许直接使用，不做文字压缩。
5. 以共享模板为骨架填充 `meta + prompt_style + model + prompt + prompt_char_count`；其中 `prompt` 固定为“英文前缀 + storyboard_group”。
6. 如有 `4-主体` 参考资产，则只把它们登记到 `model.reference_images / image_markers` 的预留位；若需人工复核，可回读 `3-明细/第N集.md`。
7. 写入单集 `第N集.json`；仅在任务要求 `full_trace` 时额外输出 `_manifest.json`。

## Prompt Assembly Rules

1. 固定前缀必须逐字保留：

   ```text
   Create a multi-panel storyboard based on the following shot breakdown.
   Add the shot sequence number in the bottom-left corner of each panel (no other text).
   Auto-adapt the panel layout grid based on the total number of shots.
   ```

2. `storyboard_group` 必须紧随其后，不插入额外模板说明。
3. `storyboard_group` 的镜级内容必须保持与上游 `分镜明细[]` 一致的顺序。
4. 若上游内容存在空缺，允许保守留空，不得为凑完整度虚构镜头事实。

## Handoff Rule

- 本子技能的消费单位是分镜组，不下沉为单帧执行面。
- 当前产物默认交给 `5-画面/subtypes/2-一致性处理` 与 `5-画面/subtypes/3-图像生成` 继续消费。
- 本子技能本身不负责真实图片生成。
