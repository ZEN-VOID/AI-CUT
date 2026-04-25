# 5-Image / 2-参照引用 / 即梦 CLI 模块

## 适用模式

- `provider_mode=jimeng_cli`
- `provider_mode=dual_mode`

## 绑定目标

把 provider-neutral 的本地图片引用，解析成 `即梦 CLI` 可直接消费的本地文件路径。

## 固定规则

1. `image_markers[].provider_variants.jimeng_cli.input_mode` 固定为 `local_path`
2. `resolved_input` 只能写真实本地路径
3. 不得写远程 URL、虚构路径、占位路径
4. 若引用本身已是本地路径，则可直接复用 `image_ref`

## 审计点

- 路径存在
- 路径位于项目本地可读目录
- `resolution_status=ready`
- 与 `reference_images[]` 顺序一致

