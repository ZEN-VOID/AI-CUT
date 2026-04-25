# Prompt Distillation Contract

本文件承接旧 `全能参照` 的组级 prompt/TXT 蒸馏语义，负责 `distill/` 段。

## Scope

- 输入是 `projects/aigc/<项目名>/3-Detail/<episode_id>.json` 中稳定的分镜组或整集分镜组集合。
- 输出是组级视频请求对象、人工审阅 TXT 与 `_manifest.json`。
- 本段不绑定真实图片资产，不组织 provider 提交计划。

## LLM Authorship

- prompt 和 TXT 主稿必须由 LLM 直接完成。
- 脚本只能做读取、投影、校验和落盘辅助，不得主创生成组级视频描述。
- 若复用旧 `generate_episode_packets.py`，只能作为兼容迁移或校验辅助。

## Distillation Requirements

- `3-Detail/<episode_id>.json` 必须是 canonical detail root，且能稳定投影为组级/镜级视图。
- 每个目标分镜组必须覆盖组级设计块和组内全部镜头事实。
- prompt 默认采用旧 `全能参照` 的 `BC` 结构：组级设计块 + 每镜一行融写结果。
- TXT 必须保留可人工审阅的组级块和镜级块，并覆盖：
  - `分镜组ID`
  - `全局风格 / 类型元素 / 导演意图`
  - `剧本正文`
  - `主体锚定.场景 / 角色 / 道具`
  - `分镜明细`
- 对 `C.主体参照`，`主体锚定` 不只是正文字段，还必须为后续 `subject-index.json` 提供候选主体证据。

## Distill Output

- `distill/<episode_id>.json`
- `distill/<episode_id>.txt`
- `distill/_manifest.json`

`_manifest.json` 至少记录：

- source detail root
- episode id
- group scope
- generated packets
- source group ids
- source shot ids
- prompt char count verification
- subject candidate extraction status
