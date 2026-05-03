# Context: libTV

This file stores reusable experience for the `libTV` Skill 2.0 package. It does not redefine the execution contract in `SKILL.md`.

## Type Map

| type_id | trigger symptom | likely root | immediate move | prevention check |
| --- | --- | --- | --- | --- |
| `TM-LIBTV-01` | User asks for LibTV/LibLib.tv media generation | route classification | Load `types/generation/generation.md` | Do not route to generic imagegen when LibTV is explicit |
| `TM-LIBTV-02` | User supplies local image/video reference(s) plus edit or generation instruction | reference handoff | Load `types/editing/editing.md`, upload all references first | Submitted message includes numbered OSS URLs and original wording |
| `TM-LIBTV-03` | User gives `sessionId` or asks progress/download | session operation | Load `types/session-ops/session-ops.md` | Do not create a new session unless requested |
| `TM-LIBTV-04` | Prompt becomes more ornate than user request | local prompt overreach | Strip local additions and ask before changing wording | Final report states pass-through behavior |
| `TM-LIBTV-05` | Script cannot run because credential is missing | environment | Stop before API call and request `LIBTV_ACCESS_KEY` setup | Help/syntax checks use compile-only validation when no key exists |

## Repair Playbook

1. If routing is wrong, reload `types/type-map.md` and select the narrowest matching package.
2. If a file upload is involved, verify file existence and MIME intent before calling `upload_file.py`.
3. If API calls fail, first check `LIBTV_ACCESS_KEY`, then optional `OPENAPI_IM_BASE` or `IM_BASE_URL`.
4. If polling stalls, preserve `sessionId` and `projectUrl`, report timeout clearly, and do not keep looping indefinitely.
5. If results are visible in session messages but not local, run `download_results.py` before final delivery.
6. If a user later corrects long-term LibTV usage preferences for a project, store project-specific preference in that project's `MEMORY.md`, not here.

## Reusable Heuristics

- The highest-risk failure is not API syntax; it is local creative overreach before sending the request to LibTV.
- Treat filename prefixes as local organization only. They must not leak into the creative instruction unless the user wrote them as part of the request.
- Return the project canvas link at completion, not during in-progress polling, unless the user explicitly asks for it.
- For edits or AIGC reference routes, uploaded OSS URLs are part of the handoff payload, but the user's own wording remains the creative source of truth.
- Prefer compile checks for bundled scripts in environments without `LIBTV_ACCESS_KEY`; several runtime paths are designed to fail fast when credentials are absent.
