# Output Template

Canonical module for `1-分集` output-template design.

- upstream router: `deconstruct-elements`
- target skill: `.agents/skills/aigc/1-规划/subtypes/1-分集`

## deconstruct-elements Design Snapshot

- 消费终局：让后续规划、编导、脚本阶段稳定读取逐集边界、分集证据，并在分集确定后立即获得空白 `编导/第N集.json` 真源文件。
- 共享核心字段：
  - 输入清单
  - 主路由决议
  - 候选边界
  - 分集规划表
  - 覆盖率结论
  - 编导根文件初始化记录
  - 验收结论
- 变体字段：
  - `episode-index.md` 是否落盘
  - 各项目自定义的 `source_span` 表达粒度

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

### `编导/第N集.json`

- 路径：`projects/<项目名>/编导/第N集.json`
- 动态加载模板：`.agents/skills/aigc/_shared/director_episode_bootstrap.template.json`
- 结构真源：`.agents/skills/aigc/_shared/director_episode_output.schema.json`
- 初始化责任：`1-分集` 首次创建；`2-组间` 与 `3-明细` 后续按字段分属 patch-in-place。

## 固定槽位落盘表

| field_id | fixed slot | 说明 |
| --- | --- | --- |
| `FIELD-EPS-CTX-01` | `执行报告.md / 输入清单` | 输入文件、范围、累计字数 |
| `FIELD-EPS-CTX-02` | `执行报告.md / 路由决议` | 主路由、证据、放弃其他主策略的原因 |
| `FIELD-EPS-STR-01` | `执行报告.md / 候选边界` | 候选切点与排除理由 |
| `FIELD-EPS-STR-02` | `执行报告.md / 分集规划表` | 每集范围、主事件、边界理由、字数 |
| `FIELD-EPS-CST-01` | `执行报告.md / 覆盖率校验` | 缺文、重文、越界检查 |
| `FIELD-EPS-MAT-01` | `projects/<项目名>/编导/第N集.json` | 初始化空白编导根文件，并登记每集 bootstrap 输出路径 |
| `FIELD-EPS-CST-02` | `执行报告.md / 验收结论与返工项` | PASS/FAIL、失败码、返工入口 |
