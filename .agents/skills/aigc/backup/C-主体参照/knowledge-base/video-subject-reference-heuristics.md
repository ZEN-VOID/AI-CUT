# Video Subject Reference Heuristics

本文件保存稳定经验与可复用策略，不承载入口路由权。

## Heuristics

- `5-分组` 的组正文通常已经比重新蒸馏的短 prompt 更可靠，尤其适合 LibTV 这类能消费长中文镜头描述的视频工具。
- YAML 主体清单越保守，参照绑定越稳；缺图主体保留在 prompt 文字里即可，不必强行找近似图。
- 多视图图适合锁身份、服装、道具结构和场景布局；主图更适合缺少多视图时作为最低锚点。
- LibTV 提交最容易丢的是状态而不是 prompt；批量任务必须先设计 queue ledger，再谈并发。
- 当 `libtv_session_with_uploaded_references` 上传图过多时，可优先保留主角、核心场景、关键道具，辅助群像和普通道具只进入文字 prompt，并在 manifest 记录未上传原因。
- 组级视频时长应继承 `5-分组` 的 `时长估算`，再按 LibTV 当前 4-15 秒范围 clamp；不要把所有组固定为 15 秒。
