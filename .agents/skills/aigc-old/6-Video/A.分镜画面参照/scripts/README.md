# scripts/

本目录只承载机械辅助脚本，不承载 prompt/TXT 主创。

当前本包不直接复制旧脚本为默认入口，原因：

- `首帧参照/scripts/generate_episode_packets.py` 仍带 LLM-first authorship gate，不能成为本融合包的默认主创执行器。
- `2-参照引用/scripts/bind_reference_assets.py` 可作为后续移植候选，但本轮先在合同层融合语义，避免误把旧输出路径写回新包。

后续若补 orchestrator，必须满足：

1. 只读取、校验、投影或串联已由 LLM 确认的 canonical creative truth。
2. 不生成创作性 prompt、TXT 主稿或 provider 简报正文。
3. 默认输出到 `projects/aigc/<项目名>/6-Video/A.分镜画面参照/<episode_id>/`。
4. 提供 `--dry-run`。
