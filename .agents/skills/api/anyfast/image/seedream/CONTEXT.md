# Context: seedream

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
current_chars: auto
current_lines: auto
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-03-10T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

本文件作为 `seedream` 技能的经验层，默认以知识库模式维护：优先沉淀火山引擎方舟 Ark API 的 SEEDREAM 5.0 请求构造、连续多图生成、流式 SSE 解析，以及响应处理与排错顺序。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-SDR-AUTH-MISSING` | 真实请求启动即报"缺少 API Key"并退出 | 环境配置层 | 在根目录 `.env` 中配置 `SEEDREAM_API_KEY=...` | 保持 `.env` 为 API Key 单一事实源；脚本支持 `SEEDREAM_API_KEY / ARK_API_KEY / VOLCENGINE_ARK_API_KEY` 三级回退 | 非 dry-run 调用时不再报认证错误 |
| `TM-SDR-DRYRUN-NOAUTH` | 只想看 payload，却因为没有 API Key 连 dry-run 都跑不起来 | 执行入口层 | 让 `--dry-run --print-payload` 跳过认证检查 | 固化“真实请求强认证，dry-run 只验结构”的入口合同 | 无 key 时 dry-run 仍能输出 payload |
| `TM-SDR-STREAM-HANG` | 启用 `--stream` 后请求挂起或无输出 | 网络/SSE 层 | 去掉 `--stream` 回退非流式模式重试 | 在技能文档与排错流程中固化"流式不稳定时优先回退非流式"策略 | 非流式模式下正常返回图片 |
| `TM-SDR-PAYLOAD-MISMATCH` | 请求返回 4xx，错误信息指示字段不合法 | 请求体构造层 | 使用 `--dry-run --print-payload` 检查最终 payload，与 `references/api.md` 对照 | 保持脚本 payload 构造与 Ark API 文档同步；新增字段时先更新 `references/api.md` | payload 中所有字段在 API 文档中有对应 |
| `TM-SDR-IMAGE-URL-INVALID` | 参考图生图失败，错误信息指示图片 URL 不可访问 | 输入层 | 确认 `--image-url` 传入的 URL 可公网访问；必要时将图片上传到可访问的存储 | 在调用前增加 URL 可达性预检查（HEAD 请求） | 参考图 URL 返回 200 |
| `TM-SDR-OUTPUT-PATH` | 产物落到脚本默认的 `output/seedream` 而非项目化目录 | 输出路由层 | 显式传 `--output-dir "output/影片/[项目名]/5-API/image/seedream/"` | 在上游调用时统一注入项目化输出路径 | 报告中的 `saved_files` 路径包含项目名 |
| `TM-SDR-DEDUP-MISS` | 流式返回中出现重复图片 | SSE 解析层 | 检查 `_merge_items` 去重逻辑是否覆盖当前返回格式 | 保持脚本中 URL/Base64 双维度去重 | `result_count` 与实际不重复图片数一致 |
| `TM-SDR-B64-DECODE` | `response_format=b64_json` 时图片文件损坏 | 响应解析层 | 检查 Base64 数据是否完整（未被截断）；检查文件扩展名是否正确 | 在脚本中增加 Base64 长度校验 | 落盘图片可正常打开 |
| `TM-SDR-LARGE-SEQUENTIAL-TIMEOUT` | `--max-images` 较大且非流式调用时读超时，错误类似 `Read timed out` | 执行/网络层 | 改用 `--stream`，或提高 `--timeout`，或降低 `--max-images` 分批测试 | 脚本失败报告写入 `diagnostic_hint`；排错流程优先把大批量连续图切到流式 | 报告中出现可执行诊断提示；流式或分批调用能返回图片 |
| `TM-SDR-STREAM-TOPLEVEL-URL` | 流式完成事件显示 `usage.generated_images > 0`，但脚本 `result_count=0` | SSE 解析层 | 解析 `image_generation.partial_succeeded` 顶层 `url / b64_json`，不只读取非流式 `data[]` | 空结果必须写 `ok=false`；报告保留 `stream_event_count / stream_event_types` 便于定位事件形态 | 流式调用能从 partial 事件提取图片；无图时退出码非 0 |

## Repair Playbook

1. **认证检查**：
   - 确认 `.env` 存在且包含 `SEEDREAM_API_KEY`（或 `ARK_API_KEY` / `VOLCENGINE_ARK_API_KEY`）
   - 确认 Key 未过期、未被吊销
2. **Dry Run 验证**：
   - 运行 `python3 .agents/skills/api/anyfast/image/seedream/scripts/seedream_generate.py --prompt "test" --dry-run --print-payload`
   - 核查 payload 中 `model / prompt / size / sequential_image_generation` 等字段
   - 该步骤允许在无 key 情况下执行；只有真实请求才要求认证
3. **流式回退**：
   - 若 `--stream` 挂起或无输出，先去掉 `--stream` 重试
   - 非流式成功后再排查流式问题
   - 若 `--max-images >= 5` 的非流式连续多图读超时，优先改用 `--stream`；仍不稳定时再降低 `--max-images` 分批验证
   - 若流式报告出现 `usage.generated_images > 0` 但 `result_count=0`，检查解析器是否兼容顶层 `url / b64_json` 事件
4. **参考图排查**：
   - 确认每个 `--image-url` 可公网 GET 访问
   - 用 `curl -I <url>` 验证返回 200
5. **HTTP 错误排查**：
   - 查看报告 JSON 中的 `error` 字段
   - 对照 `references/api.md` 核实字段合法性
   - 常见 4xx：认证失败（401）、参数错误（400）、模型不存在（404）
   - 常见 5xx：服务端异常，等待重试
6. **输出目录排查**：
   - 确认 `--output-dir` 指向 `output/影片/[项目名]/5-API/image/seedream/`
   - 确认目录有写权限
7. **落盘排查**：
   - 若 `saved_files` 为空但 `result_count > 0`，检查 `--no-save-images` 是否被意外传入
   - 若 URL 下载失败，检查图片 URL 是否临时有效（可能过期）

## Reusable Heuristics

- 首次使用前，务必先跑一次 `--dry-run --print-payload` 确认 payload 结构；真实请求前再确认 API Key 是否正确加载。
- `response_format=url` 是默认且最稳定的模式；`b64_json` 适用于不方便从外部 URL 下载的场景。
- 连续多图（`sequential_image_generation=auto`）是 SEEDREAM 5.0 的核心差异化能力，适合生成同一主题的系列图片。
- `--max-images` 控制连续图上限，但实际输出数量可能少于该值（取决于模型判断）。
- 大批量连续图不要优先使用非流式长等；`--max-images >= 5` 的研究性测试优先启用 `--stream`，便于避免读超时并保留中间事件。
- SEEDREAM 流式图片结果可能出现在 `image_generation.partial_succeeded` 事件顶层，非流式结果通常在 `data[]`；解析器必须同时支持两种结构。
- 流式返回适合大批量或需要实时进度的场景，但网络不稳定时优先使用非流式。
- 参考图数量建议 1-3 张；过多参考图可能导致模型难以融合。
- `--extra-json` 可用于注入 API 文档中已发布但脚本尚未显式支持的新字段。
- 输出文件名由 `--filename-prefix` 控制，默认 `seedream`；批量场景建议按分镜 ID 设置前缀。
- 密钥优先从根目录 `.env` 读取，脚本支持三级回退：`SEEDREAM_API_KEY > ARK_API_KEY > VOLCENGINE_ARK_API_KEY`。
- 水印默认启用；正式交付场景可用 `--no-watermark` 关闭。
