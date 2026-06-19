# Output Template Map

Active `$aigc-init` writeback is scaffold plus centralized project memory.

| output | target path | template | status |
| --- | --- | --- | --- |
| project scaffold directories | `projects/aigc/<项目名>/1-分集/` through `10-画布/` | none | active |
| project memory | `projects/aigc/<项目名>/MEMORY.md` | `templates/project-memory.template.md` | active; owns initialization user requirements, team configuration, supplied-reference absorption summaries, and downstream context guidance |
| project context root | `projects/aigc/<项目名>/CONTEXT/README.md` | `templates/project-context-readme.template.md` | active |

Inactive former initialization outputs:

- `projects/aigc/<项目名>/0-初始化/init_handoff.yaml`
- `projects/aigc/<项目名>/0-初始化/story-source-manifest.yaml`
- `projects/aigc/<项目名>/team.yaml`
- `projects/aigc/<项目名>/STATE.json`
- `projects/aigc/<项目名>/CHANGELOG.md`

The former `north_star.yaml` carrier is fully retired and has no active template. Downstream aesthetic context belongs to `2-美学`: `类型风格.md`, `画面基调/全局风格协议.md`, and current-episode or baseline style protocol outputs. Templates for other inactive outputs may remain only as migration material and are not active initialization writeback targets. User-specified information that previously would have been split into `team.yaml`, handoff seeds, or other initialization carriers must be summarized into `MEMORY.md` unless a later owning workflow explicitly creates a separate canonical artifact.
