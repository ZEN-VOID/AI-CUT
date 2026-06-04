# Init Review Gate

This file owns quality evaluation for scaffold-only `$aigc-init`.

## Sufficiency Gate

Initialization is incomplete unless all applicable items pass:

- project name and root are clear
- project root is under `projects/aigc/<项目名>/`
- current scaffold directories exist: `0-初始化/`, `1-分集/`, `2-编剧/`, `3-美学/`, `4-导演/`, `5-表演/`, `6-氛围/`, `7-分镜/`, `8-摄影/`, `9-光影/`, `10-分组/`, `11-主体/`, `12-图像/`, `13-画布/`, `14-审片/`
- project root `MEMORY.md` exists
- project root `CONTEXT/` exists, with `README.md` when this run creates the context root
- initialization-time user requirements and stable long-term inclinations are recorded in `MEMORY.md` when supplied
- existing `MEMORY.md` was merged or preserved, not silently overwritten
- this run did not create former initialization artifacts: `north_star.yaml`, `init_handoff.yaml`, `story-source-manifest.yaml`, `team.yaml`, `STATE.json`, `CHANGELOG.md`, `源/`, or governance sidecars
- empty scaffold directories are treated only as readiness containers

## Pass Table

| field_id | pass standard | fail code | rework entry |
| --- | --- | --- | --- |
| `FIELD-INIT-03` | Canonical project root is resolved under `projects/aigc/<项目名>/` | `FAIL-INIT-03` | `N1-project-root` |
| `FIELD-INIT-05` | Current 0-14 scaffold directories and project `CONTEXT/` exist, and removed outputs are absent | `FAIL-INIT-05` | `N2-scaffold` / `N4-readback` |
| `FIELD-INIT-09` | `MEMORY.md` exists and captures supplied long-term requirements without losing prior memory; `CONTEXT/README.md` exists when context root is created | `FAIL-INIT-09` | `N3-memory` |

## Review Dimensions

| dimension | check |
| --- | --- |
| scope | root stays under `projects/aigc/<项目名>/` |
| runtime | stage directories match latest 0-14 skill package names |
| context | `CONTEXT/` exists as neutral project context root |
| memory | `MEMORY.md` exists, preserves previous memory, and records supplied long-term requirements |
| removed artifacts | former multi-file initialization outputs are not generated |
| compatibility | old aliases are treated only as historical inputs, not new scaffold paths |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | scaffold is ready |
| `pass_with_todo` | usable with non-blocking follow-up |
| `needs_rework` | blocking scaffold or memory issue exists |
| `blocked` | missing input, path conflict, or unsafe overwrite/delete scope prevents execution |

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: scope | runtime | context | memory | removed_artifacts | compatibility
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Maintenance Review Flow

1. Run `python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/aigc/0-初始化` when the validator is available.
2. Run `python3 scripts/aigc_skill_audit.py --strict` when changing AIGC registry, stage, or runtime contracts; report unrelated existing failures separately.
3. Reusable findings belong in `CONTEXT.md`.
