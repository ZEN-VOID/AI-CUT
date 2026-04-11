# 首帧参照 执行流程细则

## Canonical Inputs

- `projects/<项目名>/编导/第N集.json`
- `.agents/skills/aigc/_shared/director_episode_output.schema.json`

## Canonical Landing

- `projects/<项目名>/视频/首帧参照/第N集/第N集.json`
- `projects/<项目名>/视频/首帧参照/第N集/第N集.txt`
- `projects/<项目名>/视频/首帧参照/第N集/_manifest.json`

## Workflow

1. 读取 episode JSON，锁定 `final_output.main_content.分镜组列表`。
2. 遍历分镜组并按 `分镜明细[].分镜ID` 锁定目标分镜及其所属 `分镜组ID`。
3. 提取目标分镜所属组的：
   - `分镜组ID`
   - `剧本正文`
   - `组间设计.全局风格`
   - `组间设计.类型元素`
   - `组间设计.导演意图`
   - 目标 `分镜明细`
4. 先从 `剧本正文` 中裁出对应目标分镜帧的剧情桥段：
   - 若该分镜组只有 1 个分镜，直接使用整段 `剧本正文`
   - 若该分镜组有多个分镜，结合目标分镜的 `时间段`、`角色表现`、`分镜表现` 和角色/空间状态，只保留与该帧直接对应的事件阶段、动作节点或状态变化
   - 若桥段边界仍不清晰，保守压缩到“该帧可见的最小剧情事实”，不得虚构过渡
5. 原文保留 `组间设计.全局风格`。
6. 把 `组间设计.类型元素`、`组间设计.导演意图` 与目标镜级字段压缩到剩余字数预算。
7. 组织为 `meta + prompt_style + model + prompt + prompt_char_count` 请求对象；`meta.source_shot_ids` 固定只放 1 个目标 `分镜ID`。
8. 按共享 txt 模板额外整理 `提示词 + 字数统计` 阅读视图。
9. 写入单集 JSON、TXT 与最小 manifest。

## Prompt Assembly Rules

1. 只允许显式保留 `分镜组 <ID>` 与 `分镜 <ID>` 两类标签。
2. `全局风格` 直接贴原文，不改写、不重命名。
3. `剧情桥段` 只允许对应目标分镜帧，不得直接整段复用全组 `剧本正文`，除非组内只有 1 个分镜。
4. 其余字段一律不写字段标题，改写为自然句或高密度短语。
5. 字数吃紧时，优先把非固定字段压缩为短语、关键词或顿号串。
6. 源信息不足时，不为凑字数而虚构新事实；允许保守低于下限，但必须在 manifest 备注。

## Handoff

- 若后续要正式生成视频，直接将本 JSON 交给 `.agents/skills/cli/dreamina-cli/SKILL.md` 继续消费；TXT 仅作为人工审阅副产物保留。
