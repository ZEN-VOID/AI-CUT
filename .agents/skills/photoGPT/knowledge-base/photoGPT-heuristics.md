# photoGPT Knowledge Base Boundary

`knowledge-base/` 只用于维护者手动加入的外部资料、资料索引或参考包说明，不承载运行经验、失败模式、提示词策略或执行规则。

当前可复用经验已迁入同目录 `CONTEXT.md`：

- 类型定位、图序锁定、保留/变化/负面约束经验。
- `元素替换`、`修图`、`多视图`、`多图融合`、`风格化` 的失败模式。
- `gpt-image-2` provider 边界和禁止 fallback 经验。
- `steps/` 节点漂移、脚本作者性越权和 `knowledge-base` 边界漂移经验。

若后续加入外部参考资料，必须满足：

- 由用户或维护者手动加入。
- 只作为内容参考，不自动成为 `photoGPT` 执行规则。
- 需要参与运行时，必须先由 `SKILL.md` 的 `Module Loading Matrix` 授权。
