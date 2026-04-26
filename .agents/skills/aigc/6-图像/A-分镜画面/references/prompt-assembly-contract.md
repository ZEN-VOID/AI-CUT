# Prompt Assembly Contract

本文件定义 step2：以每一个四段式分镜为单位，生成英文 AIGC 生图提示词。

## Mandatory Source Lines

每个分镜 prompt 文档必须直引 `north_star.yaml` 三项字段，保持原文，不翻译、不摘要、不改写：

1. `全局风格.全局风格提示词`
2. `类型元素.类型元素提示词`
3. `细分风格.画面风格`

## Required Markdown Shape

```markdown
## 1-1-1-1

<直引 north_star.yaml 全局风格.全局风格提示词>
<直引 north_star.yaml 类型元素.类型元素提示词>
<直引 north_star.yaml 细分风格.画面风格>

Characters:
Scene:
Props:

<Integrated AIGC image prompt in English, <= 2000 characters>
```

## Prompt Authorship

- `Integrated AIGC image prompt` 必须由 LLM 直接生成。
- 脚本可以把 LLM 直出的 prompt 投影为 Markdown 或 JSON，但不得自动扩写、补剧情、拼接主创段落。
- 允许做画面表现增量：composition, lens, shot size, camera angle, depth of field, lighting, material texture, color hierarchy, spatial blocking, visual pressure, continuity anchors.
- 禁止改变核心内容：角色身份、动作结果、剧情因果、死亡/惩罚事实、公开规则/隐藏规则、场景归属、关键道具。

## English Prompt Requirements

`Integrated AIGC image prompt` 应包含：

- one single frame only;
- subject, action, location, narrative pressure;
- composition and camera language from the source shot;
- lighting and material cues;
- style constraints from north_star, translated or integrated in English;
- reference awareness if slot images exist, without naming unavailable paths inside the prose;
- negative constraints such as no anime, no neon, no jump-scare monster when relevant.

## Character Limit

- `Integrated AIGC image prompt` 字数限定为 2000 字符以内，按 Unicode 字符数统计。
- north_star 三项直引、槽位标题和 Markdown 标题不计入英文 prompt 的 2000 字符限制。
- 超限时优先删除重复风格词和次要背景，保留主体、动作、空间、镜头、光影和关键道具。

## Slot Semantics

`Characters:`、`Scene:`、`Props:` 是参照槽位，不是剧情正文。

- 有真实图片参照时写主体名与图片路径。
- 暂无真实图片时可只写主体名，或在最终 manifest 中移除空槽位。
- 不得把不存在的图片、JSON prompt 文件或外部未知 URL 写入参照槽位。
