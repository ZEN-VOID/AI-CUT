# SEEDREAM 5.0 API 参考

## 1. 接口地址

- `POST https://ark.cn-beijing.volces.com/api/v3/images/generations`

## 2. 认证

- Header: `Authorization: Bearer <API_KEY>`
- 建议在仓库根 `.env` 使用 `SEEDREAM_API_KEY=...`

## 3. 核心请求字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `model` | string | 模型 ID，当前为 `doubao-seedream-5-0-260128` |
| `prompt` | string | 提示词 |
| `image` | string[] | 参考图 URL 列表（I2I） |
| `sequential_image_generation` | string | 连续多图模式，常用 `auto` |
| `sequential_image_generation_options.max_images` | int | 连续图最大张数 |
| `response_format` | string | `url` 或 `b64_json` |
| `size` | string | 输出尺寸，如 `2K` |
| `stream` | bool | 是否启用流式返回 |
| `watermark` | bool | 是否开启水印 |

## 4. 与脚本参数映射

| CLI 参数 | API 字段 |
| --- | --- |
| `--model` | `model` |
| `--prompt` | `prompt` |
| `--image-url` | `image[]` |
| `--sequential-image-generation` | `sequential_image_generation` |
| `--max-images` | `sequential_image_generation_options.max_images` |
| `--response-format` | `response_format` |
| `--size` | `size` |
| `--stream` | `stream=true` |
| `--watermark/--no-watermark` | `watermark` |
| `--extra-json` | 合并到请求体顶层 |

## 5. 官方文档

- [Volcengine 文档（SEEDREAM 5.0）](https://www.volcengine.com/docs/82379/1824121?lang=zh)

## 6. 官方示例（用户提供）

文本生图（连续 4 张）：

```bash
curl -X POST https://ark.cn-beijing.volces.com/api/v3/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${SEEDREAM_API_KEY}" \
  -d '{
    "model": "doubao-seedream-5-0-260128",
    "prompt": "生成连贯插画，核心为同一庭院一角的四季变迁，以统一风格展现四季独特色彩、元素与氛围",
    "sequential_image_generation": "auto",
    "sequential_image_generation_options": {
      "max_images": 4
    },
    "response_format": "url",
    "size": "2K",
    "stream": true,
    "watermark": true
  }'
```

参考图生图（连续 3 张）：

```bash
curl -X POST https://ark.cn-beijing.volces.com/api/v3/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${SEEDREAM_API_KEY}" \
  -d '{
    "model": "doubao-seedream-5-0-260128",
    "prompt": "生成女孩和奶牛玩偶在游乐园开心地坐过山车的图片，涵盖早晨、中午、晚上",
    "image": [
      "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimages_1.png",
      "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimages_2.png"
    ],
    "sequential_image_generation": "auto",
    "sequential_image_generation_options": {
      "max_images": 3
    },
    "response_format": "url",
    "size": "2K",
    "stream": true,
    "watermark": true
  }'
```
