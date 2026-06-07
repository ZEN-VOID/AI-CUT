# HTML Skill Router Context

## Local Heuristics

- Use `html-anything` when the main uncertainty is artifact type, template taxonomy, or how to turn content into a known HTML surface.
- Use `claude-design` when the main weakness is visual maturity, art direction, composition, responsive polish, or browser-verified craft.
- For courseware workflows, preserve canonical lesson content outside this router. HTML skills may expand presentation copy and visual hierarchy, but they should not silently rewrite the course's authoritative DOC/source text.

## Known Pitfalls

- Do not treat upstream template wording as a hard contract when it conflicts with Codex frontend guidance or project rules.
- Do not install or run the HTML Anything Next app by default. The local adapter uses its template skill library as reference material.
- If both child skills are useful, apply them in this order: choose format/template with `html-anything`, then raise craft and visual system with `claude-design`.
