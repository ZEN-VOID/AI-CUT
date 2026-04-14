# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/5-Image/2-参照引用` 的经验层知识库，不是过程日志。
- 调用本技能时，应先加载根 `aigc`、`1-提示词蒸馏` 与本技能主合同。
- provider-specific 规范真源在 `references/`，经验层只沉淀失败模式、修复顺序与复用 heuristic。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 请求对象仍是旧 `image_url` 结构 | 共享模板层 | 升级到 `image_ref + ref_kind + provider_variants` | 在 `_shared` 模板与本技能 `R1` 固化双模式骨架 | 绑定结果不再依赖旧 URL 字段 |
| `jimeng_cli` 槽位写成 URL | provider 解析层 | 改回真实本地路径 | 在 `references/jimeng-cli.md` 固化 `local_path only` | 即梦 CLI 侧输入可直接上传 |
| `nano_banana` 提前写入伪 BASE64 | provider 解析层 | 回退到 `pending_encode`，让 `3-图像生成` 再做编码 | 在 `references/nano-banana.md` 固化“兼容态不伪造 base64” | 请求对象不再携带假编码 |
| `dual_mode` 只保留了单边 provider 槽位 | 模式裁决层 | 补回另一侧 provider_variants | 在主合同固化 `dual_mode` 的双槽位要求 | 双模式请求对象保持可续跑 |
| 本地图片歧义时被脚本或人工硬选一张 | 资产匹配层 | 阻断并报告歧义 | 在 `R3` 固化“歧义即失败” | 不再出现猜测性绑定 |

## Repair Playbook

1. 先查输入请求对象是否兼容 `v2` 模板。
2. 再查 `provider_mode` 是 `jimeng_cli`、`nano_banana` 还是 `dual_mode`。
3. 再查 `reference_images / image_markers` 是否能回链真实本地文件。
4. 再查 provider-specific 槽位是否写对：
   - 即梦 CLI 只收本地路径
   - NANO-banana 兼容态允许 `pending_encode`
5. 最后查三件套落盘与下一入口是否清楚。

## Reusable Heuristics

- `2-参照引用` 的核心不是“把图塞进去”，而是“保持 provider-neutral 真源与 provider-specific 槽位同时成立”。
- 即梦 CLI 与 NANO-banana 的最大差异不在 prompt，而在图片输入运输层：前者吃本地路径，后者最终吃 BASE64-compatible 载体。
- `dual_mode` 最稳的做法不是提前生成巨大的 BASE64，而是保留 canonical 本地引用，再把编码责任下沉到 `3-图像生成`。
- 绑定阶段若出现歧义，宁可阻断，也不要为了流畅感强行选图。

