# 漫画执行流程细则

## Canonical Inputs

- `projects/<项目名>/编导/第N集.json`
- `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- `.agents/skills/aigc/5-画面/_shared/image-generation-input.template.json`

## Canonical Landing

- 子路径根目录：`projects/<项目名>/画面/漫画/`
- 单集目录：`projects/<项目名>/画面/漫画/第N集/`
- 汇总 JSON：`projects/<项目名>/画面/漫画/第N集/第N集.json`
- 汇总清单：`projects/<项目名>/画面/漫画/第N集/_manifest.json`（可选）

## 输入合同

### 必需输入

- `projects/<项目名>/编导/第N集.json`
- `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- `.agents/skills/aigc/5-画面/_shared/image-generation-input.template.json`
- 一个能通过 shared schema 唯一定位的分镜组与组内镜头顺序

### 推荐输入

- `projects/<项目名>/3-明细/第N集.md`，当需要补充对白原文或 markdown 上下文时再读取
- `projects/<项目名>/主体/` 下的角色、场景、道具参考

### 输入处理原则

1. 漫画子技能不新增镜头事实，只把 `final_output.main_content.分镜组列表[]` 中已存在的组/镜信息组织为漫画图像请求。
2. 默认保持 `1 shot = 1 panel`，不得把多个镜头压成不可追溯的大格。
3. `projects/<项目名>/3-明细/第N集.md` 只作为补充证据，不再充当第一结构化真源。
4. 当前阶段允许直接使用上游内容，不做压缩；但不得虚构新镜头或新对白。

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
4. 将上述内容组织为 `comic_page_group` 内容块；内容允许直接使用，不做文字压缩。
5. 以共享模板为骨架填充 `meta + prompt_style + model + prompt + prompt_char_count`；其中 `prompt` 固定为“漫画前缀 + comic_page_group”。
6. 如有 `4-主体` 参考资产，则只把它们登记到 `model.reference_images / image_markers` 的预留位；若需人工复核，可回读 `3-明细/第N集.md`。
7. 写入单集 `第N集.json`；仅在任务要求 `full_trace` 时额外输出 `_manifest.json`。

## Prompt Assembly Rules

1. 固定前缀必须逐字保留：

   ```text
   Create a single comic page based on the following storyboard group.
   Keep exactly one panel per shot in the original sequence.
   Place dialogue, monologue, and narration only inside their corresponding panels.
   Auto-adapt the comic page layout based on the total number of shots.
   ```

2. `comic_page_group` 必须紧随其后，不插入额外模板说明。
3. `comic_page_group` 的镜级内容必须保持与上游 `分镜明细[]` 一致的顺序。
4. `comic_page_group` 必须明确要求 `1 shot = 1 panel` 和文字系统按对应 panel 落点。
5. 若上游内容存在空缺，允许保守留空，不得为凑完整度虚构镜头事实。

## Handoff Rule

- 本子技能的消费单位是分镜组，不下沉为单帧执行面。
- 当前产物默认交给 `5-画面/subtypes/2-一致性处理` 与 `5-画面/subtypes/3-图像生成` 继续消费。
- 本子技能本身不负责真实图片生成。
