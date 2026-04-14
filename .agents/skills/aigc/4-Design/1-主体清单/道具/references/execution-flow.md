# Execution Flow

## Inputs

- 首选：`projects/aigc/<项目名>/3-Detail/第N集.json`
- 兼容：legacy `projects/aigc/<项目名>/编导/第N集.json`
- shared consumption：`.agents/skills/aigc/4-Design/1-主体清单/_shared/detail-output-consumption-contract.md`
- shared schema：`.agents/skills/aigc/_shared/director_episode_output.schema.json`
- shared normalization：`.agents/skills/aigc/4-Design/1-主体清单/_shared/object-normalization-contract.md`

## Default Output Root

- `projects/aigc/<项目名>/4-Design/道具/1-清单/第N集/`

## Commands

```bash
python3 .agents/skills/aigc/4-Design/1-主体清单/道具/scripts/run_prop_list_pipeline.py \
  --input "projects/aigc/<项目名>/3-Detail/第N集.json"
```

```bash
python3 .agents/skills/aigc/4-Design/1-主体清单/道具/scripts/run_prop_list_pipeline.py \
  --input "projects/aigc/<项目名>/3-Detail/第N集.json" \
  --output-dir "projects/aigc/<项目名>/4-Design/道具/1-清单/第N集"
```

```bash
python3 .agents/skills/aigc/4-Design/1-主体清单/道具/scripts/run_prop_list_pipeline.py \
  --input "projects/aigc/<项目名>/3-Detail/第N集.json" \
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
5. 对象名必须优先命中 stable noun；整句导演描述只能保留为 `state / raw_mentions`。
