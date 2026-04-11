# 全能参照 执行流程细则

## Canonical Inputs

- `projects/<项目名>/编导/第N集.json`
- `.agents/skills/aigc/_shared/director_episode_output.schema.json`

## Canonical Landing

- `projects/<项目名>/视频/全能参照/第N集/第N集.json`
- `projects/<项目名>/视频/全能参照/第N集/第N集.txt`
- `projects/<项目名>/视频/全能参照/第N集/_manifest.json`

## Workflow

1. 读取 episode JSON，锁定 `final_output.main_content.分镜组列表`。
2. 对每个分镜组提取：
   - `分镜组ID`
   - `剧本正文`
   - `组间设计.全局风格`
   - `组间设计.类型元素`
   - `组间设计.导演意图`
   - 全部 `分镜明细[]`
3. 先原文保留 `剧本正文` 与 `全局风格`。
4. 再把其余组级与镜级字段均匀压缩到剩余字数预算。
5. 组织为 `meta + prompt_style + model + prompt + prompt_char_count` 请求对象；`meta` 锁定分镜级别与来源定位，`prompt_style` 锁定类型/语言/字数限制，`model` 仅保留留空参数骨架与图片标记。
6. 按共享 txt 模板额外整理 `提示词 + 字数统计` 阅读视图。
7. 写入单集 JSON、TXT 与最小 manifest。

## Prompt Assembly Rules

1. 只允许显式保留 `分镜组 <ID>` 与 `分镜 <ID>` 两类标签。
2. `剧本正文` 与 `全局风格` 直接贴原文，不改写、不重命名。
3. 其余字段一律不写字段标题，改写为自然句或高密度短语。
4. 字数吃紧时，优先把非固定字段压缩为短语、关键词或顿号串。
5. 源信息不足时，不为凑 1800 字而虚构新事实；允许保守低于下限，但必须在 manifest 备注。

## Handoff

- 若后续要正式生成视频，直接将本 JSON 交给 `.agents/skills/cli/dreamina-cli/SKILL.md` 继续消费；TXT 仅作为人工审阅副产物保留。
