---
name: html-anything
description: Use when selecting Open Design / HTML Anything template skills to turn Markdown, data, or structured content into designed HTML surfaces such as prototypes, decks, reports, posters, social cards, dashboards, and documents.
governance_tier: full
metadata:
  upstream: nexu-io/html-anything
  upstream_commit: b54a0fbac2942bd82b113199712d488d4b3b3cfa
  codex_adapter: true
---

# Open Design / HTML Anything Codex Adapter

## Context Loading Contract

- Always load this `SKILL.md` and sibling `CONTEXT.md`.
- Use `references/upstream/templates/skills/` as a template-skill library.
- Load only the selected template skill folders and their directly needed files.
- The upstream Next app is not part of the default Codex runtime. Do not install or run it unless the user explicitly asks.

## Runtime Spine Contract

Use this skill when the task needs a suitable HTML surface pattern before or during generation: web prototype, dashboard, report, deck, poster, carousel, document, notification frame, social card, finance/data report, mobile screen, or motion frame.

This adapter owns template selection and projection. It does not own final business truth or project source content.

## Input Contract

Expected inputs:

- source material: markdown, outline, data, lesson content, brief, or files;
- intended surface: report, deck, prototype, card, poster, dashboard, etc.;
- target viewport or aspect ratio when known;
- export/use case when relevant.

If the surface is unknown, classify it from the content and user goal, then name the selected template before generating.

## Type Routing Matrix

| Request Type | Template Family Examples |
|---|---|
| Web/product prototype | `prototype-web`, `saas-landing`, `pricing-page`, `web-proto-*` |
| Dashboard/app UI | `dashboard`, `mobile-app`, `mobile-onboarding`, `gamified-app` |
| Reports and documents | `data-report`, `finance-report`, `exec-briefing-memo`, `blog-post`, `article-magazine`, `digital-eguide` |
| Deck/course presentation | `deck-*`, `ppt-keynote` |
| Social and marketing cards | `social-*`, `magazine-poster`, `deck-xhs-*` |
| Motion/title/frame concepts | `motion-frames`, `video-hyperframes`, `frame-*`, `vfx-*` |
| Wireframe or rough concept | `wireframe-sketch` |

## Thinking-Action Node Map

1. Parse the user's content and target use case.
2. Select one primary template family and optional supporting template.
3. Load the selected template `SKILL.md` and, if useful, its example HTML or metadata files.
4. Map source content into the template's structure without inventing unsupported facts.
5. Generate or revise the HTML artifact using Codex frontend constraints and project assets.
6. Verify layout and interaction when a runnable artifact is produced.
7. Return selected template, generated paths, and verification status.

## Module Loading Matrix

| Module | Trigger | Permission | Prohibition |
|---|---|---|---|
| `references/upstream/README.md` | Need package overview or template count context | Summarize upstream library role | Do not treat marketing copy as execution contract. |
| `references/upstream/templates/skills/*/SKILL.md` | Template selected or being compared | Apply template structure and surface expectations | Do not load all templates by default. |
| `references/upstream/templates/skills/*/example.*` | Need concrete layout/sample behavior from selected template | Use as visual/structural reference | Do not copy sample content as project truth. |
| `references/upstream/templates/skills/*/assets/` | Selected template needs local assets | Reuse mechanically when license and fit permit | Do not replace project-specific assets silently. |
| `references/upstream/LICENSE` | Redistribution or packaging question | Confirm upstream license | Do not provide legal advice beyond license identification. |

## Convergence Contract

A run passes only when:

- a selected template or template combination is named;
- source content is mapped into the chosen structure without unsupported filler;
- generated HTML follows the requested surface and viewport;
- any visual/runtime verification is complete or explicitly reported as not run.

Failure conditions include selecting templates by name only without mapping, loading the whole library indiscriminately, running the upstream app unnecessarily, or presenting template sample text as real content.

## Root-Cause Execution Contract

When output quality is weak, diagnose whether the failure is template mismatch, insufficient source content, unsupported facts, viewport mismatch, missing assets, or CSS/runtime breakage. Correct that cause before restyling.

## Field Mapping

| Codex Field | Meaning |
|---|---|
| `selected_template` | Primary upstream template skill folder |
| `supporting_templates` | Optional secondary references |
| `source_mapping` | How source content maps into template sections |
| `artifact_path` | Generated HTML file or app path |
| `verification` | Browser/viewport/runtime checks |

## Output Contract

Return:

- selected template(s);
- generated or modified file paths;
- source mapping summary when nontrivial;
- verification status and caveats.

## Learning / Context Writeback

Write template-selection heuristics, mismatches, and successful combinations to `CONTEXT.md`. Keep project-specific content preferences in the project context, not this adapter.
