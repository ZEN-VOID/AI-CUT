# Video Reference Heuristics

## Heuristics

- 视频分镜画面参照的主要风险是跳步：有 prompt 就下命令、有图就临时拼参数、有 provider 名就假装可执行。
- 融合包要把三段 handoff 变成证据链：distill 证明请求对象稳定，reference-binding 证明引用可信，generation-handoff 证明下一入口可执行。
- 无参照图不一定失败；无参照图但项目 `Assets/` 已有可用素材且没有 `no_reference` 声明，通常是 unresolved。
- 同一 `Assets/` token 命中多个高分候选时，最稳策略是阻断，让用户或上游资产管理重新裁决。
- provider-neutral 的 `image_ref` 不是 provider-specific 参数；Dreamina 等本地上传型 provider 必须在 handoff 层解析成可上传本地路径。
- 旧三段包仍存在时，新包要避免“双写真源”：旧包是来源与兼容入口，新包是本融合路径的当前入口。
