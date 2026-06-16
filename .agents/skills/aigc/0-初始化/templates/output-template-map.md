# Output Template Map

Active `$aigc-init` writeback is scaffold-only.

| output | target path | template | status |
| --- | --- | --- | --- |
| project scaffold directories | `projects/aigc/<项目名>/0-初始化/` through `10-画布/` | none | active |
| project memory | `projects/aigc/<项目名>/MEMORY.md` | `templates/project-memory.template.md` | active |
| project context root | `projects/aigc/<项目名>/CONTEXT/README.md` | `templates/project-context-readme.template.md` | active |

Inactive former initialization outputs:

- `projects/aigc/<项目名>/0-初始化/north_star.yaml`
- `projects/aigc/<项目名>/0-初始化/init_handoff.yaml`
- `projects/aigc/<项目名>/0-初始化/story-source-manifest.yaml`
- `projects/aigc/<项目名>/team.yaml`
- `projects/aigc/<项目名>/STATE.json`
- `projects/aigc/<项目名>/CHANGELOG.md`

The templates for inactive outputs may remain in the package as historical or migration material, but they are not active initialization writeback targets.
