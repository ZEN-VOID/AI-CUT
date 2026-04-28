# Vidu 回调签名

## 官方链接

- [callback-signature](https://platform.vidu.cn/docs/callback-signature)

## 最后核对日期

- `2026-04-21`

## 端点/认证

- 本模块不是单独的任务创建端点，而是验证 Vidu 回调请求真实性的算法说明。
- 其中：
  - `secret_key` = 创建任务时使用的 token
  - `access_key` = 固定字符串 `vidu`

## 请求体字段总表

无业务请求体；核心输入是签名算法所需的这些值：

| 字段 | 说明 |
| --- | --- |
| `http_method` | 大写 HTTP 方法 |
| `http_uri` | 从 `callback_url` 解析出的 path |
| `canonical_query_string` | 从 `callback_url` 解析出的 query string |
| `Date` | 请求头 Date |
| `X-HMAC-SIGNED-HEADERS` | 参与签名的 header 列表 |
| 各 signed headers 的值 | 按顺序拼接 |

## 子字段展开表

### 签名公式

```text
signature = base64(HMAC-SHA256(secret_key, signingString))
```

### `signingString`

```text
http_method + "\n" +
http_uri + "\n" +
canonical_query_string + "\n" +
access_key + "\n" +
Date + "\n" +
signed_headers_string
```

### `signed_headers_string`

```text
HeaderKey1:HeaderValue1\n
HeaderKey2:HeaderValue2\n
...
```

## 模型差异矩阵

- 无模型差异；该算法对所有带回调的任务统一适用。

## 默认值/范围/限制

- `http_method` 必须全大写
- `http_uri` 必须以 `/` 开头，空路径时为 `/`
- `canonical_query_string` 无 query 时为空字符串
- `access_key` 固定为 `vidu`
- `signed_headers_string` 必须按 `X-HMAC-SIGNED-HEADERS` 的顺序拼接
- 最后一行换行不能丢

## 响应体字段

- 本模块本身没有响应体字段；它服务于你验证回调头中的：
  - `X-HMAC-SIGNATURE`
  - `X-HMAC-ALGORITHM`
  - `X-HMAC-ACCESS-KEY`

## 任务状态/错误码

- 无任务状态
- 常见失败形态不是业务错误码，而是“签名不一致”

## repo-local 执行建议

- `verify-callback` 子命令中，header 名大小写和顺序不要擅自改写
- 若要比对官方回调，直接用收到的 header 原值
- 默认把 `VIDU_API_KEY` 当作 `secret_key`

## 已验证的真实踩坑记录

- 签名最容易错的不是算法，而是：
  - 把 `vidu` 误当成 `secret_key`
  - 丢掉最后一个换行
  - 改乱了 `X-HMAC-SIGNED-HEADERS` 的顺序
- repo-local 脚本已经把这些规则固定到 helper 中。
