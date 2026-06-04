# Scene Generation Heuristics

## Stable Lessons

- Treat the upstream design document as the only scene design truth. Generation can clarify delivery instructions, but it cannot invent new spatial identity.
- The main image and multi-view image should be a pair: same subject, same design source, same output directory, and same prompt lineage.
- Multi-view scene sheets fail when they become a moodboard. Prompt them as one space under multiple camera/view constraints.
- JSON records are the audit trail for future video generation. Missing JSON means the output is incomplete even if the image looks good.
- Project-bound generation is not complete until final files live under `projects/aigc/<项目名>/11-主体/场景/3-生成`.

## Common Repairs

- If the image looks visually acceptable but has no JSON, reconstruct the JSON from the source design document and final prompt before closing.
- If the multi-view sheet drifts into people, silhouettes, or separate rooms, rerun with the no-human and one-coherent-scene constraints raised near the top of the prompt.
- If the generated main image is under `$CODEX_HOME`, persist it into the project directory and update the JSON `output_path`.
- If two subjects share a sanitized filename, add a stable source prefix such as `S###-` only after checking the user's naming requirement; record the display `subject_name` unchanged in JSON.
