# 5-Image / 2-参照引用 / NANO-banana 模块

## 适用模式

- `provider_mode=nano_banana`
- `provider_mode=dual_mode`

## 绑定目标

把 provider-neutral 的本地图片引用，准备成 `NANO-banana` 可继续编码为 BASE64 / data URL 的兼容槽位。

## 固定规则

1. `image_markers[].provider_variants.nano_banana.input_mode` 固定为 `base64`
2. 本阶段默认允许：
   - `resolution_status=pending_encode`
   - `resolved_input=""`
3. 若输入本身已经是合法 data URL / BASE64，可写成 `resolution_status=ready`
4. 若输入只是本地路径，不得伪造 BASE64；编码责任交给 `3-图像生成`

## 审计点

- 未生成伪 BASE64
- `pending_encode` 与 `ready` 状态清楚
- 后续仍可从 `image_ref` 回推原始本地图片

