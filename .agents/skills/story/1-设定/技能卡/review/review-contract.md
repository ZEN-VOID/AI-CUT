# Skill Card Review Contract

| gate | pass_condition | fail_code |
| --- | --- | --- |
| taxonomy gate | `group` and `skill_taxonomy.primary_domain` are aligned | `FAIL-SKILL-TAXONOMY` |
| advisor consultation gate | when subagents are explicitly enabled, project `team.yaml` advisors have been consulted and their guidance is reduced into activation, cost, progression, counterplay, or failure-mode decisions | `FAIL-SKILL-ADVISOR` |
| rule gate | activation, limits, and costs are concrete | `FAIL-SKILL-RULES` |
| progression gate | growth path and mastery stages are usable by planning | `FAIL-SKILL-PROGRESSION` |
| counterplay gate | strong skills have credible failure or counterplay | `FAIL-SKILL-COUNTERPLAY` |
| owner gate | skill card does not rewrite world, character, scene, or item truth | `FAIL-SKILL-OWNER` |
