# Execution Flow

## Default Inputs

- `projects/<项目名>/4-Design/4-道具/1-清单/第N集/prop_design_bridge.json`
- `projects/<项目名>/4-Design/4-道具/1-清单/第N集/道具研究.json`
- `projects/<项目名>/3-Detail/第N集.json`
- `projects/<项目名>/2-Global/全局风格.md`（若存在）
- `projects/<项目名>/2-Global/类型指导.md`（若存在）

## Default Outputs

- `projects/<项目名>/4-Design/4-道具/2-设计/第N集/道具设计.json`
- `projects/<项目名>/4-Design/4-道具/2-设计/第N集/prop_design_prompt.json`
- `projects/<项目名>/4-Design/4-道具/2-设计/第N集/_manifest.json`

## CLI

```bash
python3 .agents/skills/aigc/4-Design/4-道具/2-设计/scripts/run_prop_design_pipeline.py \
  --bridge "projects/<项目名>/4-Design/4-道具/1-清单/第N集/prop_design_bridge.json" \
  --research "projects/<项目名>/4-Design/4-道具/1-清单/第N集/道具研究.json" \
  --detail "projects/<项目名>/3-Detail/第N集.json" \
  --global-style "projects/<项目名>/2-Global/全局风格.md" \
  --type-guide "projects/<项目名>/2-Global/类型指导.md"
```

## Dry Run

```bash
python3 .agents/skills/aigc/4-Design/4-道具/2-设计/scripts/run_prop_design_pipeline.py \
  --bridge "projects/<项目名>/4-Design/4-道具/1-清单/第N集/prop_design_bridge.json" \
  --research "projects/<项目名>/4-Design/4-道具/1-清单/第N集/道具研究.json" \
  --detail "projects/<项目名>/3-Detail/第N集.json" \
  --dry-run
```

## Hard Checks

1. 若 `bridge` 缺失，必须阻塞并提示先执行 `1-清单`。
2. canonical 输出根必须位于 `projects/<项目名>/4-Design/4-道具/2-设计/第N集/`。
3. `prop_design_prompt.json` 必须和 `道具设计.json` 同轮生成。
4. 若 brief 中有错位路径，必须记录到 `_manifest.json.path_normalization`。
