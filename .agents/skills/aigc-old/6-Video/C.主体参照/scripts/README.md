# Scripts

本目录只承载机械辅助脚本或脚本说明，不承载主体参照主创逻辑。

## Legacy Helpers

- `1-提示词蒸馏/全能参照/scripts/generate_episode_packets.py` 可作为旧三件套兼容迁移、字段投影和校验参考。
- `2-参照引用/scripts/bind_reference_assets.py` 可作为资产扫描和严格校验参考，但新包输出根必须投影到 `projects/aigc/<项目名>/6-Video/C.主体参照/<episode_id>/`。

## Guardrails

1. 脚本不得主创生成 prompt、TXT 主稿或主体语义裁决。
2. 脚本不得把猜测性主体匹配写入 canonical request。
3. 脚本不得移动、删除或重命名旧三个 source package。
4. 若未来新增本包脚本，必须默认提供 `--dry-run` 或等价预览模式。
