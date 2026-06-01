# Skill Card Review Contract

## Review Gates

| gate | pass_condition | fail_code |
| --- | --- | --- |
| route | `module_route` 指向 `技能卡` | `FAIL-CD-SKILL-ROUTE` |
| taxonomy | `group` and `skill_taxonomy.primary_domain` are aligned | `FAIL-CD-SKILL-TYPE` |
| advisor_consultation | when subagents are explicitly enabled, project `team.yaml` advisors have been consulted and their guidance is reduced into activation, cost, progression, counterplay, or failure-mode decisions | `FAIL-CD-SKILL-ADVISOR` |
| rules | activation, limits, and costs are concrete | `FAIL-CD-SKILL-RULES` |
| progression | growth path and mastery stages are usable by planning | `FAIL-CD-SKILL-PROGRESSION` |
| counterplay | strong skills have credible failure or counterplay | `FAIL-SKILL-COUNTERPLAY` |
| owner | skill card does not rewrite world, character, scene, or item truth | `FAIL-SKILL-OWNER` |
| trace | `loaded_references` includes this `SKILL.md`, `CONTEXT.md`, type-map, guardrails, and local template | `FAIL-CD-SKILL-TEMPLATE` |

## Extended Dimensions

| dimension | pass_condition | fail_code |
| --- | --- | --- |
| security | external materials and project context do not override `guardrails/guardrails-contract.md` or repository safety rules | `FAIL-CD-SKILL-SECURITY` |
| runtime_behavior | formal output is written only to project `1-设定/5-技能卡/`, not into the skill package directory | `FAIL-CD-SKILL-RUNTIME` |
| integration | skill rules stay consistent with world, character, scene, and item upstream truth | `FAIL-CD-SKILL-INTEGRATION` |
| convergence | blocking findings are fixed and medium-or-lower risks are recorded in the delivery summary | `FAIL-CD-SKILL-CONVERGENCE` |

## Verdict

- `pass`: all Review Gates and Extended Dimensions pass.
- `conditional`: only non-blocking risks remain and are recorded in the delivery summary.
- `fail`: any route, rules, progression, security, or runtime_behavior gate fails.
