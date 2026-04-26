# 道具处理顺序细则

## Order

1. `清单`: 从 `3-Detail` 或已有输入中收束道具主体，最终写 `道具清单.md`。
2. `设计`: 对清单中的每个道具主体，沿用 `prop_masterprompt.structured.v2.md` 写 `[主体名].md`。
3. `面板`: 对每个 `[主体名].md`，沿用 `道具面板-提示词.json` 的机制写 `[主体名].json`。

## Output Root

最终交付物统一写到：

```text
projects/aigc/<项目名>/4-设计/
```

旧路径 `5-设计/道具/1-清单/`、`5-设计/道具/2-设计/`、`5-设计/道具/3-面板/` 仅作为迁移兼容来源，不再是新合同的默认交付路径。

## Compatibility

- 旧 `道具清单.json + 道具研究.json + prop_design_bridge.json` 可以作为中间侧车保留。
- 旧 `道具设计.json / prop_design_prompt.json` 可以作为 machine-readable 兼容侧车保留。
- 兼容侧车不得替代 `道具清单.md`、`[主体名].md`、`[主体名].json` 三类最终交付物。
