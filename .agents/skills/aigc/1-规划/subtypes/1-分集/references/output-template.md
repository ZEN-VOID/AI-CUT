# Output Template

Canonical module for `1-分集` output-template design.

- upstream router: `deconstruct-elements`
- target skill: `.agents/skills/aigc/1-规划/subtypes/1-分集`

## deconstruct-elements Design Snapshot

- 消费终局：让后续规划、编导、脚本阶段稳定读取逐集边界、分集证据，并为 `2-组间` 首次创建 `编导/第N集.json` 提供稳定的 `bootstrap_output` 目标路径。
- 共享核心字段：
  - 输入清单
  - 主路由决议
  - 候选边界
  - 分集规划表
  - 覆盖率结论
  - 编导根文件目标路径
  - 验收结论
- 变体字段：
  - `episode-index.md` 是否落盘
  - 各项目自定义的 `source_span` 表达粒度

## Parent-Skill Relationship

- `1-分集` 的 canonical 子路径产物仍是 `episode-split-plan.json`。
- 但在父级 `1-规划` 全链模式下，它只负责提供“集边界、主事件、coverage 结论、bootstrap_output 目标路径”给 `projects/<项目名>/规划/第N集.md` 聚合使用。
- `projects/<项目名>/规划/1-分集/第N集.md` 可以作为 `1-分集` 的本地可读 sidecar 持续保留，用来承载“该子路径已经切好的第N集文本与边界摘要”；它不是父级主稿，因此不与 `规划/第N集.md` 竞争真源。
- `episode-split-report.md` 默认降为非默认调试 sidecar；若无复核或排障需求，不必保留。
- `1-分集` 不单独承担规划阶段最终集级主稿职责。

## Output Template: Canonical JSON Skeleton

```json
{
  "schema_version": "aigc-planning-episode-split/v2",
  "meta": {
    "project": "<项目名>",
    "inputs": [],
    "route": {
      "primary": "P1|P2|P3",
      "loaded_reference": "references/type-strategies.md"
    }
  },
  "content": {
    "boundary_candidates": [],
    "episodes": [
      {
        "episode_id": "第1集",
        "source_span": "",
        "boundary_reason": "",
        "bootstrap_output": "projects/<项目名>/编导/第1集.json"
      }
    ]
  },
  "gate_summary": {
    "coverage": {
      "status": "PASS|FAIL",
      "missing_segments": [],
      "duplicate_segments": []
    },
    "verdict": {
      "status": "PASS|FAIL",
      "fail_codes": [],
      "rework_entry": "S1-S8"
    }
  },
  "execution_notes": {
    "next_stage": "2-组间|3-明细",
    "notes": []
  }
}
```

## Markdown Projection

### `episode-split-plan.json`

- 路径：`projects/<项目名>/Init/episode-split-plan.json`
- 角色：作为 `1-分集` 的 canonical 主文件，记录边界、规划表与 bootstrap 输出路径。

### `episode-split-report.md`

```markdown
# 分集执行报告

## 输入清单

## 路由决议

## 候选边界

## 分集规划表

## 覆盖率校验

## 验收结论与返工项
```

### `episode-index.json`（可选）

```json
[
  {
    "episode_id": "第1集",
    "route": "P2",
    "source_span": "第1章-第2章",
    "bootstrap_output": "projects/<项目名>/编导/第1集.json"
  }
]
```

### `bootstrap_output` 目标路径

- 规划登记路径：`episode-split-plan.json -> content.episodes[].bootstrap_output`
- 目标文件路径：`projects/<项目名>/编导/第N集.json`
- 动态加载模板：`.agents/skills/aigc/_shared/director_episode_bootstrap.template.json`
- 结构真源：`.agents/skills/aigc/_shared/director_episode_output.schema.json`
- 初始化责任：`1-分集` 只登记目标路径；`2-组间` 首次进入且文件缺失时再自动创建；`3-明细` 后续按字段分属 patch-in-place。

规则：

- `1-分集` 只负责登记未来路径，不在本阶段提前创建根文件。
- 如果需要记录分集过程解释，应落到 `episode-split-plan.json` 或 `episode-split-report.md`，而不是在规划阶段伪造 bootstrap 根文件。

## 固定槽位落盘表

| field_id | fixed slot | 说明 |
| --- | --- | --- |
| `FIELD-EPS-CTX-01` | `episode-split-report.md / 输入清单` | 输入文件、范围、累计字数 |
| `FIELD-EPS-CTX-02` | `episode-split-report.md / 路由决议` | 主路由、证据、放弃其他主策略的原因 |
| `FIELD-EPS-STR-01` | `episode-split-report.md / 候选边界` | 候选切点与排除理由 |
| `FIELD-EPS-STR-02` | `episode-split-report.md / 分集规划表` | 每集范围、主事件、边界理由、字数 |
| `FIELD-EPS-CST-01` | `episode-split-report.md / 覆盖率校验` | 缺文、重文、越界检查 |
| `FIELD-EPS-MAT-01` | `episode-split-plan.json / bootstrap_output` | 登记每集未来编导根文件目标路径 |
| `FIELD-EPS-CST-02` | `episode-split-report.md / 验收结论与返工项` | PASS/FAIL、失败码、返工入口 |

### `规划/1-分集/第N集.md`（本地可读 sidecar）

- 路径：`projects/<项目名>/规划/1-分集/第N集.md`
- 角色：承载 `1-分集` 已经切好的当前集正文、来源范围、主事件与边界理由，供人类直接核读。
- 真源边界：
  - 它不是 `1-分集` 的 canonical machine-readable 真源，后者仍是 `Init/episode-split-plan.json`
  - 它也不是父级 `1-规划` 的最终集级主稿，后者仍是 `projects/<项目名>/规划/第N集.md`

推荐骨架：

```markdown
# 第N集

## 分集来源

- source_span:
- route:
- bootstrap_output:

## 主事件

- ...

## 边界说明

- ...

## 当前集正文

<保留原文或切分后的当前集正文>
```

硬规则：

1. 该 sidecar 只表达 `1-分集` 已确定的集边界与当前集正文，不得提前写入 `2-格式` 的格式结构或 `3-分组` 的组级容器。
2. 若主故事源本身是 `storyboard_script / hybrid_story_text`，正文默认保真保留，不要为生成 sidecar 而先行“小说化清洗”。
3. 父级 `规划/第N集.md` 可引用该 sidecar，但不得与之互相覆盖。
