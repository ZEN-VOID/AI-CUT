# Scripts

This directory is reserved for mechanical helpers for `$aigc-init`.

Allowed script responsibilities:

- validate paths and required files
- project skeleton dry-runs
- template projection checks
- YAML/JSON schema or field checks
- reference synchronization audits

Scripts must not:

- generate creative story, design, prompt, or aesthetic decisions
- replace planning direct-answer subagents
- synthesize `north_star` or `init_handoff` as canonical creative truth
- silently delete or purge project assets

Current package-level validation uses:

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/aigc/0-Init
python3 scripts/skill_context_audit.py --strict
python3 scripts/aigc_skill_audit.py --strict
```
