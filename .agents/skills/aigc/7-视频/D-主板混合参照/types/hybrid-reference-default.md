# Hybrid Reference Default Type Package

本类型包是 `D-主板混合参照` 的默认固定上下文。

## Load When

- 用户要求主体参照和分镜故事板参照合二为一。
- 用户要求同一分镜组 prompt 同时导入主体参照图和分镜故事板。
- 用户要求主体参照与故事板整组总参照同场生效。

## Fixed Semantics

1. 故事板总参照约束整组构图、镜头顺序、站位、连续性和情绪节奏。
2. 主体参照约束对应角色、场景或道具的外观一致性。
3. 故事板图必须出现在 fenced YAML 的 `故事板参照.uploaded_url` 和 manifest 的 `storyboard_total_reference` 中，不得写到某个主体后。
4. 主体图必须写在对应主体信息后，不得作为泛化全局参照。
5. 缺图可以记录为可选缺口；错绑、空路径和静默丢图必须返工。
6. 视频时长不固定 15 秒；默认读取当前组 `时长估算`，按 4-15 秒范围 clamp 后写入 `duration_hint`。

## Review Gate

- prompt 以原组标题起笔，并在 fenced YAML 绑定故事板总参照。
- 每个 bound subject 在 prompt fenced YAML 中有对应 `uploaded_url`。
- manifest 能同时表达 `storyboard_total_reference` 与 `subject_references`。
