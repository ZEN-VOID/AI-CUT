# Execution Flow

## Inputs

- 首选：`projects/<项目名>/3-Detail/第N集.json`
- 兼容：`projects/<项目名>/3-Detail/第N集.json`
- shared schema：`.agents/skills/aigc/_shared/director_episode_output.schema.json`

## Default Output Root

- `projects/<项目名>/4-Design/道具/1-清单/第N集/`

## Commands

```bash
python3 .agents/skills/aigc/4-Design/道具/1-清单/scripts/run_prop_list_pipeline.py \
  --input "projects/<项目名>/3-Detail/第N集.json"
```

```bash
python3 .agents/skills/aigc/4-Design/道具/1-清单/scripts/run_prop_list_pipeline.py \
  --input "projects/<项目名>/3-Detail/第N集.json" \
  --output-dir "projects/<项目名>/4-Design/道具/1-清单/第N集"
```

```bash
python3 .agents/skills/aigc/4-Design/道具/1-清单/scripts/run_prop_list_pipeline.py \
  --input "projects/<项目名>/3-Detail/第N集.json" \
  --dry-run
```

## Pipeline

1. `run_prop_list_pipeline.py`
2. `extract_episode_props.py`
3. `build_prop_research.py`

## Hard Gates

1. 输入必须可被 `.agents/skills/aigc/_shared/director_episode_output.schema.json` 解释。
2. 只允许抽取上游 `道具及状态` 已经出现的对象。
3. `prop_design_bridge.json` 必须和研究结果同轮生成，不能留到下游补。
4. 默认输出目录必须处于 `4-Design/道具/1-清单/`，不能继续落回旧仓 `3-设定`。
