# Scripts

This directory is reserved for mechanical helpers for `$aigc-init`.

Allowed script responsibilities:

- validate paths and required files
- project skeleton dry-runs
- template projection checks
- `MEMORY.md` template projection checks
- `CONTEXT/README.md` template projection checks
- reference synchronization audits

Scripts must not:

- generate creative story, design, prompt, or aesthetic decisions
- create former initialization artifacts such as `north_star`, `init_handoff`, `story-source-manifest`, `team.yaml`, `STATE.json`, `CHANGELOG.md`, or `源/`
- silently delete or purge project assets

Current package-level validation uses:

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/aigc/0-初始化
python3 scripts/skill_context_audit.py --strict
python3 scripts/aigc_skill_audit.py --strict
```
