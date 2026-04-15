# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/5-Image/2-参照引用` 的经验层知识库，不是过程日志。
- 调用本技能时，应先加载根 `aigc`、`5-Image` 阶段父级、`1-提示词蒸馏` 与本技能主合同。
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
| 泛词或子串匹配导致每组绑定大量重叠资产 | 候选推导层 | 重跑绑定，只放行完整角色名、主场景锚点、完整复合道具名；泛词进入 `ambiguous_candidates / rejected_candidates` | 在 `SKILL.md` 固化 `Candidate Derivation And Ambiguity Gate`，并用 `scripts/audit_reference_binding.py --strict` 防回归 | `match-report.md` 同时列出 bound / ambiguous / rejected，且审计脚本不再报过量绑定 |
| `2-参照引用` 三件套缺失 `next_entry` | 输出闭环层 | 在主 JSON、manifest、match-report 同步补下一入口 | 在 `SKILL.md` 的 Output Contract 与审计脚本中强制检查 `next_entry` | `/3-图像生成` 可从 `/2` 输出直接定位下一入口 |

## Repair Playbook

1. 先查输入请求对象是否兼容 `v2` 模板。
2. 再查 `provider_mode` 是 `jimeng_cli`、`nano_banana` 还是 `dual_mode`。
3. 再查 `reference_images / image_markers` 是否能回链真实本地文件。
4. 再查候选来源是否足够强：
   - 完整角色名、组级主场景锚点、完整复合道具名才可直接绑定
   - `门 / 灯 / 卫生间 / 吊顶 / 楼道 / 洗手池 / 门板` 等泛词不得直接绑定
   - 子串命中和同 token 多候选必须进入歧义清单
5. 再查 provider-specific 槽位是否写对：
   - 即梦 CLI 只收本地路径
   - NANO-banana 兼容态允许 `pending_encode`
6. 最后查三件套落盘与下一入口是否清楚。
7. 对已落盘结果运行：
   `python3 .agents/skills/aigc/5-Image/2-参照引用/scripts/audit_reference_binding.py --bound-json <第N集.json> --manifest <_manifest.json> --assets <selected-4-design-assets.json> --strict`

## Reusable Heuristics

- `2-参照引用` 的核心不是“把图塞进去”，而是“保持 provider-neutral 真源与 provider-specific 槽位同时成立”。
- 即梦 CLI 与 NANO-banana 的最大差异不在 prompt，而在图片输入运输层：前者吃本地路径，后者最终吃 BASE64-compatible 载体。
- `dual_mode` 最稳的做法不是提前生成巨大的 BASE64，而是保留 canonical 本地引用，再把编码责任下沉到 `3-图像生成`。
- 绑定阶段若出现歧义，宁可阻断，也不要为了流畅感强行选图。
- “路径真实存在”只是最低门槛，不等于“引用绑定正确”；引用还必须具备字段位证据和唯一候选。
- 漫画组级请求尤其容易被 `门 / 灯 / 卫生间` 这类高频词污染；这类词默认只能用于候选解释，不能直接进入 `reference_images`。
- 宽松参考图批次可以作为探索性输出，但不能冒充严格参照绑定版；严格版必须能解释每张图为什么属于该组。
