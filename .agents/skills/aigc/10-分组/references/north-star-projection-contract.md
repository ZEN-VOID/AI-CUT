# Visual Tone Projection Contract

本文件定义从 `projects/aigc/<项目名>/3-美学/画面基调/全局风格协议.md` 向每个分镜组整理 `全局风格：` 字段的规则。

文件名保留 `north-star-projection-contract.md` 只作 legacy 模块路径兼容；当前执行真源是 `3-美学/画面基调`。`north_star.yaml` 只可作为项目北极星、禁区和创作阶段不变量的辅助边界，不再提供当前组最终全局风格文本。

## Required Fields

每个分镜组都必须在标题后的场景标题行下方立即输出可见字段标题：

```text
全局风格：
视频生成的画面风格，光影和氛围与场景参照图保持一致。需要生成现场物理互动音效、氛围感音效、环境声、自然现象声、动作声，不要生成任何字幕，不要生成背景音乐。 <当前组专属全局风格整理句，300字以内>
<Visual Slogan 或 Design Principle 的引用/压缩句>
<Visual Gene Profile 的引用/压缩句；必要时追加 Negative Traits 避免项>
```

| output order | visual tone source | output rule |
| --- | --- | --- |
| 第 1 行 | `Global Style Prompt` | 在行首前置固定词，再接当前分镜组专属的全局风格整理句；整理句必须是自然单段，300 字以内，不得简单照抄完整母稿 |
| 第 2 行 | `Visual Slogan` 或 `Design Principle` | 优先直引短句；过长时压缩为一句，不得添加当前组不存在的风格信息 |
| 第 3 行 | `Visual Gene Profile`，必要时结合 `Negative Traits` | 压缩为当前组可执行的画面基因/禁区句，不得替换为 north_star 旧 `细分风格.画面风格` |

`全局风格：` 是字段标题，必须可见。第 1 行是场景化整理，不是摘要删减，也不是完整直引。第 2、3 行是 `画面基调` 的短句/画像投影。不得把项目 `MEMORY.md`、`CONTEXT/` 或 `north_star.yaml` 的风格偏好替代 `画面基调` 三项；它们只能作为当前组匹配和取舍的辅助证据。

## Placement

- 分镜组顺序固定为：`## x-y-z` -> 场景标题行 -> `全局风格：` -> 三行风格内容 -> `画面风格：` -> 第一个时间码分镜行。
- `全局风格：` 不得放在 `画面风格：`、原正文或 YAML 之后。

## Global Style Extraction Rules

每个分镜组必须先形成内部 `group_style_projection`：

1. 读取 `3-美学/画面基调/全局风格协议.md` 的 `Global Style Prompt`，必要时参考 `Visual Gene Profile`、`Setting To Visual Chain`、`Master Anchor Matrix` 与 `Negative Traits`。
2. 从当前分镜组取证：场景标题、`画面风格：`、第一个普通 `分镜N（0-N秒）：` 或 `[0-N秒]` 分镜行和组内分镜时间段。
3. 判定当前组属于哪些可复用场景类型：例如室内、室外、夜景、正午、傍晚、雨雪、旷野、战场、武打、群像、对话、仪式、密室、旅途、追逐、静物证据、情绪停顿等。
4. 从 `Global Style Prompt` 和 `Visual Gene Profile` 中只抽取与这些类型匹配的风格词：媒介/时代/质感底座可保留；光影、色彩、空气、材质、摄影、运动和负面约束必须与当前组场景证据匹配。
5. 写成一段自然语句，300 字以内；不使用标签列表、参数清单、字段名或“本组适用”等元说明；不得为凑风格加入当前组不存在的天气、光源、材质、角色或动作。
6. 若 `画面基调` 没有覆盖当前场景类型，只能抽取通用底座和当前组可证实的风格逻辑，并在执行报告记录 `style_projection_gap`；不得凭空发明新的全局风格。

## Style Signature Retention Rule

场景化整理不得把作品级风格削弱成“当前场景物件 + 普通光影”的局部描述。只要 `画面基调` 已经提供明确的作品风格签名，当前组第 1 行整理句必须同时保留：

