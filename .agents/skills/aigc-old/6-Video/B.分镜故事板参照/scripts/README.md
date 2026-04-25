# Scripts

本目录只承载机械辅助脚本说明。当前不复制旧脚本。

可引用的 legacy helper：

- `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/scripts/generate_episode_packets.py`
- `.agents/skills/aigc/6-Video/2-参照引用/scripts/bind_reference_assets.py`

使用约束：

1. 旧 `全能参照` helper 不得成为本包默认主创执行器。
2. 旧 `bind_reference_assets.py` 可作为资产扫描和严格校验参考，但新包输出根必须投影到 `projects/aigc/<项目名>/6-Video/B.分镜故事板参照/<episode_id>/`。
3. 若新增脚本，只能做读取、校验、投影、格式转换、路径审计和 manifest 回写。
