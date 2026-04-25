# 场景处理顺序细则

## Order

1. `清单`: 从 `3-Detail` 或已有输入中收束场景主体，最终写 `场景清单.md`。
2. `设计`: 对清单中的每个场景主体，沿用 `scene_masterprompt.structured.v2.md` 写 `[主体名].md`。
3. `面板`: 对每个 `[主体名].md`，沿用 `场景面板-提示词.json` 的机制写 `[主体名].json`。

## Output Root

最终交付物统一写到：

```text
projects/aigc/<项目名>/4-Design/
```

旧路径 `4-Design/场景/1-清单/`、`4-Design/场景/2-设计/`、`4-Design/场景/3-面板/` 仅作为迁移兼容来源，不再是新合同的默认交付路径。

## Compatibility

- 旧 `场景清单.json + 场景研究.json + scene_design_bridge.json` 可以作为中间侧车保留。
- 旧 `scene_design.json` 可以作为 machine-readable 兼容侧车保留。
- 兼容侧车不得替代 `场景清单.md`、`[主体名].md`、`[主体名].json` 三类最终交付物。