- **作品身份锚点**：至少保留 2 个来自 `Global Style Prompt` 或 `Visual Gene Profile` 的稳定身份词或等价中文表达，例如媒介、时代、地域/类型、核心审美风格、主情绪母题。
- **场景适配锚点**：保留当前组真实存在的空间、光源、色彩、材质、空气、动作或摄影证据，避免完整照抄母稿。
- **材质/摄影锚点**：至少保留 1 个对下游生成有强约束力的材质、镜头、质感或运动标识，例如真实 4K 质感、戏剧性明暗对比、克制推轨、危险时手持碎裂、玻璃/金属/血/布料等物理反应。
- **边界锚点**：在必要时保留当前项目的关键负面边界，例如不美化胁迫、暴力、羞辱或类型漂移。

若当前组整理句无法在 300 字以内同时保留作品身份和场景证据，应优先压缩局部物件枚举，而不是删除作品级风格签名。

## Missing Field Handling

- `Global Style Prompt` 缺失时不得继续生成 `全局风格：` 字段，除非用户明确授权临时降级。
- `Visual Slogan`、`Design Principle` 或 `Visual Gene Profile` 缺失时，不得猜测补写；可在执行报告中标记 `visual_tone_field_gap`。
- 可读取相近字段时，只能在执行报告中列为候选，不得静默替代。
- 需要继续执行时，应先修复 `3-美学/画面基调/全局风格协议.md` 或取得用户明确授权。

## Count Handling

`全局风格：` 字段标题、三行画面基调内容和第 1 行固定前置词不计入组内 `时长估算`、1680 字目标上限、1980 字硬上限或 YAML `字数统计`。每组标题后的场景标题行、`画面风格：` 和分镜剧本正文计入 YAML `字数统计`，但组头字段不计入 `时长估算`。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每个分镜组是否在场景标题行下方立即输出 `全局风格：`，且字段内有三行内容？ | `GATE-GROUP-02` | `FAIL-GROUP-02` | `N2-PROJECT-STYLE`、本文件 `Required Fields`、`Placement` | 执行报告记录每组 `全局风格：` 位置和三行内容检查。 |
| 第 1 行是否以固定前置词开头，并接当前组专属全局风格整理句？ | `GATE-GROUP-02` | `FAIL-GROUP-02` | `N2-PROJECT-STYLE`、本文件 `Required Fields` | 执行报告记录固定前置词检查、缺失/错位修复结果。 |
| 第 1 行全局风格整理句是否依据 `画面基调.Global Style Prompt` 和当前证据抽取匹配部分，保持自然单段、300 字以内，且没有完整照抄全局母稿？ | `GATE-GROUP-02` | `FAIL-GROUP-02` | `N2-PROJECT-STYLE`、本文件 `Global Style Extraction Rules` | 执行报告记录每组风格整理句字数、画面基调来源、当前组证据和照抄风险结论。 |
| 第 1 行是否在场景化整理后仍保留作品级风格签名，而不是退化为局部物件、普通光影或泛化质感描述？ | `GATE-GROUP-02` | `FAIL-GROUP-02` | `N2-PROJECT-STYLE`、本文件 `Style Signature Retention Rule` | 执行报告记录每组保留的作品身份锚点、场景适配锚点、材质/摄影锚点和边界锚点。 |
| 第 2、3 行是否分别来自 `Visual Slogan / Design Principle` 与 `Visual Gene Profile / Negative Traits`，没有被项目 `MEMORY.md`、`CONTEXT/`、`north_star.yaml` 或其他偏好替代？ | `GATE-GROUP-02` | `FAIL-GROUP-02` | `N2-PROJECT-STYLE`、本文件 `Required Fields` | 执行报告记录画面基调字段原文、输出行比对和外部偏好未替代的结论。 |
| 画面基调三项、固定前置词和 `全局风格：` 字段是否没有计入组内 `时长估算`、1680/1980 字数风险或 YAML `字数统计`？ | `GATE-GROUP-11` | `FAIL-GROUP-08` | `N7-ASSEMBLE`、本文件 `Count Handling` | 执行报告记录字数/时长统计排除项和 YAML 统计回指。 |
