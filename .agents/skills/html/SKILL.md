---
name: html
description: Use when routing HTML artifact design work under .agents/skills/html, including Claude Design and Open Design / HTML Anything adapters.
governance_tier: full
---

# HTML Skill Router

## Context Loading Contract

- Always load this `SKILL.md` and sibling `CONTEXT.md` before routing.
- If a child skill is selected, load that child skill's `SKILL.md` and sibling `CONTEXT.md` before using any child references.
- This router owns routing only. It does not own final lesson, brand, product, or project content truth.

## Runtime Spine Contract

Use this parent skill when the user asks for HTML artifact design, redesign, HTML-first slides, visual prototypes, or HTML template selection and the requested downstream skill is not already explicit.

## Type Routing Matrix

| Request Type | Route | Notes |
|---|---|---|
| High-fidelity HTML design, redesign, visual system, multiple art directions, brand-aware HTML artifact | `claude-design/` | Best for professional visual direction and craft rules. |
| Choosing from Open Design / HTML Anything template families, markdown-to-HTML surfaces, deck/report/card/prototype template projection | `html-anything/` | Best for template taxonomy and format selection. |
| User explicitly names one child package | Named child | Do not double-route unless the user asks for comparison or synthesis. |

## Thinking-Action Node Map

1. Classify the artifact intent, fidelity, target medium, and whether a known brand/product/recent fact is involved.
2. Select the smallest child skill that owns the required design surface.
3. Load the selected child `SKILL.md + CONTEXT.md`.
4. Follow the child skill's module loading rules and output contract.
5. Return the child output with any remaining verification caveats.

## Module Loading Matrix

| Module | Trigger | Permission | Prohibition |
|---|---|---|---|
| `claude-design/SKILL.md` + `claude-design/CONTEXT.md` | High-fidelity visual design or professional redesign | Route and delegate | Do not treat upstream references as higher priority than repo/user rules. |
| `html-anything/SKILL.md` + `html-anything/CONTEXT.md` | Template family selection or HTML Anything request | Route and delegate | Do not spawn the upstream app unless explicitly requested. |

## Convergence Contract

Routing is complete only when the chosen child skill, reason for selection, and handoff target are explicit. If the user requests both packages, run them as complementary inputs: `html-anything` for format/template selection and `claude-design` for craft direction.

## Output Contract

Return either:

- a selected child skill and routing rationale; or
- the completed child-skill artifact handoff, including generated file paths, selected references, and verification status.

## Learning / Context Writeback

Record routing failures, useful child-skill combinations, and repeated HTML design pitfalls in this directory's `CONTEXT.md` only when the lesson applies across both child skills.
