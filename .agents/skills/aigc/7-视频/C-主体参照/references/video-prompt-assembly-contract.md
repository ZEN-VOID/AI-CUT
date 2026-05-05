# Video Prompt Assembly Contract

本文件定义 step1 之后的组级视频 prompt 组装规则。目标是把 `4-分组` 的现有组正文保真转换为 LibTV 可提交文本，而不是重新创作分镜。

## Prompt Shape

每个分镜组生成一个独立 prompt：

```text
横屏真人实拍感视频，保持平行当代校园规则怪谈质感，低饱和冷白灯光，黑白红警告层与金色真相层分离。请根据以下完整分镜组内容生成一条连续视频，保留镜头顺序、角色动作、对白、音效、分镜明细与氛围约束；默认忽略相邻组间连接件。

主体参照说明：
角色：林寂 @projects/aigc/诡校-测试版/5-设计/角色/3-生成/林寂-多视图.png，多视图角色参考；生成时保持身份、服装与体态一致。
场景：永夜私立中学二年级A班教室 @projects/aigc/诡校-测试版/5-设计/场景/3-生成/永夜私立中学二年级A班教室-多视图.png，多视图场景参考；生成时保持空间布局和光线一致。

分镜组原文：
<直接粘贴 group_body>
```

## Provider Instruction Boundary

- 可以添加最小 provider 指令，例如横屏、连续视频、保持镜头顺序、参照图路径绑定。
- 不得重写 `group_body` 中的剧情事实、镜头顺序或角色动作。
- 不得把 YAML 主体清单写成剧情正文；只可写成主体参照说明，并在每个有图主体信息后追加 `@<图片路径>`。
- 不得承诺 LibTV 不支持的参数或能力；模型、时长、分辨率以 `.agents/skills/cli/libTV` 当前约束为准。

## Reference Path Suffix Rule

- 当使用 `libtv_session_with_uploaded_references` 时，prompt 必须在对应主体信息后追加 `@<图片路径>`，例如 `角色：林寂 @projects/.../林寂-多视图.png`。
- 每个路径后缀必须说明主体名称、类别、图片变体，例如 `多视图角色参考`、`主图道具参考`。
- 缺图主体不得添加 `@` 后缀，也不得写 `@空`、`@null` 或空路径。
- `@<图片路径>` 的顺序必须与 submit plan 的 `images[]` 顺序一致；prompt 内不使用抽象占位符替代图片路径。

## Length Handling

- 默认保留完整 `group_body`。
- 若 LibTV prompt 长度或人工策略要求压缩，必须在 submit plan 中记录：
  - `source_group_body_preserved: true`
  - `prompt_compression: none / reviewed_summary`
  - `source_group_body_path`
  - `compression_reason`
- 压缩只能保留事实，不得添加新剧情。

## Gate

通过 prompt gate 必须满足：

1. prompt 能回指 `source_file` 与 `group_id`。
2. `group_body` 是主要内容，且没有被剧情改写。
3. 若存在参考图，对应主体信息后有 `@<图片路径>`，且顺序与 `images[]` 一致。
4. 若没有参考图，prompt 不包含空 `@` 后缀。
