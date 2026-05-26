# Scope: Generated Media

用于修复图像、storyboard、视频、MP4、生成任务和审片缺陷。

## Fixed Context

- 图像问题回看 `8-图像` owning leaf、`6-分组` 源组和 `7-设计` 资产引用。
- 视频问题回看 `9-视频` owning leaf、上游图像/参照和 `10-审片` finding。
- repair 不直接修改二进制生成结果；只能保留、失效、重建任务或路由 provider。

## Review Gate

- asset action 必须是 `preserve | invalidate | regenerate | review_only` 之一。
- 若建议 regenerate，必须给出 source owner、输入修复点和 provider route。
