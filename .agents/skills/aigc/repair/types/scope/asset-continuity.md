# Scope: Asset Continuity

用于修复场景、角色、道具、参照图、资产 alias、引用路径和跨阶段资产口径。

## Fixed Context

- 必查 `7-设计` 对应 `场景 / 角色 / 道具` 的清单、设计、生成请求和 review gate。
- 必查 `6-分组` 中资产首次出现、用途和镜头消费方式。
- 必查 `8-图像` / `9-视频` 中 reference manifest 或任务引用。

## Review Gate

- 同一资产的名称、alias、身份、外观、用途和路径一致。
- 下游引用旧资产时必须标记 invalidate / update / preserve。
