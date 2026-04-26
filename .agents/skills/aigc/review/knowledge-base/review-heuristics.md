# Review Heuristics

- 先判断 gate 所在层级，再判断问题归属；不要把 source truth 冲突错归给当前阶段。
- `FAIL-COVENANT` 比普通质量 issue 更优先，因为它说明审计证据本身不可靠。
- 父层只需要一个 aggregate packet；维度报告越多，越要防止它们并列夺权。
- 若 `resume` 无法定位返工入口，优先检查 `*.review.repair.json` 与 `governance-state.yaml.review_bridge`。

