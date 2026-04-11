# 分镜帧执行流程细则

## Canonical Inputs

- `projects/<项目名>/编导/第N集.json`
- `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- `.agents/skills/aigc/5-画面/_shared/image-generation-input.template.json`

## Canonical Landing

- 子路径根目录：`projects/<项目名>/5-画面/分镜帧/`
- 单集目录：`projects/<项目名>/5-画面/分镜帧/第N集/`
- 汇总 JSON：`projects/<项目名>/5-画面/分镜帧/第N集/第N集.json`
- 汇总清单：`projects/<项目名>/5-画面/分镜帧/第N集/_manifest.json`（可选）

## 输入合同

### 必需输入

- `projects/<项目名>/编导/第N集.json`
- `.agents/skills/aigc/5-画面/_shared/image-generation-input.template.json`
- 可唯一定位的 `分镜ID`

### 推荐输入

- `projects/<项目名>/4-主体/` 下的角色、场景、道具参考
- 既有 `projects/<项目名>/5-画面/` 历史 prompt、参考图或单帧产物

### 输入处理原则

1. `projects/<项目名>/编导/第N集.json` 必须满足 `.agents/skills/aigc/_shared/director_episode_output.schema.json` 的 `metadata / thinking_chain / final_output` 三段式结构。
2. 目标分镜固定从 `final_output.main_content.分镜组列表[].分镜明细[]` 锁定，并保留所属 `分镜组ID / 剧本正文 / 组间设计` 作为上下文。
3. `分镜ID` 必须遵循四段式：`episode-scene-group-frame`。
4. `single_frame_shot` 只归纳当前帧可见画面，不复述整段对白或整组剧情。

## Mandatory Workflow

1. 读取上层 `.agents/skills/aigc/5-画面/SKILL.md + CONTEXT.md`。
2. 读取 `projects/<项目名>/编导/第N集.json`，锁定 `final_output.main_content.分镜组列表`。
3. 遍历分镜组并按 `分镜明细[].分镜ID` 锁定当前单集里唯一目标 `分镜ID`，同时保留所属 `分镜组ID / 剧本正文 / 组间设计`。
4. 从目标 `分镜明细` 与所属分镜组上下文中组织 `single_frame_shot` 内容块，优先保留：
   - `分镜组ID`
   - 所属组 `剧本正文`
   - 所属组 `组间设计`
   - 目标 `分镜ID`
   - 目标分镜的镜级字段
5. 以共享模板为骨架填充 `meta + prompt_style + model + prompt + prompt_char_count`；其中 `prompt` 固定为“单帧前缀 + single_frame_shot”。
6. 如有 `4-主体` 参考资产或既有单帧资产，则只把它们登记到 `model.reference_images / image_markers` 的预留位。
7. 写入单集 `第N集.json`；仅在任务要求 `full_trace` 时额外输出 `_manifest.json`。

## Prompt Assembly Rules

1. 固定前缀必须逐字保留：

   ```text
   Create a single cinematic frame based on the following shot breakdown.
   Render only the specified shot moment as one full-frame image (no multi-panel layout).
   Do not add any text, subtitles, speech bubbles, or graphic overlays.
   Preserve the shot's composition, camera angle, subject positions, and atmosphere as the primary visual focus.
   ```

2. `single_frame_shot` 必须紧随其后，不插入额外模板说明。
3. `single_frame_shot` 只允许服务当前唯一 `分镜ID`，不得扩写成整组多镜头摘要。
4. 若上游内容存在空缺，允许保守留空，不得为凑完整度虚构镜头事实。

## Handoff Rule

- 本子技能不承担组级 storyboard，也不承担漫画页节奏改编。
- 当前产物默认交给 `5-画面/subtypes/2-一致性处理` 与 `5-画面/subtypes/3-图像生成` 继续消费。
- 本子技能本身不负责真实图片生成。
